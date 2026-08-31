---
name: isee-worksheet
description: Build, fix, or extend Hannah's ISEE math practice worksheets (HTML/CSS/JS in this repo) — new problem sets, "redo" sets with fresh numbers, splitting into daily files, SVG diagrams, or grading-script bugs. Use whenever the task touches a file under worksheets/.
---

# ISEE worksheet builder

Context and conventions for this repo (`feielephant/HannahISEEMath`), a private repo
of static HTML worksheets built from Hannah's photographed *Elevate Prep* ISEE math
book. Read `CLAUDE.md` at the repo root first — it has the file inventory and house
rules. This skill covers the *procedure and pitfall checklist* CLAUDE.md doesn't.

## Repo location gotcha (macOS permissions)

`~/Documents/HannahISEEMath-repo` periodically becomes unreadable to the sandboxed
shell ("Operation not permitted" on plain `ls`), a macOS TCC quirk, not a real repo
problem. If that happens: clone fresh into the scratchpad directory instead
(outside `~/Documents`) and work there — `git clone https://github.com/feielephant/HannahISEEMath.git repo-clean` — then sync the finished file back and push from wherever
git access actually works. Don't wait for permissions to fix themselves.

Before starting any worksheet edit, `git pull` (or `fetch` + `reset --hard origin/main`
if the local clone has diverged/gone stale) — this repo gets pushed to from whichever
location had working permissions last, so the checkout you're sitting in may be behind.

## File families and naming

- `pXXX-N` — qid for one of the original 47 flagged problems, page-based (page XXX,
  problem N).
- `t{1,2,3}{qr,ma}-N` — qid for the 73-problem added batch (test-section-based).
- `redo-<origqid>` — a fresh-number variant of a problem Hannah missed again, e.g.
  `redo-t2ma-1`. Never reuse the original qid for a redo — different numbers need a
  different key so old localStorage answers don't collide.
- `STORAGE_KEY` is unique per file (`hannah-<slug>-v1`) since each HTML file/artifact
  is its own localStorage origin — bump the version suffix if you ever change a
  file's ANSWERS shape in a way that would make old cached answers wrong.
- "Full" worksheets have per-problem Check/Clear buttons (`injectCardControls()`,
  `checkOne`/`clearOne`) plus a global Submit & Grade. "Test mode" files
  (`*-testmode*.html`) have **only** the global Submit & Grade — no per-problem
  Check, so a kid can't peek at one answer at a time. Default to test mode unless
  told otherwise; it's what's actually in use.

## Standard build: a new "redo" set from missed problems

Triggered by the user pasting a block of problems Hannah got wrong (usually with
"You put X — correct answer Y" reveal text from a graded run).

1. **Extract the distinct problems** — the pasted block sometimes has exact
   duplicates; dedupe by qid/content first.
2. **Change the numbers, not just re-serve the answer key.** Re-derive fresh values
   and *independently solve each one in a standalone Python script* before writing
   any HTML — print qid → new numbers → computed answer, and sanity-check by hand.
   Never hand-wave a "changed" number without re-solving; a plausible-looking wrong
   answer is worse than an obviously-wrong one.
3. **Reuse the existing template**, don't invent a new look: pull the CSS block and
   the JS logic tail (grading functions, `refreshSummary`, `parseNum`) from an
   existing test-mode file, keep the same fonts/theme vars/typography.
4. **Escape WHY strings.** `WHY` entries are embedded as single-quoted JS string
   literals — any apostrophe in explanatory text ("doesn't hold") will break the
   script. Run every WHY string through an escape helper before interpolating:
   ```python
   def esc(s):
       return s.replace("\\", "\\\\").replace("'", "\\'")
   ```
5. **Diagrams**: see the dedicated section below before writing any SVG.
6. **Validate before publishing** — see Testing checklist below.
7. Publish (Artifact + sync to `worksheets/` + commit + push) — see Publish
   checklist below.

## Splitting a large set into daily files

When a set is too big for one sitting (rule of thumb Hannah has given: ~30
problems/day), split with round-robin distribution over the qids' *natural* order
(page/test order), i.e. `day[i % N]` — not sequential chunks. Sequential chunks
cluster one topic per day (e.g. all geometry on day 3); round-robin mixes topics
every day, which is what was actually asked for both times this came up. Each day
file needs its own `STORAGE_KEY` and its own `TOTAL` count.

## SVG diagrams — the recurring bug class

**Every diagram bug hit in this repo so far has been the same root cause: a
hardcoded pixel offset that doesn't account for actual text width, so a label
clips against the viewBox edge on some (but not all) label lengths.** This has
bitten the same staircase-perimeter diagram twice — fixed narrowly the first time
(one instance), then the identical bug resurfaced in a different problem's
diagram using the same generator function with a different hardcoded margin.

**The fix must be structural, not numeric.** Never hand-tune an x/y offset by
eyeballing one instance. Instead:

```python
def est_w(s):
    return len(s) * 7 + 8  # rough monospace width at font-size ~11px, plus padding
```

Compute every margin that abuts a label (left margin for an `anchor="end"` label,
right margin for `anchor="start"`, top/bottom for `anchor="middle"` labels near an
edge) as `est_w(that_label_text) + padding`, and derive the SVG's `viewBox` width/
height *from those margins*, not the reverse. If a diagram-generating function
takes label text as a parameter, its margins must be a function of that parameter
— that's what makes the fix self-correcting for future label lengths instead of
being a fix for exactly one case.

Second lesson from the prism diagram bug: a diagram can also just be **wrong on
the content level**, not clipped — e.g. a "48 unit cubes" prism that was drawn as
a handful of arbitrary lines, never actually depicting 48 cubes. Before shipping
any diagram, check it actually depicts what the problem states: for a cube-count
diagram, count the grid cells; for a perimeter/shape diagram, sum the edge lengths
via the distance formula and confirm it equals the stated total.

Third lesson, from a composite-solid volume diagram: a diagram can be geometrically
correct yet still **give away the answer's structure**. A composite-prism problem
tests whether the student can look at one fused shape and mentally split it into
the right pieces; a diagram drawn as two already-separated boxes with a "+" between
them does that splitting *for* her, deleting the actual skill being tested. Before
shipping a composite-shape diagram, ask: does this rendering perform any step the
problem is supposed to test (decomposition, identifying which edges are shared,
spotting which face is hidden)? If so, draw the single fused solid instead — join
the pieces into one continuous outline (a dashed internal seam line is fine as a
visual hint, since real textbook figures often show it, but don't render them as
visually separate objects).

## Grading script internals

- `ANSWERS[qid]` is `{type:'num', value:N}` or `{type:'choice', letter:'X'}`.
- `parseNum(raw)` strips `$`, `%`, commas, then extracts the first numeric token.
  **Known limitation**: it cannot parse compound-unit answers like "3 hours and 15
  minutes" — flag this to the user if a new problem's natural answer format is
  compound, rather than silently mis-grading it. (Not yet fixed generally as of
  this writing — ask before spending time on it, it hasn't been requested.)
- `gradeOne(qid)` must locate the card via a generic `[data-qid="..."]` selector,
  not via a selector scoped to per-problem control buttons — test-mode files have
  no per-problem buttons, so a control-scoped selector silently fails to find/clear
  the old grade note, producing duplicate notes on re-grade. Always locate the card
  with `document.querySelector('[data-qid="'+qid+'"]').closest('.card')`.
- When inserting a grade note/badge, insert relative to the actual answer element
  (`box`/`group`), not an `anchor || box` pattern where `anchor` can be null from a
  removed control — that silently no-ops the insert.

## Testing checklist (run before every publish)

1. **JS syntax check** on the extracted `<script>` block: `new Function(scriptText)`
   — catches string-escaping bugs (see WHY escaping above) before they reach a
   browser.
2. **jsdom functional test** — don't just eyeball the HTML:
   ```js
   const { JSDOM } = require('jsdom');
   const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true });
   // fill in an answer, dispatch input/click events, then assert:
   //   - the answer box got class grade-correct/grade-incorrect as expected
   //   - exactly one .grade-note per card even after grading twice
   //   - a diagram's viewBox attribute matches the freshly computed value
   //     (proves the fix landed in the live DOM, not just the source)
   ```
3. Re-verify every changed answer against an independent hand/Python computation,
   not just against what the script says — the script can be self-consistently
   wrong.

## Publish checklist

A worksheet edit isn't done until all of these are true:
1. Artifact published — if updating an existing worksheet, republish to the
   **same artifact URL** (in place), not a new one.
2. File synced into this repo's `worksheets/` directory under a filename matching
   the existing pattern.
3. `README.md` updated if a new file was added (one line describing it) — the
   README already notes: future "missed again" sets should be new files
   (`redo-set-2.html`, etc.), not overwrites of an existing redo set.
4. Committed and pushed to `origin/main`.
5. If GitHub Pages is the delivery link and a build looks stuck ("building"
   indefinitely), force a fresh build:
   `gh api -X POST repos/feielephant/HannahISEEMath/pages/builds`, then poll
   `gh api repos/feielephant/HannahISEEMath/pages/builds/latest --jq '.status'`.
6. Give the user both links (Claude Artifact + GitHub Pages) unless told
   otherwise.

## House rules (from CLAUDE.md, repeated here because they matter for every task)

- Verify any problem fix against the actual source photo in `photos/`, never
  against a possibly-paraphrased memory of it.
- A fix to a shared problem touches up to 3 files (full-workbook answer key +
  both rework worksheets) — grep for the qid/text across all three.
- Keep the existing type/color system (Petrona / Public Sans / JetBrains Mono,
  teal accent, light+dark via CSS vars) — don't introduce a new visual identity
  per worksheet.
- This repo contains a minor's schoolwork/name — don't change repo visibility or
  add more of her photos without asking first.
