# Hannah's ISEE Math Practice — Project Notes

## What this repo is
Hannah's *Elevate Prep* ISEE Math practice materials, photographed page by
page, turned into interactive HTML study tools.

- Source photos are **not in this repo** (copyright — it's a purchased
  practice book) and never should be committed here. They live locally at
  `~/Documents/HannahISEEMath/Photos-1-001/` and `Photos-1-001 2/` on the
  user's machine only. Repo history was once rewritten to purge photos that
  had been committed before this was caught — don't reintroduce them.
  **Filename timestamp order is NOT page order** in either photo folder —
  always check the printed page number in the image itself.
- `worksheets/full-workbook.html` — all problems, independently re-solved,
  answers shown. This is the answer key.
- `worksheets/rework-worksheet.html` — the 120 flagged problems (wrong now,
  or circled-number-but-later-fixed), blank, ordered by page/test.
- `worksheets/shuffled-rework-set.html` — same 120 problems, reshuffles on
  load/demand.

## The 120 flagged problems
Each has a qid: `p126-5` (page-problem#) for topic-drill pages, or
`t1qr-8` / `t2ma-14` (test#, QR or MA section, problem#) for the three full
practice tests. Two kinds per problem:
- **"num" problems** — one computable number → blank text input.
- **"choice" problems** — estimation ranges, "which of these,"
  equation-select, ratios/fractions/mixed-numbers (parseNum can't compare
  those reliably), number-line reads → four clickable lettered options.

All three worksheet files embed a `WHY` object (qid → one-line reasoning
string, shown on Check/grade) alongside `ANSWERS` (qid →
`{type:'num', value:N}` or `{type:'choice', letter:'X'}`). **If a correct
answer or problem wording ever changes, it must change in up to 3 places**:
`full-workbook.html`'s card, and the `ANSWERS`/`WHY` entries + card text in
*both* `rework-worksheet.html` and `shuffled-rework-set.html`.

## Grading system (already built)
Each problem card has its own Check/Clear buttons, plus global Submit &
Grade / Clear All. Logic lives in each file's inline `<script>`:
`gradeOne(qid)` grades one (and shows its `WHY` text), `gradeAll()` loops
it, `clearOne(qid)` / `clearGradeMarks()` reset. `parseNum()` strips
`$,%,commas,units` before comparing — this is why fraction/ratio/mixed-
number answers are "choice" type, not "num". Progress + answers autosave
to `localStorage` (separate key per file, since each artifact/file is its
own storage origin).

## House rules for future changes
1. **Never commit the source photos to this repo**, in any commit. Keep
   them local-only. If new photos get added locally, transcribe/solve from
   them but don't `git add` the image files themselves.
2. **Verify against the actual local photo before fixing a problem.**
   Several past fixes were wrong on the first pass because the text had
   been paraphrased or misread by an earlier pass.
3. **Every fix to a problem touches up to 3 files** — see above. Grep for
   the qid or distinctive text across all three before declaring done.
4. **Keep design/theme consistent**: Petrona (headings) / Public Sans
   (body) / JetBrains Mono (numbers, code), teal accent (`--accent`),
   light+dark theme via CSS vars — copy the existing pattern, don't
   reinvent it.
5. **Diagrams**: build exact geometry (SVG `clipPath`/`mask`, computed
   coordinates, or a real `<table>`) rather than hand-drawn approximations
   — past hand-drawn Venn diagrams and shapes were geometrically wrong.
6. **After editing a worksheet**, sync three places: the scratchpad working
   copy, the published Claude Artifact (same URL, so it updates in place),
   and this repo's `worksheets/` copy — then commit.
7. **Keep this repo private.** It was briefly made public and had to be
   reverted — both because it's a minor's schoolwork/name, and because the
   (now-removed) photos were copyrighted material. Don't flip visibility
   without asking first.
8. **This machine's shell sometimes loses read access to `~/Documents`**
   (a macOS Files-and-Folders permission hiccup, not a project bug). If
   `ls`/`git` suddenly fail with "Operation not permitted" even on `.`,
   that's what's happening — work around it by cloning/operating in a
   directory outside `~/Documents` (e.g. a scratch/tmp dir) instead of
   waiting on it, and resync `~/Documents` once access returns.
