# Screenshot Reorg — Handoff (paused 2026-10-25)

Paused to grade Hannah's latest QR test. This doc has everything needed to resume the screenshot-organization project without re-deriving context.

## What this project is

Four folders under `~/Documents/HannahISEEMath/` hold raw screenshots that feed `problem-library/problem_library.json` (and `ma_library.json`). The goal: every screenshot should be (a) cataloged as a library item with real question text/choices/answer, and (b) physically organized into a folder that reflects what it is — not sitting loose in a folder root.

## Status by folder (as of 2026-10-25)

| Folder | Total .png | Cataloged | Not yet scanned | Organized? |
|---|---|---|---|---|
| `mathspeed test/` | 755 | 754 | 1 | **Done** — fully reorganized into `by-topic/`, `actual-practice-tests/`, `dashboard-menus/`, `superseded-by-recapture/` |
| `recaptureQR/` | 238 | 224 | **14** | Partially — the 190 files belonging to the 5 real tests were moved out (see below); the rest (topic-bank items + the 14 new ones) are still sitting loose in `recaptureQR/` root |
| `ISEEMathAchievement/` | 208 | 206 | 2 | **Not organized** — 206 already cataloged but never physically moved out of this folder |
| `ISEEcomputer/` | 274 | 0 | **274** | **Untouched** — never scanned at all. Dated Aug 30 (earliest/oldest batch of all 4 folders). Has subfolders `0913ISEE`, `0905ISEE`, `ISEEMathAll` not yet looked inside. Unknown whether this is even still-relevant content or an old abandoned capture batch — worth asking the user what this folder actually is before investing scan time. |

## What was completed this session

### 1. `mathspeed test/` full reorg (13 batches, commits `fcaa156`..`41a8e08` and earlier)
Moved all 390 originally-loose root files into `by-topic/<topic name>/`, `actual-practice-tests/<test>/`, or `dashboard-menus/`. Along the way:
- Pixel-verified 5 number-line items (gid818-822) and 10 bar-graph conclusion items (gid868-877) — filled in previously-null `correct_letter`, saved diagram crops to `~/Documents/HannahISEEMath/problem-library-diagrams/` (non-git location — **the repo's `.gitignore` excludes `*.png`**, never save crops inside the repo).
- Pixel-counted 3 half-icon pictograph items (gid948/950/951), caught and fixed a real miscount (gid950: O'Hare's planes were 12, not the stored "about 11").
- Fixed 2 instances of a same-time-different-date file-mixup bug (substring time-matching across different dates grabbed the wrong file).

### 2. Real-test recapture consolidation (commits `62b1567`, `00b45ed`, `8ce42ae`, `359c282`, `fd9ed45`)
For each of the 5 real tests (What to Expect, ISEE Lower #1-4), moved that test's fuller `recaptureQR` screenshots (190 files total) into `mathspeed test/actual-practice-tests/<test>/`, updating each item's `recapture_source_images` path. Confirmed **no timeline/time-allocation screenshot was ever captured for any of the 5 tests** in `recaptureQR` — not just "What to Expect."

Along the way, found and fixed **6 duplicate catalog entries**: an earlier ad-hoc "recaptureQR 2026-10-09 cataloguing" pass had re-cataloged several cryptarithm/symbol-equation puzzle questions (the shape-variable ones: △○□◇) as new items without noticing they already existed in the library under the original Oct-2 screenshot capture. Each duplicate was flagged `needs_dedup_review: True` — **that field is the reliable signal for finding more of these if any remain elsewhere in the library.** Pattern: merge the duplicate's `official_solution`/`choice_percentages`/`source_images` into the original entry (which has the full schema: `topic_broad`, `status`, `set_date`, etc.), then delete the duplicate's global_id entry entirely.

Fixed pairs: gid84/1206, gid145/1207, gid149/1208, gid157/1209, gid162/1210, gid167/1211.

Also found and cleaned one stray reference: gid184 had a `recapture_source_images` entry pointing to a second, redundant full-recapture screenshot from a different occasion (Oct 2, 10:20 PM, sitting in `superseded-by-recapture/`) rather than the standard Oct 9 session — dropped the stray reference, left the file in place.

## Key conventions / gotchas to remember

- **Narrow space in filenames**: macOS screenshot filenames use U+202F (narrow no-break space) between time and AM/PM, e.g. `Screenshot 2026-10-09 at 8.55.00␟PM.png`. The *stored* `source_file`/`recapture_source_images` paths in the library use a regular space instead (established convention — don't "fix" this, it's intentional and consistent). When moving files or checking existence, always normalize: `.replace(' ',' ').replace(' ',' ')`.
- **Diagram crops**: save to `~/Documents/HannahISEEMath/problem-library-diagrams/` (outside the repo — `.gitignore` excludes `*.png` repo-wide). Reference via a `diagram_image` field.
- **Pixel-precision rule**: only pixel-measure a diagram if it's a genuine plot (number line, bar/line graph, coordinate grid) where a value is encoded spatially. Labeled shapes, pictographs with an explicit "icon = N" key, and tables have exact values in text already — verify those via independent math recomputation against the answer choices instead, much faster and usually sufficient.
- **Date-collision bug**: any script matching files by time-of-day substring (e.g. "10.16.54") can silently grab the wrong file if two different dates share that exact time. Always match on full date+time, or verify counts/collisions after any bulk move.
- **`needs_dedup_review: True`** is the breadcrumb from the earlier ad-hoc recaptureQR cataloging pass — any remaining items with this flag (search the full `problem_library.json`) are candidates for the same merge-and-delete treatment described above. Worth a full-library sweep for this flag before considering the recaptureQR consolidation fully done.
- Validate JSON + verify files exist on disk before every commit; commit scoped to one logical unit (one batch, one test, one fix) with a descriptive message; push after each commit, same pattern as `feedback_worksheet_qa` memory's "push both repos" habit.

## Next step when resuming

User was about to choose between: (a) scan the 14 new `recaptureQR` files (small, recent, Oct 10-24 — likely tied to ongoing QR review work), (b) investigate what `ISEEcomputer/` actually is before committing to scanning its 274 files, or (c) both. No decision was made before pausing — ask again when resuming, the `ISEEcomputer` folder in particular needs a "what is this and is it still relevant" check before diving in.
