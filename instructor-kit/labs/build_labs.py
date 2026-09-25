#!/usr/bin/env python3
"""Build every reference Scratch project (.sb3) for the instructor kit labs.

Each project mirrors the scripts in the matching course lesson. Run from anywhere:
    python3 labs/build_labs.py
Library assets are cached in labs/_assets/ (downloaded once from the Scratch asset server).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sb3lib import *  # noqa: E402,F401,F403

L = os.path.dirname(os.path.abspath(__file__))
CAT = ["cat-a", "cat-b"]
GAME_OVER_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="90" viewBox="0 0 300 90">'
                 '<rect x="2" y="2" width="296" height="86" rx="16" fill="#ffffff" stroke="#9966FF" stroke-width="4"/>'
                 '<text x="150" y="58" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="bold" '
                 'text-anchor="middle" fill="#9966FF">GAME OVER</text></svg>')


def lab(rel, **kw):
    build(os.path.join(L, rel), **kw)
    print("wrote", rel)


# ---- Module 1 -------------------------------------------------------------
def m1():
    lab("module-1/l1-3-cat-move-talk.sb3", sprites=[Sprite("Sprite1", CAT, ["Meow"], scripts=[
        [flag(), move(50), say_for("Hello! I'm Scratch Cat", 2)],
    ])])


# ---- Module 2 -------------------------------------------------------------
def m2():
    lab("module-2/l2-1-greeting-routine.sb3", sprites=[Sprite("Sprite1", CAT, ["Meow"], scripts=[
        [flag(), goto_xy(0, 0), say_for("Hi, I'm Scratchy!", 2), wait(1), move(120), say_for("Welcome to my world!", 2)],
    ])])
    lab("module-2/l2-2-walking-cat.sb3", sprites=[Sprite("Sprite1", CAT, ["Meow"], x=-200, scripts=[
        [flag(), goto_xy(-200, 0), repeat(20, [move(20), next_costume(), wait(0.1)])],
    ])])
    lab("module-2/l2-3-arrow-key-cat.sb3", sprites=[Sprite("Sprite1", CAT, ["Meow"], scripts=[
        [flag(), forever([
            if_(key_pressed("right arrow"), [change_x(10)]),
            if_(key_pressed("left arrow"), [change_x(-10)]),
            if_(key_pressed("up arrow"), [change_y(10)]),
            if_(key_pressed("down arrow"), [change_y(-10)]),
        ])],
    ])])


# ---- Module 3 -------------------------------------------------------------
def apple_game(bugs=False):
    """Lesson 3.2 catch-the-apple. bugs=True plants the four Bug Hunt bugs (lesson 3.3 lab):
    1 Cat follows mouse y (not x) · 2 no `set score to 0` · 3 `change y by 8` (apple never falls)
    4 `change score by 1` inside the falling loop (score races up)."""
    fall_body = [change_y(8 if bugs else -8), if_(lt(ypos(), -170), [goto_xy(rand(-200, 200), 170)])]
    if bugs:
        fall_body.append(change_var("score", 1))
    after_catch = [] if bugs else [change_var("score", 1)]
    apple_loop = [goto_xy(rand(-200, 200), 170), repeat_until(touching("Cat"), fall_body)] + after_catch
    apple_script = [flag()] + ([] if bugs else [set_var("score", 0)]) + [forever(apple_loop)]
    cat_script = [flag(), forever([goto_xy(mouse_y() if bugs else mouse_x(), -140)])]
    return dict(sprites=[Sprite("Cat", CAT, ["Meow"], y=-140, scripts=[cat_script]),
                         Sprite("Apple", ["apple"], ["Chomp"], y=170, scripts=[apple_script])],
                variables=["score"])


def m3():
    lab("module-3/l3-1-conversation.sb3", stage_backdrops=["Forest"], sprites=[
        Sprite("Cat", CAT, ["Meow"], x=-200, y=-100, scripts=[
            [flag(), goto_xy(-200, -100), glide_xy(2, -60, -100), say_for("Hi Bear!", 2), broadcast("line 2")],
            [recv("line 3"), say_for("Want to explore?", 2), broadcast("line 4")],
            [recv("line 4"), say_for("Let's go!", 1), glide_xy(2, 240, -100)],
        ]),
        Sprite("Bear", ["bear-a"], ["pop"], x=120, y=-80, size=60, scripts=[
            [flag(), goto_xy(120, -80)],
            [recv("line 2"), say_for("Hello Cat!", 2), broadcast("line 3")],
            [recv("line 4"), glide_xy(2, 240, -80)],
        ]),
    ])
    lab("module-3/l3-2-catch-the-apple.sb3", **apple_game())
    lab("module-3/l3-3-bug-hunt-starter.sb3", **apple_game(bugs=True))


# ---- Module 4 -------------------------------------------------------------
def star_catcher(final):
    """Lessons 4.3 (final=False: the smallest playable version) and 4.4 (final=True)."""
    bowl = Sprite("Bowl", ["bowl-a"], ["pop"], y=-150, scripts=[
        [define("reset game"), set_var("score", 0), set_var("lives", 3), goto_xy(0, -150), show()],
        [flag(), call("reset game"), forever([
            if_(key_pressed("right arrow"), [change_x(10)]),
            if_(key_pressed("left arrow"), [change_x(-10)]),
        ])],
    ])
    catch = if_(touching("Bowl"), [change_var("score", 1), hide(), play_until_done("Pop"), delete_clone()])
    fall = [change_y(-5), catch]
    if final:
        fall.append(if_(lt(ypos(), -170), [
            change_var("lives", -1),
            if_(eq(var("lives"), 0), [broadcast("game over")]),
            delete_clone(),
        ]))
    star = Sprite("Star", ["star"], ["Pop"], y=170, scripts=[
        [flag(), hide(), wait(1), forever([create_clone(), wait(rand(0.5, 1.5))])],
        [clone_start(), goto_xy(rand(-220, 220), 170), show(), forever(fall)],
    ])
    sprites = [bowl, star]
    stage_scripts, stage_sounds = [], []
    if final:
        sprites.append(Sprite("Game Over", ["game over"], visible=False,
                              custom_costumes={"game over": (GAME_OVER_SVG, 150, 45)}, scripts=[
            [flag(), hide()],
            [recv("game over"), go_front(), show(), stop_all()],
        ]))
        stage_scripts = [[flag(), forever([play_until_done("Xylo1")])]]
        stage_sounds = ["Xylo1"]
    return dict(sprites=sprites, stage_backdrops=["Stars"], variables=["score", "lives"],
                stage_scripts=stage_scripts, stage_sounds=stage_sounds)


def m4():
    lab("module-4/l4-1-falling-stars.sb3", stage_backdrops=["Stars"], sprites=[Sprite("Star", ["star"], ["Pop"], scripts=[
        [flag(), hide(), forever([goto_xy(rand(-220, 220), 180), create_clone(), wait(1)])],
        [clone_start(), show(), repeat_until(lt(ypos(), -170), [change_y(-5)]), delete_clone()],
    ])])
    lab("module-4/l4-2-my-blocks.sb3", variables=["score", "lives"], sprites=[Sprite("Sprite1", CAT, ["Meow"], scripts=[
        [define("jump"), repeat(10, [change_y(10)]), repeat(10, [change_y(-10)])],
        [key("space"), call("jump")],
        [clicked(), call("jump")],
        [define("dance", args=("times",)), repeat(arg("times"), [turn_right(15), wait(0.2), turn_left(15), wait(0.2)])],
        [flag(), call("dance", 3, args=("times",)), say_for("Ta-da!", 1), call("dance", 6, args=("times",))],
        [define("reset game"), set_var("score", 0), set_var("lives", 3), goto_xy(0, -150), show()],
        [flag(), call("reset game")],
    ])])
    lab("module-4/l4-3-star-catcher-part1.sb3", **star_catcher(final=False))
    lab("module-4/l4-4-star-catcher-final.sb3", **star_catcher(final=True))


if __name__ == "__main__":
    for f in sys.argv[1:] or ["m1", "m2", "m3", "m4"]:
        globals()[f]()
