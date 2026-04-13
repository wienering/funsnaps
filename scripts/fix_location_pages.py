"""Remove duplicate testimonials, orphan HTML, and inline city-page styles from location HTML files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "toronto.html",
    "mississauga.html",
    "vaughan.html",
    "oakville.html",
    "richmond-hill.html",
]


def fix(text: str) -> str:
    # Orphan fragment after FAQ (broken duplicate closing tags)
    text = re.sub(
        r"\s*</section>\s*</div>\s*<div class=\"features-image\">\s*"
        r"<img src=\"assets/images/wp-content/uploads/2022/09/photo-booth-rental-fun\.webp\"[^>]*>\s*"
        r"</div>\s*</div>\s*</div>\s*</section>",
        "",
        text,
        flags=re.DOTALL,
    )
    # First testimonial block (before Event Types)
    text = re.sub(
        r"\s*<!-- Testimonials Section -->\s*"
        r"<section class=\"services\"[^>]*>.*?"
        r"</section>\s*(?=<!-- Event Types Section -->)",
        "\n\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    # Second testimonial block (before CTA Section)
    text = re.sub(
        r"\s*<!-- Testimonials Section -->\s*"
        r"<section class=\"services\"[^>]*>.*?"
        r"</section>\s*(?=<!-- CTA Section -->)",
        "\n\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    # Inline style block for city images (now in main.css .city-page)
    text = re.sub(
        r"\s*<style>\s*/\* Limit images on city pages.*?</style>\s*",
        "\n",
        text,
        flags=re.DOTALL,
    )
    return text


def main() -> None:
    for name in FILES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        new = fix(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("fixed", name)
        else:
            print("no change", name)


if __name__ == "__main__":
    main()
