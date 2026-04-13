import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "faq.html"
t = p.read_text(encoding="utf-8")
new = re.sub(
    r'<div class="faq-question">(.*?)</div>\s*<div class="faq-answer">',
    r'<button type="button" class="faq-question" aria-expanded="false">\1</button>\n                        <div class="faq-answer">',
    t,
    flags=re.DOTALL,
)
if new == t:
    raise SystemExit("no match")
p.write_text(new, encoding="utf-8")
print("faq buttons ok")
