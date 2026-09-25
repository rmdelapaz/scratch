# Module 3 Labs — Building Real Projects

```
l3-1-conversation.sb3       3.1 — Forest backdrop; Cat glides in; a 4-line conversation chained with broadcasts (line 2 → line 3 → line 4), then both glide off
l3-2-catch-the-apple.sb3    3.2 — the catch game: Cat follows the mouse; Apple falls; score variable
l3-3-bug-hunt-starter.sb3   3.3 — the 3.2 game with FOUR planted bugs (this file is the lab)
```

## 3.2 — why the apple checks `y position < -170`
The apple starts at `y: 170`, where it is already touching the **top** edge, so an `if touching edge?`
check would send it back to the top every frame and it would never fall. "Below -170" means only "near the
bottom". (The course lesson was corrected to this version; the same trick returns in Module 4.)

## 3.3 — the Bug Hunt (instructor eyes only)

| # | Symptom participants see | Bug | Fix |
|---|---|---|---|
| 1 | The cat drifts oddly / moves when the mouse goes up and down | Cat: `go to x: (mouse y)` | use `mouse x` |
| 2 | Score starts where the last game ended | Apple: `set score to 0` missing | add it right after the green flag |
| 3 | The apple sits at the top and never falls | Apple: `change y by 8` | `change y by -8` |
| 4 | The score races up while the apple is falling | Apple: `change score by 1` is *inside* the falling loop | move it out, just below `repeat until` |

Fixed version = `l3-2-catch-the-apple.sb3`. Hint ladder and pairing format: see the facilitator guide.
