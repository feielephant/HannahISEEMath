# Screenshot Reorg — Handoff (paused 2026-10-25)

Paused to grade Hannah's latest QR test. This doc has everything needed to resume the screenshot-organization project without re-deriving context.

## What this project is

Four folders under `~/Documents/HannahISEEMath/` hold raw screenshots that feed `problem-library/problem_library.json` (and `ma_library.json`). The goal: every screenshot should be (a) cataloged as a library item with real question text/choices/answer, and (b) physically organized into a folder that reflects what it is — not sitting loose in a folder root.

## Status by folder (as of 2026-10-25)

| Folder | Total .png | Cataloged | Not yet scanned | Organized? |
|---|---|---|---|---|
| `mathspeed test/` | ~800 (grew via moves in) | all | 0 | **Done** — fully reorganized into `by-topic/`, `actual-practice-tests/`, `dashboard-menus/`, `superseded-by-recapture/` |
| `recaptureQR/` | 0 | n/a | n/a | **Done** — root fully emptied (including the `_no_header_bar` subfolder, confirmed empty). Everything moved into `mathspeed test/by-topic/` or `actual-practice-tests/`; 47 duplicate/unreliable entries removed (see below) |
| `ISEEMathAchievement/` | 208 | 206 | 2 | **Not organized** — 206 already cataloged but never physically moved out of this folder. **Next up.** |
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

## Session 2 findings (2026-10-25, after grading speed-set-7)

Investigated the 14 unscanned `recaptureQR` files (dated Oct 10, 17, 18, 24). Findings:
- **5 are our own dev/QA screenshots** (joined-prism volume diagram, an unlabeled grid/U-shape figure, a live-site zoom of speed-set-3.html) — not real content, nothing to catalog. Destination undecided — leave in place, move to a dev-screenshots holding folder, or delete (ask the user).
- **8 are "How you allocated your time" timing graphs**, captured Oct 18 ~8:51-8:53 PM in one browsing session going through all 4 ISEE Lower tests in order. One per test's QR section (38 questions) plus — for #1, #2, #4 — a second 30-question section (not yet confirmed which, but an already-cataloged item elsewhere labels a matching one "Mathematics Achievement Summary page", so probably MA). None found for "What to Expect" or Lower #3's 30q section in this particular 8-file batch.
  - **Important correction to this doc's earlier claim**: "no timeline screenshot was ever captured for any of the 5 tests" is WRONG for Lower #1/#2/#3/#4 — these 8 files are exactly that, just captured later (Oct 18) in a separate session, not during the original Oct 9 recapture. Only "What to Expect" still has no timeline screenshot found anywhere.
  - **Sep 20 vs Sep 25 red herring, resolved**: two of the 8 files show "Completed on 09/20/2026" with no visible header, which looked like a never-cataloged 6th test. It isn't — an already-cataloged item (`Screenshot 2026-10-06 at 10.41.35 AM.png`, `"type": "timing"`, `"test_set": "ISEE LOWER #3"`) already documented that this test's header reads "Sep 25, 2026" but its footer reads "Completed on 09/20/2026" — a platform date discrepancy, not a different test. So both Sep-20 files are Lower #3's QR section.
  - That Oct-6 item is evidence of a **different existing cataloging pattern** worth reusing: `"type": "timing"` entries with `test_set`, `is_timing_chart: true`, and a `diagram_description` summarizing the chart (pause point, red-bar positions, subtype breakdown) instead of the normal question/choices/answer schema. Follow this pattern when cataloging the 8 new timing screenshots, not the standard question-item schema.
  - Not yet done: actually write the 8 new catalog entries and move all 8 files into the correct `actual-practice-tests/<test>/` folders.

## Agreed plan for resuming (confirmed with user 2026-10-25)

1. **DONE.** The 14-file batch is fully resolved (commits for the dev-screenshot move and `4bac7eb` for the timing catalog): 6 were our own dev/QA screenshots (5 diagram-rendering checks + 1 more found late, a cube-views check from Oct 24 — almost certainly QR7 authoring, since "Views of 3D Figures" is a QR7 topic) — all moved to `~/Documents/HannahISEEMath-dev-screenshots/` (outside both repos, not git-tracked, for the user to review later). The other 8 are timing-graph screenshots for Lower #1-4, cataloged with `global_id` 1437-1444 using the `"type": "timing"` pattern, moved into their correct `actual-practice-tests/<test>/` folders. **Gotcha hit and fixed**: the first catalog-write attempt stored `source_file` with the narrow-space character still in it (U+202F), breaking the stored-path convention (regular space) — caught by the existence-check failing, fixed by normalizing all 8 paths before re-verifying. `recaptureQR/` root is now down to 224 files, all already-cataloged standalone items awaiting step 3's reorg.
2. **DONE.** Full-library sweep for `needs_dedup_review: True` (and separately, for the underlying note text in case a flag was missed): zero remaining in either library, across all 6 already-fixed pairs (gid84/1206, gid145/1207, gid149/1208, gid157/1209, gid162/1210, gid167/1211). Nothing more to find here.
3. **DONE.** Organized all of `recaptureQR`'s already-cataloged items into `mathspeed test/by-topic/` folders across 7 batches (commits `d22a4f3`, `588b504`, `cfdbf19`, `7b4d098`, `693e94a`, `727c4f6`, `86bfbec`) -- ~25 new topic folders created, several consolidating minor "#1/#2/##1" naming variants of the same bank into one folder. **Found and fixed a second, larger duplicate problem mid-cleanup** (commit `4d6475f`): 47 items (gid 1258-1426) were a wholesale second ad-hoc cataloging pass that fully duplicated an earlier pass (gid 986-1257ish) -- every one had a lower-id duplicate, and several had **fabricated content** that didn't match their claimed source screenshot when spot-checked (confirmed by viewing the actual image, e.g. gid1304 claimed "a science class... planetarium" when the real screenshot showed "a history class... Civil War battlefield," matching the correct lower-id duplicate gid1078). Removed all 47 from `problem_library.json` (backed up, not deleted -- `~/Documents/HannahISEEMath-dev-screenshots/removed_duplicate_catalog_entries_1258-1426.json`). `recaptureQR/` root (including its empty `_no_header_bar` subfolder) is now fully empty -- every file organized, nothing left to scan.
4. **`ISEEMathAchievement/`**: organize its 206 already-cataloged items into folders, scan the 2 genuinely unscanned ones.
5. **`ISEEcomputer/`**: 274 files, completely untouched — investigate what this folder actually is (subfolders `0913ISEE`, `0905ISEE`, `ISEEMathAll`, dated Aug 30 — earliest of all 4 folders) before committing to a full scan.

This cleanup is explicitly a prerequisite the user wants finished before building QR8 — see `QR8_PLAN.md`, which has the readiness-check findings (coverage-pace gaps, priority-staleness flags, fresh findings from speed-set-7's grading) and is waiting on this cleanup to potentially surface more real `not_done` items or fix more mistagged topics first.
