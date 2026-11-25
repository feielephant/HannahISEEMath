"""Vacation Day 2 (built 2026-11-24, parent request after Day 1, 4/7):
- drop the 4 she got right on Day 1 (percent, rectangle chain, a/b x c estimate, probability) -- rested, to come back
  later in rotation to confirm;
- keep the 3 Day 1 gaps (cube scaling, story -> expression, multiples of two numbers) with a different story,
  different language and different numbers; carry #7 rules box (not scored on Day 1: my missing-rules-box bug);
- add 4 more open topics, each with a REAL last-third miss and not secured (no 3 right in a row since):
  prediction from a table, composite-figure perimeter, joined prisms, number pattern;
- every problem information-heavy (a large table, a figure with many labels, or extra facts to read past),
  multi-step, with the stop-early number among the choices; wrong choices tagged by cause.
Every math claim is asserted."""
import json, os, sys, re
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from joined_prism_diagram import joined_prisms_svg
T = {x['topic'] for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}

def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def rules_box(*rules):
    return ('<div style="border:1.5px solid currentColor;border-radius:6px;padding:8px 12px;max-width:340px"><div style="font-weight:700;margin-bottom:4px">RULES FOR THE NEW NUMBER</div>'
            + ''.join(f'<div>{i}. {r}</div>' for i, r in enumerate(rules, 1)) + '</div>')

P, MAP = [], {}
# her record per topic (wrong / all tries, real tests + our sets + Vacation Day 1), 11/24
TOT = {'Patterns in Data Tables and Lists': '1/2 (same build: Lower 2 QR #34, MA6 #5)', 'Comparing Volume of Cubes': '6/14',
       'Translating Math Expressions': '6/20', 'Area and Perimeter of Complex Polygons': '5/17', 'Numerical Patterns': '8/29',
       'Counting Multiples within a Range': '5/11', 'Volume of Solids': '2/5', 'Value of Digits': '4/15'}
def add(topic, q, ch, right, tags, asks, key, built_on, last, vs, diagram=None):
    assert topic in T, topic
    assert len(set(ch)) == 4 and right in ch and set(tags) == set(ch) - {right}, (ch, tags)
    assert any(v.startswith('Stopped early') for v in tags.values()) or topic == 'Value of Digits', topic
    ans = 'ABCD'[ch.index(right)]
    n = len(P) + 1
    tagline = ' &middot; '.join(f'<b>{"ABCD"[ch.index(c)]}</b>: {v}' for c, v in tags.items())
    P.append({'n': n, 'tier': 'Hard', 'topic': topic, 'q': q, 'choices': dict(zip('ABCD', ch)), 'correct': ans,
              'key': f'<b>Answer: {ans}.</b> <i>The question asks for: {asks}.</i> {key} <br>Wrong choices: {tagline}',
              'ref': f'Topic: {topic} &middot; Built on: {built_on} &middot; Her record (oldest &rarr; newest): <b>{last}</b> &middot; Compared with the real one: {vs}',
              'diagram': diagram, 'gid': None, 'ma_idx': None,
              'tags': {'ABCD'[ch.index(c)]: v for c, v in tags.items()}})
    MAP[n] = dict(topic=topic, built_on=built_on, source_third='last', last5=last, counted='', comparable_wrong=TOT[topic],
                  vs_latest=vs, asks=asks, stop_early=['ABCD'[ch.index(c)] for c, v in tags.items() if v.startswith('Stopped early')])

# 1 NEW prediction from a large table, two groups compared (Lower 2 QR #34: one group, next 25; she missed it)
votes = {'Zoo': 22, 'Museum': 14, 'Aquarium': 26, 'Science center': 10, 'Park': 8}
tot = sum(votes.values())
aq, mu = F(votes['Aquarium'] * 40, tot), F(votes['Museum'] * 40, tot)
assert tot == 80 and aq == 13 and mu == 7 and aq - mu == 6 and votes['Aquarium'] - votes['Museum'] == 12
add('Patterns in Data Tables and Lists',
    'The table shows how a group of students voted for the place they most want to visit on a class trip. Based on the information in the table, what is the most reasonable prediction of how many more of the next 40 students will vote for the aquarium than for the museum?',
    ['6', '7', '12', '13'], '6',
    {'7': 'Predicted the museum only', '12': 'Known trap: subtracted the table counts (26 &minus; 14), no prediction', '13': 'Stopped early: this is the aquarium prediction only'},
    'how many more (aquarium &minus; museum)',
    'First the total, which is not given: 22 + 14 + 26 + 10 + 8 = 80. 40 is half of 80, so each prediction is half the count: aquarium 13, museum 7. 13 &minus; 7 = 6.',
    'Lower 2 QR #34 (last third, 56.3% right, her miss): votes table, predict one color out of the next 25',
    'x o', 'Harder: 5 rows, total not given, two predictions and a difference',
    table(['Place', 'Number of Votes'], [[k, v] for k, v in votes.items()], 'CLASS TRIP VOTES'))

# 2 KEPT GAP cube scaling, new story + language: "same total volume" (Day 1: she tripled the volume, not the edge)
edges = {'Small': 3, 'Medium': 6, 'Large': 9}
vs_, vl = edges['Small']**3, edges['Large']**3
assert vl // vs_ == 27 and vl % vs_ == 0 and vl == 729 and 9 // 3 == 3 and (9 // 3)**2 == 9
add('Comparing Volume of Cubes',
    'A store sells gift boxes shaped like cubes. The table shows the edge length of each size. How many Small boxes together have the same volume as one Large box?',
    ['3', '9', '27', '729'], '27',
    {'3': 'Known trap (Day 1 #2): compared the edges only (9 &divide; 3)', '9': 'Compared one face only (3 &times; 3)', '729': 'Stopped early: this is the volume of the Large box'},
    'how many Small boxes',
    'The Large edge is 3 times the Small edge (9 &divide; 3). Volume grows in all three directions: 3 &times; 3 &times; 3 = 27. Check: Large = 9 &times; 9 &times; 9 = 729, Small = 3 &times; 3 &times; 3 = 27, and 729 &divide; 27 = 27. The Medium row is extra information.',
    'Lower 4 QR #36 (last third, 48.2% right, her miss): Cube B is 5 times as wide, how many A\'s fit; Lower 5 QR #38 (39.6%, her miss)',
    'o o o x o x', 'Same idea as the real one in new words ("same total volume"), with an extra row in a table',
    table(['Box size', 'Edge length'], [[k, f'{v} inches'] for k, v in edges.items()], 'GIFT BOXES'))

# 3 KEPT GAP story -> expression, new story; now the GIVER is asked (Day 1 / MA6 #15 asked the receiver; she stopped at "now")
add('Translating Math Expressions',
    'Mr. Lee had &square; books on his shelf. Ms. Diaz gave him &#9675; books from her shelf. Now Ms. Diaz has &#9651; fewer books than Mr. Lee has. Which expression represents the number of books Ms. Diaz had at first?',
    ['&square; + &#9675; &minus; &#9651; + &#9675;', '&square; + &#9675; &minus; &#9651;', '&square; &minus; &#9651; + &#9675;', '&square; + &#9675; &minus; &#9651; &minus; &#9675;'],
    '&square; + &#9675; &minus; &#9651; + &#9675;',
    {'&square; + &#9675; &minus; &#9651;': 'Stopped early: this is how many Ms. Diaz has NOW',
     '&square; &minus; &#9651; + &#9675;': 'Forgot Mr. Lee got &#9675; more books before comparing',
     '&square; + &#9675; &minus; &#9651; &minus; &#9675;': 'Went the wrong way in time: took the gift away again instead of giving it back'},
    'Ms. Diaz, at first',
    'Timeline (before | gift | now). Now Mr. Lee has &square; + &#9675;. Ms. Diaz has &#9651; fewer: &square; + &#9675; &minus; &#9651;. Before she gave away &#9675; books she had &#9675; more: &square; + &#9675; &minus; &#9651; + &#9675;.',
    'Lower 4 QR #35 (last third, 47.4% right, her miss); Lower 1 QR #33 (54.4%, her miss)',
    'x o o o x x', 'Same timeline idea as the real one; asks about the giver, "fewer than" instead of "times as many"')

# 4 NEW composite figure perimeter, shared side (Lower 1 QR #38, 33.8% right, her miss)
whole, sq = 30, 24
s = sq // 4
two_slants = whole - 3*s
tri = two_slants + s
assert s == 6 and two_slants == 12 and tri == 18
fig4 = ('<svg viewBox="0 0 260 230" width="260" height="230" role="img">'
        '<polygon points="80,100 130,30 180,100" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<rect x="80" y="100" width="100" height="100" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<text x="130" y="80" font-size="14" text-anchor="middle" fill="currentColor">triangle</text>'
        '<text x="130" y="155" font-size="14" text-anchor="middle" fill="currentColor">square</text></svg>')
add('Area and Perimeter of Complex Polygons',
    'A sign is made of a square and a triangle that share one side, as shown. The two slanted sides of the triangle are the same length. The perimeter of the whole sign is 30 inches. The perimeter of the square alone is 24 inches. What is the perimeter of the triangle alone?',
    ['12 inches', '18 inches', '24 inches', '30 inches'], '18 inches',
    {'12 inches': 'Stopped early: this is only the two slanted sides', '24 inches': 'Gave the square\'s perimeter', '30 inches': 'Gave the whole sign\'s perimeter'},
    'perimeter of the triangle alone',
    'Square side = 24 &divide; 4 = 6. The outside of the sign has 3 square sides (18) and the 2 slanted sides, so the slanted sides add to 30 &minus; 18 = 12. The triangle alone also has the shared side: 12 + 6 = 18.',
    'Lower 1 QR #38 (last third, 33.8% right, her miss): largest polygon 20, square 16, triangle?; Lower 6 QR #30 (69.5%, her miss)',
    'x o o o x o', 'Same build as the real one with a story and new numbers', fig4)

# 5 NEW number pattern in a table, two steps past the data (Lower 1 MA #21: 2 3 5 9 17 next; MA6 #19 her miss)
mem = [3, 4, 6, 10, 18]
d = [b - a for a, b in zip(mem, mem[1:])]
m6 = mem[-1] + 2*d[-1]; m7 = m6 + 4*d[-1]
assert d == [1, 2, 4, 8] and m6 == 34 and m7 == 66 and mem[-1] + d[-1] == 26 and 2*mem[-1] == 36
add('Numerical Patterns',
    'The table shows the number of members in a chess club at the end of each month. The number of members keeps growing in the same pattern. How many members will the club have at the end of Month 7?',
    ['26', '34', '36', '66'], '66',
    {'26': 'Known trap: added the last jump (8) again', '34': 'Stopped early: this is Month 6', '36': 'Doubled the last number'},
    'members at Month 7',
    'Look at the jumps: +1, +2, +4, +8. Each jump doubles, so the next jumps are +16 and +32. Month 6: 18 + 16 = 34. Month 7: 34 + 32 = 66. Write the jumps under the table before answering.',
    'Lower 1 MA #21 (last third, 67.1% right, her miss): 2, 3, 5, 9, 17, next?',
    'o o o o o x', 'Harder: same doubling jumps, in a table, and two steps past the data',
    table(['Month', '1', '2', '3', '4', '5', '6', '7'], [['Members'] + [str(x) for x in mem] + ['?', '?']], 'CHESS CLUB MEMBERS'))

# 6 KEPT GAP multiples of two numbers, story (Day 1: counted multiples of 9 only; MA6: used 4 x 6)
both = [p for p in range(1, 201) if p % 4 == 0 and p % 10 == 0]
assert len(both) == 10 and len([p for p in range(1, 201) if p % 40 == 0]) == 5 and len([p for p in range(1, 201) if p % 4 == 0]) == 50
add('Counting Multiples within a Range',
    'Lena has a notebook with pages numbered 1 to 200. She puts a star on every 4th page (page 4, 8, 12, and so on) and a heart on every 10th page (page 10, 20, 30, and so on). She also puts a dot on every page that is a multiple of 3. How many pages have both a star and a heart?',
    ['5', '10', '20', '50'], '10',
    {'5': 'Known trap (MA6 #27): used 4 &times; 10 = 40 instead of the LCM', '20': 'Stopped early: this is the LCM (every 20th page), not how many', '50': 'Counted the stars only (Day 1: counted one number only)'},
    'how many pages',
    'A page with both is a multiple of 4 AND of 10. The smallest such page is 20 (the LCM), so the pages are 20, 40, ..., 200. 200 &divide; 20 = 10 pages. The dots are extra information.',
    'Lower 5 MA #29 (last third, 63.7% right, her miss, 134 s): between 65 and 85, divisible by 3',
    'o o o o x x', 'Harder: two numbers (LCM step) in a story, with extra information')

# 7 NEW joined prisms, choose the expression (Lower 1 QR #36 asked the expression, 37.2%; MA6 #14 her miss)
w1, h1, w2, h2, dep = 3, 5, 8, 2, 6
assert w1*dep*h1 + w2*dep*h2 == 186 and w1*dep*(h1 + h2) + w2*dep*h2 == 222 and w2*dep*(h1 + h2) == 336
fig7 = joined_prisms_svg(w1, h1, w2, h2, dep, sc=16).replace('font-size="11"', 'font-size="14"')
add('Volume of Solids',
    'The figure shown was made by joining two rectangular prisms. The side lengths are measured in feet. Which expression can be used to find the total volume of the figure? (V = lwh, where V = volume, l = length, w = width, and h = height.)',
    ['3 &times; 6 &times; 5', '8 &times; 6 &times; 7', '(3 &times; 6 &times; 7) + (8 &times; 6 &times; 2)', '(3 &times; 6 &times; 5) + (8 &times; 6 &times; 2)'],
    '(3 &times; 6 &times; 5) + (8 &times; 6 &times; 2)',
    {'3 &times; 6 &times; 5': 'Stopped early: this is the top prism only', '8 &times; 6 &times; 7': 'Treated the figure as one big box',
     '(3 &times; 6 &times; 7) + (8 &times; 6 &times; 2)': 'Known trap: used the full height 7 for the top prism (counts the bottom part twice)'},
    'total volume (expression)',
    'Split it into the two boxes. Top: 3 wide, 6 deep, 5 tall. Bottom: 8 wide, 6 deep, 2 tall. Total = (3 &times; 6 &times; 5) + (8 &times; 6 &times; 2) = 90 + 96 = 186. The 7 on the left is the full height, extra information.',
    'Lower 1 QR #36 (last third, 37.2% right, her miss)',
    'x o o o x', 'Same build as the real one (choose the expression), with a full-height label as extra information', fig7)

# 8 CARRIED rules box (Day 1 #7 not scored): smallest ODD with a 0, hundreds place
digs = [0, 4, 5, 6, 8]
best = min(int(''.join(map(str, p))) for p in permutations(digs) if p[0] != 0 and p[-1] % 2 == 1)
plain = min(int(''.join(map(str, p))) for p in permutations(digs) if p[0] != 0)
assert best == 40685 and plain == 40568 and (best // 100) % 10 == 6 and (plain // 100) % 10 == 5 and (best // 10) % 10 == 8 and (best // 1000) % 10 == 0
add('Value of Digits',
    'Students wrote a new number using the digits 0, 4, 5, 6, and 8 and these rules. What digit is in the hundreds place of the new number?',
    ['0', '5', '6', '8'], '6',
    {'0': 'Read the thousands place', '5': 'Forgot the number must be odd (40,568)', '8': 'Read the tens place'},
    'the hundreds digit',
    'Odd: the only odd digit is 5, so it goes last. Smallest: the first digit cannot be 0, so it is 4, then 0, 6, 8. The number is 40,685. Hundreds place: 6. Write the number with the place names under it before answering.',
    'Lower 3 QR #31 (last third, 61.6% right, her miss): smallest even with 0, tens place; Official QR #36 (57%, her miss)',
    'o o x o x o', 'Same build as the real one (smallest, a 0 that cannot go first); odd instead of even, hundreds place',
    rules_box('The number must have 5 digits.', 'The number must be odd.', 'The number must be the smallest number possible.', 'Each digit can be used only once.'))

for p in P:
    if re.search(r'these rules|the table|shown|the figure|the graph|the plot', p['q'], re.I):
        assert p['diagram'], f"problem {p['n']} refers to something on the page but has no diagram"
letters = Counter(p['correct'] for p in P)
assert max(letters.values()) - min(letters.values()) <= 1, letters
seq = ''.join(p['correct'] for p in P)
assert all(not (seq[i] == seq[i+1] == seq[i+2]) for i in range(len(seq) - 2))
assert len({p['topic'] for p in P}) == 8
json.dump(P, open(os.path.join(HERE, 'vac2_problems.json'), 'w'), indent=1)
json.dump({str(k): v for k, v in MAP.items()}, open(os.path.join(HERE, 'vac2_mapping.json'), 'w'), indent=1)
print(letters, seq)
