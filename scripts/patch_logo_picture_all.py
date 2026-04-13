from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OLD = '<img src="assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.png" alt="Fun Snaps Photo Booth Rental" class="logo-img" width="103" height="97">'
NEW = """<picture>
                        <source srcset="assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.webp" type="image/webp">
                        <img src="assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.png" alt="Fun Snaps Photo Booth Rental" class="logo-img" width="103" height="97" decoding="async">
                    </picture>"""

OLD404 = '<img src="/assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.png" alt="Fun Snaps Photo Booth Rental" class="logo-img" width="103" height="97">'
NEW404 = """<picture>
                        <source srcset="/assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.webp" type="image/webp">
                        <img src="/assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.png" alt="Fun Snaps Photo Booth Rental" class="logo-img" width="103" height="97" decoding="async">
                    </picture>"""

FAQ_OLD = '<img src="assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.png" alt="Fun Snaps Photo Booth Rental" class="logo-img" width="103" height="97" decoding="async">'
FAQ_NEW = """<picture>
                        <source srcset="assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.webp" type="image/webp">
                        <img src="assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.png" alt="Fun Snaps Photo Booth Rental" class="logo-img" width="103" height="97" decoding="async">
                    </picture>"""

for p in ROOT.glob("*.html"):
    t = p.read_text(encoding="utf-8")
    orig = t
    if p.name == "index.html":
        continue
    if OLD in t:
        t = t.replace(OLD, NEW)
    if OLD404 in t:
        t = t.replace(OLD404, NEW404)
    if FAQ_OLD in t:
        t = t.replace(FAQ_OLD, FAQ_NEW)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print("logo picture", p.name)
