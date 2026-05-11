import random
from pathlib import Path

WORDLIST_PATH = Path(__file__).parent / "wordlist.10000.txt"

F1_FILE = Path(__file__).parent / "series/F/1/data.yaml"
F2_FILE = Path(__file__).parent / "series/F/2/data.yaml"
F3_FILE = Path(__file__).parent / "series/F/3/data.yaml"
F4_FILE = Path(__file__).parent / "series/F/4/data.yaml"

NUM_DRILLS = 5
LINE_WIDTH = 55


_BLOCKLIST = {
    "anal", "anus", "ass", "asses", "asshole", "assholes",
    "bastard", "bastards", "bitch", "bitches",
    "blowjob", "blowjobs", "boobs", "boner",
    "cock", "cocks", "crap", "cum", "cums", "cunt", "cunts",
    "damn", "dick", "dicks", "dildo", "dildos", "dyke", "dykes",
    "fag", "fags", "faggot", "faggots", "fuck", "fucked", "fucking", "fucks",
    "gay", "gays",
    "hell", "homo", "homos", "horny",
    "jerk", "jerks", "jizz",
    "kike", "kill",
    "milf", "muff",
    "nazi", "nigga", "niggas", "nude", "nudes", "nudist",
    "orgasm", "orgy",
    "piss", "pissed", "porn", "porno", "prick", "pricks", "pussy",
    "rape", "raped", "rapist",
    "sex", "sexes", "sexual", "sexy", "shit", "shits", "shitting", "slut", "sluts",
    "spank", "spanking",
    "tit", "tits", "titties", "twat", "twats", "twink", "twinks",
    "vagina", "vibrator",
    "wank", "wanker", "whore", "whores",
}


def _load_words():
    vowels = set("aeiou")
    with open(WORDLIST_PATH) as f:
        return [
            w.strip() for w in f
            if w.strip().isalpha()
            and len(w.strip()) >= 2
            and any(c in vowels for c in w.strip())
            and w.strip() not in _BLOCKLIST
        ]


def _make_content(word_pool):
    pool = random.sample(word_pool, min(300, len(word_pool)))
    lines = []
    current: list[str] = []
    current_len = 0
    for word in pool:
        space = 1 if current else 0
        if current_len + space + len(word) > LINE_WIDTH:
            if current:
                lines.append(" ".join(current))
            if len(lines) >= 5:
                break
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += space + len(word)
    if current and len(lines) < 5:
        lines.append(" ".join(current))
    return "\n".join(lines[:5])


def _write_yaml(fp, title, description, word_pool):
    drills = [_make_content(word_pool) for _ in range(NUM_DRILLS)]
    total = NUM_DRILLS + 1

    out = [f"total_segments: {total}", "", "segments:"]

    out += [
        "  0:",
        "    type: info",
        "    intro: |",
        f"      {title}",
        "    content: |",
    ]
    for line in description.split("\n"):
        out.append(f"      {line}")

    for i, content in enumerate(drills, 1):
        out += [
            f"  {i}:",
            "    type: drill",
            "    intro: |",
            f"      Random words ({i}/{NUM_DRILLS}) - type accurately!",
            "    content: |",
        ]
        for line in content.split("\n"):
            out.append(f"      {line}")

    with open(fp, "w") as f:
        f.write("\n".join(out) + "\n")


def words_short():
    words = [w for w in _load_words() if 3 <= len(w) <= 4]
    _write_yaml(
        F1_FILE,
        "Short Words (3-4 letters)",
        "Practice short common words. Focus on rhythm and accuracy.\n"
        "Each drill is freshly randomised from 10,000 common English words.",
        words,
    )


def words_medium():
    words = [w for w in _load_words() if 5 <= len(w) <= 7]
    _write_yaml(
        F2_FILE,
        "Medium Words (5-7 letters)",
        "Practice medium-length words (5 to 7 letters).\n"
        "Each drill is freshly randomised from 10,000 common English words.",
        words,
    )


def words_long():
    words = [w for w in _load_words() if len(w) >= 8]
    _write_yaml(
        F3_FILE,
        "Long Words (8+ letters)",
        "Practice longer words (8 letters or more). These challenge your finger memory.\n"
        "Each drill is freshly randomised from 10,000 common English words.",
        words,
    )


def words_mixed():
    words = [w for w in _load_words() if len(w) >= 3]
    _write_yaml(
        F4_FILE,
        "Mixed Words (all lengths)",
        "A full mix of short, medium, and long words.\n"
        "Each drill is freshly randomised from 10,000 common English words.",
        words,
    )
