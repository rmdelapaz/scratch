# Scratch for Parents — Instructor Kit ("Course-in-a-Box")

A ready-to-teach package that lets another instructor run the course
**Scratch for Parents: Learn It, Then Teach It** as a live workshop series, without building it from scratch.
The free online course (rays-scratch.netlify.app) is the companion: participants can review any lesson at home.

**Complete — all five modules are built.**

| Module | Lessons | Session(s) | Status |
|--------|---------|------------|--------|
| 1 · Getting Started with Scratch | 1.1–1.3 | S1 | ✅ Built |
| 2 · Core Coding Concepts | 2.1–2.3 | S2 | ✅ Built |
| 3 · Building Real Projects | 3.1–3.3 | S3 | ✅ Built |
| 4 · Leveling Up — Bigger Projects | 4.1–4.4 | S4 + **S5 Family Build Night** | ✅ Built |
| 5 · Teaching Scratch to Your Child | 5.1–5.4 | S6 (+ showcase & graduation) | ✅ Built |

**Format:** six 2-hour sessions (~12 classroom hours), or three Saturday half-days. Participants are
parents and caregivers with no coding experience. Session 5 is a **Family Build Night**: children come,
and each parent–child pair builds the Star Catcher game together (child directs, parent types when asked).

### Primary documents — the combined books (start here)

The **canonical** print/hand-out documents: the whole course in one file each, with a cover, table of
contents, and one chapter per module.

| File | Audience | Contents |
|------|----------|----------|
| `participant-workbook.{html,pdf}` | Participant | All 5 modules: key ideas, worked examples, build steps, Teach-It practice, learning journal, self-checks |
| `facilitator-guide.{html,pdf}` | Instructor | Session run-sheets, timed teaching sequences, demo scripts, Teach-It role-plays, watch-outs |
| `answer-key.{html,pdf}` | Instructor | Every quiz answered and explained + lab solutions (confidential) |

The editable per-module docs live in `source/module-N/` (also usable for teaching a single module).
**If you edit a module's doc, run `python3 build-combined.py` to regenerate the three books, then
re-render their PDFs.**

### Kit-wide documents (at this folder's root)

| File | Audience | Purpose |
|------|----------|---------|
| `setup-guide.{html,pdf}` | Participant | "Before you begin" one-pager — send before Session 1 |
| `final-assessment.{html,pdf}` | Instructor | End-of-course brief: Star Catcher + personal extension, and a Teach-It demonstration; rubric + scoring sheet |
| `sell-sheet.{html,pdf}` | Prospective instructors | Marketing one-pager: what's inside, who it's for, license tiers |
| `README.md` · `LICENSE.md` | — | This overview and the tiered license template |

The 6-session **syllabus** (screen + print versions) lives in the course root, one level up:
`../syllabus.html`, `../syllabus-print.html`.

---

## Folder layout

```
instructor-kit/
├─ participant-workbook.{html,pdf}   ← canonical hand-out books (all 5 modules)
├─ facilitator-guide.{html,pdf}
├─ answer-key.{html,pdf}
├─ setup-guide / final-assessment / sell-sheet  (.html + .pdf)
├─ slides/     module-1-getting-started.html … module-5-teaching-your-child.html
├─ labs/       module-1/ … module-4/  reference Scratch projects (.sb3) + READMEs
│              module-5/  role-play cards + online-safety checklist (print)
│              build_labs.py · sb3lib.py  — regenerate the .sb3 files
├─ source/     module-1/ … module-5/  — editable per-module docs (build the books)
├─ kit.css     shared print-first stylesheet (includes the Scratch block visuals)
├─ build-combined.py  regenerate the 3 books from source/
└─ README.md · LICENSE.md
```

Every document is print-ready (a **Print / Save as PDF** button and a tuned `@media print` layout).
Slide decks are single files that need no server (arrow keys / space to advance).

### How to teach from it
1. Send participants the **setup guide** a week before Session 1.
2. Skim the **facilitator guide** chapter and the session **run-sheet** (minute by minute, 120 minutes).
3. Present from the module's deck in **`slides/`** (full-screen the browser).
4. Demo in Scratch; send participants to the lab. Use the matching **`.sb3`** in `labs/` to demo,
   check work, or rescue anyone who falls behind (**File → Load from your computer**).
5. Run the **Teach-It role-play**: pairs, one adult plays the child from a kid card, the other coaches.
6. Participants write in the **workbook** (printed or on screen); check with the **answer key**.

### The lab projects
Eleven reference projects, one for each build lesson, generated from Python by `labs/build_labs.py`
and verified in the Scratch 3 engine. `labs/module-3/l3-3-bug-hunt-starter.sb3` is deliberately broken —
it is the 3.3 debugging lab (four planted bugs; see `labs/module-3/README.md`).

### Editing
The three books at the root are **generated** from `source/module-N/` by `build-combined.py`. Edit the
source doc, run `python3 build-combined.py`, then re-render the PDFs. Don't hand-edit the combined
`.html` files — your changes will be overwritten on the next build.

**Still to do:** `LICENSE.md` is a plain-language **template** — have it reviewed before commercial
distribution. Pricing in the sell sheet is a suggested anchor; adjust to your market.

---

## License

See `LICENSE.md`. Short version: the kit is licensed to a **single instructor or organization** to teach
the course; it is **not** to be resold, and the answer key is **not** for participant distribution.
Scratch is a project of the Scratch Foundation; this kit is independent and not affiliated with or
endorsed by the Scratch Foundation or MIT.

© 2026 Ray de la Paz — Scratch for Parents: Learn It, Then Teach It — instructor kit.
