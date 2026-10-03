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

## Targeting rule
- High-priority topics appear more often; "maintain" topics appear at least once every 3 sets so strong skills don't fade.
- No topic appears more than 3 times in one set.
- Only mark a habit as her weakness after evidence from her own answers (graded practice or screenshots), not from a single guess.

## Caveats
- Tier labels come from topic-to-bank matching, so they are estimates.
- Some platform banks have no real examples yet (for example, Unit Conversion with Made Up Units); their problems are generated, not copied.
