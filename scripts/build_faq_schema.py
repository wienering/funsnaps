"""Extract FAQ Q&A from faq.html and print FAQPage mainEntity JSON snippet."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "faq.html").read_text(encoding="utf-8")
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

block = {"@type": "FAQPage", "@id": "https://www.funsnaps.ca/faq#faqpage", "mainEntity": main_entity}
print(json.dumps(block, indent=2, ensure_ascii=False))
print("COUNT", len(questions), len(answers))
