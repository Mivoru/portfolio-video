"""Tutorial: how to add an interest (hobby) to a TUL e-learning profile.

All coordinates are in source-recording pixels (1920x1080).
Times written as "s16.7" are source-recording seconds; plain numbers are
seconds from the start of the segment in the output video.
"""

SOURCE = "input/elearning-zajmy.mkv"
OUTPUT = "out/zajmy.mp4"
TITLE = ["Jak přidat zájem", "na svůj profil"]
KICKER = "Návod · e-learning TUL"
OUTRO = ["Hotovo.", "Zájem je na profilu."]
CREDIT = "Ukázkový návod · Michal Votýpka"

MUSIC_PROMPT = (
    "Light, friendly background music for a software tutorial video. "
    "Soft plucked synths, gentle lo-fi beat, 100 BPM, optimistic, no vocals, unobtrusive."
)

# Sound effects generated with ElevenLabs (cached under cache/).
SFX = {
    "whoosh": ("Fast clean whoosh transition for a modern app video, smooth air swish", 1.0),
    "rewind": ("Short reverse swoosh, tape rewind feel, clean and modern", 1.0),
    "click": ("Single soft computer mouse click, close and crisp, no room noise", 0.5),
    "pop": ("Soft subtle UI pop when a small tooltip bubble appears", 0.5),
    "success": ("Short pleasant success chime, two bright notes, modern app notification", 1.2),
    "typing": ("Soft laptop keyboard typing, a few slow keystrokes, quiet room", 3.0),
}


def blur_rects(t):
    """Personal data to hide at source time t: (x0, y0, x1, y1) boxes."""
    rects = [(0, 1050, 680, 1080)]  # browser status bar shows the user id in URLs
    if 9.7 <= t < 19.85:  # dashboard
        rects += [(185, 635, 660, 1080), (1640, 436, 1880, 850)]
        if t < 17.25:  # before the user menu covers the top of the sidebar
            rects.append((1640, 340, 1880, 436))
    elif 19.85 <= t < 25.1:  # profile page
        rects += [(174, 443, 330, 467), (174, 563, 270, 587), (174, 623, 270, 647),
                  (824, 723, 1125, 746), (824, 783, 1125, 806), (174, 884, 570, 1080)]
    elif 25.1 <= t < 27.0:  # edit form, e-mail field
        rects.append((572, 548, 834, 584))
    elif 27.0 <= t < 28.6:  # form scrolling, e-mail field moves up and out
        rects.append((560, 0, 900, 600))
    elif t >= 44.6:  # profile page after saving (content shifted by the banner)
        rects += [(174, 512, 330, 536), (174, 692, 270, 716), (174, 752, 270, 776),
                  (824, 793, 1135, 816), (824, 853, 1135, 876), (174, 1013, 570, 1080)]
    return rects


# docs/ site: before/after pair (segment id, time) and the poster frame (output seconds)
DOC_COMPARE = ("s5", "s43.6")
DOC_POSTER = 3.6

FULL = (960, 540, 1.0)
CARD = (960, 400, 0.6)

SEGMENTS = [
    {
        "id": "intro", "hold_src": 47.0, "min_dur": 4.6, "vo_at": 0.35,
        "vo": "Chceš mít na profilu v e-learningu i svoje zájmy? Ukážu ti, jak na to.",
        "cam": [(0, (194, 645, 2.6)), (1.25, (194, 645, 2.85)), (2.45, CARD)],
        "rings": [((176, 636, 36, 18), 0.25, 1.4)],
        "callouts": [("Tvůj zájem na profilu", (212, 645), "right", 0.4, 1.4)],
        "sfx": [("pop", 0.4), ("whoosh", 1.2), ("rewind", "end-0.35")],
        "title": True,
    },
    {
        "id": "s1", "step": "Otevři svůj profil", "doc_at": "s19.2", "vo_at": 0.45,
        "pieces": [(15.4, 19.85, 1.0)],
        "vo": "Vpravo nahoře klikni na svoje iniciály a v nabídce vyber Profil.",
        "cam": [(0, CARD), (0.55, FULL), ("s15.95", FULL), ("s16.65", (1600, 240, 2.0))],
        "rings": [((1690, 12, 58, 40), "s16.15", "s16.95"), ((1537, 121, 218, 30), "s17.6", "end")],
        "callouts": [("Klikni na své iniciály", (1690, 32), "left", "s16.0", "s17.25"),
                     ("Vyber Profil", (1537, 136), "left", "s17.6", "end")],
        "clicks": [((1712, 32), "s16.7"), ((1600, 135), "s19.7")],
        "sfx": [("whoosh", 0.0), ("pop", "s16.0"), ("pop", "s17.6")],
    },
    {
        "id": "s2", "step": "Upravit profil", "doc_at": "s24.6", "vo_at": 0.2,
        "pieces": [(19.85, 24.2, 1.7), (24.2, 25.1, 1.0)],
        "vo": "Na stránce profilu klikni na Upravit profil.",
        "cam": [(0, FULL), (0.7, (600, 400, 1.9))],
        "rings": [((688, 391, 98, 27), 0.9, "end")],
        "callouts": [("Upravit profil", (786, 404), "right", 0.95, "end")],
        "clicks": [((736, 404), "s25.0")],
        "sfx": [("pop", 0.95)],
    },
    {
        "id": "s3", "step": "Rozbal sekci Zájmy", "doc_at": "s30.3", "vo_at": 0.3,
        "pieces": [(25.1, 26.9, 2.0), (26.9, 28.6, 1.0), (28.6, 30.6, 1.4), (30.6, 31.8, 1.0)],
        "vo": "Sjeď níž a rozbal sekci Zájmy.",
        "cam": [(0, FULL), ("s28.7", FULL), ("s29.4", (420, 800, 1.8))],
        "rings": [((178, 757, 144, 40), "s29.5", "s30.8")],
        "callouts": [("Rozbal sekci Zájmy", (322, 777), "right", "s29.55", "s30.8")],
        "clicks": [((197, 776), "s30.45")],
        "sfx": [("pop", "s29.55")],
    },
    {
        "id": "s4", "step": "Napiš svůj zájem", "doc_at": "s40.05", "vo_at": 0.3,
        "pieces": [(31.8, 33.1, 1.5), (33.1, 40.0, 1.5), (40.0, 42.4, 2.0)],
        "vo": "Do pole napiš, co tě baví. Třeba běh.",
        "cam": [(0, (420, 800, 1.8)), ("s32.6", (665, 800, 2.6)), ("s40.2", (665, 800, 2.6)),
                ("s41.6", (654, 900, 1.8))],
        "rings": [((570, 843, 192, 39), "s32.0", "s40.2")],
        "callouts": [("Napiš zájem, třeba běh", (762, 862), "right", "s32.2", "s40.2")],
        "clicks": [((665, 862), "s31.85")],
        "sfx": [("pop", "s32.2"), ("typing", "s33.3")],
    },
    {
        "id": "s5", "step": "Ulož změny", "doc_at": "s43.7", "vo_at": 0.1, "cap": "top",
        "pieces": [(42.4, 44.55, 1.0)],
        "vo": "Nakonec klikni na Aktualizovat profil.",
        "cam": [(0, (654, 900, 1.8))],
        "rings": [((574, 1022, 161, 42), 0.3, "end")],
        "callouts": [("Aktualizovat profil", (735, 1043), "right", 0.35, "end")],
        "clicks": [((654, 1042), "s44.2")],
        "sfx": [("pop", 0.35)],
    },
    {
        "id": "s6", "vo_at": 0.6, "doc_at": "s49.6",
        "pieces": [(44.6, 50.5, 1.0)],
        "vo": "A je to. Tvůj zájem se teď zobrazuje na profilu.",
        "cam": [(0, FULL), ("s45.3", (560, 520, 1.6)), ("s47.2", (560, 520, 1.6)),
                ("s48.4", (210, 640, 3.0))],
        "rings": [((176, 636, 36, 18), "s47.4", "end")],
        "callouts": [("Uloženo", (212, 645), "right", "s47.6", "end")],
        "checks": [((194, 645), "s47.5")],
        "sfx": [("success", "s47.5")],
    },
    {
        "id": "outro", "hold_src": 50.5, "min_dur": 3.2,
        "cam": [(0, (210, 640, 3.0)), (1.0, CARD)],
        "sfx": [("whoosh", 0.0)],
        "outro": True,
    },
]
