# QR8 Planning Notes (written 2026-10-25, before building)

Not yet built — `plan_set.py` has NOT been run (practice-log.json still has 7 QR sets). Sequencing per parent's instruction: finish the library cleanup first (see `SCREENSHOT_REORG_HANDOFF.md`), since it may surface more real `not_done` items or fix mistagged `official_topic`s that would directly improve QR8's slot-filling — then come back and build with the updated library.

## Readiness check run 2026-10-25 (before pausing)

**`check_coverage_pace.py`**: 5 full practice weeks left before the Dec 10 test (10 more QR sessions, 5 more MA sessions). **38 topics have zero data ever** — not in any graded or queued set. Full list was printed in-session; rerun the script fresh when resuming rather than trusting this snapshot, since the library cleanup may change tracker-visible topic coverage.

**`check_priority_staleness.py`**: 4 topics flagged for high wrong rate, worth escalating:
- Split Line Segments — 2/2 wrong (100%), priority currently `low`
- Cryptarithm / digit substitution — 4/5 wrong (80%), priority currently `medium`
- Solving Problems with Geometric Formulas — 4/8 wrong (50%), priority currently `medium`
- Input Output Tables — 1/2 wrong (50%), priority currently `unknown`

## Findings from QR7's grading (2026-10-25) that should directly shape QR8

1. **Cryptarithm borrowing/regrouping gap, confirmed with Hannah** (speed-set-7 #4): she can misread which letter is asked (M vs N), and separately has a real gap in recognizing a borrow/regroup is needed in a subtraction cryptarithm (MNN − MM = 745 style) to get from one letter's value to the other's. QR8 should include a cryptarithm item that specifically requires this borrow step — not just another letter-identification trap. See [[project]] — matches the staleness flag above (4/5 wrong).

2. **Write-it-down gap, confirmed across 4 manifestations** (see `feedback_write_it_down_gap` memory): equation substitution (geometric formulas), multi-step unit conversion, ordering 3+ values, sequence differences. This is a technique gap, not purely content — but QR8 should still test these same topics on genuinely novel numbers (not the mental-math-combo-4 drill content) to see whether the technique generalizes under real-test conditions, where she can't rely on a UI forcing the written step.

3. **Order-three gap recurring, refined**: specifically ordering **more than 2** values breaks down (she compares 2 fine). QR8's ordering item (if any) should use 3-4 values, not 2.

4. **Worksheet formatting bug found and must not recur**: #15 ran two equations together on one line, misread as a doubled symbol. **Any QR8 problem with 2+ equations must put each on its own line** — this is now a standing convention, see `feedback_equations_separate_lines` memory.

## Open question for after the library cleanup

Once `recaptureQR`'s remaining 14 files and (if in scope) `ISEEcomputer`'s 274 files are scanned, re-check whether any of the 38 never-tested topics or the 4 staleness-flagged topics above now have a usable `not_done` real item that wasn't visible before — pulling a real item is always preferred over inventing (see `GENERATION_WORKFLOW.md`'s done/not-done rule). Also re-run `check_coverage_pace.py` fresh at that point, since newly-cataloged items could change which topics are flagged as zero-data.
