#!/usr/bin/env python3
"""Capture public Scratch pages for Module 4 (no login needed)."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
VW, VH = 1366, 900

def dismiss(page):
    for sel in ['button:has-text("Accept")','button:has-text("Got it")','[aria-label*="lose"]']:
        try:
            e = page.query_selector(sel)
            if e and e.is_visible(): e.click(); page.wait_for_timeout(400)
        except Exception: pass

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--use-gl=swiftshader"])
    ctx = b.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=2)
    page = ctx.new_page()

    def grab(url, name, wait=3500):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(wait); dismiss(page); page.wait_for_timeout(600)
            page.screenshot(path=os.path.join(OUT, name))
            print("saved", name)
        except Exception as e:
            print("FAIL", name, repr(e)[:120])

    grab("https://scratch.mit.edu/parents/", "scratch_parents_page.png")
    grab("https://scratch.mit.edu/community_guidelines", "scratch_community_guidelines.png")
    grab("https://www.scratchjr.org/", "scratchjr_home.png")

    # A public project page (best-effort): pick the first project from Explore
    try:
        page.goto("https://scratch.mit.edu/explore/projects/all", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000); dismiss(page)
        href = page.evaluate("""() => {
            const a = [...document.querySelectorAll('a[href*="/projects/"]')]
                .map(x => x.getAttribute('href'))
                .find(h => /\\/projects\\/\\d+/.test(h));
            return a || null;
        }""")
        if href:
            url = href if href.startswith("http") else ("https://scratch.mit.edu" + href)
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000); dismiss(page); page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(OUT, "scratch_project_page.png"))
            print("saved scratch_project_page.png from", url)
        else:
            print("no project link found")
    except Exception as e:
        print("FAIL project page", repr(e)[:140])

    b.close()
print("DONE")
