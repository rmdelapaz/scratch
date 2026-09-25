# Labs

Reference Scratch projects (`.sb3`) and activity materials for the workshop, grouped by module.
Each module folder has its own README; this is the map.

```
labs/
├─ module-1/   Getting Started — the first moving, talking cat (1.3)
├─ module-2/   Core Coding Concepts — greeting routine (2.1), walking cat (2.2), arrow-key cat (2.3)
├─ module-3/   Building Real Projects — forest conversation (3.1), catch-the-apple (3.2), Bug Hunt starter (3.3)
├─ module-4/   Leveling Up — falling stars (4.1), My Blocks (4.2), Star Catcher checkpoint (4.3) + finished game (4.4)
├─ module-5/   Teaching Scratch to Your Child — role-play cards + online-safety checklist (print these)
├─ build_labs.py · sb3lib.py   regenerate every .sb3 from Python (see below)
```

## Opening a project
In the Scratch editor (online at scratch.mit.edu → **Create**, or the offline app):
**File → Load from your computer** → choose the `.sb3`. Click the green flag to run it.
Every file bundles its own costumes and sounds, so it opens without internet in the offline app.

## How to use them in class
- Each `.sb3` is the **finished reference** for its lesson — exactly the scripts drawn in the course
  lesson, the participant workbook, and the answer key. Use it to demo, to check work, or as a
  **rescue file** for anyone who falls behind (load it and keep going from there).
- The one exception is `module-3/l3-3-bug-hunt-starter.sb3`, which is deliberately broken — it *is* the lab.
- **Do not hand out reference files before the lab.** Building it is the point.

## Regenerating the projects
The `.sb3` files are generated, not hand-made:

```
python3 labs/build_labs.py          # all modules
python3 labs/build_labs.py m3       # just one module (m1 … m4)
```

`build_labs.py` holds each project's scripts; `sb3lib.py` compiles them into Scratch 3 format.
Library assets (the Scratch cat, Bear, Apple, Star, Bowl, backdrops, sounds) are downloaded once from the
Scratch asset server into `labs/_assets/` (git-ignored). Scratch library media is © the Scratch Foundation,
shared under CC BY-SA 2.0.

Every project was verified by loading it into the Scratch 3 engine and running it with the green flag
(falling clones, scoring, lives, Game Over).
