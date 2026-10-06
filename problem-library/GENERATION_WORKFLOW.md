# Speed-Training Set Generation — Workflow

Purpose: generate 38-problem Quantitative Reasoning practice sets (matched to the real test's difficulty and topic mix) for Hannah, rotating topics so strong skills keep getting practice and weak ones get targeted.

## Files (all in problem-library/)
- `problem_library.json` — ~757 real questions from 8 full tests, drills, and dashboards (source of examples and topic/difficulty context)
- `student-tracker.json` — Hannah's gaps, habits, wrong-rates, and priorities (update after each set is graded)
- `practice-log.json` — every set generated so far, with its topic list (written by plan_set.py)
- `problem-library-banks.json` — the platform's Easy / Medium / Hard bank titles
- `plan_set.py` — makes the next 38-slot plan (tier mix + rotation + per-topic cap)

## Real test profile (from 8 full tests, 392 questions)
- Format: 38 problems, 35 minutes, four choices A–D, Quantitative Reasoning
- Difficulty mix (topic-matched): ~28% Easy, ~53% Medium, ~16% Hard (+ ~3% unmatched)
- Most frequent real topics: Translating Math Expressions (8/8 tests), Converting to a Decimal (8/8), Angles in Triangles (7/8), Area of Triangles (7/8)

## Steps for each new set
1. Run `python3 plan_set.py` in problem-library/ — it prints the 38-slot plan and appends to practice-log.json.
2. For each slot, write one NEW problem on that topic and tier. Use real examples from problem_library.json as the model (same wording style, same number of steps), but fresh numbers and scenario. Never copy a real question verbatim.
3. Check every problem by solving it. Build the answer key from the solved values, not from memory. Make distractors reflect her habit traps (for example, a "NOT" question with an equivalent answer as the trap; a percent-change question with the +10%/−10% cancel trap).
4. Build the worksheet (no answers shown) and a separate answer key. Add a 35-minute timer.
5. After she takes the set, grade it and update student-tracker.json: wrong counts per topic, last practiced, and any new habit evidence.

## Set-shape rules (added 2026-10-02)
- Answer letters: balanced A/B/C/D (10/10/9/9 across 38), no three identical letters in a row. The planner assigns them.
- Difficulty: a soft ramp, not a rule. Real tests show Hard share ~5–9% in the first half and ~17–21% in the second. The planner places ~2 Hard slots in the first half and ~5 in the second; Easy and Medium shuffle freely.
- Diagrams: about 55% of real questions include a diagram, chart, or table, so ~21 of 38 slots are diagram slots. Build the diagram as an inline SVG or table in the same style as the real test (bar graph, number line, shaded figure, composite shape), not as a text description.
- Each slot carries a reference (wrong_so_far, graded_so_far, times_practised_before, last_practised_set). Mention the relevant habit and gap in the answer key so she sees why each problem is there.

## Pacing rule (added 2026-10-06)
- Questions 31–38 of the official 38-question tests are pacing-affected (rushed answers, error rate 41% vs 10% for Q1–30). The library marks these pacing_affected=true.
- Exclude pacing-affected items from topic gap counts. Track pacing separately (tracker "pacing" block).
- Speed sets: include full timed sections, and practise the last third under time pressure.

## Targeting rule
- High-priority topics appear more often; "maintain" topics appear at least once every 3 sets so strong skills don't fade.
- No topic appears more than 3 times in one set.
- Only mark a habit as her weakness after evidence from her own answers (graded practice or screenshots), not from a single guess.

## Caveats
- Tier labels come from topic-to-bank matching, so they are estimates.
- Some platform banks have no real examples yet (for example, Unit Conversion with Made Up Units); their problems are generated, not copied.
