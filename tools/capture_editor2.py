#!/usr/bin/env python3
"""Capture Scratch editor states: category palettes + Make-a-Variable modal
+ sprite/backdrop libraries. Locates the left category menu by geometry."""
import os
from PIL import Image
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
VW, VH = 1366, 820

def crop_palette(page, name):
    tmp = os.path.join(OUT, "_tmp_full.png")
    page.screenshot(path=tmp)
    Image.open(tmp).crop((0, 116, 640, VH*2)).save(os.path.join(OUT, name))
    print("saved", name)

JS_MENU = """
() => {
  const names = ["Motion","Looks","Sound","Events","Control","Sensing","Operators","Variables"];
  const res = {};
  const all = [...document.querySelectorAll('div,span,li,button,p')];
  for (const n of names) {
    const el = all.find(e => {
      if (e.textContent.trim() !== n) return false;
      const r = e.getBoundingClientRect();
      return r.width > 5 && r.width < 130 && r.height < 90 && r.left < 120 && r.top > 60;
    });
    if (el) { const r = el.getBoundingClientRect(); res[n] = [Math.round(r.left + r.width/2), Math.round(r.top + r.height/2)]; }
  }
  return res;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--use-gl=swiftshader"])
    ctx = b.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto("https://scratch.mit.edu/projects/editor/", wait_until="domcontentloaded", timeout=90000)
    for sel in ['[class*="green-flag"]','[class*="stage-header"]']:
        try:
            page.wait_for_selector(sel, timeout=45000); break
        except Exception: continue
    page.wait_for_timeout(6000)

    coords = page.evaluate(JS_MENU)
    print("menu coords:", coords)

    wanted = {"Control":"scratch_palette_control.png",
              "Sensing":"scratch_palette_sensing.png",
              "Operators":"scratch_palette_operators.png",
              "Looks":"scratch_palette_looks.png",
              "Variables":"scratch_palette_variables.png"}
    for label, fname in wanted.items():
        if label not in coords:
            print("no coord for", label); continue
        x, y = coords[label]
        try:
            page.mouse.click(x, y); page.wait_for_timeout(1400)
            crop_palette(page, fname)
        except Exception as e:
            print("FAIL", label, repr(e)[:100])

    # Make a Variable modal (Variables palette should be showing now)
    try:
        page.get_by_role("button", name="Make a Variable").first.click()
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(OUT, "scratch_make_variable.png"))
        print("saved scratch_make_variable.png")
        try: page.get_by_role("button", name="Cancel").first.click()
        except Exception: page.keyboard.press("Escape")
        page.wait_for_timeout(600)
    except Exception as e:
        print("FAIL make-variable", repr(e)[:140])

    # Sprite & backdrop libraries (use .first to avoid strict-mode)
    for lbl, fname in [("Choose a Sprite","scratch_sprite_library.png"),
                       ("Choose a Backdrop","scratch_backdrop_library.png")]:
        try:
            page.get_by_role("button", name=lbl).first.click()
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUT, fname))
            print("saved", fname)
            page.keyboard.press("Escape"); page.wait_for_timeout(800)
        except Exception as e:
            print("FAIL", lbl, repr(e)[:120])

    try: os.remove(os.path.join(OUT, "_tmp_full.png"))
    except Exception: pass
    b.close()
print("DONE")
