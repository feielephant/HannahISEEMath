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
  redo-set-5.html                           24 problems from two online practice sessions, grouped by topic
  online-set-2.html                         Same 9 problems as redo-set-5.html's original 9, numbers unchanged
  redo-set-6.html                           15 problems from a 9/13 online session, grouped by topic, no self-check
  redo-set-6-answer-key.html                Answer key for redo-set-6.html &mdash; for parent/coach use only
  redo-set-7.html                           23 new problems on the topics that keep recurring, no self-check
  redo-set-7-answer-key.html                Answer key for redo-set-7.html &mdash; for parent/coach use only
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

### `worksheets/online-set-2.html`

Started as the other half of the redo-set-5 pair (the identical 9 problems from the 9/5 session, same numbers, same diagrams, nothing changed &mdash; meant for a calm, focused redo rather than a memory-proof one), but `redo-set-5.html` has since grown to 24 problems across two sessions, so this file now only pairs with the first 9 of those (probability, time-zone, decimal sum, Venn diagram, mean weight, number-line, recipe estimate, cube-counting, calculator estimate). Comparing results between the two on those 9 is the actual point: right on both points to attention as the original issue; wrong on both (even with fresh numbers the second time) points to the concept itself needing review.

### `worksheets/redo-set-6.html`

15 problems from a 9/13 online ISEE practice session (both math sections &mdash; the ISEE splits math into Quantitative Reasoning and Mathematics Achievement, which is why the source screenshots had two different "Question 24," "Question 26," etc.), organized into the same five-topic layout as redo-set-5.html: Number Theory & Estimation, Fractions & Ratios, Patterns & Algebraic Thinking, Geometry & Measurement, and Data Analysis. Unlike the earlier sets, these source screenshots didn't show a graded reveal (no green-correct/pink-wrong highlighting, just "% of other test-takers" stats), so there was no way to tell which of the 15 she'd actually missed &mdash; this set treats all 15 as worth a fresh look rather than guessing. Numbers, diagrams, and answer-choice positions are all changed from the original; a couple of the diagram-heavy problems (an array-of-squares factor-pair question, a partially-shaded floor-tile grid) needed pixel-level re-measurement of the original screenshots to get the exact grid dimensions right before building fresh versions.

**No self-check, unlike every earlier worksheet in this repo.** This file has no Submit & grade button, and — more importantly — no answer key embedded in its HTML/JS at all (not just a hidden button; the correct answers genuinely aren't present anywhere in the page source). Clicking a lettered choice just records the pick and saves it, nothing more. This was a deliberate change after a run of suspiciously strong redo-set results didn't carry over to an actual practice test, raising the possibility that the in-page grading reveal was getting used to check answers rather than to learn from them. Answers now live only in `redo-set-6-answer-key.html`, a separate, unlinked page meant for a parent or coach to check work against after the worksheet is done by hand.

### `worksheets/redo-set-6-answer-key.html`

The answer key for `redo-set-6.html`: correct letter and a one-line "Why" for each of the 15 problems, grouped the same way as the worksheet. Deliberately not linked from the worksheet itself — keep this link separate from whatever link she uses to do the problems.

### `worksheets/redo-set-7.html`

23 brand-new problems, not reused from any earlier worksheet, built specifically around the topics that have kept recurring as errors across the whole project's history (checked by comparing every confirmed-miss worksheet from redo-set-1 through redo-set-6, not just redo-set-4's original analysis): grocery running-total tables (the single most repeated miss overall, 8+ instances), time-zone elapsed time and composite-shape volume/area (both came back wrong on an actual practice test even after redo-set-4 drilled them directly), number-machine tables, estimation/rounding, and divisibility rules (the last two identified by cross-checking redo-set-5 against redo-set-6 and finding the same skills recurring across two independent sessions). Weighted by recurrence: 5 grocery-table variants, 4 time-zone, 6 composite-shape (2 volume, 2 overlapping-square-area, 2 combined-perimeter), 2 number-machine, 3 estimation, 3 divisibility. Like redo-set-6, this ships with no self-check and a separate answer key.

### `worksheets/redo-set-7-answer-key.html`

The answer key for `redo-set-7.html`: correct answer and a one-line "Why" for each of the 23 problems, grouped the same way as the worksheet. Not linked from the worksheet itself.

## Working on this repo with Claude Code

`.claude/skills/isee-worksheet/SKILL.md` captures the build procedure, naming
conventions, and recurring-bug checklist (SVG label clipping, WHY-string
escaping, grading-script gotchas) so future sessions don't have to rediscover
them. It auto-loads whenever a task touches `worksheets/`.

## Using the worksheets

Each file in `worksheets/` is self-contained — open it directly in a browser, no server or build step needed. Progress is saved per-browser via `localStorage`, so it won't carry over between devices or browsers.

## Notes on the source material

A handful of problems involving reading an approximate value off a hand-drawn number line, pie chart, or bar graph couldn't be graded with full confidence from a photo and are mostly left out; a couple of number-line reads that came out clean on a careful recheck are included anyway. One page's photo was rotated in a way that separated questions from their answer choices and wasn't included. Diagram-heavy problems from the later practice-test batch were rebuilt from a written description of each figure rather than a pixel-traced copy of the original.
