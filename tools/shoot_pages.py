#!/usr/bin/env python3
"""Render served course pages to PNGs for review (light/dark, desktop/mobile)."""
import os, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8091"
OUT = os.path.join(os.path.dirname(__file__), "..", "_review")
os.makedirs(OUT, exist_ok=True)

# (name, path, width, height, scheme, full_page)
JOBS = [
    ("lesson1_desktop_light", "/lesson_01.html", 1280, 900, "light", True),
    ("lesson1_desktop_dark",  "/lesson_01.html", 1280, 900, "dark",  True),
    ("lesson1_mobile_light",  "/lesson_01.html", 390, 844, "light", True),
    ("index_desktop_light",   "/index.html",     1280, 900, "light", True),
    ("index_desktop_dark",    "/index.html",     1280, 900, "dark",  True),
    ("lesson2_desktop_light", "/lesson_02.html", 1280, 900, "light", True),
    ("lesson3_desktop_light", "/lesson_03.html", 1280, 900, "light", True),
    ("index_mobile_light",    "/index.html",     390, 844, "light", True),
]
only = sys.argv[1:] if len(sys.argv) > 1 else None

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--use-gl=swiftshader"])
    for name, path, w, h, scheme, full in JOBS:
        if only and name not in only:
            continue
        ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto(BASE + path, wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(2500)  # let mermaid render
        out = os.path.join(OUT, name + ".png")
        pg.screenshot(path=out, full_page=full)
        print("saved", name, os.path.getsize(out)//1024, "KB")
        ctx.close()
    b.close()
print("DONE")
