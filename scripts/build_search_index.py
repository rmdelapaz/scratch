#!/usr/bin/env python3
"""Build search-index.json (course-wide search) from the lesson pages.

Run after editing any lesson:  python3 scripts/build_search_index.py
Lesson order and titles come from course-config.json.
"""
import json, re, html
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"script", "style", "nav", "footer", "button"}


class Sections(HTMLParser):
    """Collect (id, heading, text) for each <section id=...> in <main>."""
    def __init__(self):
        super().__init__()
        self.sections, self.cur, self.skip, self.in_h2 = [], None, 0, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP or (tag == "div" and "mermaid" in (a.get("class") or "")):
            self.skip += 1
        elif tag == "section" and a.get("id"):
            self.cur = {"id": a["id"], "heading": "", "text": []}
            self.sections.append(self.cur)
        elif tag == "h2" and self.cur is not None:
            self.in_h2 = True

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        elif tag == "h2":
            self.in_h2 = False

    def handle_data(self, data):
        if self.skip or self.cur is None:
            return
        if self.in_h2:
            self.cur["heading"] += data
        else:
            self.cur["text"].append(data)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def main():
    cfg = json.loads((ROOT / "course-config.json").read_text())
    out = []
    for mi, mod in enumerate(cfg["modules"], 1):
        for li, les in enumerate(mod["lessons"], 1):
            p = Sections()
            p.feed((ROOT / les["filename"]).read_text())
            out.append({
                "url": les["filename"],
                "label": f"Lesson {mi}.{li}",
                "title": les["title"],
                "sections": [{"id": s["id"], "heading": clean(s["heading"]), "text": clean(" ".join(s["text"]))}
                             for s in p.sections],
            })
    (ROOT / "search-index.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(f"search-index.json: {len(out)} lessons, {sum(len(l['sections']) for l in out)} sections")


if __name__ == "__main__":
    main()
