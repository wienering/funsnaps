# Laws of UX — reference for design and critique

**Source:** [Laws of UX](https://lawsofux.com/) by Jon Yablonski (summaries, takeaways, and examples below are drawn from the site’s articles unless noted). Use this doc when reviewing flows, UI copy, layout, and interaction patterns.

**URL note:** Fitts’s Law article path is `fittss-law`; Law of Prägnanz is `law-of-prägnanz` (UTF-8 in the path).

---

## Aesthetic-Usability Effect

**Link:** https://lawsofux.com/aesthetic-usability-effect/

**One line:** Users often perceive aesthetically pleasing design as design that’s more usable.

**Takeaways**

1. Pleasing visuals create a positive response and bias people toward believing the design works better.
2. Users tolerate minor usability issues more when the design looks good.
3. Good visuals can mask usability problems and prevent issues from surfacing in usability tests—so test carefully.

**Practical examples**

- A polished landing page feels “professional,” so people forgive a slightly confusing form label.
- In a usability study, participants may rate a beautiful but clunky prototype higher on “ease of use” than an ugly but efficient one—triangulate with task success and time-on-task.

**Origins (brief):** Kurosu & Kashimura (1995), ATM UI study—stronger link between perceived aesthetics and *perceived* ease of use than between aesthetics and *actual* ease of use.

---

## Choice Overload

**Link:** https://lawsofux.com/choice-overload/

**One line:** People get overwhelmed with too many options (related to “paradox of choice”). Closely related to [Hick’s Law](https://lawsofux.com/hicks-law/).

**Takeaways**

1. Many options hurt decision-making and overall satisfaction with the experience.
2. When comparison matters, support side-by-side comparison (e.g. pricing tiers).
3. Prioritize what you show (e.g. featured product), and offer search/filtering to narrow choices.

**Practical examples**

- SaaS pricing: highlight “Most popular” and collapse secondary tiers.
- E-commerce: default to a curated set; filters reduce perceived overload without removing inventory.

**Origins (brief):** “Overchoice” popularized by Alvin Toffler (*Future Shock*, 1970).

---

## Chunking

**Link:** https://lawsofux.com/chunking/

**One line:** Break information into pieces and group them into meaningful wholes. Closely related to [Miller’s Law](https://lawsofux.com/millers-law/).

**Takeaways**

1. Chunking improves scanning; users spot what matches their goal faster.
2. Visual groups + clear hierarchy match how people evaluate digital content.
3. Use modules, separators, and hierarchy to show relationships.

**Practical examples**

- Long form: sections with headings, not one wall of text.
- Payment flow: “Shipping,” “Payment,” “Review” as distinct steps/chunks.

**Origins (brief):** George A. Miller (1956), “The Magical Number Seven…”; chunking as a strategy for working memory limits.

---

## Cognitive Bias

**Link:** https://lawsofux.com/cognitive-bias

**One line:** Systematic errors in thinking that affect perception and decisions.

**Takeaways**

1. We use heuristics (rules of thumb) to decide quickly; they help efficiency but skew judgment outside our awareness.
2. Knowing biases doesn’t remove them, but helps you spot them in yourself, teammates, and research.
3. Example: **confirmation bias**—seeking information that supports what we already believe.

**Practical examples**

- Only listening to user feedback that matches the roadmap (“they get it”) while dismissing painful tasks.
- Peak moments and endings disproportionately shaping how people remember a study session ([Peak–End Rule](https://lawsofux.com/peak-end-rule/)).

**Origins (brief):** Tversky & Kahneman (1972)—judgment deviates from rational choice theory; heuristics explain both speed and error.

---

## Cognitive Load

**Link:** https://lawsofux.com/cognitive-load/

**One line:** Mental effort required to understand and use an interface. Closely related to [Miller’s Law](https://lawsofux.com/millers-law/).

**Takeaways**

1. When incoming information exceeds capacity, tasks get harder, details are missed, users feel overwhelmed.
2. **Intrinsic load:** effort tied to the goal—holding goals, absorbing new information.
3. **Extraneous load:** mental work that doesn’t help understanding (noise, decoration, unclear layout).

**Practical examples**

- Checkout: remove redundant fields; don’t explain internal SKUs to shoppers.
- Dashboard: one primary action per view vs. twelve-equal-weight widgets.

**Origins (brief):** John Sweller, cognitive load theory (1980s), instructional design and problem-solving.

---

## Doherty Threshold

**Link:** https://lawsofux.com/doherty-threshold/

**One line:** Interaction feels productive when system feedback stays roughly under **400 ms** so neither human nor machine is waiting.

**Takeaways**

1. Aim for feedback within ~400 ms to hold attention and productivity.
2. Use **perceived** performance (skeletons, optimistic UI) when work takes longer.
3. Animation can engage during background work; progress bars make waits tolerable even if imperfectly accurate.
4. A deliberate short delay can *increase* perceived trust/value for some actions (e.g. “secure processing”).

**Practical examples**

- Button press: immediate pressed state; spinner only if > ~400 ms.
- Heavy report: show stepwise progress, not a frozen screen.

**Origins (brief):** Doherty & Thadani (1982, IBM)—400 ms as threshold for “addicting” responsiveness vs. earlier 2 s norms.

---

## Fitts’s Law

**Link:** https://lawsofux.com/fittss-law/

**One line:** Time to hit a target grows with distance and shrinks with target size.

**Takeaways**

1. Touch targets large enough to select accurately.
2. Enough spacing between targets to avoid mis-taps.
3. Place frequent actions where they’re easy to acquire (thumb zones on mobile, Fitts-wise placement on desktop).

**Practical examples**

- Primary CTA larger than secondary; destructive actions not adjacent to “Save.”
- Mobile: bottom nav for key tabs vs. tiny targets in a top corner.

**Origins (brief):** Paul Fitts (1954)—speed/accuracy tradeoff; foundational for UI target sizing.

---

## Flow

**Link:** https://lawsofux.com/flow/

**One line:** Deep engagement when challenge matches skill—focused, in control, enjoying the activity.

**Takeaways**

1. Flow needs balance: too hard → frustration; too easy → boredom.
2. Clear feedback on what happened and what was accomplished.
3. Remove unnecessary friction; make capabilities discoverable so people don’t disengage.

**Practical examples**

- Expert tool: shortcuts + progressive depth; beginner path stays simple.
- Creative app: uninterrupted composition mode with subtle status cues.

**Origins (brief):** Mihály Csíkszentmihályi (1975).

---

## Goal-Gradient Effect

**Link:** https://lawsofux.com/goal-gradient-effect/

**One line:** Motivation increases as users get closer to finishing.

**Takeaways**

1. Near the end of a task, people speed up.
2. **Artificial** progress (e.g. profile “50% complete”) can increase completion.
3. Show clear progress indicators.

**Practical examples**

- Stepped checkout with “Step 3 of 4.”
- Loyalty “two visits to next reward” vs. opaque points balance.

**Origins (brief):** Clark Hull—goal-gradient hypothesis (1930s), tested with approach behavior.

---

## Hick’s Law

**Link:** https://lawsofux.com/hicks-law/

**One line:** Decision time grows with the number and complexity of choices.

**Takeaways**

1. Minimize choices when speed matters.
2. Break complex tasks into smaller steps to lower cognitive load.
3. Highlight recommended options; avoid walls of equal-weight choices.
4. Progressive onboarding for newcomers.
5. Don’t oversimplify into vagueness.

**Examples (from Laws of UX)**

- **Google homepage:** minimal chrome so the main decision is “what to search.”
- **Apple TV remote:** fewer buttons; complexity moves on-screen into organized menus.
- **Slack:** Slackbot onboarding focuses on messaging first; other features appear progressively.

**Practical examples**

- Emergency UI: one obvious action, not six peer buttons.
- Settings: “Recommended” tab vs. exposing every toggle at once.

**Origins (brief):** Hick & Hyman (1952)—reaction time vs. number of stimuli.

---

## Jakob’s Law

**Link:** https://lawsofux.com/jakobs-law/

**One line:** Users spend most time on *other* sites; they expect yours to behave like what they know.

**Takeaways**

1. Expectations transfer from familiar products to similar-looking ones.
2. Leverage existing mental models so users focus on tasks, not relearning.
3. When changing UX, reduce discord (e.g. optional preview, temporary legacy mode).

**Examples (from Laws of UX)**

- **Form controls:** toggles, radios, buttons echo physical and web conventions.
- **YouTube redesign (2017):** users could preview Material UI, give feedback, and revert—easing mental-model shift.

**Practical examples**

- Cart icon top-right; logo links home—don’t novelty-reinvent without reason.
- Breaking a pattern requires extra teaching or a migration period.

**Origins (brief):** Jakob Nielsen (Nielsen Norman Group).

---

## Law of Common Region

**Link:** https://lawsofux.com/law-of-common-region/

**One line:** Elements in a clearly bounded area are perceived as a group.

**Takeaways**

1. Common region clarifies structure and relationships.
2. Borders are a quick way to create it.
3. Shared background behind a group also creates region.

**Practical examples**

- Card with border around title + meta + actions = one unit.
- Settings: grouped panels vs. one undifferentiated list.

**Origins (brief):** Gestalt **principles of grouping** (with Proximity, Similarity, etc.).

---

## Law of Proximity

**Link:** https://lawsofux.com/law-of-proximity/

**One line:** Things close together are seen as related.

**Takeaways**

1. Proximity implies relationship.
2. Nearby elements read as shared function or traits.
3. Proper spacing speeds understanding.

**Examples (from Laws of UX)**

- **Google search results:** spacing groups each result’s title, URL, snippet as one cluster.

**Practical examples**

- Label visually nearer to its field than to the next field.
- Error message adjacent to the field it refers to.

**Origins (brief):** Gestalt grouping principles.

---

## Law of Prägnanz

**Link:** https://lawsofux.com/law-of-pr%C3%A4gnanz/

**One line:** People interpret ambiguous or complex shapes as the **simplest** plausible form (least cognitive effort).

**Takeaways**

1. The visual system prefers simple, ordered interpretations of complexity.
2. Simple figures are easier to process and remember than overly complex ones.
3. We “unify” complex shapes into one simpler whole.

**Practical examples**

- Logo: readable silhouette at small sizes—avoid fussy detail that doesn’t resolve to a simple shape.
- Data viz: default to the simplest chart that answers the question.

**Origins (brief):** Max Wertheimer (~1910)—apparent motion from flashing lights; foundation of Gestalt perception.

---

## Law of Similarity

**Link:** https://lawsofux.com/law-of-similarity/

**One line:** Similar-looking elements read as one pattern or group, even if separated.

**Takeaways**

1. Visual similarity implies relation.
2. Color, shape, size, orientation, motion can signal same group/meaning.
3. Differentiate links and navigation from body text.

**Practical examples**

- All “destructive” actions use the same red text style.
- Tags vs. body: don’t make ads look like content ([Selective Attention](https://lawsofux.com/selective-attention/) / banner blindness).

**Origins (brief):** Gestalt grouping principles.

---

## Law of Uniform Connectedness

**Link:** https://lawsofux.com/law-of-uniform-connectedness/

**One line:** Visually connected elements feel more related than disconnected ones.

**Takeaways**

1. Connect related functions with color, lines, frames, or enclosures.
2. Lines/arrows can show sequence or relationship.
3. Use connection to show context or emphasize related items.

**Examples (from Laws of UX)**

- **Google search:** borders around video packs and featured snippets connect content and separate it from standard results.

**Practical examples**

- Timeline: single vertical line tying events.
- Wizard: connector between steps in one horizontal strip.

**Origins (brief):** Gestalt grouping principles.

---

## Mental Model

**Link:** https://lawsofux.com/mental-model/

**One line:** What users believe about how a system works shapes how they use it. Closely related to [Jakob’s Law](https://lawsofux.com/jakobs-law/).

**Takeaways**

1. Users build a working model and apply it to similar systems.
2. Align design with users’ models to reduce learning cost.
3. E-commerce patterns (cards, cart, checkout) work because they match expectations.
4. Closing the gap between designer and user models is a core UX challenge—use interviews, personas, journeys, empathy maps.

**Practical examples**

- “Trash” metaphor for recoverable delete vs. instant obliteration—match OS/email mental models.
- Mislabeled “Settings” that opens billing—breaks the model and erodes trust.

**Origins (brief):** Kenneth Craik (1943)—internal small-scale models of how the world works.

---

## Miller’s Law

**Link:** https://lawsofux.com/millers-law/

**One line:** Working memory holds about **7 ± 2** chunks—not a license to max out every screen.

**Takeaways**

1. Don’t use “seven” as an excuse for lazy, arbitrary limits.
2. Organize content into **smaller chunks** for processing and memory.
3. Capacity varies with prior knowledge and context.

**Examples (from Laws of UX)**

- **Chunking** organizes content to match memory limits.

**Practical examples**

- Phone number grouping: `012 345 6789` vs. `0123456789`.
- Navigation: seven peer items at top level is often already too many without hierarchy.

**Origins (brief):** George A. Miller (1956)—channel capacity and “bits” of information.

---

## Occam’s Razor

**Link:** https://lawsofux.com/occams-razor/

**One line:** Among hypotheses that fit the evidence equally well, prefer the one with fewest assumptions.

**Takeaways**

1. Best complexity reduction is avoiding it up front.
2. Remove elements until function suffers, then stop.
3. “Done” when nothing else can be removed without harm.

**Practical examples**

- Two flows merge into one if both serve the same user goal.
- Prefer default + “More options” over exposing every edge case by default.

**Origins (brief):** William of Ockham (~14th c.), parsimony in explanation.

---

## Paradox of the Active User

**Link:** https://lawsofux.com/paradox-of-the-active-user/

**One line:** Users skip manuals and dive in—even when reading would save time later.

**Takeaways**

1. Motivation favors immediate tasks over upfront learning.
2. Long-term, learning would help—but short-term incentives win.
3. Offer guidance **in context** (tooltips, inline help) on the paths users actually take.

**Practical examples**

- Empty state with one suggested action + “Learn more” link, not a 10-page PDF.
- Progressive disclosure: power features after basics feel solid.

**Origins (brief):** Rosson & Carroll (1987), *Interfacing Thought*—new users skipped docs and hit errors.

---

## Pareto Principle

**Link:** https://lawsofux.com/pareto-principle/

**One line:** Often ~**80%** of effects come from ~**20%** of causes.

**Takeaways**

1. Inputs and outputs are rarely even.
2. A few contributors usually drive most of the outcome you care about.
3. Concentrate effort where impact is largest for most users.

**Practical examples**

- Fix the top 3 tasks that fail in analytics before polishing rare workflows.
- Prioritize performance on the slow pages that drive 80% of exits.

**Origins (brief):** Vilfredo Pareto—wealth distribution observation, generalized as 80/20 thinking.

---

## Parkinson’s Law

**Link:** https://lawsofux.com/parkinsons-law/

**One line:** Work expands to fill the time (or space) available.

**Takeaways**

1. Keep task duration aligned with user expectations.
2. Finishing **faster** than expected improves perceived UX.
3. Use autofill, saved info, smart defaults to **prevent** tasks ballooning.

**Practical examples**

- 12-field registration when 4 suffice invites abandonment and “task inflation.”
- Autofill address after postal code where possible.

**Origins (brief):** Cyril Northcote Parkinson (1955 essay, *The Economist*)—bureaucracy expands to use available time.

---

## Peak–End Rule

**Link:** https://lawsofux.com/peak-end-rule/

**One line:** People remember experiences by emotional **peaks** and the **ending**, not the average of every moment. Closely related to [Cognitive Bias](https://lawsofux.com/cognitive-bias).

**Takeaways**

1. Design for the most intense moments and the final moment of the journey.
2. Find when the product is most helpful, valuable, or entertaining—delight there.
3. Negative peaks are remembered vividly; mitigate them.

**Examples (from Laws of UX)**

- **Mailchimp:** first-send confirmation uses brand, illustration, animation, humor to reduce stress at a peak moment.
- **Uber:** reducing perceived wait and post-request cancel risk avoids a strong *negative* peak.

**Practical examples**

- Onboarding ends with a clear “you’re ready” win, not an error modal.
- Subscription cancellation: respectful close reduces lasting bitterness.

**Origins (brief):** Kahneman et al. (1993)—cold-hand experiment; longer milder end preferred in memory.

---

## Postel’s Law (Robustness Principle)

**Link:** https://lawsofux.com/postels-law/

**One line:** **Be liberal in what you accept, conservative in what you send.**

**Takeaways**

1. Empathize with messy real-world input and capabilities.
2. Anticipate variability; keep the interface reliable and accessible.
3. Plan for edge inputs; translate/normalize; set boundaries; give clear feedback.

**Practical examples**

- Phone field accepts `555-123-4567`, `(555) 123-4567`, spaces—normalize server-side.
- Date parsing: accept common formats; store ISO; show consistent display format.

**Origins (brief):** Jon Postel—TCP/network robustness: strict emitters, tolerant receivers.

---

## Selective Attention

**Link:** https://lawsofux.com/selective-attention/

**One line:** People focus on a **subset** of stimuli—usually goal-relevant—and ignore the rest. Related to [Von Restorff Effect](https://lawsofux.com/von-restorff-effect/).

**Takeaways**

1. Guide attention; avoid overwhelming or distracting from the main task.
2. **Banner blindness:** users ignore ad-shaped or ad-placed content—don’t style key UI like ads.
3. **Change blindness:** big simultaneous changes can be missed—avoid competing visual shocks.

**Practical examples**

- Critical alert: one modal, not three stacked modals and a toast.
- Don’t put essential account tasks in a banner that looks like marketing.

**Origins (brief):** Attention research—Broadbent, Cherry, Treisman, etc. (1950s onward).

---

## Serial Position Effect

**Link:** https://lawsofux.com/serial-position-effect/

**One line:** First and last items in a series are remembered best (**primacy** and **recency**).

**Takeaways**

1. Least important items are least harmful in the **middle** of lists.
2. Key actions at **far left and right** in toolbars/navigation can aid memory (cf. Apple, Nike, EA patterns noted on site).

**Practical examples**

- “Home” and “Account” at ends; middling utilities in between.
- Feature list: lead with strongest benefit, end with memorable differentiator.

**Origins (brief):** Herman Ebbinghaus—serial position and recall accuracy.

---

## Tesler’s Law (Law of Conservation of Complexity)

**Link:** https://lawsofux.com/teslers-law/

**One line:** Every system has a core of complexity that cannot vanish—only move between system and user.

**Takeaways**

1. Something must own the inherent complexity: product/engineering or the user.
2. Shift burden to the system during design/dev when possible.
3. Real users aren’t always “rational”; plan for messy behavior.
4. Contextual guidance helps regardless of path (tooltips, inline help)—aligns with active users.

**Practical examples**

- Smart defaults and validation messages vs. “read the 40-page spec.”
- Simplifying the UI may lead users to attempt harder tasks (Tognazzini note on Laws of UX)—monitor support and success metrics.

**Origins (brief):** Larry Tesler (Xerox PARC); popularized via *Designing for Interaction* (Dan Saffer) interview.

---

## Von Restorff Effect (Isolation Effect)

**Link:** https://lawsofux.com/von-restorff-effect/

**One line:** Among similar items, the **different** one is most likely remembered.

**Takeaways**

1. Make critical info and primary actions visually distinct.
2. Don’t overuse emphasis or everything competes; salient items may look like **ads**.
3. Don’t rely on color alone—color-vision deficiency and low vision.
4. Consider motion sensitivity when using motion for emphasis.

**Practical examples**

- One primary button per view; secondaries ghost or outline.
- Table row highlight for the item the user just edited.

**Origins (brief):** Hedwig von Restorff (1933)—distinctive item in a homogeneous list better recalled.

---

## Working Memory

**Link:** https://lawsofux.com/working-memory/

**One line:** Short-term store that holds and manipulates information for ongoing tasks. Closely related to [cognitive load](https://lawsofux.com/cognitive-load/).

**Takeaways**

1. Roughly **4–7 chunks** at once; chunks decay in ~**20–30 seconds**—show only necessary, relevant information.
2. Support **recognition over recall**: visited-link styles, breadcrumbs, clear “already completed” states.
3. **Place memory burden on the system**—carry forward selections (e.g. comparison tables).

**Practical examples**

- Multi-step flow shows chosen plan at checkout—don’t make users memorize it.
- Autosave drafts so users aren’t holding paragraph text in head across interruptions.

**Origins (brief):** Miller, Galanter & Pribram; Atkinson & Shiffrin “short-term store”; modern emphasis on manipulation not just storage.

---

## Zeigarnik Effect

**Link:** https://lawsofux.com/zeigarnik-effect/

**One line:** **Incomplete** tasks are remembered better than completed ones.

**Takeaways**

1. Use clear signifiers of more content to invite discovery.
2. Artificial progress can motivate completion (overlap with [Goal-Gradient Effect](https://lawsofux.com/goal-gradient-effect/)).
3. Show progress clearly.

**Practical examples**

- “Profile 80% complete” with explicit missing items.
- Saved cart / “Continue where you left off” leverages open loops.

**Origins (brief):** Bluma Zeigarnik (1920s)—memory for incomplete vs. complete tasks.

---

## Quick cross-reference (when troubleshooting UX)

| Symptom | Laws to consider |
|--------|-------------------|
| Too slow / sluggish | Doherty Threshold, Flow, perceived performance |
| Can’t decide / abandons | Hick’s Law, Choice Overload, Tesler’s Law |
| Looks pretty but tasks fail | Aesthetic-Usability Effect (test deeper), Cognitive Load |
| Users lost / surprised | Jakob’s Law, Mental Model, Law of Proximity / Common Region |
| Nobody sees the CTA | Von Restorff, Selective Attention, Fitts’s Law |
| Remembers wrong parts of flow | Peak–End Rule, Serial Position Effect |
| Bad data / edge inputs | Postel’s Law |
| Over-built settings | Occam’s Razor, Pareto Principle, Parkinson’s Law |
| Skips help / errors | Paradox of the Active User |

---

*Last compiled from lawsofux.com articles for local reference. For illustrations, posters, and updates, see the official site.*
