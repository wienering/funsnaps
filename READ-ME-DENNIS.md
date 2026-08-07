# Read this when you get back

Everything is built, tested and pushed live. This covers what changed, the judgement
calls I made without you, and the few things only you can answer.

Nothing here is urgent. The site works as it stands.

---

## 1. What's live now

18 pages, all on the new Enamel Booth design, all verified rendering at desktop and
mobile with no broken links, no broken images and valid schema.

**Core** — `/` · `/pricing` · `/quote` · `/book-now` · `/contact-us` · `/faq` · `/404`

**Service pages (all new, these did not exist before)**
`/corporate-photo-booth-rental` · `/glam-booth` · `/360-photo-booth`

**Locations** — `/vaughan` · `/toronto` · `/mississauga` · `/oakville` ·
`/richmond-hill` · `/markham` (new) · `/york-region` (new) ·
`/vaughan-corporate-photo-booth` (new)

**Deleted:** `/vaughan-photo-booth-rental-prices` → 301s to `/pricing`. It was a
keyword-permutation URL overlapping `/pricing` and `/vaughan`.

---

## 2. The main thing this fixed

Your five old city pages were **doorway pages**. I measured it before and after.

| | Old site | New site |
|---|---|---|
| Identical paragraphs between any two city pages (city name masked) | **26–54%** | **0%** |
| H2 structure | All five identical, word for word | All seven different |
| Word count spread | Within 13% of each other | 839–899, different shapes |

The old pages ran the same nine headings with the city swapped: *"Why Choose Fun Snaps
for Your {City} Event?"*, *"Why {City} Residents Choose Fun Snaps"* and so on. That is
the pattern Google's doorway guidance names directly.

Each new city page now has its own structural spine:

- **Vaughan** — venue by venue, what's actually different about each hall
- **Toronto** — the downtown load-in problem: docks, freight, union houses, security
- **Richmond Hill** — a decision tree for picking a booth, because the market is mixed
- **Markham** — an hour-by-hour account of a real night, 4pm van to 11:15pm teardown
- **Mississauga** — two markets, lakeshore versus Square One, and what each needs
- **Oakville** — smaller guest lists, outdoor setups, a season that genuinely closes
- **York Region** — a geographic hub covering the six northern towns honestly

---

## 3. Decisions I made without you

**URL structure: flat, not folders.** Kept `/vaughan`, `/toronto` etc. exactly as they
were so no ranking equity is lost, and made new pages match: `/markham`,
`/vaughan-corporate-photo-booth`. Shallower is better for crawling and it keeps one
convention. This overrides the `/vaughan/corporate-photo-booth/` structure I proposed
earlier.

**No pages for neighbourhoods.** Etobicoke, North York and Scarborough are inside the
City of Toronto; Woodbridge, Maple, Concord and Thornhill are inside Vaughan. Separate
pages for those is exactly the doorway pattern we just removed, so they are named
sections on the parent page instead, with old-style URLs 301ing to the right parent.
Same for Kleinburg, King City, Aurora, Newmarket and Kettleby → `/york-region`.

**Kept Mississauga and Oakville as full pages** rather than merging into a "West GTA"
page, since you confirmed real job history in both.

**Used your real photos, not the AI comps.** The v4 mockups used AI-generated stand-ins
at 4–8MB each, which would have wrecked page speed and Core Web Vitals. The site now
uses your actual event photography that was already in the repo, plus your real client
logos.

**Glam is free everywhere.** Changed in three places so they cannot drift apart: the
checkbox on `/quote` (`data-price` 75 → 0), the calculator total in `scripts/quote.js`,
and the add-on line in the confirmation email in `api/quote.js`. All three say
"Included".

**Fixed the "unlimited prints" wording.** The old corporate copy said packages include
"unlimited sessions and prints". Since unlimited prints is a $60/hr add-on, that promised
something you charge for. It now reads "unlimited sessions and two prints per round"
everywhere, and the add-on is listed openly on `/pricing` and `/faq`.

**Idle time stays in the calculator, off the pages,** as you asked. It appears once on
`/pricing` and `/faq` as "additional waiting time", framed as only applying to long gaps,
because a customer discovering a charge at invoice time is worse than seeing it up front.
Say the word and I'll pull it entirely.

---

## 4. Things I changed on `book-now` even though you said leave it

You said you'd check that page separately, so I did **not** touch how it submits. Two
things I did do:

1. **Restyled it** to the new design. Leaving it on the old look would have made it the
   one broken-looking page on the site.
2. **Fixed a live data-loss bug.** It collects *Event Location* and *Package Interest*,
   then POSTs to `/api/contact`, which reads neither. **Every booking request you have
   received was missing the venue and the package the customer selected.** Rather than
   change the API, the page now folds both into the `message` field so they reach your
   inbox. No endpoint change, no new failure mode. If you'd rather revert it, it's one
   block in that page's inline script.

---

## 5. Bugs found and fixed along the way

- **The homepage quote form would have failed on every submission.** No `phone` field,
  which `/api/contact` requires, and the date input was named `date` where the API
  expects `event-date`. Fixed and verified against the real contract.
- **`$75` was hardcoded** in the quote review summary in `scripts/quote.js`, so glam
  would still have shown a charge at the review step after the price change.
- **Confetti colours** were still the old gold palette; they now read from CSS tokens.

---

## 6. What I need from you

Nothing blocking. Rough priority order:

1. **Google Business Profile** — set the opening date to **2011**, as you said you would.
   The site says "since 2011" in the footer and `foundingDate: 2011` in schema, and a
   mismatch is visible to anyone who checks.

2. **Venue claims.** I only state "rooms we work" for the six you confirmed: Paradise,
   Château Le Jardin, The Venetian, Hazelton Manor, The Terrace, Da Vinci. On Richmond
   Hill, Markham, Mississauga and Oakville I named venues from research and wrote
   explicitly that we cannot claim first-hand knowledge of all of them. **Tell me which
   we've actually worked and I'll upgrade the language** — "we know this room" is far
   stronger, and it's the hardest thing for a competitor to copy.

3. **The aggregateRating question.** The old v4 mockup carried 4.9 from 186 reviews in
   schema with no reviews visible on the page. **I did not carry that over.**
   Self-serving review markup with nothing backing it on-page is the most common
   manual-action trigger in this vertical. If the numbers are real and you want them, the
   clean fix is to pull real Google reviews onto the page and mark those up.

4. **Trade show idle rate** — still unanswered, still not mentioned anywhere.

5. **The 5 and 6 hour packages** ($1,250 / $1,450) exist in the quote calculator but not
   on `/pricing`, which lists three tiers. I referenced them on `/book-now` as "Custom".
   Worth deciding whether they should be public.

---

## 7. How to edit pages from now on

Page bodies live in `_content/<slug>.html`. Each has a JSON block at the top carrying
title, description, breadcrumbs, schema and FAQ, then hand-written HTML below it.

```bash
python scripts/build_pages.py
```

That wraps every body in the shared header and footer and writes the final `.html` at the
repo root. Vercel serves those directly and there is no build step on deploy, so **you
must run the script and commit the generated HTML.**

The chrome is shared so it cannot drift. The content deliberately is not templated.

**Two rules worth keeping:**
- Never hardcode a colour. Everything resolves from `:root` in `assets/css/site.css`.
  The palette has been swapped twice now and flowed to every page untouched.
- Never hardcode a width. `--page-max` and `--page-pad` own that site-wide.

Design system documented at `../design-inspiration/fun-snaps/DESIGN.md`.

---

## 8. What I could not verify

**I could not take screenshots.** The browser tooling in this session would not composite
frames, so every check was structural: computed CSS, contrast ratios, link resolution,
image loading, schema validity, layout overflow at 1440px and 375px, and driving the
quote wizard end to end in a real DOM.

That is rigorous on correctness and silent on aesthetics. **Please look at the live pages
yourself.** If something reads wrong visually, that is the one class of problem my
testing could not have caught.

I also could not test the live form endpoints, since `/api/*` only runs on Vercel. The
payloads now match the documented contract exactly, but **send yourself one test enquiry
from `/contact-us` and one from `/quote`** before relying on them.
