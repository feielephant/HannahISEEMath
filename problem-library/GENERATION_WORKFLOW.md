# Speed-Training Set Generation — Workflow

Purpose: generate 38-problem Quantitative Reasoning practice sets (matched to the real test's difficulty and topic mix) for Hannah, rotating topics so strong skills keep getting practice and weak ones get targeted.

## Files (all in problem-library/)
- `problem_library.json` — ~757 real questions from 8 full tests, drills, and dashboards (source of examples and topic/difficulty context)
- `student-tracker.json` — Hannah's gaps, habits, wrong-rates, and priorities (update after each set is graded)
- `practice-log.json` — every set generated so far, with its topic list (written by plan_set.py)
- `problem-library-banks.json` — the platform's Easy / Medium / Hard bank titles
- `plan_set.py` — makes the next 38-slot plan (tier mix + rotation + per-topic cap)

## Real test profile (from 8 full tests, 392 questions)
- Format: 38 problems, 35 minutes, four choices A–D, Quantitative Reasoning
- Difficulty mix (topic-matched): ~28% Easy, ~53% Medium, ~16% Hard (+ ~3% unmatched)
- Most frequent real topics: Translating Math Expressions (8/8 tests), Converting to a Decimal (8/8), Angles in Triangles (7/8), Area of Triangles (7/8)

## Steps for each new set
1. Run `python3 plan_set.py` in problem-library/ — it prints the 38-slot plan and appends to practice-log.json.
2. For each slot, write one NEW problem on that topic and tier. Use real examples from problem_library.json as the model (same wording style, same number of steps), but fresh numbers and scenario. Never copy a real question verbatim.
3. Check every problem by solving it. Build the answer key from the solved values, not from memory. Make distractors reflect her habit traps (for example, a "NOT" question with an equivalent answer as the trap; a percent-change question with the +10%/−10% cancel trap).
4. Build the worksheet (no answers shown) and a separate answer key. Add a 35-minute timer. The live worksheet must use `speed-tools/harness_v2_template.js` (one problem per page, index nav, timer top-right) -- see that file's README entry for why and how. The answer key stays full-page/scrollable, for quick parent review.
5. After she takes the set, grade it and update student-tracker.json: wrong counts per topic, last practiced, and any new habit evidence.

## Set-shape rules (added 2026-10-02)
- Answer letters: balanced A/B/C/D (10/10/9/9 across 38), no three identical letters in a row. The planner assigns them.
- Difficulty: a soft ramp, not a rule. Real tests show Hard share ~5–9% in the first half and ~17–21% in the second. The planner places ~2 Hard slots in the first half and ~5 in the second; Easy and Medium shuffle freely.
- Diagrams: about 55% of real questions include a diagram, chart, or table, so ~21 of 38 slots are diagram slots. Build the diagram as an inline SVG or table in the same style as the real test (bar graph, number line, shaded figure, composite shape), not as a text description.
- Each slot carries a reference (wrong_so_far, graded_so_far, times_practised_before, last_practised_set). Mention the relevant habit and gap in the answer key so she sees why each problem is there.

## Pacing rule (added 2026-10-06)
- Questions 31–38 of the official 38-question tests are pacing-affected (rushed answers, error rate 41% vs 10% for Q1–30). The library marks these pacing_affected=true.
- Exclude pacing-affected items from topic gap counts. Track pacing separately (tracker "pacing" block).
- Speed sets: include full timed sections, and practise the last third under time pressure.

## Targeting rule
- High-priority topics appear more often; "maintain" topics appear at least once every 3 sets so strong skills don't fade.
- No topic appears more than 3 times in one set.
- Only mark a habit as her weakness after evidence from her own answers (graded practice or screenshots), not from a single guess.

## Caveats
- Tier labels come from topic-to-bank matching, so they are estimates.
- Some platform banks have no real examples yet (for example, Unit Conversion with Made Up Units); their problems are generated, not copied.

## Selection criteria (required for every set)
1. **Coverage:** every topic in the tracker should appear across recent sets. Use the planner's rotation so no topic goes unpractised for long, and include the new topics (net type, estimation banks, remaining-amount fractions).
2. **Focus on weak spots:** prioritise topics she gets wrong and problems that took her longer (from the tracker, the timing charts, and her CSV times). Multi-step, constraint-based, fraction-comparison, pattern, and relationship problems come first. Her late-test pacing is handled by timed sections, not by excluding topics.

## Done vs not-done rule (added 2026-10-06)
- Every library item has status: "done" (she answered it: a marked answer, a green/maroon marker, or a review screen) or "not_done" (no answer shown).
- Not-done items: use the ORIGINAL problem as-is (same numbers, wording, scenario). She has not seen it, so it is a fair real test of the topic.
- Done items: change the numbers, wording, or scenario, but keep the same math concept and trap. Do not give her a verbatim repeat of something she has already answered.

## Known format conventions (added 2026-10-11 — read before building ANY diagram)
Every bug found in sets 1-3 so far has been a *format* bug, not a math bug: the right answer was always mathematically correct, but the problem wasn't presented the way the real test presents it. These are no longer guesses — they're confirmed either against a real official-test screenshot or against every matching example in problem_library.json. Build diagram-topic problems this way from the start; don't wait for a parent catch or a sanitize_diagrams.py flag.

- **Never state a diagram topic's values directly in the question text.** If the topic is number line / midpoint, shaded figure / fraction-of-figure, bar graph, or pictograph, the real test ALWAYS shows a diagram and has her read the values off it — it never just tells her the numbers in a sentence. Check `problem_library.json` for every real example of the topic before writing one; if they all say "shown"/"below"/"the chart shows", yours needs an actual diagram too, not prose. (Set 3 #23 stated "A is at 14 and C is at 50" instead of showing a number line; set 2 #10/#29/#36 stated pictograph counts directly instead of showing icons; set 3 #22 stated "5/8 of the figure is shaded" instead of showing a figure.)
- **Number line diagrams:** only the two line endpoints get numeric labels. Lettered points (A, B, P, Q, ...) are shown bare, with no value next to them. The answer/target point is typically NOT drawn on the visible line at all — it's computed beyond what's shown. (Confirmed against a real official-test screenshot.)
- **Pictograph diagrams:** show icon rows (e.g. `★★★★★`) with a legend line ("Each ★ = N units"), never the raw count in text. A half-unit is a clipped icon (CSS: `.half{display:inline-block;width:0.52em;overflow:hidden}` on the last icon in a row). Reusable CSS lives in speed-set-2.html/-answer-key.html as `.pictograph`/`.pictorow`/`.piclabel`/`.picicons`/`.pictokey` — copy that block into any new set that uses this topic.
- **Shaded-figure / fraction-of-figure diagrams:** show a grid (or other equal-division shape) as inline SVG with the correct count of cells shaded (`fill="var(--accent-soft)"`) vs unshaded (`fill="var(--surface)"`), `stroke="currentColor"`. She reads the fraction by counting shaded vs total cells shown — never state the fraction/percent in the question text. Reference implementation: speed-set-3.html/-answer-key.html #21 and #22.
- **Column-sum / cryptarithm diagrams (`.colsum`):** use a monospace font (`ui-monospace,"SF Mono","Cascadia Mono","Courier New",monospace` + ~2px `letter-spacing`) so place-value columns actually line up — a proportional font breaks column alignment even with `text-align:right`, since letters/digits/the `+` sign aren't equal width. Don't pad the operator row with a space (write `+QQ`, not `+ QQ`) — the space is its own character cell and throws off the column count. Give each row `padding:2px 6px` + `line-height:1.5`, and extra `margin-top`/`padding-top` (~5px) on the total row before its `border-top` rule, so it doesn't read as cramped.
- **Never print an answer-revealing diagram/table on the question page.** (Sets 1-3 all shipped a "divisible by both X/Y" or "round to" table that gave away the correct row/value just by pattern-matching, visible on the worksheet itself, not just the key.) Diagrams go on both pages; the only difference between worksheet and answer key should be the key's "Answer:"/"Why" text and the `.ref` line.
- **CSS for anything nested inside `.choices`:** scope container rules to direct children (`.choices > span`, not `.choices span`) so they don't silently also style nested `.frac`/`.diag`/`.colsum`/`.pictograph` markup that happens to land inside a choice.
- **Before publishing or handing a set to her:** run `python3 problem-library/speed-tools/sanitize_diagrams.py`. It catches two things automatically — an explanation that assumes a value never shown on the page, and a diagram-convention topic with no diagram at all — but it's heuristic, so also eyeball every new/edited diagram against a real screenshot or a cross-check of `problem_library.json`'s real examples for that topic.

## QR vs MA: a real but partial distinction (added 2026-10-11)
Checked this properly after the parent asked whether MA generation was just "a shorter QR" — it had been, more than it should've been. `problem_library.json` (QR) and `ma_library.json` (MA) are separate real-evidence sources; MA topic selection should use `ma_library.json`'s `official_topic`/`is_wrong` data as the evidence base (same way QR uses `problem_library.json`), not just reuse QR's topic list with fewer slots.

**The distinction is real but it's a skew in emphasis, not a hard format rule.** Comparing topic frequency between the two libraries: MA is disproportionately heavier on direct computation/execution (Adding and Subtracting Integers, Order of Operations, Adding/Subtracting Decimals, Estimating Sums/Differences of Decimal Numbers), direct formula/procedure application (Finding Area/Perimeter of a Rectangle, Solving 1-Variable Equations), and direct recall/translation (Identifying Numbers Standard Form <> Word Form). QR is disproportionately heavier on reasoning/logic/interpretation (Whole Number "Who am I?", Solving for Subsets in a Venn Diagram, Word Problems with Ratios, Matching Stories to Equations, Patterns in Data Tables and Lists, Algebra with Geometric Shapes). But it's emphasis, not exclusivity — checked directly and the "which expression gives the best estimate" format, for instance, appears in BOTH libraries at real frequency; don't assume a format is QR-only or MA-only without actually checking both libraries first the way the topic-frequency comparison above did.

**When building an MA set:** weight topic selection toward MA's characteristic computation/procedure/recall topics in addition to using `ma_library.json`'s real wrong-rate evidence — don't just port over whichever QR-style word-problem template is easiest to adapt. A direct "What is 48 × 23?" or "What is the value of the digit 7 in 3.472?" is a perfectly authentic MA question on its own, with no word-problem wrapper needed — don't add one reflexively.

**Mean/Median/Mode/Range** is real, confirmed content in both libraries under `Finding MMMR given Bar Graph Data Table` / `Finding Median given Sets of Numbers`, and it hadn't shown up in any QR set 1-4 purely by rotation luck (not a structural gap — it's in the Medium bank). The real format is sometimes harder than "read one bar graph and compute the mean": e.g. `problem_library.json` has "The table shows the math quiz scores of three students. Which statement about the median quiz scores is true?" — a compute-all-N-then-evaluate-every-choice format (MA1 #14 rebuilt to this format 2026-10-11). Prefer this compound style over a single bar-graph read when building future MMMR problems; it's the harder, more authentic version and was previously underrepresented.

## Fraction/decimal comparison problems: pick a technique first, then numbers (added 2026-10-11)
Caught via a real click-log: set 3 #2 (7/12, 0.58, 9/16 — order least to greatest) got rapid, chaotic answer-cycling from Hannah, unlike her usual clean self-corrections. The cause: all three values sit on the *same side* of 1/2 (0.58–0.61), so the standard benchmark technique gives zero separation, forcing brute-force decimal conversion with no entry point. Checked official solutions for every real "Comparing & Ordering Fractions & Decimals" example in `problem_library.json` — the real test always picks numbers so ONE of these four techniques applies cleanly, never forces brute-force conversion of everything:

1. **Benchmark comparison** — compare each value to a reference point (usually 1/2). Works when the values split meaningfully across the benchmark. Real example: "Which is the largest fraction? 2/3, 3/7, 1/100, 5/6" — official solution: *"comparing each fraction to a benchmark fraction... 2/3 is greater than 1/2... 3/7 is less than 1/2."*
2. **Common numerator or denominator** — convert so two fractions share a numerator (or denominator), then compare the other part directly: same numerator → smaller denominator wins (bigger pieces); same denominator → bigger numerator wins. Real example: 3/6 vs 6/10 → convert 3/6 to 6/12 (matching 6/10's numerator), then 12 vs 10 decides it (6/12 < 6/10 since 12 > 10).
3. **Cross-multiplication** — for exactly two fractions: multiply the first numerator by the second denominator and vice versa, compare the two products. Real example: "Which comparison is true? 3/4 < 3/8, 3/4 > 4/8, 3/4 < 5/8, 3/4 > 7/8."
4. **Visual fraction-bar / shaded-parts model** — reason about "how many shaded parts out of how many total," used when the question already shows/describes fraction bars.

**Before publishing any "order these values" or "which is greatest/least" problem**, pick which technique it's meant to test, then choose numbers that make THAT technique actually work (e.g. for benchmark: make sure not every value lands on the same side of 1/2). Check the result against problem_library.json's real examples for the same topic if unsure. Don't just pick numbers that are numerically close and assume that's "hard" — closeness alone doesn't make a problem authentic, and can accidentally make it *unsolvable by any real technique*, which is a different and worse kind of hard.

**One more thing, found the same day on a second pass of the fixes above:** when a magnitude-comparison problem pairs a fraction with a decimal, the real test's decimal is always simple -- one decimal place (0.3, 0.5, 0.6), never something like 0.58. This is specific to *comparison* problems; *equivalence/conversion* problems ("which fraction is equivalent to 0.455?", "write 0.527 as a fraction") are a different task and do use precise multi-digit decimals on purpose, since precision is the point there. Don't carry a conversion problem's decimal precision into a comparison problem -- it adds an unintended second skill (parsing an unfamiliar decimal) on top of the comparison technique being tested.
