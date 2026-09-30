# Hannah's ISEE Math Practice

This repo tracks Hannah's work through *Elevate Prep* ISEE Math practice materials (topic drills plus three full practice tests), re-solved digitally so she can rework the problems she missed without needing the original book.

The source photos of the book aren't included here (copyright) — they're kept locally only. Everything in `worksheets/` was independently transcribed and re-solved from those photos, not copied from an answer key.

## What's here

```
worksheets/       Generated HTML study tools
  full-workbook.html                        Every problem, independently re-solved, with diagrams
  rework-worksheet.html                     The 120 flagged/missed problems, blank, with per-problem Check + Submit & grade
  rework-worksheet-testmode.html            Same, but no per-problem Check — only Submit & grade at the end
  shuffled-rework-set.html                  Same 120 problems, random order each visit, with per-problem Check + Submit & grade
  shuffled-rework-set-testmode.html         Same, but no per-problem Check — only Submit & grade at the end
  shuffled-rework-set-testmode-day1.html    30 of the 120, day 1 of a 4-day split (test mode)
  shuffled-rework-set-testmode-day2.html    30 of the 120, day 2 of a 4-day split (test mode)
  shuffled-rework-set-testmode-day3.html    30 of the 120, day 3 of a 4-day split (test mode)
  shuffled-rework-set-testmode-day4.html    30 of the 120, day 4 of a 4-day split (test mode)
  redo-set-1.html                           Problems missed a 2nd time, rebuilt with fresh numbers
  online-set-1.html                         Problems 21-30 from an online session, rushed past unread
  redo-set-2.html                           8 problems she genuinely missed on that same session, fresh numbers
  redo-set-3.html                           29 problems missed a 2nd time across earlier sets, fresh numbers
  redo-set-4.html                           20 problems, extra drill on the most persistent topics
  redo-set-5.html                           24 redo problems from two online sessions, plus the 33 exact original problems from the 203-screenshot review
  online-set-2.html                         Same 9 problems as redo-set-5.html's original 9, numbers unchanged
  redo-set-6.html                           15 problems from a 9/13 online session, grouped by topic, no self-check
  redo-set-6-answer-key.html                Answer key for redo-set-6.html &mdash; for parent/coach use only
  redo-set-7.html                           33 new problems on the topics that keep recurring, no self-check
  redo-set-7-answer-key.html                Answer key for redo-set-7.html &mdash; for parent/coach use only
  redo-set-8.html                           27 new problems on gap categories from the full 203-problem review, no self-check
  redo-set-8-answer-key.html                Answer key for redo-set-8.html &mdash; for parent/coach use only
  redo-set-9.html                           The 9 exact problems missed on the 0920 test, a second try, no self-check
  redo-set-9-answer-key.html                Answer key for redo-set-9.html &mdash; for parent/coach use only
  redo-set-10.html                          30 new problems training the 5 attention habits, ahead of the Friday test
  redo-set-10-answer-key.html                Answer key for redo-set-10.html &mdash; for parent/coach use only
  redo-set-11.html                          15 new problems: 3 sticky-gap groups from real redo-set-10 misses, plus 6 multi-habit combos
  redo-set-11-answer-key.html                Answer key for redo-set-11.html &mdash; for parent/coach use only
  redo-set-12.html                          14 new problems from a real 9/27 practice-test attempt, the last practice test before the real one
  redo-set-12-answer-key.html                Answer key for redo-set-12.html &mdash; for parent/coach use only
  redo-set-13.html                          28 exact-repeat problems, personally re-verified against source images after an earlier pass fabricated some content
  redo-set-13-answer-key.html                Answer key for redo-set-13.html &mdash; for parent/coach use only
```

### `worksheets/full-workbook.html`

A clean reference copy of every problem, transcribed and re-solved from scratch, with recreated diagrams: number lines, coordinate grids, Venn diagrams, isometric cubes/prisms, pie and bar charts, and tables. Each problem shows the correct choice and a one-line explanation. This is the answer key for checking work against the worksheets below.

### `worksheets/rework-worksheet.html` / `shuffled-rework-set.html`

The 120 problems Hannah needs to redo independently: everything she got wrong, plus everything flagged by a circled question number even where the current answer is correct. No answers are shown up front. Problems that reduce to one computed number get a blank text field; problems that are inherently multiple-choice (estimation ranges, "which of these," equation-select, the number-line reads) keep clickable lettered options.

Each problem has its own **Check** / **Clear** buttons, plus a global **Submit & grade** / **Clear all answers**. Checking a problem (or submitting) reveals the correct answer and a short "Why" explanation, and tallies a running correct/wrong count. The shuffled version reshuffles into a new random order on load or on demand, so a repeat attempt isn't just recalling problem position. Answers autosave to the browser (localStorage), separately per file.

### `worksheets/rework-worksheet-testmode.html` / `shuffled-rework-set-testmode.html`

Same content and behavior as above, minus the per-problem Check/Clear buttons — there's nothing to peek at mid-way through. She works the whole set cold, then hits **Submit & grade** once at the end to see everything reveal at once.

### `worksheets/shuffled-rework-set-testmode-day{1,2,3,4}.html`

The 120 problems are a lot to finish in one sitting, so these split the shuffled test-mode set into four independent 30-problem days — one file per day. Each day's 30 problems were assigned by taking the full 120 in their natural page/test order and distributing round-robin across the four days, so every day gets a mix of topics and tests rather than one being all percents and another all geometry. Each day has its own random shuffle, its own progress tracking, and grades independently of the others.

### `worksheets/redo-set-1.html`

A one-off set built from problems Hannah got wrong a second time on a graded worksheet. Same problem type and difficulty as the original miss, but with the numbers changed and each one independently re-solved from scratch, so it's a genuine retry rather than the same problem with a memorized answer. No per-problem Check — Submit & grade at the end, same as the test-mode worksheets. Future "missed again" sets should follow this pattern (`redo-set-2.html`, etc.) rather than reusing this file.

### `worksheets/online-set-1.html`

Problems 21 through 30 from a session on an online ISEE practice platform (not the *Elevate Prep* book) that she clicked through quickly without actually reading — same 10 questions and same numbers, presented fresh with blanks so they get a genuine first attempt. Sourced from screenshots of the platform's post-answer review screens, independently re-verified rather than trusted from the reveal text. Same test-mode behavior as the sets above: no per-problem Check, Submit & grade at the end.

### `worksheets/redo-set-2.html`

The other side of that same online session: 8 problems (numbers 5, 18, 20, 22, 29a, 33, 36, and 38 from the platform's own numbering) she actually read and answered — and got wrong for real, before the rushing that produced `online-set-1.html` started. Problem 22 also appears in `online-set-1.html` with its original numbers (it's ambiguous which "mode" that one attempt was in), but here it gets its own independent fresh-number version like the rest. Same pattern as `redo-set-1.html`: numbers changed, each one independently re-solved from scratch, no per-problem Check.

### `worksheets/redo-set-3.html`

A larger "missed again" set: 29 problems pulled from across several earlier worksheets (the original book-based rework set, `redo-set-1.html`/`redo-set-2.html`, and the T2/T3 practice-test batches) that she got wrong a second time on a repeat attempt. Same pattern — numbers changed and each one independently re-solved from scratch — plus the correct answer's letter position shuffled throughout, so neither the numbers nor "it's usually A" pattern-matching carries over from memory. The composite-prism volume diagram is additionally mirrored (both left-right and up-down) from its source so the picture itself doesn't look familiar.

### `worksheets/redo-set-4.html`

A focused-practice set, not a straight "missed again" dump: 20 problems weighted by how often each *topic* has kept recurring across `redo-set-1.html`, `-2.html`, and `-3.html`, rather than one problem per miss. The grocery-total table (solve for a missing item's quantity from a running total) got the most repetition — 5 variants — since it's been wrong in four separate worksheets now; word-problem-to-equation translation, "closest to a fraction of X" estimation, time-zone elapsed time, and composite-shape scaling each get 2–3; the odd-number cubing pattern, which has been closer to solid, gets just 1. Fresh numbers throughout, independently re-solved.

### `worksheets/redo-set-5.html`

A different kind of redo, and the largest single-topic-grouped set so far: 24 problems pulled from her online ISEE practice-platform sessions (9/5 and 8/30) that she missed on the first pass, organized into five topic sections &mdash; Number Theory & Estimation, Fractions & Decimals, Patterns & Algebraic Thinking, Geometry & Measurement, and Data Analysis & Probability &mdash; rather than one flat list. The point isn't just scoring it &mdash; if she gets most of these right with fresh numbers, that points to focus rather than a skill gap; if the same topics come back wrong again, that's worth reviewing together directly. Numbers, diagrams, and answer-choice positions are all changed from the original. The time-zone problem uses the actual map image from the source screenshot (embedded directly in the page) rather than a redrawn approximation, since an accurate hand-drawn US time-zone map isn't worth the risk of introducing a geography error. Three problems from the 8/30 session that she'd actually already answered correctly (a fraction-thickness comparison, a coordinate-plane quadrilateral, and an area estimate) were deliberately left out &mdash; this file is for redoing misses, not re-serving what she already has.

**Update:** redo-set-5 now ends with a 33-problem section, "Original Online-Test Errors," containing the exact problems (same numbers, same choices, rebuilt from the screenshots) that she got wrong in the 203-screenshot online review, so there is one page of every confirmed online-platform error. It keeps this file's Submit & grade behavior (answers and "Why" are embedded in the page).

### `worksheets/online-set-2.html`

Started as the other half of the redo-set-5 pair (the identical 9 problems from the 9/5 session, same numbers, same diagrams, nothing changed &mdash; meant for a calm, focused redo rather than a memory-proof one), but `redo-set-5.html` has since grown to 24 problems across two sessions, so this file now only pairs with the first 9 of those (probability, time-zone, decimal sum, Venn diagram, mean weight, number-line, recipe estimate, cube-counting, calculator estimate). Comparing results between the two on those 9 is the actual point: right on both points to attention as the original issue; wrong on both (even with fresh numbers the second time) points to the concept itself needing review.

### `worksheets/redo-set-6.html`

15 problems from a 9/13 online ISEE practice session (both math sections &mdash; the ISEE splits math into Quantitative Reasoning and Mathematics Achievement, which is why the source screenshots had two different "Question 24," "Question 26," etc.), organized into the same five-topic layout as redo-set-5.html: Number Theory & Estimation, Fractions & Ratios, Patterns & Algebraic Thinking, Geometry & Measurement, and Data Analysis. Unlike the earlier sets, these source screenshots didn't show a graded reveal (no green-correct/pink-wrong highlighting, just "% of other test-takers" stats), so there was no way to tell which of the 15 she'd actually missed &mdash; this set treats all 15 as worth a fresh look rather than guessing. Numbers, diagrams, and answer-choice positions are all changed from the original; a couple of the diagram-heavy problems (an array-of-squares factor-pair question, a partially-shaded floor-tile grid) needed pixel-level re-measurement of the original screenshots to get the exact grid dimensions right before building fresh versions.

**No self-check, unlike every earlier worksheet in this repo.** This file has no Submit & grade button, and — more importantly — no answer key embedded in its HTML/JS at all (not just a hidden button; the correct answers genuinely aren't present anywhere in the page source). Clicking a lettered choice just records the pick and saves it, nothing more. This was a deliberate change after a run of suspiciously strong redo-set results didn't carry over to an actual practice test, raising the possibility that the in-page grading reveal was getting used to check answers rather than to learn from them. Answers now live only in `redo-set-6-answer-key.html`, a separate, unlinked page meant for a parent or coach to check work against after the worksheet is done by hand.

### `worksheets/redo-set-6-answer-key.html`

The answer key for `redo-set-6.html`: correct letter and a one-line "Why" for each of the 15 problems, grouped the same way as the worksheet. Deliberately not linked from the worksheet itself — keep this link separate from whatever link she uses to do the problems.

### `worksheets/redo-set-7.html`

33 brand-new problems, not reused from any earlier worksheet, built specifically around the topics that have kept recurring as errors across the whole project's history (checked by comparing every confirmed-miss worksheet from redo-set-1 through redo-set-6, not just redo-set-4's original analysis): grocery running-total tables (the single most repeated miss overall, 8+ instances), time-zone elapsed time and composite-shape volume/area (both came back wrong on an actual practice test even after redo-set-4 drilled them directly), number-machine tables, estimation/rounding, and divisibility rules (the last two identified by cross-checking redo-set-5 against redo-set-6 and finding the same skills recurring across two independent sessions). Weighted by recurrence: 5 grocery-table variants, 4 time-zone, 6 composite-shape (2 volume, 2 overlapping-square-area, 2 combined-perimeter), 2 number-machine, 3 estimation, 3 divisibility &mdash; that's the original 23. Seven more were added after a real redo-set-6 attempt and a real redo-set-8 attempt both confirmed the same gaps keep resurfacing: 2 more multi-step area/perimeter problems (this project's single most persistent gap, per the full 203-problem diagnostic review), 1 more divisibility, 1 more estimation, 1 "always true" logic problem, 1 distributive-property problem, and 1 proportional-prediction problem &mdash; bringing the set to 30. It was then rebalanced up to 33: the three thinnest new topics ("always true" logic, distributive property, organize-the-data) were brought up to 3 problems each (from 1), while one grocery-table, one time-zone, and one composite-perimeter problem were trimmed since those specific sub-types haven't come back wrong in any of the recent real attempts. Like redo-set-6, this ships with no self-check and a separate answer key.

### `worksheets/redo-set-7-answer-key.html`

The answer key for `redo-set-7.html`: correct answer and a one-line "Why" for each of the 33 problems, grouped the same way as the worksheet. Not linked from the worksheet itself.

### `worksheets/redo-set-8.html`

27 brand-new problems built from a full independent review of 203 screenshots from a separate "all problems" practice folder (not tied to any single missed-worksheet comparison like earlier sets) — every problem was read individually, classified right/wrong, and every wrong answer further classified as a careless slip or a genuine knowledge gap. redo-set-7's four topics (divisibility, time-zone, composite-perimeter, estimation) were confirmed as real recurring issues by this larger sample, but 7 more categories showed up that weren't covered anywhere yet: multi-step area/perimeter strategy (find an intermediate value before the final step — 4 problems), "always true" logical reasoning that misses an edge case or converse (4 problems), organizing data before computing — sorting before taking a median, reading a stem-and-leaf plot correctly, building a ratio for a prediction (4 problems), number-line tick-density — a standing weak spot from earlier work that still hadn't resolved (3 problems), probability category identification (the asked-for event vs. its complement — 3 problems), spatial/grid counting (3 problems), and the distributive property applied to only one term instead of both (2 problems). A closing 4-problem "Quick Check" group revisits redo-set-7's own topics with fresh numbers to confirm those gains are sticking. Like redo-set-6 and -7, no self-check — answers live only in the separate answer key.

### `worksheets/redo-set-8-answer-key.html`

The answer key for `redo-set-8.html`: correct answer and a "Why" for each of the 27 problems, grouped the same way as the worksheet. Not linked from the worksheet itself.

### `worksheets/redo-set-9.html`

The 9 problems she missed on the 0920 practice test, presented exactly as they were (same numbers, same answer choices), as a second chance: if she fixes them all, they were attention slips; anything still wrong is worth working through together. The misses were mostly "answered part of the question" slips (dropped the odd condition, reversed least-to-greatest, added only one class on a graph, missed "shared equally"), plus a remainder problem, a multiply-by-3 pattern and a volume-with-gaps concept. No self-check; answers are in `redo-set-9-answer-key.html`.

### `worksheets/redo-set-10.html`

30 brand-new problems, not reused from any earlier worksheet, built ahead of a Friday test. The first 25 train the 5 attention habits identified by scanning every wrong answer across the 203-problem review, redo-set-6, redo-set-7, redo-set-8, and the 0920 test (see `habit-checklist.html` in the parent folder): checking every stated condition, using all the given data, watching the one key word that flips the answer, giving the exact thing asked for rather than an intermediate step, and computing both sides of a comparison instead of assuming. 5 problems per habit; every wrong choice is a deliberate trap matching exactly what she'd pick if she skipped that specific check. The last 5 are a separate "Knowledge Gap Check" &mdash; fresh-number versions of specific concepts confirmed wrong before but never yet re-tested (a messy-ratio proportional prediction, composite 3D volume, a non-constant growth pattern, fraction-vs-a-whole comparison, and what "volume" means when a box has gaps), deliberately excluding always-true logic since that's already had heavy reinforcement elsewhere. No self-check; answers are in `redo-set-10-answer-key.html`.

### `worksheets/redo-set-10-answer-key.html`

The answer key for `redo-set-10.html`: correct answer and a "Why" for each of the 30 problems, explicitly naming the trap each wrong choice represents.

### `worksheets/redo-set-11.html`

15 brand-new problems, not reused from any earlier worksheet, built directly from a real redo-set-10 attempt rather than a fresh diagnostic pass. Three real misses drove 9 of the problems, grouped as sticky-gap sections: predicting a count from a ratio (missed with fresh numbers on the Wildcat-mascot table problem, confirming this gap is still real), composite volume being the sum of two joined solids (missed even in a picture-free, text-only version, ruling out diagram-reading as the cause), and a newly identified issue &mdash; trusting the math even when the answer isn't a whole number (she used the correct method on a square-vs-rectangle area problem but abandoned it on seeing 49&divide;14 wasn't an integer, assuming she'd made an error). All three "trust the math" problems deliberately have decimal answers. The last 6 problems each combine two (one combines three) of the 5 attention habits in a single question, closer to how a real test problem can layer several small checks at once. No self-check; answers are in `redo-set-11-answer-key.html`.

### `worksheets/redo-set-11-answer-key.html`

The answer key for `redo-set-11.html`: correct answer and a "Why" for each of the 15 problems, grouped the same way as the worksheet.

### `worksheets/redo-set-12.html`

14 brand-new problems, not reused from any earlier worksheet, built from a real attempt at the 9/27 online practice test &mdash; the last practice test before the real ISEE. Seven sticky spots showed up in that attempt, two fresh problems each: a repeated-digit addition cryptarithm where the hundreds digit is always forced to 1 by carrying, no matter the specific digits (missed on `AA+BB=CDE`); matching each symbol in a word problem to the right quantity before combining them (missed on a pencils/stickers-style translation, swapping which symbol was the original amount versus the amount given away); cubing a linear scale factor to get a volume ratio instead of using a surface-area-style formula (missed on a "how many small cubes fit in a bigger cube" problem, picking 150 instead of 125 &mdash; recreated with an actual isometric cube-pair diagram, not just a text description); the direction of a successive percent change (got the 4% magnitude right on a 20%-up-then-20%-down salary problem but called it an increase instead of a decrease); the MORE-vs-LESS attention habit, confirmed still not secure on an easy fraction-to-decimal comparison that 90% of test-takers got right; a decimal-addition place-value slip; and reading a tape/bar-diagram model correctly (missed a stretch-bandage problem where all 4 answer choices were diagrams, picking one that only modeled a single roll instead of the full total &mdash; recreated as actual tape diagrams, not text). No self-check; answers are in `redo-set-12-answer-key.html`.

**Correction:** the first version of this file only had 6 groups and described the cube and bandage problems in text. A closer look at the practice-test screenshots found the bandage/tape-diagram problem had also been missed (a highlighted wrong pick that was easy to mistake for the platform's "eliminate this choice" button), and that a genuine diagram belonged on the cube problem rather than a text description. Both are now fixed.

### `worksheets/redo-set-12-answer-key.html`

The answer key for `redo-set-12.html`: correct answer and a "Why" for each of the 14 problems, grouped the same way as the worksheet.

### `worksheets/redo-set-13.html`

28 exact-repeat problems, following the same pattern as `redo-set-9.html` (unchanged numbers, wording, and answer choices). Rebuilt 9/29 after a full re-read of the entire practice history surfaced major gaps that earlier, narrower searches had missed entirely &mdash; then rebuilt again the same day after several of those "verbatim transcriptions" turned out to be fabricated rather than sourced from the real page, once personally re-checked against the original images.

Seven groups:
- **Final check &mdash; cube scale factor &amp; decimal addition** (2 problems) &mdash; both aced with fresh numbers in redo-set-12, kept as one last exact-repeat check rather than a full re-drill.
- **9/27 test, one more miss found** (1 problem) &mdash; the "Beach Restaurant" table problem was originally misread as correct; the wrong-answer highlight color looked similar to the platform's elimination marker, the same mistake that happened once before on this test. Re-checked directly: she picked $42, correct is $39.
- **Estimation: matching your answer to the right bucket** (9 problems) &mdash; the single largest gap in the whole archive (10 confirmed wrong). "About how many / reasonable estimate / closest approximation" problems with range-based answer choices; several instances show CORRECT scratch work with the wrong bucket circled anyway.
- **Off by a factor of 10, plus one translation miss** (6 problems) &mdash; losing a factor of 10 somewhere in a metric conversion or percent calculation; two of these she actually caught and self-corrected on the original page (crossed out a first answer, circled the right one), which still counts as real evidence of the instinct even though she caught it that time. Plus one word-problem-to-equation translation miss (a "twice as much" multiplier dropped) found on the same page.
- **Multi-step unit conversion** (4 problems, new) &mdash; conversions needing more than one step (yards&rarr;inches, gallons&rarr;pints) get only partially completed.
- **Decimal/fraction to percent: which way the point moves** (3 problems, new) &mdash; a sibling of the off-by-10 gap from a dedicated conversion drill: shifting the decimal point the wrong number of places when converting to a percent.
- **Reverse-percent problems** (3 problems, new) &mdash; straightforward "what is P% of X" is solid, but reversed framings ("X is what% of Y," "X is P% of what number") are not; each wrong instance uses a different broken mechanism (backwards fraction, multiplying instead of dividing). One of these she also self-corrected on the page.

**A data-integrity note, since it matters for how much to trust the rest of this project's research:** an earlier version of this file, also 25 problems but across six *different* groups, included a "word problems with a letter variable" group built from what was reported as 4 verbatim transcriptions. On direct re-inspection of the actual source images, only 1 of those 4 was real (the apple/banana problem, now folded into the "off by a factor of 10" group above) &mdash; the other 3 (including a "Roger and Cory" problem and one supposedly from page 312) were invented by a research pass that, when it couldn't find an exact match for a vague prior description, generated plausible-sounding content instead of reporting the miss. Two percent problems were also briefly removed over ambiguous circle marks, then restored once re-examined: a circled-and-crossed-out answer is a discarded first attempt, a clean circle is the corrected final one &mdash; real evidence of the off-by-10 instinct even though she caught it herself that time. Two more batches (3 decimal-to-percent problems, then 3 reverse-percent problems) were added after being independently re-verified against their source pages. Every problem in the current file has been personally re-checked against its source image.

### `worksheets/redo-set-13-answer-key.html`

The answer key for `redo-set-13.html`: correct answer and a "Why" for each of the 28 problems, grouped the same way as the worksheet.

## Working on this repo with Claude Code

`.claude/skills/isee-worksheet/SKILL.md` captures the build procedure, naming
conventions, and recurring-bug checklist (SVG label clipping, WHY-string
escaping, grading-script gotchas) so future sessions don't have to rediscover
them. It auto-loads whenever a task touches `worksheets/`.

## Using the worksheets

Each file in `worksheets/` is self-contained — open it directly in a browser, no server or build step needed. Progress is saved per-browser via `localStorage`, so it won't carry over between devices or browsers.

## Notes on the source material

A handful of problems involving reading an approximate value off a hand-drawn number line, pie chart, or bar graph couldn't be graded with full confidence from a photo and are mostly left out; a couple of number-line reads that came out clean on a careful recheck are included anyway. One page's photo was rotated in a way that separated questions from their answer choices and wasn't included. Diagram-heavy problems from the later practice-test batch were rebuilt from a written description of each figure rather than a pixel-traced copy of the original.
