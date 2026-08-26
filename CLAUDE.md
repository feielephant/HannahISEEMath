# Hannah's ISEE Math Practice — Project Notes

## What this repo is
Hannah's *Elevate Prep* ISEE Math practice book, photographed page by page,
turned into interactive HTML study tools.

- `photos/` — 37 source photos (pages 126–194). **Filename timestamp order
  is NOT page order** — the photographer shot out of sequence. Always check
  the printed page number in the image itself, never assume from filename.
- `worksheets/full-workbook.html` — all ~223 problems, independently
  re-solved, answers shown. This is the answer key.
- `worksheets/rework-worksheet.html` — the 47 flagged problems (wrong now,
  or circled-number-but-later-fixed), blank, ordered by page.
- `worksheets/shuffled-rework-set.html` — same 47 problems, reshuffles on
  load/demand.

## The 47 flagged problems
Each has an id like `p126-5` (page-problem#). Two kinds:
- **30 "num" problems** — one computable number → blank text input.
- **17 "choice" problems** — estimation ranges, "which of these,"
  equation-select, number-line reads → four clickable lettered options.

Both worksheet files embed an identical `ANSWERS` JS object keyed by qid
(`{type:'num', value:N}` or `{type:'choice', letter:'X'}`). **If a correct
answer or problem wording ever changes, it must change in three places**:
`full-workbook.html`'s card, and the `ANSWERS` entry + card text in
*both* `rework-worksheet.html` and `shuffled-rework-set.html`.

## Grading system (already built)
Each problem card has its own Check/Clear buttons, plus global Submit &
Grade / Clear All. Logic lives in each file's inline `<script>`:
`gradeOne(qid)` grades one, `gradeAll()` loops it, `clearOne(qid)` /
`clearGradeMarks()` reset. `parseNum()` strips `$,%,commas,units` before
comparing. Progress + answers autosave to `localStorage` (separate key
per file, since each artifact/file is its own storage origin).

## House rules for future changes
1. **Verify against the actual photo before fixing a problem.** Several
   past fixes were wrong on the first pass because the text had been
   paraphrased or misread. Read the source image in `photos/` directly.
2. **Every fix to a problem touches up to 3 files** — see above. Grep for
   the qid or distinctive text across all three before declaring done.
3. **Keep design/theme consistent**: Petrona (headings) / Public Sans
   (body) / JetBrains Mono (numbers, code), teal accent (`--accent`),
   light+dark theme via CSS vars — copy the existing pattern, don't
   reinvent it.
4. **Diagrams**: build exact geometry (SVG `clipPath`/`mask`, computed
   coordinates) rather than hand-drawn approximations — past
   hand-drawn Venn diagrams and shapes were geometrically wrong.
5. **After editing a worksheet**, sync three places: the scratchpad
   working copy, the published Claude Artifact (same URL, so it
   updates in place), and this repo's `worksheets/` copy — then commit.
6. **Repo is private** (contains a minor's schoolwork/name). Don't make
   it public or add photos of her elsewhere without asking first.
