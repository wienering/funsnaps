"""Replace FAQPage mainEntity in faq.html with all Q&A pairs from the page content."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "faq.html"
text = path.read_text(encoding="utf-8")

questions = re.findall(r'<div class="faq-question">(.*?)</div>', text, re.DOTALL)
answers = re.findall(r'<div class="faq-answer">\s*<p>(.*?)</p>', text, re.DOTALL)


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    return " ".join(s.split())


main_entity = []
for q, a in zip(questions, answers):
    main_entity.append(
        {
            "@type": "Question",
            "name": clean(q),
            "acceptedAnswer": {"@type": "Answer", "text": clean(a)},
        }
    )

LOGO = "https://www.funsnaps.ca/assets/images/wp-content/uploads/2024/03/Fun-Snaps-Logo-png-103x97-1.webp"

target_idx = None
raw_scripts: list[str] = []
for m in re.finditer(
    r'<script type="application/ld\+json">(.*?)</script>',
    text,
    re.DOTALL,
):
    raw_scripts.append(m.group(1).strip())
    try:
        j = json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        continue
    if not isinstance(j, dict) or "@graph" not in j:
        continue
    for item in j["@graph"]:
        if item.get("@type") == "FAQPage":
            target_idx = len(raw_scripts) - 1
            data = j
            break
    if target_idx is not None:
        break

if target_idx is None:
    raise SystemExit("FAQ graph not found")

for item in data["@graph"]:
    if item.get("@type") == "FAQPage":
        item["mainEntity"] = main_entity
        item["@id"] = "https://www.funsnaps.ca/faq#faqpage"
    if isinstance(item.get("@type"), list) and "LocalBusiness" in item["@type"]:
        item["image"] = LOGO
        item["logo"] = LOGO

new_inner = json.dumps(data, indent=4, ensure_ascii=False)
# Re-find and replace the exact script inner that we parsed (second graph block)
old_scripts = list(
    re.finditer(
        r'<script type="application/ld\+json">(.*?)</script>',
        text,
        re.DOTALL,
    )
)
replaced = False
for m in old_scripts:
    try:
        j = json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        continue
    if not isinstance(j, dict) or "@graph" not in j:
        continue
    if any(x.get("@type") == "FAQPage" for x in j["@graph"]):
        full = m.group(0)
        new_full = f'<script type="application/ld+json">\n    {new_inner}\n    </script>'
        text = text.replace(full, new_full, 1)
        replaced = True
        break

if not replaced:
    raise SystemExit("Could not replace script block")

path.write_text(text, encoding="utf-8")
print("Updated FAQ JSON-LD,", len(main_entity), "questions")
