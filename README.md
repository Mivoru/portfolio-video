# portfolio-video

Narrated tutorial videos built from raw screen recordings. This is a separate portfolio from `D:\portfolio`.

## Pipeline

`tools/build.py <project>` runs these steps for a spec in `projects/<project>.py`:

1. Voice-over for each segment through the ElevenLabs `with-timestamps` endpoint (Czech voice "Jan - Kind Educator"). The word timings drive the dynamic captions.
2. Sound effects and background music generated with ElevenLabs.
3. The timeline. Each segment plays parts of the recording at a set speed. When the voice-over is longer than the video, the first frame is held.
4. Source frames with personal data blurred, using `blur_rects()` in the spec.
5. `src/compositor.html`, rendered frame by frame in Playwright. It adds camera zooms, highlight rings, click ripples, callouts, the step badge, captions, the intro title and the outro.
6. ffmpeg mixes the audio (the music ducks under the voice, then loudness is normalised to -16 LUFS) and encodes H.264.

API results are cached in `cache/`, so re-renders do not spend credits unless a text or prompt changes.

## Usage

```
python tools/build.py zajmy --stills 3 12.5   # PNG previews into out/stills/
python tools/build.py zajmy                   # full render into out/zajmy.mp4
```

Requirements: Python with `playwright` and `pillow`, ffmpeg on PATH, and `ELEVENLABS_API_KEY` in `.env` or the environment.

`input/`, `cache/`, `work/`, `out/` and `.env` are git-ignored. The recordings contain personal data.

## Adding a tutorial

Copy `projects/zajmy.py`, then change `SOURCE`, the texts, `blur_rects()` and `SEGMENTS`. Coordinates are in recording pixels. A time written as `"s16.7"` is a time in the source recording, and a plain number is seconds from the start of the segment.

## Site

`docs/` is published with GitHub Pages at https://mivoru.github.io/portfolio-video/ (Czech) and `/en/` (English).

```
python tools/build.py zajmy --docs      # Czech media into docs/media/
python tools/build.py zajmy_en --docs   # English media into docs/media/en/
python tools/site.py                    # both pages from one template
```

`projects/zajmy_en.py` reuses the Czech spec and swaps only the texts and the voice.
