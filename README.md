# Hannah's ISEE Math Practice

This repo tracks Hannah's work through *Elevate Prep* ISEE Math practice materials (topic drills plus three full practice tests), re-solved digitally so she can rework the problems she missed without needing the original book.

The source photos of the book aren't included here (copyright) — they're kept locally only. Everything in `worksheets/` was independently transcribed and re-solved from those photos, not copied from an answer key.

## What's here

```
worksheets/       Generated HTML study tools
  full-workbook.html        Every problem, independently re-solved, with diagrams
  rework-worksheet.html     The 120 flagged/missed problems, blank for her to redo
  shuffled-rework-set.html  Same 120 problems, reshuffled into random order each visit
```

### `worksheets/full-workbook.html`

A clean reference copy of every problem, transcribed and re-solved from scratch, with recreated diagrams: number lines, coordinate grids, Venn diagrams, isometric cubes/prisms, pie and bar charts, and tables. Each problem shows the correct choice and a one-line explanation. This is the answer key for checking work against `rework-worksheet.html` and `shuffled-rework-set.html`.

### `worksheets/rework-worksheet.html`

The 120 problems Hannah needs to redo independently: everything she got wrong, plus everything flagged by a circled question number even where the current answer is correct. No answers are shown up front. Problems that reduce to one computed number get a blank text field; problems that are inherently multiple-choice (estimation ranges, "which of these," equation-select, the number-line reads) keep clickable lettered options.

Each problem has its own **Check** / **Clear** buttons, plus a global **Submit & grade** / **Clear all answers**. Checking a problem reveals the correct answer and a short "Why" explanation, and tallies a running correct/wrong count. Answers autosave to the browser (localStorage).

### `worksheets/shuffled-rework-set.html`

The same 120 problems as a single flowing list that reshuffles into a new random order on load or on demand (a "Reshuffle order" button), so a repeat attempt isn't just recalling problem position. Progress is tracked and saved independently from the ordered worksheet, with the same Check/grade behavior.

## Using the worksheets

Each file in `worksheets/` is self-contained — open it directly in a browser, no server or build step needed. Progress is saved per-browser via `localStorage`, so it won't carry over between devices or browsers.

## Notes on the source material

A handful of problems involving reading an approximate value off a hand-drawn number line, pie chart, or bar graph couldn't be graded with full confidence from a photo and are mostly left out; a couple of number-line reads that came out clean on a careful recheck are included anyway. One page's photo was rotated in a way that separated questions from their answer choices and wasn't included. Diagram-heavy problems from the later practice-test batch were rebuilt from a written description of each figure rather than a pixel-traced copy of the original.
