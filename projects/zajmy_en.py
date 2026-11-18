"""English version of the zajmy tutorial: same recording, timeline and effects.

The e-learning interface stays in Czech, so callouts name the Czech label and
give its English meaning, while the narration uses the English meaning.
"""
import copy
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("zajmy_base", Path(__file__).with_name("zajmy.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

SOURCE = base.SOURCE
blur_rects = base.blur_rects
SFX = base.SFX
MUSIC_PROMPT = base.MUSIC_PROMPT
DOC_COMPARE = base.DOC_COMPARE
DOC_POSTER = base.DOC_POSTER

OUTPUT = "out/zajmy_en.mp4"
DOCS_DIR = "docs/media/en"
LANG = "en"
VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"  # "Alice - Clear, Engaging Educator", ElevenLabs premade
TITLE = ["How to add an interest", "to your profile"]
KICKER = "Tutorial · TUL e-learning"
OUTRO = ["Done.", "Your interest is on your profile."]
CREDIT = "Sample tutorial · Michal Votýpka"

TEXT = {
    "intro": {"vo": "Want your interests to show on your e-learning profile? Here's how to add one.",
              "callouts": ["Your interest on your profile"]},
    "s1": {"step": "Open your profile",
           "vo": "In the top right corner, click your initials, then choose Profile.",
           "callouts": ["Click your initials", "Choose “Profil” (Profile)"]},
    "s2": {"step": "Edit profile", "vo": "On your profile page, click Edit profile.",
           "callouts": ["“Upravit profil” = Edit profile"]},
    "s3": {"step": "Expand Interests", "vo": "Scroll down and expand the Interests section.",
           "callouts": ["Expand “Zájmy” (Interests)"]},
    "s4": {"step": "Type an interest", "vo": "Type in something you enjoy. Here, it's running.",
           "callouts": ["Type an interest, e.g. běh (running)"]},
    "s5": {"step": "Save changes", "vo": "Finally, click Update profile.",
           "callouts": ["“Aktualizovat profil” = Update profile"]},
    "s6": {"vo": "That's it. Your interest now shows on your profile.", "callouts": ["Saved"]},
}

SEGMENTS = copy.deepcopy(base.SEGMENTS)
for seg in SEGMENTS:
    t = TEXT.get(seg["id"])
    if not t:
        continue
    seg["vo"] = t["vo"]
    if "step" in t:
        seg["step"] = t["step"]
    seg["callouts"] = [(new,) + tuple(old[1:]) for new, old in zip(t["callouts"], seg["callouts"])]
