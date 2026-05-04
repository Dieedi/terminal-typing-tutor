# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
ttt                        # Launch the tutor (entry point installed by pip)
python -m terminal_typing_tutor  # Alternative launch
```

No build step — this is a pure Python package installed via pip.

## Architecture Overview

**terminal_typing_tutor** is a `blessed`-based terminal typing tutor inspired by GNU Typist. The application is almost entirely procedural, centered on `tutor.py` (~580 lines), with global state variables (`series`, `lesson`, `segment`, and current drill stats).

**Main flow**: `main.py` → `tutor()` → series menu → lesson menu → loop over segments (info screens or interactive drills) → stats/PB tracking → repeat.

### Key Files

- `tutor.py` — entire application logic: menus, drill loop, stats, UI rendering
- `constants.py` — terminal handle (`TERM` via `blessed`), type definitions (`TSeries`, `TStats`), `MAIN_MENU`
- `qotd.py` — dynamically generates Series D lessons by fetching quotes from Wikiquote
- `series/` — all exercise content as YAML + metadata files

## Exercise Data Format

Exercises live under `series/[LETTER]/[LESSON_NUMBER]/data.yaml`:

```yaml
total_segments: 3

segments:
  0:
    type: info        # info | drill
    intro: |
      Introductory text shown before the segment.
    content: |
      Text displayed on the info screen.
  1:
    type: drill
    intro: |
      Instructions shown above the typing area.
    content: |
      Text the user must type (97%+ accuracy required to pass).
```

**Series metadata** (files in `series/[LETTER]/`):
- `title` — plain text, one line, series display name
- `lesson_count` — plain text, single integer
- `menu.json` — JSON array of `{"title": "..."}` objects, one per lesson

## Adding New Exercises

### Add a lesson to an existing series
1. Create `series/[LETTER]/[N]/data.yaml` with the YAML format above.
2. Increment `series/[LETTER]/lesson_count` by 1.
3. Append an entry to `series/[LETTER]/menu.json`.

### Add a new series
1. Create `series/[NEW_LETTER]/` with `title`, `lesson_count`, `menu.json`, and lesson subdirectories.
2. Add the series to `MAIN_MENU` in `constants.py` (type `TSeries` is a `Literal` of valid letters).
3. Update the `TSeries` `Literal` type in `constants.py` to include the new letter.
4. Add a case for the new series in `run_series_menu()` / `run_lesson()` in `tutor.py` if any custom behavior is needed (Series D is the only special case — it calls `qotd.py`).

### Drill content rules
- Lines should be short enough to fit terminal width when centered (~60 chars max per line recommended).
- Special characters: the app replaces newlines with spaces during drill input (`pressed_info()` in `tutor.py`).
- Accuracy threshold: 97.0% (hardcoded in `end_drill()`).
- PB tracking activates only for drills ≥ 200 characters (`MIN_CHARS` in `constants.py`).

## User Statistics

Stored at `~/.config/terminal-typing-tutor/`:
- `pb.yaml` — all-time personal best (WPM, CPM, accuracy, words, characters)
- `pb/[SERIES]/[LESSON]/[SEGMENT].yaml` — per-drill personal bests

Stats are loaded/written via `get_stats()` and `track_pb()` in `tutor.py`.

## Dependencies

| Package | Role |
|---|---|
| `blessed` | Terminal control (colors, input, cursor) |
| `pyyaml` | Load/write YAML exercise data and stats |
| `typer[all]` | CLI scaffolding (minimal use currently) |
| `wikiquote` | Quote fetching for Series D (QOTD) |
