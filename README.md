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
  redo-set-2.html                           7 problems she genuinely missed on that same session, fresh numbers
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

The other side of that same online session: 7 problems (numbers 18, 20, and 29a/33/36/38/5 from the platform's own numbering, outside the 21&ndash;30 range) she actually read and answered — and got wrong for real, before the rushing that produced `online-set-1.html` started. Same pattern as `redo-set-1.html`: numbers changed, each one independently re-solved from scratch, no per-problem Check.

## Working on this repo with Claude Code

`.claude/skills/isee-worksheet/SKILL.md` captures the build procedure, naming
conventions, and recurring-bug checklist (SVG label clipping, WHY-string
escaping, grading-script gotchas) so future sessions don't have to rediscover
them. It auto-loads whenever a task touches `worksheets/`.

## Using the worksheets

Each file in `worksheets/` is self-contained — open it directly in a browser, no server or build step needed. Progress is saved per-browser via `localStorage`, so it won't carry over between devices or browsers.

## Notes on the source material

A handful of problems involving reading an approximate value off a hand-drawn number line, pie chart, or bar graph couldn't be graded with full confidence from a photo and are mostly left out; a couple of number-line reads that came out clean on a careful recheck are included anyway. One page's photo was rotated in a way that separated questions from their answer choices and wasn't included. Diagram-heavy problems from the later practice-test batch were rebuilt from a written description of each figure rather than a pixel-traced copy of the original.
