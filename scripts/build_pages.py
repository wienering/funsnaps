#!/usr/bin/env python3
"""
Static page builder for funsnaps.ca.

Wraps hand-written page bodies in the shared site chrome (head, header, footer)
so the chrome stays identical across pages without being copy-pasted sixteen
times. Run it, commit the generated .html — Vercel serves plain static files and
has no build step.

    python scripts/build_pages.py

Page bodies live in _content/<slug>.html. Each starts with a JSON front-matter
block between <!--META ... META--> carrying title, description, h1, lede,
breadcrumbs and any extra schema graph nodes. The CONTENT is hand-written per
page and deliberately NOT templated: these are local landing pages and
search-and-replace city pages are doorway pages.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "_content")
SITE = "https://www.funsnaps.ca"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800'
         '&family=DM+Sans:wght@400;500&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">')

BUSINESS = {
    "@type": "LocalBusiness",
    "@id": SITE + "/#business",
    "name": "Fun Snaps Photo Booth",
    "image": SITE + "/assets/images/wp-content/uploads/2022/09/photo-booth-rental-fun.webp",
    "logo": SITE + "/assets/img/logo-light.png",
    "url": SITE + "/",
    "telephone": "+1-647-375-0660",
    "email": "info@funsnaps.ca",
    "priceRange": "$550-$1000",
    "foundingDate": "2011",
    "currenciesAccepted": "CAD",
    "sameAs": ["https://www.instagram.com/funsnaps.ca",
               "https://www.facebook.com/FunSnaps.ca/"],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "160 Applewood Crescent",
        "addressLocality": "Concord",
        "addressRegion": "ON",
        "postalCode": "L4K 4E5",
        "addressCountry": "CA",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 43.8014, "longitude": -79.4869},
    "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                      "Friday", "Saturday", "Sunday"],
        "opens": "07:00",
        "closes": "23:00",
    },
}

NAV = [("/pricing", "Pricing"), ("/corporate-photo-booth-rental", "Corporate"),
       ("/glam-booth", "Glam"), ("/360-photo-booth", "360"),
       ("/faq", "FAQ"), ("/contact-us", "Contact")]

AREAS = [("/vaughan", "Vaughan"), ("/toronto", "Toronto"),
         ("/mississauga", "Mississauga"), ("/oakville", "Oakville"),
         ("/richmond-hill", "Richmond Hill"), ("/markham", "Markham"),
         ("/york-region", "York Region")]


def header():
    links = "\n      ".join(
        '<a href="%s">%s</a>' % (h, t) for h, t in NAV)
    mob = "\n    ".join('<a href="%s">%s</a>' % (h, t) for h, t in NAV)
    return f"""<header class="site-header site-header--solid">
  <div class="wrap header-row">
    <a href="/" class="logo" aria-label="Fun Snaps Photo Booth, home"><img src="/assets/img/logo-light.png" alt="Fun Snaps Photo Booth Co." class="logo-mark" width="103" height="97"></a>
    <nav class="main-nav" aria-label="Primary">
      {links}
    </nav>
    <div class="header-actions">
      <a href="/quote" class="btn btn-solid btn-small">Get a Quote</a>
      <button class="nav-toggle" id="navToggle" type="button" aria-expanded="false" aria-controls="mobileNav" aria-label="Open menu">
        <span class="nav-toggle-line"></span>
        <span class="nav-toggle-line"></span>
        <span class="nav-toggle-line"></span>
      </button>
    </div>
  </div>
  <nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
    {mob}
    <a href="/quote">Get a Quote</a>
  </nav>
</header>"""


def footer():
    fnav = "\n      ".join('<a href="%s">%s</a>' % (h, t) for h, t in NAV)
    fareas = "\n      ".join('<a href="%s">%s</a>' % (h, t) for h, t in AREAS)
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <img src="/assets/img/logo-light.png" alt="Fun Snaps Photo Booth Co." class="footer-logo footer-logo-mark" width="103" height="97" loading="lazy">
      <p class="footer-contact">
        <a href="mailto:info@funsnaps.ca">info@funsnaps.ca</a><br>
        <a href="tel:+16473750660">647.375.0660</a><br>
        160 Applewood Crescent, Concord, ON L4K 4E5<br>
        Serving Vaughan &amp; the GTA since 2011 &middot; Mon-Sun, 7am-11pm
      </p>
    </div>
    <nav class="footer-nav" aria-label="Footer">
      {fnav}
    </nav>
    <nav class="footer-nav" aria-label="Service areas">
      {fareas}
    </nav>
    <div class="footer-social">
      <p class="mono-tag">FOLLOW</p>
      <a href="https://www.instagram.com/funsnaps.ca" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.facebook.com/FunSnaps.ca/" target="_blank" rel="noopener">Facebook</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span class="mono-tag">&copy; 2026 FUN SNAPS PHOTO BOOTH CO.</span>
    <span class="mono-tag">CONCORD, ONTARIO</span>
  </div>
</footer>

<button class="back-to-top" id="backToTop" type="button" aria-label="Back to top">
  <span class="back-to-top-arrow" aria-hidden="true"></span>
</button>

<script src="/assets/js/site.js" defer></script>"""


def breadcrumb_html(crumbs, current):
    parts = []
    for href, label in crumbs:
        parts.append('<a href="%s">%s</a><span>/</span>' % (href, label))
    parts.append(current)
    return ('<nav class="breadcrumbs" aria-label="Breadcrumb">\n        '
            + "".join(parts) + "\n      </nav>")


def breadcrumb_schema(crumbs, current):
    items = []
    for i, (href, label) in enumerate(crumbs, start=1):
        items.append({"@type": "ListItem", "position": i, "name": label,
                      "item": SITE + (href if href != "/" else "/")})
    items.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": current})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def build(slug, meta, body):
    url = SITE + ("/" if slug == "index" else "/" + slug)
    crumbs = [tuple(c) for c in meta.get("breadcrumbs", [["/", "Home"]])]
    current = meta.get("crumb", meta["h1"])

    graph = [dict(BUSINESS)]
    if meta.get("areaServed"):
        graph[0]["areaServed"] = meta["areaServed"]
    graph.append(breadcrumb_schema(crumbs, current))
    for node in meta.get("schema", []):
        graph.append(node)
    if meta.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in meta["faq"]
            ],
        })

    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    indent=2, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{url}">
{FONTS}
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="stylesheet" href="/assets/css/content.css">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/images/wp-content/uploads/2022/09/photo-booth-rental-fun.webp">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{ld}
</script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

{header()}

<main id="main">

  <div class="page-head">
    <div class="wrap">
      {breadcrumb_html(crumbs, current)}
      <div class="page-head-grid">
        <h1>{meta['h1']}</h1>
        <p class="page-lede">{meta['lede']}</p>
      </div>
    </div>
  </div>

{body}

</main>

{footer()}
</body>
</html>
"""


def main():
    if not os.path.isdir(CONTENT):
        sys.exit("missing _content/ directory")
    built = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".html"):
            continue
        slug = fn[:-5]
        raw = open(os.path.join(CONTENT, fn), encoding="utf-8").read()
        m = re.search(r"<!--META(.*?)META-->", raw, re.S)
        if not m:
            sys.exit("no META block in " + fn)
        meta = json.loads(m.group(1))
        body = raw[m.end():].strip()
        out = os.path.join(ROOT, slug + ".html")
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(build(slug, meta, body))
        built.append(slug)
    print("built %d pages: %s" % (len(built), ", ".join(built)))


if __name__ == "__main__":
    main()
