# Module 4 Labs — Leveling Up (Sessions 4 and 5)

```
l4-1-falling-stars.sb3         4.1 — hidden original + forever: go to random x, create clone, wait 1; clones fall and delete themselves
l4-2-my-blocks.sb3             4.2 — define jump (space key / click), define dance (times) with an input, define reset game (score, lives)
l4-3-star-catcher-part1.sb3    4.3 — Star Catcher smallest playable version (bowl, falling star clones, score, reset game)
l4-4-star-catcher-final.sb3    4.4 — finished Star Catcher: lives, Game Over sprite + stop all, music loop on the Stage
```

**Family Build Night rescue file:** if a family falls far behind in Session 5, load
`l4-3-star-catcher-part1.sb3` so they can still do Part 2 (lives, Game Over) together.

In the Part 1 checkpoint, missed stars pile up at the bottom — that's expected; Part 2's
`if y position < -170` check (lose a life, delete the clone) fixes it.
