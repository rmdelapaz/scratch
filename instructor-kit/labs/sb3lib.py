"""Tiny builder for Scratch 3 (.sb3) projects, used by build_labs.py.

Scripts are written as nested Python calls, e.g.

    flag(), say_for("Hello!", 2), forever([move(10), if_(touching("_edge_"), [turn(180)])])

and compiled into project.json with correct ids/parents/next/inputs.
Library assets (the Scratch cat, Bear, Apple, ...) are fetched once from the
Scratch asset server into labs/_assets/ and bundled, so the .sb3 files open offline.
"""
import hashlib
import io
import itertools
import json
import os
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(HERE, "_assets")
ASSET_URL = "https://assets.scratch.mit.edu/internalapi/asset/{}/get/"

# ---------------------------------------------------------------- blocks


class N:
    """A block node. inputs: name -> (kind, value); kind in num/text/bool/stack/menu/bcast/proto."""
    def __init__(self, opcode, inputs=None, fields=None, mutation=None, shadow=False):
        self.opcode, self.inputs, self.fields = opcode, inputs or {}, fields or {}
        self.mutation, self.shadow = mutation, shadow


def _n(op, **kw):
    return N(op, **kw)

# events / hats
def flag(): return _n("event_whenflagclicked")
def key(k): return _n("event_whenkeypressed", fields={"KEY_OPTION": [k, None]})
def clicked(): return _n("event_whenthisspriteclicked")
def recv(msg): return _n("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": [msg, "bc:" + msg]})
def clone_start(): return _n("control_start_as_clone")
def broadcast(msg): return _n("event_broadcast", inputs={"BROADCAST_INPUT": ("bcast", msg)})

# motion
def move(n): return _n("motion_movesteps", inputs={"STEPS": ("num", n)})
def turn_right(n): return _n("motion_turnright", inputs={"DEGREES": ("num", n)})
def turn_left(n): return _n("motion_turnleft", inputs={"DEGREES": ("num", n)})
def goto_xy(x, y): return _n("motion_gotoxy", inputs={"X": ("num", x), "Y": ("num", y)})
def glide_xy(s, x, y): return _n("motion_glidesecstoxy", inputs={"SECS": ("num", s), "X": ("num", x), "Y": ("num", y)})
def change_x(n): return _n("motion_changexby", inputs={"DX": ("num", n)})
def change_y(n): return _n("motion_changeyby", inputs={"DY": ("num", n)})
def set_x(n): return _n("motion_setx", inputs={"X": ("num", n)})
def set_y(n): return _n("motion_sety", inputs={"Y": ("num", n)})
def rotation_style(s): return _n("motion_setrotationstyle", fields={"STYLE": [s, None]})
def xpos(): return _n("motion_xposition")
def ypos(): return _n("motion_yposition")

# looks
def say_for(t, s): return _n("looks_sayforsecs", inputs={"MESSAGE": ("text", t), "SECS": ("num", s)})
def say(t): return _n("looks_say", inputs={"MESSAGE": ("text", t)})
def think_for(t, s): return _n("looks_thinkforsecs", inputs={"MESSAGE": ("text", t), "SECS": ("num", s)})
def next_costume(): return _n("looks_nextcostume")
def show(): return _n("looks_show")
def hide(): return _n("looks_hide")
def set_size(n): return _n("looks_setsizeto", inputs={"SIZE": ("num", n)})
def change_size(n): return _n("looks_changesizeby", inputs={"CHANGE": ("num", n)})
def change_effect(effect, n): return _n("looks_changeeffectby", inputs={"CHANGE": ("num", n)}, fields={"EFFECT": [effect, None]})
def go_front(): return _n("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]})
def switch_backdrop(name): return _n("looks_switchbackdropto", inputs={"BACKDROP": ("menu", ("looks_backdrops", "BACKDROP", name))})

# sound
def play_until_done(snd): return _n("sound_playuntildone", inputs={"SOUND_MENU": ("menu", ("sound_sounds_menu", "SOUND_MENU", snd))})
def start_sound(snd): return _n("sound_play", inputs={"SOUND_MENU": ("menu", ("sound_sounds_menu", "SOUND_MENU", snd))})

# control
def wait(s): return _n("control_wait", inputs={"DURATION": ("num", s)})
def repeat(n, body): return _n("control_repeat", inputs={"TIMES": ("num", n), "SUBSTACK": ("stack", body)})
def forever(body): return _n("control_forever", inputs={"SUBSTACK": ("stack", body)})
def if_(cond, body): return _n("control_if", inputs={"CONDITION": ("bool", cond), "SUBSTACK": ("stack", body)})
def if_else(cond, a, b): return _n("control_if_else", inputs={"CONDITION": ("bool", cond), "SUBSTACK": ("stack", a), "SUBSTACK2": ("stack", b)})
def repeat_until(cond, body): return _n("control_repeat_until", inputs={"CONDITION": ("bool", cond), "SUBSTACK": ("stack", body)})
def wait_until(cond): return _n("control_wait_until", inputs={"CONDITION": ("bool", cond)})
def stop_all(): return _n("control_stop", fields={"STOP_OPTION": ["all", None]}, mutation={"tagName": "mutation", "children": [], "hasnext": "false"})
def create_clone(): return _n("control_create_clone_of", inputs={"CLONE_OPTION": ("menu", ("control_create_clone_of_menu", "CLONE_OPTION", "_myself_"))})
def delete_clone(): return _n("control_delete_this_clone")

# sensing
def touching(obj): return _n("sensing_touchingobject", inputs={"TOUCHINGOBJECTMENU": ("menu", ("sensing_touchingobjectmenu", "TOUCHINGOBJECTMENU", obj))})
def key_pressed(k): return _n("sensing_keypressed", inputs={"KEY_OPTION": ("menu", ("sensing_keyoptions", "KEY_OPTION", k))})
def mouse_x(): return _n("sensing_mousex")
def mouse_y(): return _n("sensing_mousey")

# operators
def rand(a, b): return _n("operator_random", inputs={"FROM": ("num", a), "TO": ("num", b)})
def lt(a, b): return _n("operator_lt", inputs={"OPERAND1": ("text", a), "OPERAND2": ("text", b)})
def gt(a, b): return _n("operator_gt", inputs={"OPERAND1": ("text", a), "OPERAND2": ("text", b)})
def eq(a, b): return _n("operator_equals", inputs={"OPERAND1": ("text", a), "OPERAND2": ("text", b)})

# variables (resolved to ids at compile time)
class Var:
    def __init__(self, name): self.name = name
def var(name): return Var(name)
def set_var(name, v): return _n("data_setvariableto", inputs={"VALUE": ("text", v)}, fields={"VARIABLE": [name, "var:" + name]})
def change_var(name, v): return _n("data_changevariableby", inputs={"VALUE": ("num", v)}, fields={"VARIABLE": [name, "var:" + name]})

# custom blocks ("My Blocks"). Args are number/text ("%s").
def define(name, args=(), warp=False):
    proccode = " ".join([name] + ["%s" for _ in args]) if args else name
    return _n("procedures_definition", inputs={"custom_block": ("proto", (proccode, list(args), warp))})
def call(name, *vals, args=()):
    proccode = " ".join([name] + ["%s" for _ in args]) if args else name
    return _n("procedures_call", inputs={f"arg:{proccode}:{a}": ("text", v) for a, v in zip(args, vals)},
              mutation={"proccode": proccode, "argnames": list(args)})
def arg(name): return _n("argument_reporter_string_number", fields={"VALUE": [name, None]})

# ---------------------------------------------------------------- compiler

PRIM = {"num": 4, "text": 10}
C_BLOCKS = {"control_repeat", "control_forever", "control_if", "control_if_else", "control_repeat_until"}
REPORTERS = {"operator_random", "operator_lt", "operator_gt", "operator_equals", "motion_xposition",
             "motion_yposition", "sensing_mousex", "sensing_mousey", "sensing_touchingobject",
             "sensing_keypressed", "argument_reporter_string_number"}


class Compiler:
    def __init__(self, target_is_stage=False):
        self.blocks, self.ids = {}, itertools.count(1)

    def nid(self):
        return f"b{next(self.ids)}"

    def script(self, stack, x, y):
        self.stack(stack, parent=None, top=(x, y))

    def stack(self, nodes, parent, top=None):
        first, prev = None, None
        for i, node in enumerate(nodes):
            bid = self.node(node, parent=prev or parent, top=top if i == 0 else None)
            if prev:
                self.blocks[prev]["next"] = bid
            first = first or bid
            prev = bid
        return first

    def node(self, n, parent, top=None):
        bid = self.nid()
        b = {"opcode": n.opcode, "next": None, "parent": parent, "inputs": {}, "fields": dict(n.fields),
             "shadow": n.shadow, "topLevel": top is not None}
        if top is not None:
            b["x"], b["y"] = top
        self.blocks[bid] = b
        for name, (kind, val) in n.inputs.items():
            b["inputs"].update(self.input(bid, name, kind, val))
        if n.opcode == "procedures_call":
            m = n.mutation
            argids = [f"arg:{m['proccode']}:{a}" for a in m["argnames"]]
            b["mutation"] = {"tagName": "mutation", "children": [], "proccode": m["proccode"],
                             "argumentids": json.dumps(argids), "warp": "false"}
        elif n.mutation:
            b["mutation"] = n.mutation
        return bid

    def input(self, bid, name, kind, val):
        if kind == "stack":
            return {name: [2, self.stack(val, parent=bid)]} if val else {}
        if kind == "bool":
            return {name: [2, self.node(val, parent=bid)]}
        if kind == "menu":
            opcode, field, value = val
            sid = self.nid()
            self.blocks[sid] = {"opcode": opcode, "next": None, "parent": bid, "inputs": {},
                                "fields": {field: [value, None]}, "shadow": True, "topLevel": False}
            return {name: [1, sid]}
        if kind == "bcast":
            return {name: [1, [11, val, "bc:" + val]]}
        if kind == "proto":
            proccode, args, warp = val
            pid = self.nid()
            argids = [f"arg:{proccode}:{a}" for a in args]
            proto = {"opcode": "procedures_prototype", "next": None, "parent": bid, "inputs": {}, "fields": {},
                     "shadow": True, "topLevel": False,
                     "mutation": {"tagName": "mutation", "children": [], "proccode": proccode,
                                  "argumentids": json.dumps(argids), "argumentnames": json.dumps(args),
                                  "argumentdefaults": json.dumps(["" for _ in args]), "warp": json.dumps(warp)}}
            self.blocks[pid] = proto
            for a, aid in zip(args, argids):
                rid = self.nid()
                self.blocks[rid] = {"opcode": "argument_reporter_string_number", "next": None, "parent": pid,
                                    "inputs": {}, "fields": {"VALUE": [a, None]}, "shadow": True, "topLevel": False}
                proto["inputs"][aid] = [1, rid]
            return {name: [1, pid]}
        # num / text slot: literal, variable, or reporter block
        prim = PRIM[kind]
        if isinstance(val, Var):
            return {name: [3, [12, val.name, "var:" + val.name], [prim, ""]]}
        if isinstance(val, N):
            return {name: [3, self.node(val, parent=bid), [prim, ""]]}
        return {name: [1, [prim, str(val)]]}

# ---------------------------------------------------------------- assets


def asset(md5ext):
    """Return bytes of a Scratch library asset, cached in labs/_assets/."""
    os.makedirs(ASSET_DIR, exist_ok=True)
    path = os.path.join(ASSET_DIR, md5ext)
    if not os.path.exists(path):
        with urllib.request.urlopen(ASSET_URL.format(md5ext)) as r:
            data = r.read()
        if hashlib.md5(data).hexdigest() != md5ext.split(".")[0]:
            raise ValueError(f"checksum mismatch for {md5ext}")
        open(path, "wb").write(data)
    return open(path, "rb").read()


def custom_svg(svg):
    """Register an inline SVG; returns (md5ext, bytes)."""
    data = svg.encode()
    return hashlib.md5(data).hexdigest() + ".svg", data

# Scratch library entries: name -> (md5ext, rotationCenterX, rotationCenterY, bitmapResolution)
COSTUMES = {
    "cat-a": ("bcf454acf82e4504149f7ffe07081dbc.svg", 48, 50, 1),
    "cat-b": ("0fb9be3e8397c983338cb71dc84d0b25.svg", 46, 53, 1),
    "bear-a": ("deef1eaa96d550ae6fc11524a1935024.svg", 100, 90, 1),
    "apple": ("3826a4091a33e4d26f87a2fac7cf796b.svg", 31, 31, 1),
    "bowl-a": ("d147f16e3e2583719c073ac5b55fe3ca.svg", 30, 15, 1),
    "star": ("551629f2a64c1f3703e57aaa133effa6.svg", 22, 23, 1),
    "backdrop1": ("cd21514d0531fdffb22204e0ec5ed84a.svg", 240, 180, 1),
    "Forest": ("92968ac16b2f0c3f7835a6dacd172c7b.png", 480, 360, 2),
    "Stars": ("47282ff0f7047c6fab9c94b531abf721.png", 480, 360, 2),
}
SOUNDS = {
    "Meow": ("83c36d806dc92327b9e7049a565c6bff.wav", 44100, 37376),
    "pop": ("83a9787d4cb6f3b7632b4ddfebf74367.wav", 44100, 1032),
    "Pop": ("83a9787d4cb6f3b7632b4ddfebf74367.wav", 44100, 1032),
    "Chomp": ("0b1e3033140d094563248e61de4039e5.wav", 44100, 11648),
    "Xylo1": ("6ac484e97c1c1fe1384642e26a125e70.wav", 22050, 238761),
}

# ---------------------------------------------------------------- project


class Sprite:
    def __init__(self, name, costumes, sounds=(), x=0, y=0, size=100, visible=True, scripts=(),
                 custom_costumes=None, direction=90, layer=1):
        self.name, self.costumes, self.sounds = name, list(costumes), list(sounds)
        self.x, self.y, self.size, self.visible, self.scripts = x, y, size, visible, list(scripts)
        self.custom = custom_costumes or {}   # costume name -> (svg text, cx, cy)
        self.direction, self.layer = direction, layer


def build(path, sprites, stage_backdrops=("backdrop1",), stage_scripts=(), variables=(), stage_sounds=(), current_backdrop=0):
    files, targets, broadcasts = {}, [], {}

    def costume_entries(names, custom):
        out = []
        for c in names:
            if c in custom:
                svg, cx, cy = custom[c]
                md5ext, data = custom_svg(svg)
                files[md5ext] = data
                out.append({"name": c, "bitmapResolution": 1, "dataFormat": "svg", "assetId": md5ext[:-4],
                            "md5ext": md5ext, "rotationCenterX": cx, "rotationCenterY": cy})
            else:
                md5ext, cx, cy, res = COSTUMES[c]
                files[md5ext] = asset(md5ext)
                out.append({"name": c, "bitmapResolution": res, "dataFormat": md5ext.split(".")[1],
                            "assetId": md5ext.split(".")[0], "md5ext": md5ext, "rotationCenterX": cx, "rotationCenterY": cy})
        return out

    def sound_entries(names):
        out = []
        for s in names:
            md5ext, rate, count = SOUNDS[s]
            files[md5ext] = asset(md5ext)
            out.append({"name": s, "assetId": md5ext[:-4], "dataFormat": "wav", "format": "", "rate": rate,
                        "sampleCount": count, "md5ext": md5ext})
        return out

    def compile_scripts(scripts):
        c = Compiler()
        col_y = [20, 20]                      # two columns; stack scripts by their approximate height
        for s in scripts:
            col = 0 if col_y[0] <= col_y[1] else 1
            before = len(c.blocks)
            c.script(s, 20 + col * 420, col_y[col])
            new = [b for b in list(c.blocks.values())[before:] if not b["shadow"] and b["opcode"] not in REPORTERS]
            arms = sum(2 if b["opcode"] == "control_if_else" else 1 for b in new if b["opcode"] in C_BLOCKS)
            col_y[col] += 100 + len(new) * 56 + arms * 40
        for b in c.blocks.values():
            for f, v in b["fields"].items():
                if f == "BROADCAST_OPTION":
                    broadcasts[v[1]] = v[0]
            for inp in b["inputs"].values():
                if isinstance(inp[1], list) and inp[1][0] == 11:
                    broadcasts[inp[1][2]] = inp[1][1]
        return c.blocks

    stage_blocks = compile_scripts(stage_scripts)
    sprite_targets = []
    for i, sp in enumerate(sprites):
        sprite_targets.append({
            "isStage": False, "name": sp.name, "variables": {}, "lists": {}, "broadcasts": {},
            "blocks": compile_scripts(sp.scripts), "comments": {}, "currentCostume": 0,
            "costumes": costume_entries(sp.costumes, sp.custom), "sounds": sound_entries(sp.sounds),
            "volume": 100, "layerOrder": i + 1, "visible": sp.visible, "x": sp.x, "y": sp.y, "size": sp.size,
            "direction": sp.direction, "draggable": False, "rotationStyle": "all around"})
    stage = {"isStage": True, "name": "Stage",
             "variables": {"var:" + v: [v, 0] for v in variables}, "lists": {}, "broadcasts": broadcasts,
             "blocks": stage_blocks, "comments": {}, "currentCostume": current_backdrop,
             "costumes": costume_entries(stage_backdrops, {}), "sounds": sound_entries(stage_sounds),
             "volume": 100, "layerOrder": 0, "tempo": 60, "videoTransparency": 50, "videoState": "on",
             "textToSpeechLanguage": None}
    monitors = [{"id": "var:" + v, "mode": "default", "opcode": "data_variable", "params": {"VARIABLE": v},
                 "spriteName": None, "value": 0, "width": 0, "height": 0, "x": 5, "y": 5 + 27 * i,
                 "visible": True, "sliderMin": 0, "sliderMax": 100, "isDiscrete": True} for i, v in enumerate(variables)]
    project = {"targets": [stage] + sprite_targets, "monitors": monitors, "extensions": [],
               "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "Scratch for Parents instructor kit"}}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project))
        for name, data in sorted(files.items()):
            z.writestr(name, data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(buf.getvalue())
    return project
