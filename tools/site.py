"""Generate the docs/ site in Czech and English from one template.

Usage: python tools/site.py
Writes docs/index.html (cs) and docs/en/index.html (en). Media come from
`python tools/build.py zajmy --docs` and `python tools/build.py zajmy_en --docs`.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://mivoru.github.io/portfolio-video/"

T = {
    "cs": {
        "lang": "cs", "out": "docs/index.html", "base": "", "media": "media/", "video": "zajmy.mp4",
        "other": "en/", "other_label": "EN", "other_name": "English", "here_label": "CZ",
        "title": "Návod: zájem na profilu",
        "desc": "Ukázkový vzdělávací návod ve dvou podobách: video s voiceoverem a textový postup se snímky. Včetně rozpisu, jak video vzniklo.",
        "nav": ["Video", "Textový návod", "Jak vzniklo", "Kontakt"],
        "meta": "Návod č. 01 · e-learning TUL · listopad 2026",
        "h1": 'Jak přidat <mark>zájem</mark> na&nbsp;svůj profil',
        "lead": "Jeden návod ve dvou podobách: krátké video s voiceoverem a textový postup se snímky pro ty, kdo radši čtou. Na konci stránky je rozepsané, jak video vzniklo.",
        "colophon": [("Délka", "0:38"), ("Kroky", "5"), ("Jazyk", 'čeština · <a href="en/">English</a>'),
                     ("Hlas", "ElevenLabs"), ("Podoba", "video a text")],
        "video_cap": "<b>Video 1.</b> Celý návod. Osobní údaje jsou rozmazané.",
        "s1": "Textový návod", "s1_h": "Zájem na profil za minutu",
        "s1_p": "Stejné kroky jako ve videu. Snímky vyrenderoval stejný skript jako video, takže spolu vždy sedí.",
        "need": [("Potřebuješ", "přihlášení do e-learningu"), ("Čas", "asi 1 minutu"), ("Zařízení", "počítač s prohlížečem")],
        "fig": "Obr.",
        "steps": [
            ("Otevři svůj profil", "Vpravo nahoře klikni na kroužek se svými <b>iniciálami</b>. Otevře se nabídka. V ní vyber <b>Profil</b>.",
             "Otevřená nabídka pod iniciálami, zvýrazněná položka Profil."),
            ("Klikni na Upravit profil", "Na stránce profilu najdeš v bloku <b>Detaily uživatele</b> odkaz <b>Upravit profil</b>.",
             "Stránka profilu se zvýrazněným odkazem Upravit profil."),
            ("Rozbal sekci Zájmy", "Formulář je dlouhý. Sjeď dolů k sekci <b>Zájmy</b> a kliknutím na šipku ji rozbal.",
             "Formulář úprav profilu se zvýrazněnou sekcí Zájmy."),
            ("Napiš svůj zájem", "Do pole <b>Vložte štítky…</b> napiš, co tě baví, třeba <b>běh</b>, a potvrď klávesou <kbd>Enter</kbd>. Každý zájem je samostatný štítek, takže jich můžeš přidat víc.",
             "Pole pro štítky s napsaným slovem běh."),
            ("Ulož změny", "Úplně dole klikni na <b>Aktualizovat profil</b>. Bez uložení se zájem neprojeví.",
             "Spodní lišta formuláře se zvýrazněným tlačítkem Aktualizovat profil."),
            ("Hotovo", "Zobrazí se hláška <b>Změny uloženy</b> a zájem uvidíš na profilu v bloku <b>Detaily uživatele</b>.",
             "Detail profilu se štítkem Běh v řádku Zájmy."),
        ],
        "tip": ("Tip", "Zájem odstraníš stejnou cestou: v sekci Zájmy klikni na křížek u štítku a profil znovu ulož."),
        "s2": "Jak video vzniklo", "s2_h": "Z 56 sekund surové nahrávky na hotový návod",
        "s2_p": "Obrazovku jsem natočil jedním průchodem bez střihu. Zbytek dělá skript, který jsem si k tomu postavil s Claude Code. O tempu, textu a zvýraznění rozhoduji já.",
        "stats": [("56 → 38 s", "surová nahrávka a hotové video"), ("1 154", "snímků vykreslených kompozicí"),
                  ("7", "vět voiceoveru s časováním slov"), ("6", "generovaných zvukových efektů"), ("~4 min", "render celého videa na notebooku")],
        "pipe": [
            ("Natočení", "Záznam obrazovky ve Full HD, jeden průchod. Čekání a pomalá místa zrychlí až střih.", "OBS Studio"),
            ("Anonymizace", "E-mail, studijní čísla, data přihlášení a kurzy jsou rozmazané. Oblasti mají souřadnice i čas, takže sedí i při scrollování.", "Python · Pillow"),
            ("Scénář a hlas", "Krátké věty, jedna na krok. Hlas vrací i časování každého slova, a z něj vznikají titulky.", "ElevenLabs API"),
            ("Kompozice", "Zoomy, zvýraznění, kliknutí, popisky a odznak kroku. HTML šablona vykreslená snímek po snímku.", "HTML/CSS · Playwright"),
            ("Zvuk", "Efekty na kliknutí a přechody. Hudba se pod hlasem ztiší, hlasitost je srovnaná na −16 LUFS.", "ElevenLabs · ffmpeg"),
            ("Export a text", "Video v H.264. Stejný skript vyrenderuje i čisté snímky pro textový návod.", "ffmpeg"),
        ],
        "cmp_h": "Před a po", "cmp_p": "Vlevo surový snímek (už s rozmazanými údaji), vpravo stejný okamžik ve videu. Posuň jezdcem.",
        "cmp_l": ("Nahrávka", "Video"), "cmp_aria": "Porovnání nahrávky a videa",
        "cmp_alt": ("Hotový snímek videa s přiblížením, popiskem a titulkem.", "Surový záznam obrazovky ve stejném okamžiku."),
        "strip_h": "Kontaktní arch", "strip_p": "Šestnáct snímků z hotového videa. Kamera vede oko k místu kliknutí a na konci se vrátí na celou obrazovku.",
        "strip_alt": "Snímek videa v čase",
        "tl_h": "Časová osa a scénář", "tl_p": "Každý krok má svůj úsek. Když je věta delší než záběr, skript podrží první snímek, aby hlas nepředběhl obraz.",
        "seg": {"intro": "Intro", "outro": "Konec", "step": "Krok", "result": "Výsledek"},
        "code_h": "Jeden krok v kódu", "code_p": "Krok 4 je pár řádků dat: které části nahrávky a jak rychle, kam se přiblížit, co zvýraznit a co říct. Nový návod je nový soubor, ne nový střih od nuly.",
        "code_c": ["úseky nahrávky: od, do, zrychlení", "kamera: čas → střed a přiblížení"],
        "code_vo": "Do pole napiš, co tě baví. Třeba běh.", "code_step": "Napiš svůj zájem", "code_callout": "Napiš zájem, třeba běh",
        "ai_h": "Co dělá AI", "ai": ["čte věty scénáře a vrací časování slov", "generuje zvukové efekty a hudbu", "pomohla mi napsat skript, který vše skládá"],
        "me_h": "Co dělám já", "me": ["scénář: co říct, v jakém pořadí a jak stručně", "tempo: co zrychlit, kde zastavit, kam přiblížit", "kontrolu: rozmazání údajů, srozumitelnost, zvuk"],
        "s3": "Proč takhle", "s3_h": "Návody se mění. Výroba to má unést.",
        "why": [("Aktualizace bez přetáčení všeho", "Když se změní prostředí aplikace, přetočím jen dotčený krok. Zbytek videa se vyrenderuje znovu sám."),
                ("Jazykové verze", 'Anglická verze znamená přeložit věty a vybrat hlas. Osa, zoomy i zvýraznění zůstávají. <a href="en/">Podívej se na ni.</a>'),
                ("Jednotný styl", "Barvy, písmo, odznaky kroků a titulky jsou v jedné šabloně. Každé další video vypadá jako ze stejné série."),
                ("Video a text vždy sedí", "Snímky pro textový návod vznikají ze stejného zdroje jako video. Oprava kroku opraví obojí.")],
        "s4": "Kontakt", "foot_h": "Rád takhle vyrobím i vaše návody.",
        "foot_p": "Studuji 3. ročník bakalářského oboru IT. Stříhám v DaVinci Resolve a výrobu si automatizuji skripty.",
        "links": [("promichalcz@gmail.com", "mailto:promichalcz@gmail.com"), ("Hlavní portfolio", "https://mivoru.github.io/portfolio/"),
                  ("Zdrojový kód", "https://github.com/Mivoru/portfolio-video")],
        "fine": "Ukázkový návod nad školním e-learningem TUL, vytvořený pro portfolio. Osobní údaje ve videu i na snímcích jsou rozmazané.",
    },
    "en": {
        "lang": "en", "out": "docs/en/index.html", "base": "../", "media": "../media/en/", "video": "zajmy_en.mp4",
        "other": "../", "other_label": "CZ", "other_name": "Čeština", "here_label": "EN",
        "title": "Tutorial: profile interest",
        "desc": "A sample tutorial in two forms: a narrated video and a written guide with screenshots, plus a breakdown of how the video was made.",
        "nav": ["Video", "Written guide", "How it was made", "Contact"],
        "meta": "Tutorial no. 01 · TUL e-learning · November 2026",
        "h1": 'How to add an <mark>interest</mark> to your profile',
        "lead": "One tutorial in two forms: a short narrated video, and a written guide with screenshots for people who prefer reading. The end of the page shows how the video was made.",
        "colophon": [("Length", "0:38"), ("Steps", "5"), ("Language", 'English · <a href="../">čeština</a>'),
                     ("Voice", "ElevenLabs"), ("Format", "video and text")],
        "video_cap": "<b>Video 1.</b> The full tutorial. Personal data is blurred. The e-learning interface itself is in Czech.",
        "s1": "Written guide", "s1_h": "An interest on your profile in a minute",
        "s1_p": "The same steps as in the video. The screenshots come from the same script as the video, so the two always match. Czech labels are given with their English meaning.",
        "need": [("You need", "an e-learning login"), ("Time", "about 1 minute"), ("Device", "a computer with a browser")],
        "fig": "Fig.",
        "steps": [
            ("Open your profile", "In the top right corner, click the circle with your <b>initials</b>. A menu opens. Choose <b>Profil</b> (Profile).",
             "The open menu under the initials, with Profil highlighted."),
            ("Click Edit profile", "On your profile page, find the <b>Upravit profil</b> (Edit profile) link in the <b>Detaily uživatele</b> (User details) block.",
             "The profile page with the Upravit profil link highlighted."),
            ("Expand Interests", "The form is long. Scroll down to the <b>Zájmy</b> (Interests) section and click its arrow to expand it.",
             "The edit form with the Zájmy section highlighted."),
            ("Type an interest", "In the <b>Vložte štítky…</b> (Enter tags) field, type something you enjoy, for example <b>běh</b> (running), and press <kbd>Enter</kbd>. Each interest is a separate tag, so you can add several.",
             "The tag field with the word běh typed in."),
            ("Save changes", "At the very bottom, click <b>Aktualizovat profil</b> (Update profile). Nothing changes until you save.",
             "The bottom bar of the form with the Aktualizovat profil button highlighted."),
            ("Done", "The message <b>Změny uloženy</b> (Changes saved) appears, and your interest shows in the <b>User details</b> block.",
             "Profile detail with the Běh tag in the Zájmy row."),
        ],
        "tip": ("Tip", "To remove an interest, go the same way: in the Zájmy section, click the cross on the tag and save the profile again."),
        "s2": "How it was made", "s2_h": "From 56 seconds of raw recording to a finished tutorial",
        "s2_p": "I recorded the screen in one take, with no cuts. A script that I built with Claude Code does the rest. I decide the pacing, the wording and what to highlight.",
        "stats": [("56 → 38 s", "raw recording and final video"), ("1,154", "frames rendered by the compositor"),
                  ("7", "voice-over lines with word timings"), ("6", "generated sound effects"), ("~4 min", "to render the whole video on a laptop")],
        "pipe": [
            ("Recording", "Full HD screen capture in one take. Waiting and slow parts get sped up in the edit.", "OBS Studio"),
            ("Anonymising", "E-mail, student numbers, login dates and courses are blurred. Each area has coordinates and a time range, so it holds while scrolling.", "Python · Pillow"),
            ("Script and voice", "Short lines, one per step. The voice comes back with the timing of every word, which drives the captions.", "ElevenLabs API"),
            ("Compositing", "Zooms, highlights, clicks, callouts and the step badge. An HTML template rendered frame by frame.", "HTML/CSS · Playwright"),
            ("Sound", "Effects on clicks and transitions. The music ducks under the voice, and loudness is levelled to −16 LUFS.", "ElevenLabs · ffmpeg"),
            ("Export and text", "H.264 video. The same script also renders clean screenshots for the written guide.", "ffmpeg"),
        ],
        "cmp_h": "Before and after", "cmp_p": "Left: a raw frame (personal data already blurred). Right: the same moment in the video. Drag the slider.",
        "cmp_l": ("Recording", "Video"), "cmp_aria": "Compare recording and video",
        "cmp_alt": ("Final video frame with zoom, callout and caption.", "Raw screen recording at the same moment."),
        "strip_h": "Contact sheet", "strip_p": "Sixteen frames from the finished video. The camera leads the eye to each click, then returns to the full screen at the end.",
        "strip_alt": "Video frame at",
        "tl_h": "Timeline and script", "tl_p": "Each step has its own section. When a line is longer than the shot, the script holds the first frame, so the voice never runs ahead of the picture.",
        "seg": {"intro": "Intro", "outro": "End", "step": "Step", "result": "Result"},
        "code_h": "One step in code", "code_p": "Step 4 is a few lines of data: which parts of the recording and how fast, where to zoom, what to highlight and what to say. A new tutorial is a new file, not a new edit from scratch.",
        "code_c": ["recording sections: from, to, speed", "camera: time → centre and zoom"],
        "code_vo": "Type in something you enjoy. Here, it's running.", "code_step": "Type an interest", "code_callout": "Type an interest, e.g. běh (running)",
        "ai_h": "What AI does", "ai": ["reads the script lines and returns word timings", "generates sound effects and music", "helped me write the script that puts it all together"],
        "me_h": "What I do", "me": ["the script: what to say, in which order, how briefly", "the pacing: what to speed up, where to pause, where to zoom", "the checks: blurring, clarity, sound"],
        "s3": "Why this way", "s3_h": "Tutorials change. Production has to keep up.",
        "why": [("Updates without re-recording everything", "When the app interface changes, I re-record only the affected step. The rest of the video renders again on its own."),
                ("Language versions", 'This English version meant translating the lines and picking a voice. Timeline, zooms and highlights stayed the same. <a href="../">See the Czech one.</a>'),
                ("One consistent style", "Colours, type, step badges and captions live in one template. Every next video looks like part of the same series."),
                ("Video and text always match", "Screenshots for the written guide come from the same source as the video. Fixing a step fixes both.")],
        "s4": "Contact", "foot_h": "I would be glad to make your tutorials this way.",
        "foot_p": "I am in the 3rd year of an IT bachelor's degree. I edit in DaVinci Resolve and automate production with scripts.",
        "links": [("promichalcz@gmail.com", "mailto:promichalcz@gmail.com"), ("Main portfolio (Czech)", "https://mivoru.github.io/portfolio/"),
                  ("Source code", "https://github.com/Mivoru/portfolio-video")],
        "fine": "A sample tutorial on the TUL university e-learning, made for a portfolio. Personal data in the video and screenshots is blurred.",
    },
}

CSS = """
@font-face{font-family:"Instrument Serif";src:url(%(base)sfonts/instrument-serif-latin-ext-400-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+20A0-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Instrument Serif";src:url(%(base)sfonts/instrument-serif-latin-400-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Instrument Serif";font-style:italic;src:url(%(base)sfonts/instrument-serif-latin-ext-400-italic.woff2) format("woff2");font-display:swap;unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+20A0-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Instrument Serif";font-style:italic;src:url(%(base)sfonts/instrument-serif-latin-400-italic.woff2) format("woff2");font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Plex";font-weight:400;src:url(%(base)sfonts/ibm-plex-sans-latin-ext-400-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+20A0-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Plex";font-weight:400;src:url(%(base)sfonts/ibm-plex-sans-latin-400-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Plex";font-weight:600;src:url(%(base)sfonts/ibm-plex-sans-latin-ext-600-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+20A0-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Plex";font-weight:600;src:url(%(base)sfonts/ibm-plex-sans-latin-600-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Plex Mono";font-weight:400;src:url(%(base)sfonts/ibm-plex-mono-latin-ext-400-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+20A0-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Plex Mono";font-weight:400;src:url(%(base)sfonts/ibm-plex-mono-latin-400-normal.woff2) format("woff2");font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Plex Mono";font-weight:500;src:url(%(base)sfonts/ibm-plex-mono-latin-500-normal.woff2) format("woff2");font-display:swap}

:root{--paper:#f2efe6;--paper-2:#e9e5d8;--ink:#1a1a17;--mute:#66625a;--rule:#cfc9b8;--hl:#d4f54a;--film:#1b1a17;--max:1200px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#161512;--paper-2:#1f1e1a;--ink:#ebe7da;--mute:#a39e90;--rule:#3a3832;--film:#0c0c0a}}
:root[data-theme="dark"]{--paper:#161512;--paper-2:#1f1e1a;--ink:#ebe7da;--mute:#a39e90;--rule:#3a3832;--film:#0c0c0a}

*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font:400 17px/1.65 "Plex",system-ui,sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
img,video{display:block;max-width:100%%;height:auto}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{text-decoration-thickness:2px}
mark{background:linear-gradient(transparent 12%%,var(--hl) 12%%,var(--hl) 88%%,transparent 88%%);color:#1a1a17;padding:0 .08em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.wrap{max-width:var(--max);margin:0 auto;padding:0 16px}
@media (min-width:760px){.wrap{padding:0 40px}}
.mono{font-family:"Plex Mono",ui-monospace,monospace;font-size:13px;letter-spacing:.02em;text-transform:uppercase}
.serif{font-family:"Instrument Serif",Georgia,serif;font-weight:400;letter-spacing:-.01em}
.mute{color:var(--mute)}

header{border-bottom:1px solid var(--ink)}
header .wrap{display:flex;align-items:center;gap:24px;height:56px}
header .who{font-weight:600;text-decoration:none;white-space:nowrap}
header nav{margin-left:auto;display:flex;gap:22px;overflow-x:auto}
header nav a{text-decoration:none;color:var(--mute);white-space:nowrap}
header nav a:hover{color:var(--ink)}
header .lang{border:1px solid var(--ink);padding:3px 8px;text-decoration:none;white-space:nowrap}
header .lang:hover{background:var(--ink);color:var(--paper)}
@media (max-width:720px){header nav a.opt{display:none}}
@media (max-width:600px){header nav{display:none}header .lang{margin-left:auto}}

.hero{padding-top:44px;padding-bottom:28px}
.hero .meta{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-bottom:28px;color:var(--mute)}
.hero .grid{display:grid;gap:28px;align-items:end}
@media (min-width:960px){.hero .grid{grid-template-columns:1fr 300px;gap:56px}}
.hero h1{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:clamp(46px,8vw,112px);line-height:.95;letter-spacing:-.025em}
.hero .lead{font-size:clamp(18px,1.8vw,20px);max-width:58ch;margin-top:24px}
dl.colophon{border-top:1px solid var(--ink)}
dl.colophon div{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--rule)}
dl.colophon dt{color:var(--mute)}
dl.colophon dd{text-align:right}
figure.video{margin-top:36px}
figure.video .frame{border:1px solid var(--ink);background:#000;padding:0}
figure.video video{width:100%%;aspect-ratio:16/9}
figcaption{font-size:14px;color:var(--mute);margin-top:10px}
figcaption b{color:var(--ink);font-weight:600}

section{padding:72px 0 24px}
.sh{display:grid;gap:10px 40px;border-top:1px solid var(--ink);padding-top:18px;margin-bottom:40px}
@media (min-width:960px){.sh{grid-template-columns:240px 1fr}}
.sh .num{color:var(--mute)}
.sh h2{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:clamp(36px,5vw,62px);line-height:1;letter-spacing:-.02em;max-width:18ch}
.sh p{max-width:62ch;margin-top:14px;color:var(--mute);font-size:18px}
.body{display:grid;gap:40px}
@media (min-width:960px){.body{grid-template-columns:240px 1fr}.body > .side{align-self:start}}

.need{border-top:1px solid var(--rule)}
.need div{padding:10px 0;border-bottom:1px solid var(--rule)}
.need dt{color:var(--mute);font-size:14px}
ol.steps{list-style:none;display:grid;gap:56px}
.step{display:grid;gap:18px}
@media (min-width:1100px){.step{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:36px;align-items:start}}
.step figure img{border:1px solid var(--ink);background:#fff}
.step .n{font-family:"Instrument Serif",Georgia,serif;font-size:76px;line-height:.8;display:block;margin-bottom:12px}
.step h3{font-size:22px;font-weight:600;line-height:1.25;margin-bottom:8px}
.step p{color:var(--mute)}
.step p b{color:var(--ink);font-weight:600}
kbd{font:500 13px/1 "Plex Mono",monospace;border:1px solid var(--ink);border-bottom-width:2px;padding:2px 6px;border-radius:3px;color:var(--ink)}
.tip{margin-top:48px;border-left:3px solid var(--hl);padding:6px 0 6px 18px;max-width:62ch}
.tip strong{display:block;font-family:"Plex Mono",monospace;font-size:13px;text-transform:uppercase;font-weight:500;margin-bottom:4px}

table.stats{width:100%%;border-collapse:collapse;margin-bottom:56px}
table.stats td{border-bottom:1px solid var(--rule);padding:12px 0;vertical-align:baseline}
table.stats tr:first-child td{border-top:1px solid var(--ink)}
table.stats td:first-child{font-family:"Instrument Serif",Georgia,serif;font-size:clamp(32px,4vw,48px);line-height:1;width:44%%;white-space:nowrap;padding-right:16px}
table.stats td:last-child{color:var(--mute)}

ol.pipe{list-style:none;display:grid;gap:0;margin-bottom:72px;counter-reset:p;border-top:1px solid var(--ink)}
ol.pipe li{counter-increment:p;display:grid;grid-template-columns:44px 1fr;gap:4px 16px;padding:18px 0;border-bottom:1px solid var(--rule)}
@media (min-width:760px){ol.pipe li{grid-template-columns:56px 200px 1fr 180px;align-items:baseline}}
ol.pipe li::before{content:counter(p,decimal-leading-zero);font-family:"Plex Mono",monospace;font-size:13px;color:var(--mute);grid-row:span 3}
@media (min-width:760px){ol.pipe li::before{grid-row:auto}}
ol.pipe h3{font-size:18px;font-weight:600}
ol.pipe p{color:var(--mute);font-size:16px}
ol.pipe .tool{color:var(--mute)}
@media (min-width:760px){ol.pipe .tool{text-align:right}}

.block{margin-bottom:72px}
.block h3{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:34px;line-height:1.05;margin-bottom:6px}
.block > p{color:var(--mute);max-width:62ch;margin-bottom:20px}

.compare{position:relative;aspect-ratio:16/9;border:1px solid var(--ink);overflow:hidden;background:#000;user-select:none}
.compare img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.compare .top{clip-path:inset(0 calc(100%% - var(--x,50%%)) 0 0)}
.compare .bar{position:absolute;top:0;bottom:0;left:var(--x,50%%);width:2px;margin-left:-1px;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.25);pointer-events:none}
.compare .bar::after{content:"";position:absolute;top:50%%;left:50%%;width:34px;height:34px;transform:translate(-50%%,-50%%) rotate(45deg);background:#fff;border:1px solid #1a1a17}
.compare input{position:absolute;inset:0;width:100%%;height:100%%;opacity:0;cursor:ew-resize}
.compare .lbl{position:absolute;bottom:10px;background:#fff;color:#1a1a17;padding:4px 8px;border:1px solid #1a1a17;pointer-events:none}
.compare .l1{left:10px}.compare .l2{right:10px;background:var(--hl)}

.sheet{background:var(--film);padding:22px 14px;display:grid;grid-template-columns:repeat(2,1fr);gap:18px 10px;
  border:1px solid var(--ink);position:relative}
@media (min-width:640px){.sheet{grid-template-columns:repeat(4,1fr);padding:30px 18px}}
.sheet::before,.sheet::after{content:"";position:absolute;left:0;right:0;height:10px;
  background:repeating-linear-gradient(90deg,transparent 0 10px,#ece6d2 10px 18px,transparent 18px 28px);opacity:.5}
.sheet::before{top:6px}.sheet::after{bottom:6px}
.sheet figure img{width:100%%;aspect-ratio:16/9;object-fit:cover}
.sheet figcaption{font-family:"Plex Mono",monospace;font-size:11px;color:#f0b44a;margin-top:4px;letter-spacing:.04em;display:flex;justify-content:space-between}

.tl{display:flex;height:34px;border:1px solid var(--ink);margin-bottom:18px}
.tl div{display:flex;align-items:center;padding:0 8px;font-family:"Plex Mono",monospace;font-size:11px;text-transform:uppercase;
  border-right:1px solid var(--ink);white-space:nowrap;overflow:hidden;min-width:0}
.tl div:last-child{border-right:0}
.tl .st{background:var(--paper-2)}.tl .hi{background:var(--hl);color:#1a1a17}
ol.vo{list-style:none;border-top:1px solid var(--ink)}
ol.vo li{display:grid;grid-template-columns:64px 1fr;gap:16px;padding:12px 0;border-bottom:1px solid var(--rule)}
ol.vo time{font-family:"Plex Mono",monospace;font-size:13px;color:var(--mute);padding-top:4px}
ol.vo q{font-family:"Instrument Serif",Georgia,serif;font-size:23px;line-height:1.25;quotes:"„" "“"}
html[lang=en] ol.vo q{quotes:"“" "”"}
ol.vo small{display:block;font-size:13px;color:var(--mute);margin-top:2px}

pre{font:400 13.5px/1.7 "Plex Mono",ui-monospace,monospace;background:var(--paper-2);border:1px solid var(--rule);padding:20px;overflow-x:auto}
pre .c{color:var(--mute)}
pre .s{color:inherit;background:color-mix(in srgb,var(--hl) 35%%,transparent)}

.split{display:grid;border-top:1px solid var(--ink)}
@media (min-width:760px){.split{grid-template-columns:1fr 1fr}.split > div + div{border-left:1px solid var(--rule);padding-left:28px}}
.split > div{padding:20px 20px 20px 0}
.split h4{font-family:"Plex Mono",monospace;font-size:13px;font-weight:500;text-transform:uppercase;margin-bottom:10px}
.split ul{list-style:none}
.split li{padding:6px 0 6px 20px;position:relative;color:var(--mute)}
.split li::before{content:"—";position:absolute;left:0;color:var(--ink)}

.why{display:grid;border-top:1px solid var(--ink)}
@media (min-width:760px){.why{grid-template-columns:1fr 1fr}}
.why > div{padding:22px 24px 26px 0;border-bottom:1px solid var(--rule)}
@media (min-width:760px){.why > div:nth-child(even){padding-left:28px;border-left:1px solid var(--rule)}}
.why h3{font-size:19px;font-weight:600;margin-bottom:6px}
.why p{color:var(--mute)}

footer{margin-top:72px;border-top:1px solid var(--ink);padding:40px 0 48px}
footer h2{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:clamp(40px,6vw,80px);line-height:.98;letter-spacing:-.02em;max-width:16ch;margin:14px 0 18px}
footer p{max-width:58ch;color:var(--mute)}
footer ul{list-style:none;display:flex;flex-wrap:wrap;gap:10px 28px;margin:24px 0 36px;font-size:18px}
footer .fine{font-size:13px;color:var(--mute);border-top:1px solid var(--rule);padding-top:16px}

.fade{opacity:0;transform:translateY(10px);transition:opacity .7s ease,transform .7s ease}
.fade.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.fade{opacity:1;transform:none;transition:none}}
"""


def page(L):
    b, m = L["base"], L["media"]
    nav = "".join(f'<a href="#{i}"{" class=opt" if k == 3 else ""}>{t}</a>'
                  for k, (i, t) in enumerate(zip(["video", "guide", "making", "contact"], L["nav"])))
    colophon = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in L["colophon"])
    need = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in L["need"])
    steps = "".join(
        f'<li class="step fade"><figure><img src="{m}step-{i + 1}.webp" width="1600" height="900" loading="lazy" alt="{alt}">'
        f'<figcaption><b>{L["fig"]} {i + 1}.</b> {h}</figcaption></figure>'
        f'<div><span class="n">{i + 1 if i < 5 else "✓"}</span><h3>{h}</h3><p>{p}</p></div></li>'
        for i, (h, p, alt) in enumerate(L["steps"]))
    stats = "".join(f"<tr><td>{a}</td><td>{c}</td></tr>" for a, c in L["stats"])
    pipe = "".join(f'<li><h3>{h}</h3><p>{p}</p><span class="tool mono">{t}</span></li>' for h, p, t in L["pipe"])
    why = "".join(f"<div><h3>{h}</h3><p>{p}</p></div>" for h, p in L["why"])
    links = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in L["links"])
    ai = "".join(f"<li>{x}</li>" for x in L["ai"])
    me = "".join(f"<li>{x}</li>" for x in L["me"])
    c1, c2 = L["code_c"]
    css = CSS % {"base": b}
    alt_href = SITE + ("en/" if L["lang"] == "cs" else "")
    return f"""<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{L['title']}</title>
<meta name="description" content="{L['desc']}">
<link rel="alternate" hreflang="{'en' if L['lang'] == 'cs' else 'cs'}" href="{alt_href}">
<meta property="og:title" content="{L['title']}">
<meta property="og:description" content="{L['desc']}">
<meta property="og:image" content="{SITE}{m.replace('../', '')}poster.webp">
<style>{css}</style>
</head>
<body>
<header><div class="wrap">
  <a class="who" href="#top">Michal Votýpka</a>
  <nav>{nav}</nav>
  <a class="lang mono" href="{L['other']}" hreflang="{'en' if L['lang'] == 'cs' else 'cs'}" title="{L['other_name']}">{L['other_label']}</a>
</div></header>

<main id="top">
<div class="hero wrap" id="video">
  <div class="meta mono"><span>{L['meta']}</span><span>Michal Votýpka</span></div>
  <div class="grid">
    <div><h1>{L['h1']}</h1><p class="lead">{L['lead']}</p></div>
    <dl class="colophon">{colophon}</dl>
  </div>
  <figure class="video">
    <div class="frame"><video controls playsinline preload="metadata" poster="{m}poster.webp" width="1920" height="1080"><source src="{m}{L['video']}" type="video/mp4"></video></div>
    <figcaption>{L['video_cap']}</figcaption>
  </figure>
</div>

<section id="guide"><div class="wrap">
  <div class="sh"><span class="num mono">01 — {L['s1']}</span><div><h2>{L['s1_h']}</h2><p>{L['s1_p']}</p></div></div>
  <div class="body">
    <dl class="need side">{need}</dl>
    <div><ol class="steps">{steps}</ol>
      <div class="tip"><strong>{L['tip'][0]}</strong>{L['tip'][1]}</div></div>
  </div>
</div></section>

<section id="making"><div class="wrap">
  <div class="sh"><span class="num mono">02 — {L['s2']}</span><div><h2>{L['s2_h']}</h2><p>{L['s2_p']}</p></div></div>
  <table class="stats fade">{stats}</table>
  <ol class="pipe fade">{pipe}</ol>

  <div class="block fade"><h3>{L['cmp_h']}</h3><p>{L['cmp_p']}</p>
    <div class="compare" style="--x:50%">
      <img src="{m}compare-final.webp" width="1600" height="900" loading="lazy" alt="{L['cmp_alt'][0]}">
      <img class="top" src="{m}compare-raw.webp" width="1600" height="900" loading="lazy" alt="{L['cmp_alt'][1]}">
      <div class="bar"></div><span class="lbl l1 mono">{L['cmp_l'][0]}</span><span class="lbl l2 mono">{L['cmp_l'][1]}</span>
      <input type="range" min="0" max="100" value="50" aria-label="{L['cmp_aria']}">
    </div></div>

  <div class="block fade"><h3>{L['strip_h']}</h3><p>{L['strip_p']}</p><div class="sheet" id="sheet"></div></div>

  <div class="block fade"><h3>{L['tl_h']}</h3><p>{L['tl_p']}</p><div class="tl" id="tl"></div><ol class="vo" id="vo"></ol></div>

  <div class="block fade"><h3>{L['code_h']}</h3><p>{L['code_p']}</p>
<pre><code>{{
  "step": <span class="s">"{L['code_step']}"</span>,
  <span class="c"># {c1}</span>
  "pieces": [(31.8, 33.1, 1.5), (33.1, 40.0, 1.5), (40.0, 42.4, 2.0)],
  "vo": <span class="s">"{L['code_vo']}"</span>,
  <span class="c"># {c2}</span>
  "cam": [(0, (420, 800, 1.8)), ("s32.6", (665, 800, 2.6)), ("s41.6", (654, 900, 1.8))],
  "rings": [((570, 843, 192, 39), "s32.0", "s40.2")],
  "callouts": [(<span class="s">"{L['code_callout']}"</span>, (762, 862), "right", "s32.2", "s40.2")],
  "sfx": [("pop", "s32.2"), ("typing", "s33.3")],
}}</code></pre></div>

  <div class="split fade"><div><h4>{L['ai_h']}</h4><ul>{ai}</ul></div><div><h4>{L['me_h']}</h4><ul>{me}</ul></div></div>
</div></section>

<section id="why"><div class="wrap">
  <div class="sh"><span class="num mono">03 — {L['s3']}</span><div><h2>{L['s3_h']}</h2></div></div>
  <div class="why fade">{why}</div>
</div></section>
</main>

<footer id="contact"><div class="wrap">
  <span class="mono mute">04 — {L['s4']}</span>
  <h2>{L['foot_h']}</h2>
  <p>{L['foot_p']}</p>
  <ul>{links}</ul>
  <p class="fine">{L['fine']}</p>
</div></footer>

<script>
const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {{
  if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
}}), {{ rootMargin: '0px 0px -6% 0px' }}) : null;
document.querySelectorAll('.fade').forEach(el => io ? io.observe(el) : el.classList.add('in'));
document.querySelectorAll('.compare').forEach(c => {{
  const r = c.querySelector('input');
  r.addEventListener('input', () => c.style.setProperty('--x', r.value + '%'));
}});
const SEG = {L['seg']!r};
const fmt = s => `${{Math.floor(s / 60)}}:${{String(Math.floor(s % 60)).padStart(2, '0')}}`;
fetch('{m}timeline.json').then(r => r.json()).then(d => {{
  const sheet = document.getElementById('sheet');
  for (let i = 0; i < 16; i++) {{
    const t = i * d.total / 16 + 0.6, n = String(i).padStart(2, '0');
    sheet.insertAdjacentHTML('beforeend', `<figure><img src="{m}strip/${{n}}.webp" width="480" height="270" loading="lazy" alt="{L['strip_alt']} ${{fmt(t)}}"><figcaption><span>${{n}}A</span><span>${{fmt(t)}}</span></figcaption></figure>`);
  }}
  const tl = document.getElementById('tl'), vo = document.getElementById('vo');
  d.segments.forEach(s => {{
    const name = s.id === 'intro' ? SEG.intro : s.id === 'outro' ? SEG.outro : s.step ? `${{SEG.step}} ${{s.id.slice(1)}}` : SEG.result;
    const cls = s.step ? 'st' : s.id === 's6' ? 'hi' : '';
    tl.insertAdjacentHTML('beforeend', `<div class="${{cls}}" style="flex:${{s.dur}}" title="${{name}}">${{s.dur > 3.4 ? name : ''}}</div>`);
    if (s.vo) vo.insertAdjacentHTML('beforeend', `<li><time>${{fmt(s.start)}}</time><div><q>${{s.vo}}</q><small>${{name}}${{s.step ? ' · ' + s.step : ''}}</small></div></li>`);
  }});
}}).catch(() => {{}});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for L in T.values():
        out = ROOT / L["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(L), encoding="utf-8")
        print(out.relative_to(ROOT))
