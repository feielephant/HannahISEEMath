# Speed-Practice Worksheet Spec

Use this every time a new speed set is built, so every set has the same features.

## Files
- `plan_set.py` — makes the 38-slot plan (tier mix, rotation, letter balance, diagram slots, difficulty pattern). Reads ../student-tracker.json, ../problem-library-banks.json; logs to ../practice-log.json.
- `build_set1.py` — example of writing the problems for a plan: one dict per slot with q (question), ch (4 choices), diag (optional SVG/table), why (answer explanation). Then checks the correct value sits at the planned letter (reorder choices if not).
- `render_set1.py` — renders the worksheet and the answer key HTML from the problem list.
- Output goes to worksheets/speed-set-N.html (worksheet, GitHub Pages) and worksheets/speed-set-N-answer-key.html (key, not linked from the worksheet).

## Rules for the problems
- 38 problems, four choices A–D, letters balanced 10/10/9/9, no three identical in a row.
- 11 Easy, 20 Medium, 7 Hard. Hard slots: about 2 in the first half, 5 in the second.
- About 21 of 38 have a diagram (inline SVG or table). Diagrams should match the real test's style.
- Fresh numbers and wording: never copy a real question. Keep the same concept and trap.
- Each answer is checked by solving it, and the correct choice sits at the planned letter.
- Each key entry shows the answer, a short "why", the tier, the topic, and the history (times practised before, wrong so far).
- Put the slow-problem types and her gaps from the tracker into the plan (see workflow doc).

## Worksheet features (every set)
1. Sticky top bar: a 35:00 countdown with Start (greyed out while running) and Reset (asks to confirm). The remaining time is saved in localStorage so refreshing keeps it running. Also an "Answered: n / 38" counter.
2. Choices are buttons. Clicking a choice selects it; clicking the selected one again clears it. Picks are saved in localStorage.
3. Each answered problem shows its time beside its number (seconds from the previous answer click).
4. A Timing panel at the top: total time, answered count, a table of time and answer per problem, a "Download times (CSV)" button, and a "Clear all answers" button (confirms first).
5. Copy, cut, right-click, select, and drag are blocked on the worksheet, except the CSV button.
6. No answers or explanations in the worksheet HTML. The answer key is a separate page and is not linked from the worksheet.

## Steps
1. Run plan_set.py to get the 38 slots.
2. Write the problems (build_set1.py pattern), check letters, and fix the order.
3. Render (render_set1.py pattern), then copy both HTML files to worksheets/ and push.
4. After she takes the set, get the CSV and her answers, grade against the key, update student-tracker.json, and record the set in practice-log.json.

## Selection criteria (required for every set)
1. **Coverage:** every topic in the tracker should appear across recent sets. Use the planner's rotation so no topic goes unpractised for long, and include the new topics (net type, estimation banks, remaining-amount fractions).
2. **Focus on weak spots:** prioritise topics she gets wrong and problems that took her longer (from the tracker, the timing charts, and her CSV times). Multi-step, constraint-based, fraction-comparison, pattern, and relationship problems come first. Her late-test pacing is handled by timed sections, not by excluding topics.
