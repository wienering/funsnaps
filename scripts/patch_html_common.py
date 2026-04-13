"""Apply common head/script patches to root-level HTML files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_BLOCK = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
"""


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = text.replace('lang="en-CA"', 'lang="en"')
    if "preconnect" not in text and 'name="viewport"' in text:
        text = text.replace(
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + FONT_BLOCK,
            1,
        )
    text = text.replace('href="styles/main.css"', 'href="styles/main.min.css"')
    text = re.sub(
        r'<script src="scripts/main\.js"></script>',
        '<script src="scripts/main.min.js" defer></script>',
        text,
    )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("patched", path.name)


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        patch_file(p)


if __name__ == "__main__":
    main()
