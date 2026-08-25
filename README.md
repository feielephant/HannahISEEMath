# Hannah's ISEE Math Practice

This repo tracks Hannah's work through an *Elevate Prep* ISEE Math Multiple Choice practice book, photographed page by page and re-solved digitally so she can rework the problems she missed without needing the original book.

## What's here

```
photos/           37 photos of the practice book, pages 126-194 (source material)
worksheets/       Generated HTML study tools, built from those photos
  full-workbook.html        Every problem (~223), independently re-solved, with diagrams
  rework-worksheet.html     The 47 flagged/missed problems, blank for her to redo
  shuffled-rework-set.html  Same 47 problems, reshuffled into random order each visit
```

### `photos/`

Each photo is one page (or spread) of the practice book, showing the printed problems plus Hannah's handwritten circled answers. Answer choices she got wrong are circled; a circled *question number* means that problem was wrong at some point, even if it shows a correct answer now.

### `worksheets/full-workbook.html`

A clean reference copy of every problem in the book, transcribed and re-solved from scratch (not copied from the answer key), with recreated diagrams: number lines, coordinate grids, Venn diagrams, isometric cubes/prisms, pie and bar charts, and tables. Each problem shows the correct choice and a one-line explanation. This is the answer key for checking work against `rework-worksheet.html` and `shuffled-rework-set.html`.

### `worksheets/rework-worksheet.html`

The 47 problems Hannah needs to redo independently: everything she got wrong, plus everything flagged by a circled question number even where the current answer is correct. No answers are shown. Problems that reduce to one computed number get a blank text field; problems that are inherently multiple-choice (estimation ranges, "which of these," the two number-line reads) keep clickable lettered options. Answers typed or selected are saved automatically in the browser (localStorage), with a live progress counter and a "clear all" reset.

### `worksheets/shuffled-rework-set.html`

The same 47 problems as a single flowing list that reshuffles into a new random order on load or on demand (a "Reshuffle order" button), so a repeat attempt isn't just recalling problem position. Progress is tracked and saved independently from the ordered worksheet.

## Using the worksheets

Each file in `worksheets/` is self-contained — open it directly in a browser, no server or build step needed. Progress is saved per-browser via `localStorage`, so it won't carry over between devices or browsers.

## Notes on the source material

A handful of problems from pages 132–134, 165–166, and 190 involve reading an approximate value off a hand-drawn number line, pie chart, or bar graph. These can't be graded with full confidence from a photo, so most are left out of the rework set; two number-line reads that came out clean on a careful recheck are included anyway. Page 187's photo is rotated in a way that separates each question from its answer choices and isn't included.
