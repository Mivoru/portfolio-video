"""Build a narrated screen-recording tutorial from a project spec.

Pipeline: ElevenLabs voice-over and sound effects (cached) -> timeline ->
source frames with personal data blurred -> HTML compositor rendered frame by
frame in Playwright -> ffmpeg mix and encode.

Usage:
  python tools/build.py zajmy                  full render to the spec's OUTPUT
  python tools/build.py zajmy --stills 1 5.5   PNG previews at output seconds
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
WORK = ROOT / "work"
FPS = 30
API = "https://api.elevenlabs.io"
VOICE_ID = "KIDKfqJyZ6ASuyzsKfh5"  # "Jan - Kind Educator", Czech, shared library
VOICE_MODEL = "eleven_multilingual_v2"


# ---------------------------------------------------------------- helpers

def load_spec(name):
    path = ROOT / "projects" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("ELEVENLABS_API_KEY missing: set it in the environment or in .env")
    return key


def post(path, body):
    req = urllib.request.Request(
        API + path, data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": api_key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"ElevenLabs {path} failed: {e.code} {e.read()[:300]!r}") from None


def digest(*parts):
    return hashlib.sha1(json.dumps(parts, ensure_ascii=False).encode()).hexdigest()[:12]


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(out.stdout.strip())


# ---------------------------------------------------------------- audio assets

def voice(text, voice_id=VOICE_ID, lang="cs"):
    """Voice-over line with word timings, cached by text and settings."""
    settings = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.15,
                "use_speaker_boost": True, "speed": 1.05}
    key = digest(text, voice_id, VOICE_MODEL, settings)
    mp3, meta = CACHE / f"vo_{key}.mp3", CACHE / f"vo_{key}.json"
    if not mp3.exists():
        print(f"  voice: {text}")
        raw = post(f"/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128",
                   {"text": text, "model_id": VOICE_MODEL, "voice_settings": settings,
                    "language_code": lang})
        data = json.loads(raw)
        mp3.write_bytes(base64.b64decode(data["audio_base64"]))
        meta.write_text(json.dumps(data["alignment"], ensure_ascii=False), encoding="utf-8")
    align = json.loads(meta.read_text(encoding="utf-8"))
    return mp3, words_from(align), duration(mp3)


def words_from(align):
    words, cur, start = [], "", None
    for ch, s, e in zip(align["characters"], align["character_start_times_seconds"],
                        align["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"w": cur, "s": start, "e": last})
            cur, start = "", None
            continue
        if start is None:
            start = s
        cur, last = cur + ch, e
    if cur:
        words.append({"w": cur, "s": start, "e": last})
    return words


def sfx(name, prompt, seconds):
    key = digest(prompt, seconds)
    path = CACHE / f"sfx_{name}_{key}.mp3"
    if not path.exists():
        print(f"  sfx: {name}")
        path.write_bytes(post("/v1/sound-generation",
                              {"text": prompt, "duration_seconds": seconds, "prompt_influence": 0.6}))
    return path


def music(prompt, seconds):
    key = digest(prompt, round(seconds))
    path = CACHE / f"music_{key}.mp3"
    if not path.exists():
        print("  music")
        try:
            path.write_bytes(post("/v1/music", {"prompt": prompt, "music_length_ms": int(seconds * 1000),
                                                "model_id": "music_v1"}))
        except RuntimeError as e:
            print(f"  music skipped: {e}")
            return None
    return path


# ---------------------------------------------------------------- timeline

def piece_len(p):
    return (p[1] - p[0]) / p[2]


def build_timeline(spec):
    """Place segments on the output clock and resolve every event time."""
    t, segs = 0.0, []
    for seg in spec.SEGMENTS:
        s = dict(seg)
        s["start"] = t
        video = sum(piece_len(p) for p in s.get("pieces", []))
        if s.get("vo"):
            s["vo_file"], words, vo_dur = voice(s["vo"], getattr(spec, "VOICE_ID", VOICE_ID), getattr(spec, "LANG", "cs"))
            s["words"] = [{**w, "s": w["s"] + t + s["vo_at"], "e": w["e"] + t + s["vo_at"]} for w in words]
            need = s["vo_at"] + vo_dur + 0.45
        else:
            need = 0
        s["dur"] = max(video, need, s.get("min_dur", 0))
        s["lead"] = s["dur"] - video if s.get("pieces") else 0.0
        t += s["dur"]
        segs.append(s)

    def at(seg, v):
        """Segment-local value (number, 'sNN.N' source time, 'end', 'end-0.3') -> output seconds."""
        if isinstance(v, (int, float)):
            return seg["start"] + v
        if v.startswith("end"):
            return seg["start"] + seg["dur"] + (float(v[3:]) if len(v) > 3 else 0)
        src, local = float(v[1:]), seg["lead"]
        for a, b, speed in seg["pieces"]:
            if src <= b:
                return seg["start"] + local + max(0.0, src - a) / speed
            local += (b - a) / speed
        return seg["start"] + local

    ev = {"cam": [], "rings": [], "callouts": [], "clicks": [], "checks": [], "steps": [],
          "words": [], "sfx": [], "captop": [], "title": None, "outro": None}
    steps = [s for s in segs if s.get("step")]
    for s in segs:
        for v, c in s.get("cam", []):
            ev["cam"].append({"t": at(s, v), "cx": c[0], "cy": c[1], "z": c[2]})
        if s.get("cam") and s is not segs[-1]:
            c = s["cam"][-1][1]
            ev["cam"].append({"t": s["start"] + s["dur"] - 0.001, "cx": c[0], "cy": c[1], "z": c[2]})
        for r, a, b in s.get("rings", []):
            ev["rings"].append({"r": r, "a": at(s, a), "b": at(s, b)})
        for text, p, side, a, b in s.get("callouts", []):
            ev["callouts"].append({"text": text, "p": p, "side": side, "a": at(s, a), "b": at(s, b)})
        for p, v in s.get("clicks", []):
            ev["clicks"].append({"p": p, "t": at(s, v)})
            ev["sfx"].append(("click", at(s, v) - 0.02))
        for p, v in s.get("checks", []):
            ev["checks"].append({"p": p, "t": at(s, v)})
        for name, v in s.get("sfx", []):
            ev["sfx"].append((name, at(s, v)))
        if s.get("step"):
            ev["steps"].append({"n": steps.index(s) + 1, "of": len(steps), "text": s["step"],
                                "a": s["start"], "b": s["start"] + s["dur"]})
        ev["words"] += s.get("words", [])
        if s.get("cap") == "top":
            ev["captop"].append([s["start"], s["start"] + s["dur"]])
        if s.get("title"):
            ev["title"] = {"a": s["start"] + 2.0, "b": s["start"] + s["dur"],
                           "lines": spec.TITLE, "kicker": spec.KICKER}
        if s.get("outro"):
            ev["outro"] = {"a": s["start"] + 0.55, "b": s["start"] + s["dur"],
                           "lines": spec.OUTRO, "credit": spec.CREDIT}
    ev["cam"].sort(key=lambda k: k["t"])
    return segs, ev, t, at


def src_time(segs, t):
    for s in segs:
        if t < s["start"] + s["dur"] or s is segs[-1]:
            if "hold_src" in s:
                return s["hold_src"]
            local = t - s["start"] - s["lead"]
            if local < 0:
                return s["pieces"][0][0]
            for a, b, speed in s["pieces"]:
                if local < (b - a) / speed:
                    return a + local * speed
                local -= (b - a) / speed
            return s["pieces"][-1][1] - 1 / FPS


# ---------------------------------------------------------------- frames

def source_frames(spec):
    raw = WORK / "src"
    if not (raw / "done").exists():
        raw.mkdir(parents=True, exist_ok=True)
        print("  extracting source frames")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / spec.SOURCE), "-vf", f"fps={FPS}",
                        "-q:v", "2", str(raw / "%05d.jpg")], check=True)
        (raw / "done").write_text("ok")
    return raw


def blurred(spec, raw, idx):
    """Source frame idx with personal data blurred, cached per blur layout."""
    t = idx / FPS
    rects = spec.blur_rects(t)
    out = WORK / "blur" / f"{idx:05d}_{digest(rects)}.jpg"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(raw / f"{idx + 1:05d}.jpg").convert("RGB")
        for r in rects:
            box = (max(0, r[0]), max(0, r[1]), min(1920, r[2]), min(1080, r[3]))
            region = im.crop(box).resize((max(1, (box[2] - box[0]) // 10), max(1, (box[3] - box[1]) // 10)))
            region = region.resize((box[2] - box[0], box[3] - box[1]), Image.BILINEAR)
            im.paste(region.filter(ImageFilter.GaussianBlur(6)), box)
        im.save(out, quality=93)
    return out


# ---------------------------------------------------------------- audio mix

def mix(spec, segs, ev, total, out_wav):
    inputs, chains, n = [], [], 0

    def add(path, t, gain_db, label):
        nonlocal n
        inputs.extend(["-i", str(path)])
        ms = max(0, int(t * 1000))
        chains.append(f"[{n}:a]aresample=44100,aformat=channel_layouts=stereo,volume={gain_db}dB,"
                      f"adelay={ms}|{ms}[{label}{n}]")
        n += 1
        return f"[{label}{n - 1}]"

    vo = [add(s["vo_file"], s["start"] + s["vo_at"], 0, "v") for s in segs if s.get("vo")]
    gains = {"click": -6, "pop": -14, "whoosh": -12, "rewind": -12, "success": -8, "typing": -16}
    fx = [add(sfx(name, *spec.SFX[name]), t, gains.get(name, -10), "f") for name, t in ev["sfx"]]
    mus = music(spec.MUSIC_PROMPT, total + 1)
    g = chains[:]
    g.append("".join(vo) + f"amix=inputs={len(vo)}:normalize=0,apad=whole_dur={total:.3f},asplit=2[vo][vokey]")
    g.append("".join(fx) + f"amix=inputs={len(fx)}:normalize=0,apad=whole_dur={total:.3f}[fx]")
    parts = "[vo][fx]"
    if mus:
        inputs.extend(["-i", str(mus)])
        g.append(f"[{n}:a]aresample=44100,aformat=channel_layouts=stereo,volume=-11dB,"
                 f"afade=t=in:d=0.8,afade=t=out:st={total - 1.6:.2f}:d=1.6[mraw]")
        g.append("[mraw][vokey]sidechaincompress=threshold=0.04:ratio=4:attack=40:release=450[mus]")
        parts += "[mus]"
    else:
        g.append("[vokey]anullsink")
    k = 3 if mus else 2
    g.append(f"{parts}amix=inputs={k}:normalize=0,atrim=0:{total:.3f},loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(g),
                    "-map", "[out]", "-ar", "48000", str(out_wav)], check=True)


# ---------------------------------------------------------------- docs site media

def render_docs(spec, segs, ev, total, at, raw):
    """Step images (no captions), before/after pair, poster, filmstrip and timeline data for docs/."""
    docs = ROOT / getattr(spec, "DOCS_DIR", "docs/media")
    docs.mkdir(parents=True, exist_ok=True)
    nframes = len(list(raw.glob("*.jpg")))
    shots = []
    for s in segs:
        if s.get("doc_at"):
            shots.append((f"step-{len(shots) + 1}", at(s, s["doc_at"]), True))
    seg = next(s for s in segs if s["id"] == spec.DOC_COMPARE[0])
    t_cmp = at(seg, spec.DOC_COMPARE[1])
    shots.append(("compare-final", t_cmp, False))
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "src" / "compositor.html").as_uri())
        for name, t, clean in shots:
            page.evaluate("d => init(d)", {"ev": ev, "total": total, "nocap": clean,
                                          "fonts": (ROOT / "assets" / "fonts").as_uri()})
            idx = min(round(src_time(segs, t) * FPS), nframes - 1)
            page.evaluate("([t, s]) => render(t, s)", [t, blurred(spec, raw, idx).as_uri()])
            png = WORK / f"{name}.png"
            page.screenshot(path=str(png))
            Image.open(png).convert("RGB").resize((1600, 900), Image.LANCZOS).save(docs / f"{name}.webp", quality=86)
            print(f"  docs/media/{name}.webp  (t={t:.2f})")
            page.reload()
        browser.close()
    idx = min(round(src_time(segs, t_cmp) * FPS), nframes - 1)
    Image.open(blurred(spec, raw, idx)).resize((1600, 900), Image.LANCZOS).save(docs / "compare-raw.webp", quality=86)

    video = ROOT / spec.OUTPUT
    if video.exists():
        name = Path(spec.OUTPUT).name
        (docs / name).write_bytes(video.read_bytes())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(spec.DOC_POSTER), "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=1600:-1", "-q:v", "80", str(docs / "poster.webp")], check=True)
        strip = docs / "strip"
        strip.mkdir(exist_ok=True)
        n = 0
        for i, t in enumerate([x * total / 16 + 0.6 for x in range(16)]):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                            "-vf", "scale=480:-1", "-q:v", "75", str(strip / f"{i:02d}.webp")], check=True)
            n += 1
        print(f"  video, poster and {n} filmstrip frames copied")

    info = {"total": round(total, 2), "frames": int(total * FPS),
            "segments": [{"id": s["id"], "start": round(s["start"], 2), "dur": round(s["dur"], 2),
                          "step": s.get("step"), "vo": s.get("vo")} for s in segs],
            "source_seconds": round(duration(ROOT / spec.SOURCE), 1)}
    (docs / "timeline.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  docs/media/timeline.json")


# ---------------------------------------------------------------- render

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--stills", nargs="*", type=float)
    ap.add_argument("--docs", action="store_true", help="render step images and media for the docs/ site")
    args = ap.parse_args()
    spec = load_spec(args.project)
    CACHE.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)

    print("timeline")
    segs, ev, total, at = build_timeline(spec)
    print(f"  {total:.2f} s, {len(segs)} segments")
    raw = source_frames(spec)
    if args.docs:
        return render_docs(spec, segs, ev, total, at, raw)

    times = args.stills if args.stills is not None else [f / FPS for f in range(int(total * FPS))]
    out = ROOT / spec.OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    silent = WORK / f"{args.project}_video.mp4"

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto((ROOT / "src" / "compositor.html").as_uri())
        page.evaluate("d => init(d)", {"ev": ev, "total": total, "fonts": (ROOT / "assets" / "fonts").as_uri()})
        enc = None
        if args.stills is None:
            enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
                                    "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                                    "-pix_fmt", "yuv420p", str(silent)], stdin=subprocess.PIPE)
        nframes = len(list(raw.glob("*.jpg")))
        for i, t in enumerate(times):
            idx = min(round(src_time(segs, t) * FPS), nframes - 1)
            img = blurred(spec, raw, idx).as_uri()
            page.evaluate("([t, s]) => render(t, s)", [t, img])
            if enc:
                enc.stdin.write(page.screenshot(type="jpeg", quality=94))
                if i % 150 == 0:
                    print(f"  frame {i}/{len(times)}")
            else:
                still = ROOT / "out" / "stills" / f"{args.project}_{t:06.2f}.png"
                still.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(still))
                print(f"  {still.relative_to(ROOT)}")
        browser.close()
    if not enc:
        return
    enc.stdin.close()
    enc.wait()

    print("audio")
    wav = WORK / f"{args.project}_mix.wav"
    mix(spec, segs, ev, total, wav)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(wav), "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print(f"done: {out.relative_to(ROOT)} ({total:.1f} s)")


if __name__ == "__main__":
    main()
