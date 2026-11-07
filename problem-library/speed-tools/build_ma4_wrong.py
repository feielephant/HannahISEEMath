"""MA Set 4 wrong problems (2026-11-06), parent request: the same 9 problems she missed on 11/6,
unchanged, so the parent can work them with her and find where each gap is. The answer key shows
her answer, what it most likely came from, and one question to ask her."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
M = {p['n']: p for p in json.load(open(os.path.join(HERE, 'ma4_problems.json')))}

# MA4 number: (her final answer, what it likely came from, question to ask her)
WRONG = {
 8: ('B', '8 multiplied only the 6, not both numbers in the parentheses',
     'What does the 8 multiply? Can you write 8 &times; (6 &minus; 3) without parentheses?'),
 13: ('B', 'subtracted the percents: 50 &minus; 20 = 30',
      'Start with $100. What is the price after each change?'),
 15: ('D', 'turned "&#9651; more than" into minus &#9651;',
      'Try &#9633; = 10, &#9675; = 3, &#9651; = 5. How many does Ben have now? Before Ava gave him some?'),
 17: ('A', 'took the 1/2 from the formula and left out the base',
      'Put base = 10 into the formula. What is A when the height is 2? When it is 4?'),
 18: ('A', 'stopped one step early: 112 is the jump from the 9th to the 25th, not the 25th number',
      'What does 112 stand for? What does the question ask for?'),
 24: ('D', 'added the shells LOST (10) instead of the shells left (5)',
      'Point to the number of shells he still has.'),
 25: ('D', 'found the 6th number (35), then doubled 35 instead of doubling the difference',
      'Write the differences under the numbers. What is the next difference?'),
 27: ('B', 'no clear source for 27 (maybe 42 &minus; 15)',
      'How did you get 27? Draw one box for basketball, then football, then soccer.'),
 28: ('B (first picked D, then changed)', 'had it right, then changed to multiplying 2,000 &times; 1,000',
      'Why did you change from D? What does the total number of words mean?'),
}
P = []
for i, k in enumerate(sorted(WRONG), 1):
    her, why, ask = WRONG[k]
    p = M[k]
    assert p['correct'] != her[0] or k == 28
    P.append(dict(n=i, topic=p['topic'], q=p['q'], diagram=p['diagram'], choices=p['choices'], correct=p['correct'],
                  key=p['key'] + f'<br><b>Ask her:</b> {ask}',
                  ref=f'MA Set 4 #{k} &middot; Her answer on 11/6: {her} (correct {p["correct"]}) &middot; Likely: {why}'))
assert len(P) == 9
json.dump(P, open(os.path.join(HERE, 'ma4_wrong_problems.json'), 'w'), ensure_ascii=False, indent=1)
print(len(P), [p['correct'] for p in P])
