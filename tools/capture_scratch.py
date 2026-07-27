#!/usr/bin/env python3
"""Capture real screenshots of scratch.mit.edu for the parent course.
Saves PNGs into ../images/. Uses Playwright (chromium)."""
import os, time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(OUT, exist_ok=True)
VW, VH = 1366, 820

def dismiss_cookies(page):
    for sel in [
        'button:has-text("Accept")',
        'button:has-text("I Accept")',
        'button:has-text("Got it")',
        '[aria-label*="ccept"]',
    ]:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click(); page.wait_for_timeout(500); return
        except Exception:
            pass

def shot(page, name, clip=None):
    path = os.path.join(OUT, name)
    page.screenshot(path=path, clip=clip)
    print("saved", name, "clip" if clip else "full")

def bbox_of(page, selectors):
    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if el:
                b = el.bounding_box()
                if b and b["width"] > 40 and b["height"] > 40:
                    return b
        except Exception:
            pass
    return None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist"])
    ctx = browser.new_context(viewport={"width":VW,"height":VH}, device_scale_factor=2)
    page = ctx.new_page()

    # 1) Home page
    page.goto("https://scratch.mit.edu", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3500)
    dismiss_cookies(page)
    page.wait_for_timeout(1000)
    shot(page, "scratch_home.png")

    # 2) Project editor
    page.goto("https://scratch.mit.edu/projects/editor/", wait_until="domcontentloaded", timeout=90000)
    # wait for the GUI to appear (green flag / stage controls)
    for sel in ['[class*="green-flag"]','[class*="stage-header"]','[class*="controls_"]']:
        try:
            page.wait_for_selector(sel, timeout=45000); break
        except Exception:
            continue
    page.wait_for_timeout(6000)
    dismiss_cookies(page)
    page.wait_for_timeout(1500)
    shot(page, "scratch_editor_full.png")

    # 3) Blocks palette (left) — clipped
    b = bbox_of(page, ['[class*="blocklyFlyout"]','.blocklyFlyout','[class*="gui_flex-wrapper"]'])
    palette = bbox_of(page, ['[class*="scratch-category-menu"]'])
    if palette:
        # widen to include flyout to the right of the category menu
        clip = {"x":max(palette["x"]-4,0),"y":max(palette["y"]-4,0),
                "width":min(360, VW-palette["x"]),"height":min(640, VH-palette["y"])}
        shot(page, "scratch_blocks_palette.png", clip=clip)

    # 4) Stage + sprite — clipped
    stage = bbox_of(page, ['[class*="stage-wrapper"]','[class*="stage_stage"]'])
    if stage:
        clip = {"x":stage["x"],"y":stage["y"],"width":min(stage["width"], VW-stage["x"]),"height":min(stage["height"], VH-stage["y"])}
        shot(page, "scratch_stage.png", clip=clip)

    # 5) Top controls (green flag + stop) — clipped narrow strip
    ctrl = bbox_of(page, ['[class*="controls_controls-container"]','[class*="controls_"]'])
    if ctrl:
        clip = {"x":ctrl["x"],"y":max(ctrl["y"]-6,0),"width":min(ctrl["width"]+20, VW-ctrl["x"]),"height":ctrl["height"]+12}
        shot(page, "scratch_controls.png", clip=clip)

    browser.close()
print("DONE")
