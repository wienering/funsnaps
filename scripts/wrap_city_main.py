"""Add skip link, city-page body class, site-navigation id, and main#main-content wrapper."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["toronto.html", "mississauga.html", "vaughan.html", "oakville.html", "richmond-hill.html"]

for name in FILES:
    p = ROOT / name
    t = p.read_text(encoding="utf-8")
    orig = t
    if 'class="city-page"' not in t:
        t = t.replace("<body>", '<body class="city-page">', 1)
    if "skip-link" not in t:
        t = t.replace(
            '<body class="city-page">',
            '<body class="city-page">\n    <a href="#main-content" class="skip-link">Skip to main content</a>',
            1,
        )
    t = t.replace('<header class="navbar', '<header id="site-navigation" class="navbar', 1)
    marker = "</header>\n\n    <section class=\"inner-hero-lucci\">"
    if "<main id=\"main-content\"" not in t and marker in t:
        t = t.replace(
            marker,
            "</header>\n\n    <main id=\"main-content\" tabindex=\"-1\">\n\n    <section class=\"inner-hero-lucci\">",
            1,
        )
    foot = "\n    <!-- Footer -->"
    if foot in t and "</main>" not in t.split("<!-- Footer -->")[0]:
        t = t.replace(foot, "\n    </main>" + foot, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print("wrapped", name)
    else:
        print("skip", name)
