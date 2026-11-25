"""Vacation Day 1 (built 2026-11-23): 8 problems / 10 minutes, parent request while traveling.
Topics = the 8 top-ranked open topics agreed 11/23: each has a REAL last-third problem she missed
(QR #26-38 / MA #21-30) and is not secured since. Built like that real problem, with the asked part changed.
Cross-topic target (parent 11/23): she stops at an intermediate value on multi-step / information-heavy
problems. So every problem is multi-step, and every problem lists her stop-early number (or her known
wrong habit) as a choice. Each wrong choice is tagged with its cause in the answer key so the result can
count "stopped early" separately. Every math claim is asserted."""
import json, os, sys
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
T = {x['topic'] for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}

def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def rules_box(*rules):
    return ('<div style="border:1.5px solid currentColor;border-radius:6px;padding:8px 12px;max-width:340px"><div style="font-weight:700;margin-bottom:4px">RULES FOR THE NEW NUMBER</div>'
            + ''.join(f'<div>{i}. {r}</div>' for i, r in enumerate(rules, 1)) + '</div>')

P, MAP = [], {}
# her full record per topic (wrong / all tries, real tests + our sets, through MA6 incl. the #20-29 redo), from topic_history.py 11/23
TOT = {'Percent Increase Decrease basic': '6/10', 'Comparing Volume of Cubes': '5/13', 'Finding Area/Perimeter of Rectangle, given Length & Width': '6/19',
       'Estimating Multiplication & Division': '9/35', 'Translating Math Expressions': '5/19', 'Counting Multiples within a Range': '4/10',
       'Value of Digits': '4/15', 'Probability of 1 Event, given a List of Items': '3/27'}
def add(topic, q, ch, right, tags, asks, key, built_on, last, vs, diagram=None):
    """ch: 4 choices in display order; right: the correct one; tags: {choice text: cause} for the 3 wrong ones;
    asks: the 1-3 words the question asks for (what she should write down before choosing)."""
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
                  vs_latest=vs, asks=asks, stop_early=[ 'ABCD'[ch.index(c)] for c, v in tags.items() if v.startswith('Stopped early')])

# 1 percent: whole from a percent part, then the sale price (Lower 6 MA #28 + one more step; 30% = her weak percent)
reg = F(18) / F(30, 100)
assert reg == 60 and reg - 18 == 42 and F(18) - F(18)*F(30, 100) == F('12.60') and reg + 18 == 78
add('Percent Increase Decrease basic',
    'A store is having a sale that ends on Sunday. Every jacket is 30% off its regular price, and every hat is 20% off. For one jacket, the discount is $18. What is the sale price of this jacket?',
    ['$12.60', '$42', '$60', '$78'], '$42',
    {'$12.60': 'Known trap: took 30% off the $18 discount instead of the price', '$60': 'Stopped early: this is the regular price',
     '$78': 'Added the discount instead of taking it off'},
    'sale price of the jacket',
    '$18 is 30% of the regular price. 10% is $18 &divide; 3 = $6, so 100% is $60. The sale price is $60 &minus; $18 = $42. The hat discount and "Sunday" are extra information.',
    'Lower 6 MA #28 (last third, 74.6% right; her miss, 92 s): 20% discount is $3, regular price?; Lower 4 QR #38 (40.6%, her miss)',
    'x x o o o x', 'Harder: one more step (the sale price, not the regular price), 30% instead of 20%, plus extra information')

# 2 cubes: scale factor, then a difference (Lower 4 QR #36: B is 5 times as wide as A, how many A's fit)
va, vb = 2**3, 6**3
assert vb - va == 208 and vb == 216 and (vb // va) == 27 and 3*va - va == 16
add('Comparing Volume of Cubes',
    'Cube A has edges that are 2 centimeters long. Cube B is 3 times as wide as Cube A. How many cubic centimeters greater is the volume of Cube B than the volume of Cube A?',
    ['16', '27', '208', '216'], '208',
    {'16': 'Known trap: thought 3 times as wide means 3 times the volume (24 &minus; 8)', '27': 'Answered the real test\'s question: how many Cube A\'s fit',
     '216': 'Stopped early: this is the volume of Cube B'},
    'how much greater (a difference)',
    'Cube B has edges 2 &times; 3 = 6 cm. Volume of B = 6 &times; 6 &times; 6 = 216. Volume of A = 2 &times; 2 &times; 2 = 8. 216 &minus; 8 = 208. (27 Cube A\'s fit inside B, but the question asks for the difference.)',
    'Lower 4 QR #36 (last third, 48.2% right, her miss); also missed Lower 5 QR #38, Lower 3 QR #29, WTE QR #28',
    'x o o o x o', 'Harder: same scale step as the real one, then both volumes and a difference')

# 3 square perimeter -> area -> rectangle -> its perimeter (Lower 1 MA #30 asked the length; this asks the perimeter)
side = 36 // 4; area = side * side; w = F(area, 27)
assert side == 9 and area == 81 and w == 3 and 2*(27 + 3) == 60 and 27 + 3 == 30
add('Finding Area/Perimeter of Rectangle, given Length & Width',
    'A square has a perimeter of 36 centimeters. A rectangle has the same area as the square. The length of the rectangle is 27 centimeters. What is the perimeter of the rectangle?',
    ['3 centimeters', '30 centimeters', '60 centimeters', '81 centimeters'], '60 centimeters',
    {'3 centimeters': 'Stopped early: this is the width of the rectangle', '30 centimeters': 'Stopped early: length + width, only half the perimeter',
     '81 centimeters': 'Stopped early: this is the area (and the wrong unit)'},
    'perimeter of the rectangle',
    'Square side = 36 &divide; 4 = 9, so its area is 9 &times; 9 = 81. The rectangle has area 81 and length 27, so its width is 81 &divide; 27 = 3. Perimeter = 27 + 3 + 27 + 3 = 60.',
    'Lower 1 MA #30 (last third, 35.9% right, her miss)',
    'x x o o x x', 'Harder: same chain as the real one (perimeter &rarr; side &rarr; area &rarr; missing side), then one more step to the perimeter')

# 4 a / b x c estimate: round to a compatible number (parent taught 47 -> 48 for 6; she rounds the divisor 6 -> 10)
exact = F(71, 8) * 203
assert 1700 < exact < 1900 and F(70, 10)*200 == 1400 and 8*200 == 1600 and 8*203 == 1624 and F(72, 8)*200 == 1800 and 1 < F(71, 8) < 10
add('Estimating Multiplication & Division',
    'Mia did the problem 71 &divide; 8 &times; 203 on her calculator. Approximately what was her answer?',
    ['between 1 and 10', 'between 1,200 and 1,500', 'between 1,500 and 1,700', 'between 1,700 and 1,900'], 'between 1,700 and 1,900',
    {'between 1 and 10': 'Stopped early: this is only 71 &divide; 8', 'between 1,200 and 1,500': 'Known trap: rounded 8 to 10 (70 &divide; 10 &times; 200 = 1,400)',
     'between 1,500 and 1,700': 'Known trap: rounded 71 &divide; 8 down to 8 (8 &times; 200 = 1,600)'},
    'about how much the whole problem is',
    'Change 71 to 72 so it divides by 8: 72 &divide; 8 = 9. Then 9 &times; 200 = 1,800. (Exactly: 1,801.6.) Round the first number to a friendly number for the divisor; do not round 8 to 10.',
    'Lower 6 QR #36 (last third, 50.1% right, her miss, 107 s): 60 &divide; 13 &times; 152; WTE QR #33 (49.0%, her miss)',
    'x x o o o x', 'Same build as the real one, with new numbers; the divisor is close to 10 to catch her 6 &rarr; 10 rounding')

# 5 story -> expression (Lower 4 QR #35: "times as many as Jeremiah HAD"; here "as Leo has LEFT", asked at the start)
add('Translating Math Expressions',
    'Leo had &square; stickers. He gave &#9675; of them to Ava. Now Ava has &#9651; times as many stickers as Leo has left. Which expression represents the number of stickers Ava had to begin with?',
    ['&#9651; &times; &square; &minus; &#9675;', '&#9651; &times; (&square; &minus; &#9675;)', '&#9651; &times; (&square; &minus; &#9675;) + &#9675;', '&#9651; &times; (&square; &minus; &#9675;) &minus; &#9675;'],
    '&#9651; &times; (&square; &minus; &#9675;) &minus; &#9675;',
    {'&#9651; &times; &square; &minus; &#9675;': 'Answered the real test\'s version ("as he HAD"), not "has left"',
     '&#9651; &times; (&square; &minus; &#9675;)': 'Stopped early: this is how many Ava has NOW',
     '&#9651; &times; (&square; &minus; &#9675;) + &#9675;': 'Went the wrong way in time: added the gift instead of taking it back'},
    'Ava, at the beginning',
    'Timeline. After the gift, Leo has &square; &minus; &#9675; left, and Ava has &#9651; times that: &#9651; &times; (&square; &minus; &#9675;). Before the gift, Ava had &#9675; fewer: &#9651; &times; (&square; &minus; &#9675;) &minus; &#9675;. Teaching tip (parent 11/21: she did not get the idea on MA6 #15): draw "before | gift | now" and fill in Leo first, then Ava, then go back one step.',
    'Lower 4 QR #35 (last third, 47.4% right, her miss); Lower 1 QR #33 (54.4%, her miss)',
    'o x o o o x', 'Same build as the real one; "has left" instead of "had", so the real one\'s answer is a trap')

# 6 counting multiples of two numbers: LCM, then count (Lower 5 MA #29 asked one divisor; parent: LCM first, then count)
m18 = [k for k in range(51, 150) if k % 6 == 0 and k % 9 == 0]
m54 = [k for k in range(51, 150) if k % 54 == 0]
m9 = [k for k in range(51, 150) if k % 9 == 0]
assert len(m18) == 6 and len(m54) == 2 and len(m9) == 11
add('Counting Multiples within a Range',
    'How many whole numbers between 50 and 150 are divisible by both 6 and 9?',
    ['2', '6', '11', '18'], '6',
    {'2': 'Known trap: used 6 &times; 9 = 54 instead of the LCM 18', '11': 'Checked only 9', '18': 'Stopped early: this is the LCM, not how many'},
    'how many numbers',
    'Step 1, the smallest number divisible by both 6 and 9 (the LCM): 18. Step 2, count the multiples of 18 between 50 and 150: 54, 72, 90, 108, 126, 144 = 6.',
    'Lower 5 MA #29 (last third, 63.7% right, her miss, 134 s): between 65 and 85, divisible by 3',
    'x o o o o x', 'Harder: two divisors (LCM step) like MA6 #27, a wider range')

# 7 rules box: largest ODD number, tens place (Lower 3 QR #31 asked smallest even / tens; MA6 #23 asked smallest even / thousands)
digs = [2, 3, 5, 7, 8, 9]
best = max(int(''.join(map(str, p))) for p in permutations(digs) if p[-1] % 2 == 1)
plain = max(int(''.join(map(str, p))) for p in permutations(digs))
assert best == 987523 and plain == 987532 and (best // 10) % 10 == 2 and (plain // 10) % 10 == 3 and (best // 100) % 10 == 5 and (best // 1000) % 10 == 7
add('Value of Digits',
    'Students wrote a new number using the digits 2, 3, 5, 7, 8, and 9 and these rules. What digit is in the tens place of the new number?',
    ['2', '3', '5', '7'], '2',
    {'3': 'Forgot the number must be odd (987,532)', '5': 'Read the hundreds place (her QR11 #35 habit)', '7': 'Read the thousands place'},
    'the tens digit',
    'Largest means the big digits go first. Odd means the last digit is 3, 5, 7 or 9; to keep the front as big as possible, put the SMALLEST odd digit (3) last. The number is 987,523. Tens place: 2. Write the number with the place names under it before answering.',
    'Lower 3 QR #31 (last third, 61.6% right, her miss): smallest even number, tens place; Official QR #36 (her miss)',
    'o o x o x o', 'Same build, flipped: largest and odd instead of smallest and even',
    rules_box('The number must have 6 digits.', 'The number must be odd.', 'The number must be the largest number possible.', 'Each digit can be used only once.'))

# 8 probability: 2/5 purple means 3/5 not purple; asks the purple count (MA6 #21 asked the total; parent: no sense of 2/5 vs 3/5 yet)
others = 5 + 4 + 3
total = F(others) / F(3, 5)
assert others == 12 and total == 20 and total * F(2, 5) == 8 and F(12) / F(2, 5) - 12 == 18
add('Probability of 1 Event, given a List of Items',
    'The table shows the number of each color of marble in a bag. The probability of picking a purple marble without looking is ' + frac(2, 5) + '. How many purple marbles are in the bag?',
    ['8', '12', '18', '20'], '8',
    {'12': 'Counted the marbles that are not purple', '18': 'Known trap (MA6 #21): took the 12 non-purple marbles as the 2/5',
     '20': 'Stopped early: this is all the marbles, not the purple ones'},
    'how many purple',
    'Purple is 2/5, so the other colors are 3/5. Red + blue + green = 5 + 4 + 3 = 12 marbles = 3/5 of the bag. 1/5 is 4, so the whole bag is 20 and purple is 2 &times; 4 = 8. Check: 8/20 = 2/5.',
    'Official QR #34 (last third, 57.6% right, her miss): P = 1/3, how many purple?',
    'o o o x o x', 'Harder: 2/5 is not a unit fraction (the real one is 1/3); asks the purple count like the real one, not the total like MA6 #21',
    table(['Color', 'Number'], [['Red', 5], ['Blue', 4], ['Green', 3], ['Purple', '?']], 'MARBLES IN THE BAG'))

import re
for p in P:
    if re.search(r'these rules|the table|shown|the figure|the graph|the plot', p['q'], re.I):
        assert p['diagram'], f"problem {p['n']} refers to something on the page but has no diagram"
letters = Counter(p['correct'] for p in P)
assert max(letters.values()) - min(letters.values()) <= 1, letters
seq = ''.join(p['correct'] for p in P)
assert all(seq[i] != seq[i+1] or seq[i] != seq[i+2] for i in range(len(seq) - 2))
assert len({p['topic'] for p in P}) == 8
json.dump(P, open(os.path.join(HERE, 'vac1_problems.json'), 'w'), indent=1)
json.dump({str(k): v for k, v in MAP.items()}, open(os.path.join(HERE, 'vac1_mapping.json'), 'w'), indent=1)
print(letters, seq)
