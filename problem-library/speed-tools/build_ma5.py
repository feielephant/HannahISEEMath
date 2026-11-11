"""MA Set 5 (2026-11-11). Plan agreed with the parent 11/11:
- the QR10 follow-ups from the parent's 11/11 read with Hannah;
- real last-third misses first (higher priority), then real middle-third misses, official ISEE practice
  exercises she missed, and one item from the parent's own observation (a x b - c + d x e);
- topics she has secured on QR10 (right 3+ times in a row) are rested.
Nothing is invented from a topic name: every problem names the real item it is built on (BUILT_ON).
Order follows the real test: non-last-third sources first, last-third sources in positions 12-30.
Every math claim is asserted."""
import json, os
from fractions import Fraction as F
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
T = {x['topic']: x for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}
SW = 'stroke="currentColor" stroke-width="1.6"'
def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def svg(w, h, body): return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{body}</svg>'
def txt(x, y, s, size=13, anchor='middle', weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="currentColor">{s}</text>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'

P, MAP = [], {}
def add(topic, q, ch, ans, key, built_on, third, diagram=None):
    assert topic in T, topic
    assert len(set(ch)) == 4 and ans in 'ABCD'
    n = len(P) + 1
    t = T[topic]
    hist = f"Wrong so far: {t.get('wrong')}/{t.get('graded')}" if t.get('graded') else 'Few graded so far'
    P.append({'n': n, 'tier': 'Hard', 'topic': topic, 'q': q, 'choices': dict(zip('ABCD', ch)), 'correct': ans,
              'key': f'<b>Answer: {ans}.</b> {key}',
              'ref': f'Tier: Hard &middot; Topic: {topic} &middot; {hist} &middot; New problem &middot; Built on: {built_on}',
              'diagram': diagram, 'gid': None, 'ma_idx': None})
    MAP[n] = dict(built_on=built_on, source_third=third)

# ================= diagrams =================
def grouped_bars(cats, a, b, ymax, title, la='Class A', lb='Class B'):
    W, H, L, B, TOP = 430, 270, 46, 220, 30
    unit = (B - TOP) / ymax
    g = ''
    for y in range(ymax + 1):
        yy = B - y*unit
        g += f'<line x1="{L}" y1="{yy:.1f}" x2="{W-10}" y2="{yy:.1f}" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>' + txt(L-8, yy+4, y, 11, 'end')
    slot = (W - 10 - L) / len(cats)
    for i, c in enumerate(cats):
        x0 = L + i*slot + slot/2 - 26
        g += f'<rect x="{x0:.1f}" y="{B-a[i]*unit:.1f}" width="24" height="{a[i]*unit:.1f}" fill="#4A86C5" stroke="currentColor" stroke-width="1"/>'
        g += f'<rect x="{x0+26:.1f}" y="{B-b[i]*unit:.1f}" width="24" height="{b[i]*unit:.1f}" fill="#D08B3C" stroke="currentColor" stroke-width="1"/>'
        g += txt(L + i*slot + slot/2, B+16, c, 12)
    g += f'<line x1="{L}" y1="{B}" x2="{W-10}" y2="{B}" {SW}/><line x1="{L}" y1="{TOP-6}" x2="{L}" y2="{B}" {SW}/>'
    g += txt(W/2, 16, title, 13, weight='600') + f'<text x="14" y="{(B+TOP)/2}" font-size="11" text-anchor="middle" fill="currentColor" transform="rotate(-90 14 {(B+TOP)/2})">Number of Students</text>'
    g += f'<rect x="{W-150}" y="{B+28}" width="12" height="12" fill="#4A86C5"/>' + txt(W-134, B+38, la, 11, 'start')
    g += f'<rect x="{W-80}" y="{B+28}" width="12" height="12" fill="#D08B3C"/>' + txt(W-64, B+38, lb, 11, 'start')
    return svg(W, H + 2, g)

def coord_grid(pts, lo=-5, hi=5, u=22):
    n = hi - lo; S = n*u; off = 24
    g = ''
    for k in range(n + 1):
        p = off + k*u
        g += f'<line x1="{p}" y1="{off}" x2="{p}" y2="{off+S}" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>'
        g += f'<line x1="{off}" y1="{p}" x2="{off+S}" y2="{p}" stroke="currentColor" stroke-opacity="0.25" stroke-width="1"/>'
    X = lambda x: off + (x - lo)*u
    Y = lambda y: off + (hi - y)*u
    g += f'<line x1="{off}" y1="{Y(0)}" x2="{off+S}" y2="{Y(0)}" {SW}/><line x1="{X(0)}" y1="{off}" x2="{X(0)}" y2="{off+S}" {SW}/>'
    for v in range(lo, hi + 1):
        if v == 0: continue
        g += txt(X(v), Y(0)+14, v, 9) + txt(X(0)-6, Y(v)+3, v, 9, 'end')
    g += txt(off+S+12, Y(0)+4, 'x', 12) + txt(X(0), off-8, 'y', 12)
    for lab, (x, y) in pts.items():
        g += f'<circle cx="{X(x)}" cy="{Y(y)}" r="4.5" fill="currentColor"/>' + txt(X(x)+10, Y(y)-7, lab, 14, 'start', '700')
    return svg(S + 2*off + 10, S + 2*off, g)

def stacked(rows, total):
    # fixed-width column grid so shapes and digits line up by place value (op, hundreds, tens, ones)
    cell = lambda x, extra='': f'<td style="width:1.6em;text-align:center;padding:3px 0;{extra}">{x}</td>'
    body = ''.join('<tr>' + ''.join(cell(x) for x in r) + '</tr>' for r in rows)
    body += '<tr>' + ''.join(cell(x, 'border-top:1.5px solid currentColor;padding-top:6px;') for x in total) + '</tr>'
    return f'<table style="margin:0 auto;border-collapse:collapse;font-size:1.25em;">{body}</table>'

def array_svg(rows, cols, u=14):
    g = ''.join(f'<rect x="{2+c*u}" y="{2+r*u}" width="{u}" height="{u}" fill="none" stroke="currentColor" stroke-width="1.2"/>' for r in range(rows) for c in range(cols))
    return svg(cols*u + 4, rows*u + 4, g)

def shape(kind, x, y, s=16):
    if kind == 'tri': return f'<polygon points="{x},{y-s/2} {x-s/2},{y+s/2} {x+s/2},{y+s/2}" fill="none" {SW}/>'
    if kind == 'cir': return f'<circle cx="{x}" cy="{y}" r="{s/2}" fill="none" {SW}/>'
    return f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" fill="none" {SW}/>'

def scale(left, right, label):
    W = 300; g = f'<polygon points="150,62 136,100 164,100" fill="none" {SW}/><line x1="30" y1="62" x2="270" y2="62" {SW}/>'
    g += f'<line x1="20" y1="56" x2="120" y2="56" {SW}/><line x1="180" y1="56" x2="280" y2="56" {SW}/>'
    g += f'<line x1="70" y1="56" x2="70" y2="62" {SW}/><line x1="230" y1="56" x2="230" y2="62" {SW}/>'
    for side, items, cx in (('l', left, 70), ('r', right, 230)):
        k = len(items); x0 = cx - (k-1)*11
        for i, s in enumerate(items): g += shape(s, x0 + i*22, 44)
    return svg(W, 108, txt(150, 14, label, 12, weight='600') + g)

def net_svg(cells, u=46):
    g = ''
    for (r, c), sym in cells.items():
        g += f'<rect x="{4+c*u}" y="{4+r*u}" width="{u}" height="{u}" fill="none" {SW}/>' + txt(4+c*u+u/2, 4+r*u+u/2+8, sym, 22)
    return svg(4*u + 8, 3*u + 8, g)

# fold a net by rolling a cube across it; returns {cell: cube face}
def fold(cells):
    start = next(iter(sorted(cells)))
    faces = {start: 'bottom'}
    orient0 = dict(bottom='bottom', top='top', north='north', south='south', east='east', west='west')
    stack = [(start, orient0)]
    roll = {(0, 1): ('east', 'west'), (0, -1): ('west', 'east'), (1, 0): ('south', 'north'), (-1, 0): ('north', 'south')}
    while stack:
        (r, c), o = stack.pop()
        for (dr, dc), (fwd, back) in roll.items():
            nb = (r+dr, c+dc)
            if nb in cells and nb not in faces:
                n = dict(o); n['bottom'], n[fwd], n['top'], n[back] = o[fwd], o['top'], o[back], o['bottom']
                faces[nb] = n['bottom']; stack.append((nb, n))
    assert len(set(faces.values())) == 6 == len(cells)
    return faces
OPP = dict(bottom='top', top='bottom', north='south', south='north', east='west', west='east')

# ================= positions 1-11: middle/first-third, official exercises, parent observation =================
# 1 PT3 QR #24 two-class grouped bar graph (middle third, wrong); also the parent's "wide data" request
cats1, a1, b1 = ['Apple', 'Banana', 'Grape', 'Orange'], [7, 4, 3, 5], [2, 6, 3, 4]
tot1 = [x+y for x, y in zip(a1, b1)]
assert tot1 == [9, 10, 6, 9] and max(tot1) == 10 and cats1[tot1.index(10)] == 'Banana' and max(a1+b1) == 7 and cats1[a1.index(7)] == 'Apple'
add('Comparing Adding Subtracting Bar Graph Data Table Values',
    'Two classes, Class A and Class B, each recorded the favorite fruit of the students in the class. The graph shows the results. Which fruit was the favorite of the most students in the two classes together?',
    ['apple', 'banana', 'grape', 'orange'], 'B',
    'Add the two bars for each fruit: apple 7 + 2 = 9, banana 4 + 6 = 10, grape 3 + 3 = 6, orange 5 + 4 = 9. Banana has the most, 10. A has the tallest single bar (7), but the question asks about both classes together.',
    'Lower 3 QR #24 (her miss, middle third, 74% right)', 'middle',
    grouped_bars(cats1, a1, b1, 8, 'FAVORITE FRUIT'))

# 2 PT5 MA #17 mode from a wide table (middle third, wrong; "many data values, confused")
sc2 = {'Ana': [92, 86, 79, 95], 'Ben': [84, 97, 86, 90], 'Cara': [79, 91, 88, 86], 'Dev': [93, 88, 95, 81]}
cnt2 = Counter(v for r in sc2.values() for v in r)
assert cnt2.most_common(1)[0] == (86, 3) and sorted(cnt2.values(), reverse=True)[:2] == [3, 2]
add('Finding MMMR given Bar Graph Data Table',
    'The table shows four test scores for each of four students. What is the mode of this set of data?',
    ['79', '86', '88', '97'], 'B',
    'The mode is the score that appears most often. 86 appears 3 times (Ana, Ben, Cara). 79, 88, and 95 appear only twice. D is the highest score, not the mode.',
    'Lower 5 MA #17 (her miss, middle third, 83% right)', 'middle',
    table(['Student', 'Test 1', 'Test 2', 'Test 3', 'Test 4'], [[k] + v for k, v in sc2.items()], 'TEST SCORES'))

# 3 PT6 MA #12 story -> equation, answer NOT in the direct "p = 48 / 6" form (parent 11/11)
assert 6*8 == 48
add('Matching Stories to Equations',
    'A box holds 48 crayons that are packed into groups of 6. If p represents the number of packs in the box, which equation can be used to find p?',
    ['p &minus; 6 = 48', '48 &times; p = 6', '6 + p = 48', '6 &times; p = 48'], 'D',
    'p packs with 6 crayons in each make 48 crayons: 6 &times; p = 48 (so p = 8). B is backwards: try p = 8, and 48 &times; 8 is not 6. That is the PT6 MA #12 and QR10 #4 slip.',
    'Lower 6 MA #12 (her miss, middle third) and QR10 #4', 'middle')

# 4 PT6 MA #13 input/output, plain "+ n" with n > 7 (parent 11/11: mix in simpler rules)
r4 = lambda x: x + 9
rows4 = [(14, 23), (19, 28), (27, 36), (33, 42)]
assert all(r4(a) == b for a, b in rows4) and r4(46) == 55
add('Input Output Tables',
    'The number machine performs the same operation on each input to create an output. What is the output for an input of 46?',
    ['37', '55', '56', '92'], 'B',
    'Every output is 9 more than its input: 14 + 9 = 23, 33 + 9 = 42. So 46 + 9 = 55. A subtracts 9. C adds 10. D doubles.',
    'Lower 6 MA #13 (her miss, middle third); rule kept plain on purpose', 'middle',
    table(['Input', 'Output'], rows4, 'NUMBER MACHINE'))

# 5 PT6 MA #13 / QR10 #5 retry: input / 2 + 5
r5 = lambda x: x // 2 + 5
rows5 = [(6, 8), (10, 10), (18, 14), (24, 17)]
assert all(r5(a) == b for a, b in rows5) and r5(40) == 25 and all(a % 2 == 0 for a, _ in rows5)
add('Input Output Tables',
    'The number machine performs the same operation on each input to create an output. What is the output for an input of 40?',
    ['20', '25', '30', '45'], 'B',
    'From 6 to 10 the input goes up 4 and the output goes up 2, so the output grows half as fast: try input &divide; 2. 6 &divide; 2 = 3, and the output is 8, so add 5: output = input &divide; 2 + 5. Check: 24 &divide; 2 + 5 = 17. So 40 &divide; 2 + 5 = 25. A forgets the + 5. D is 40 + 5, leaving out the half (her QR10 #5 slip).',
    'Lower 6 MA #13 and QR10 #5 (her misses)', 'middle',
    table(['Input', 'Output'], rows5, 'NUMBER MACHINE'))

# 6 PT6 QR #6 pick the rule (first third); parent liked QR10 #26. Each wrong rule fits exactly one row.
rows6 = [(2, 4), (4, 10), (5, 13), (7, 19)]
R6 = {'△ &times; 2 = ■': lambda t: 2*t, '△ + 6 = ■': lambda t: t + 6, '△ &times; 3 &minus; 2 = ■': lambda t: 3*t - 2, '△ &times; 2 + 3 = ■': lambda t: 2*t + 3}
fits = {k: sum(f(a) == b for a, b in rows6) for k, f in R6.items()}
assert fits == {'△ &times; 2 = ■': 1, '△ + 6 = ■': 1, '△ &times; 3 &minus; 2 = ■': 4, '△ &times; 2 + 3 = ■': 1}
add('Input Output Tables',
    'The table shows how a number machine changes each input number (△) into an output number (■). Which equation shows the rule for the number machine?',
    ['△ &times; 3 &minus; 2 = ■', '△ &times; 2 = ■', '△ + 6 = ■', '△ &times; 2 + 3 = ■'], 'A',
    'Check every row. 2 &times; 3 &minus; 2 = 4, 4 &times; 3 &minus; 2 = 10, 5 &times; 3 &minus; 2 = 13, 7 &times; 3 &minus; 2 = 19. B works only for 2, C only for 4, D only for 5.',
    'Lower 6 QR #6 (first third) and QR10 #26 (her miss)', 'first',
    table(['Input (△)', 'Output (■)'], rows6, 'NUMBER MACHINE'))

# 7 ordering exactly 3 close numbers (PT1 QR #22, PT3 QR #20 middle-third misses; parent: 3 numbers, not obvious)
v7 = {'0.65': F(65, 100), '5/8': F(5, 8), '2/3': F(2, 3)}
assert sorted(v7, key=v7.get) == ['5/8', '0.65', '2/3']
add('Comparing & Ordering Fractions & Decimals',
    f'Which list shows 0.65, {frac(5,8)}, and {frac(2,3)} in order from least to greatest?',
    [f'0.65, &nbsp;{frac(5,8)}, &nbsp;{frac(2,3)}', f'{frac(2,3)}, &nbsp;0.65, &nbsp;{frac(5,8)}', f'{frac(5,8)}, &nbsp;0.65, &nbsp;{frac(2,3)}', f'{frac(5,8)}, &nbsp;{frac(2,3)}, &nbsp;0.65'], 'C',
    'Change each to a decimal: 5/8 = 0.625, 0.65, 2/3 &asymp; 0.667. Least to greatest: 5/8, 0.65, 2/3. B is greatest to least. D puts the decimal last because it is written differently.',
    'Lower 1 QR #22 and Lower 3 QR #20 (her misses, middle third); QR10 #13', 'middle')

# 8 PT6 QR #25 / QR10 #11 yards -> feet -> inches (middle third, wrong)
assert 5*3*12 == 180 and 180 // 8 == 22 and 180 % 8 == 4 and 5*12 // 8 == 7
add('English Unit Conversions',
    'Lena has 5 yards of ribbon. She cuts it into pieces that are each 8 inches long. There are 3 feet in 1 yard and 12 inches in 1 foot. How many 8-inch pieces can she cut?',
    ['7', '15', '22', '23'], 'C',
    '1 yard = 3 &times; 12 = 36 inches, so 5 yards = 180 inches. 180 &divide; 8 = 22 R4, so 22 full pieces (4 inches are left over). A uses 12 inches in a yard (her QR10 #11 slip). B is the number of feet. D rounds up, but a 4-inch piece is not a full piece.',
    'Lower 6 QR #25 (her miss, middle third) and QR10 #11', 'middle')

# 9 official ISEE exercise gid 1108 (pear, "decreased by 16%", she missed it on MA3 #3): new numbers
assert F('4.50')*F(88, 100) == F('3.96') and F('4.50') - F('0.12') == F('4.38') and F('4.50')*F(112, 100) == F('5.04')
add('Evaluating Percents of Numbers',
    'A store sells a notebook for $4.50. The price of the notebook decreased by 12%. What is the price of the notebook now?',
    ['$3.96', '$4.38', '$4.62', '$5.04'], 'A',
    '12% of $4.50 is 0.12 &times; 4.50 = $0.54. The new price is 4.50 &minus; 0.54 = $3.96. B subtracts 0.12 instead of 12% of the price (the "decreased by" slip). C adds 0.12. D increases by 12%.',
    'Official ISEE practice exercise (gid 1108, her MA3 #3 miss)', 'exercise')

# 10 official ISEE exercise gid 1453 shortest distance moving down or right (her MA3 #30 miss)
A10, B10 = (-3, 4), (2, -2)
assert (B10[0]-A10[0]) + (A10[1]-B10[1]) == 11
add('Minimum Distance on Coordinate Plane / Grid',
    'Use the grid to answer the question. How many units is the shortest distance from point A to point B if you can only move down or to the right?',
    ['8', '9', '10', '11'], 'D',
    'Right: from x = &minus;3 to x = 2 is 5 units (3 to reach 0, then 2 more). Down: from y = 4 to y = &minus;2 is 6 units (4 to reach 0, then 2 more). 5 + 6 = 11. A, B, and C come from missing a unit when crossing 0; count the grid squares one by one.',
    'Official ISEE practice exercise (gid 1453, her MA3 #30 miss)', 'exercise',
    coord_grid({'A': A10, 'B': B10}))

# 11 parent observation 11/11: she sometimes does 2 x 5 - 3 + 6 x 3 as 5 - 3 first
assert 4*6 - 2 + 3*5 == 37 and 4*(6-2) + 3*5 == 31 and 4*6 - (2 + 3*5) == 7 and ((4*6 - 2) + 3)*5 == 125
add('Order of Operations and Equivalence',
    'What is the value of 4 &times; 6 &minus; 2 + 3 &times; 5?',
    ['7', '31', '37', '125'], 'C',
    'Multiply first: 4 &times; 6 = 24 and 3 &times; 5 = 15. Then left to right: 24 &minus; 2 + 15 = 37. B does 6 &minus; 2 first, as if there were parentheses. A subtracts the whole 2 + 15. D works left to right with no multiplying first.',
    "Parent's 11/11 observation (2 &times; 5 &minus; 3 + 6 &times; 3); real order-of-operations items Lower 2 MA #11, Lower 3 MA #29", 'parent')

# ================= positions 12-30: real last-third sources =================
# 12 PT6 QR #38 (18.4% right, her miss) / Lower 5 MA #30 (18.8%): the list is categories, find the one category
add('Data Collection & Random Sampling',
    'Maya recorded information about the books in her class library. She listed the information in categories or groups.<div style="margin-top:6px">1. Type of book: mystery, science, poetry</div><div>2. Language each book is written in</div><div>3. ?</div><div style="margin-top:6px">Which information best completes Maya&rsquo;s list?</div>',
    ['the number of pages in each book', 'how many times each book was borrowed', 'the price of each book', 'the color of each book&rsquo;s cover'], 'D',
    'Type and language are categories (words, not numbers). Only the color of the cover is a category. A, B, and C are all numbers you count or measure. Find the one choice unlike the other three.',
    'Lower 6 QR #38 (her miss, last third, 18.4% right) and Lower 5 MA #30', 'last')

# 13 Lower 5 MA #29 counting multiples, "multiple of" wording (her shortcut must give a wrong answer)
m13 = [k for k in range(28, 78) if k % 7 == 0]
assert m13[0] == 28 and m13[-1] == 77 and len(m13) == 8 and (78 - 27) // 7 == 7
add('Counting Multiples within a Range',
    'How many numbers between 27 and 78 are multiples of 7?',
    ['5', '6', '7', '8'], 'D',
    'The first multiple of 7 after 27 is 28 = 7 &times; 4. The last one before 78 is 77 = 7 &times; 11. Count 4 through 11: 11 &minus; 4 + 1 = 8. C is her shortcut (78 &minus; 27) &divide; 7 = 7 R2, which misses one.',
    'Lower 5 MA #29 (her miss, last third); QR9 #36, QR6 #28', 'last')

# 14 PT6 MA #28 whole from 20%, discount wording
assert F(9) / F(20, 100) == 45 and 45 - 9 == 36
add('Percent Word Problems',
    'A store owner offered a 20% discount off the regular price of a lamp. The amount of the discount was $9. What is the regular price of the lamp?',
    ['$18', '$36', '$45', '$54'], 'C',
    '$9 is 20% of the regular price. 20% is one fifth, so the price is 9 &times; 5 = $45 (or 9 &divide; 0.2). A is 9 &times; 2. B is the sale price, 45 &minus; 9. D adds 9 to 45.',
    'Lower 6 MA #28 (her miss, last third); official exercise gid 709 (30% took 1 hour)', 'last')

# 15 PT6 MA #28 whole from 20%, increase wording (parent 11/11): same original price
assert F(16) / F(20, 100) == 80 and 80 + 16 == 96 and 80 - 16 == 64
add('Percent Word Problems',
    'The price of a bike was increased by 20%. The amount of the increase was $16. What was the price of the bike before the increase?',
    ['$64', '$80', '$96', '$112'], 'B',
    'The $16 increase is 20% of the price before the increase. 20% is one fifth, so the price was 16 &times; 5 = $80. C is the new price, 80 + 16. A takes the 16 away. D adds 16 to the new price again.',
    'Lower 6 MA #28 with increase wording (parent 11/11)', 'last')

# 16 PT6 QR #36 a / b x c estimate: invisible-brace trap and rough-rounding trap
ex16 = F(70, 9) * 124
assert 900 < ex16 < 1200 and F(70, 9*124) < 1 and 70 // 10 * 120 == 840
add('Estimating Multiplication & Division',
    'Maria did the problem 70 &divide; 9 &times; 124. Approximately what was her answer?',
    ['less than 1', 'between 600 and 900', 'between 900 and 1,200', 'between 1,200 and 1,500'], 'C',
    'Work left to right: 70 &divide; 9 first. 72 &divide; 9 = 8, so 70 &divide; 9 is a little less than 8 (about 7.8). 7.8 &times; 124 is about 964: between 900 and 1,200. A comes from doing 9 &times; 124 first, as if the problem were 70 &divide; (9 &times; 124). B comes from rounding too much: 70 &divide; 10 &times; 120 = 840.',
    'Lower 6 QR #36 (her miss, last third); parent 11/11: she adds parentheses that are not there', 'last')

# 17 PT1 QR #29 (fraction + decimal) and QR10 #14 (order, then calculate)
v17 = sorted([F(5, 8), F(6, 10), F(7, 10)])
assert v17[-1] - v17[0] == F(1, 10) and F(7, 10) - F(5, 8) == F(75, 1000) and 1 - F(6, 10) == F(4, 10)
add('Converting to a Decimal',
    f'Three bottles hold {frac(5,8)} liter, 0.6 liter, and {frac(7,10)} liter of water. How much more water does the bottle with the most hold than the bottle with the least?',
    ['0.075 liter', '0.1 liter', '0.375 liter', '0.4 liter'], 'B',
    '5/8 = 0.625 and 7/10 = 0.7. In order: 0.6, 0.625, 0.7. Most minus least: 0.7 &minus; 0.6 = 0.1. A is 0.7 &minus; 0.625. C is 1 &minus; 5/8. D is 1 &minus; 0.6.',
    'Lower 1 QR #29 (her miss, last third) and QR10 #14', 'last')

# 18 Lower 3 MA #21 (x3 pattern, sixth number): x4 pattern
s18 = [2*4**i for i in range(7)]
assert s18[:4] == [2, 8, 32, 128] and s18[4] == 512 and s18[5] == 2048 and s18[6] == 8192
add('Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.',
    'Use the number pattern to answer the question.<div style="margin-top:6px">2, &nbsp;8, &nbsp;32, &nbsp;128, &nbsp;?, &nbsp;?</div><div style="margin-top:6px">What is the sixth number in the pattern?</div>',
    ['256', '512', '2,048', '8,192'], 'C',
    'Each number is 4 times the one before: 128 &times; 4 = 512 (5th), 512 &times; 4 = 2,048 (6th). A doubles 128. B stops at the 5th. D goes one too far.',
    'Lower 3 MA #21 (her miss, last third)', 'last')

# 19 nth term, arithmetic, off-by-one trap (QR9 #26 and MA4 #18 misses; Lower 3 MA #21)
assert 38 + (20 - 5)*7 == 143 and 38 + 14*7 == 136 and 38 + 16*7 == 150
add('Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.',
    'In a sequence, each number is 7 more than the number before it. The 5th number in the sequence is 38. What is the 20th number in the sequence?',
    ['136', '143', '150', '157'], 'B',
    'From the 5th number to the 20th number is 20 &minus; 5 = 15 steps. 15 &times; 7 = 105, and 38 + 105 = 143. A takes 14 steps and C takes 16 steps (off by one). D takes 17.',
    'QR9 #26 and MA4 #18 (her misses, last third); Lower 3 MA #21', 'last')

# 20 Lower 3 QR #38 cryptarithm (shapes, with a borrow)
sol20 = [(t, c) for t in range(1, 10) for c in range(1, 10) if t != c and (100*t + 11*c) - 11*t == 745]
assert sol20 == [(8, 3)] and 3 < 8  # unique; ones column needs a borrow
add('Cryptarithm / digit substitution',
    'Each shape shown represents a different digit from 1 through 9. What is the value of ○?',
    ['3', '5', '7', '8'], 'A',
    'Start with the hundreds: nothing is subtracted there, but 1 was borrowed, so △ &minus; 1 = 7 and △ = 8. Ones: ○ &minus; 8 needs a borrow, so ○ + 10 &minus; 8 = 5 and ○ = 3. Check the tens: 3 &minus; 1 = 2, borrow again, 12 &minus; 8 = 4. So 833 &minus; 88 = 745. D is △, not ○.',
    'Lower 3 QR #38 (last third, 40% right); QR3/6/8 misses', 'last',
    stacked([['', '△', '○', '○'], ['&minus;', '', '△', '△']], ['', '7', '4', '5']))

# 21 Lower 3 QR #31 value of digits with a rules box (her miss, last third); QR9 #24
from itertools import permutations
c21 = [int(''.join(map(str, p))) for p in permutations([2, 5, 6, 7, 9]) if p[0] != 0 and p[-1] % 2 == 1]
best21 = max(c21)
assert best21 == 97625 and (best21 // 10) % 10 == 2 and (97652 // 10) % 10 == 5
add('Value of Digits',
    'Students were asked to write a new number using all the rules shown and the digits 2, 5, 6, 7, and 9. What digit is in the tens place of the new number?',
    ['2', '5', '6', '7'], 'A',
    'To be odd, the number must end in 5, 7, or 9. To be as large as possible, put the big digits first and end with the smallest odd digit, 5: 97625. The tens digit is 2. B ignores the "odd" rule (97652).',
    'Lower 3 QR #31 (her miss, last third, 61.6% right); QR9 #24', 'last',
    '<div style="border:1.5px solid currentColor;border-radius:6px;padding:8px 12px;max-width:340px"><div style="font-weight:700;margin-bottom:4px">RULES FOR THE NEW NUMBER</div><div>1. The number must have 5 digits.</div><div>2. The number must be odd.</div><div>3. The number must be the largest number possible.</div><div>4. Each digit can be used only once.</div></div>')

# 22 Lower 2 MA #26 distributive property (her miss, last third)
assert 9*(40 - 3) == 9*40 - 9*3 and 9*(40 - 3) != 9*40 - 3
add('Identifying Number Properties',
    'Which expression is equivalent to 9 &times; (40 &minus; 3)?',
    ['(9 &times; 40) &minus; 3', '(9 &minus; 3) &times; 40', '(9 &times; 40) &minus; (9 &times; 3)', '(9 &times; 40) + (9 &times; 3)'], 'C',
    'The 9 multiplies both numbers inside the parentheses: 9 &times; 40 &minus; 9 &times; 3 = 360 &minus; 27 = 333, and 9 &times; 37 = 333. A multiplies only the 40 (the MA4 #8 slip). D changes minus to plus.',
    'Lower 2 MA #26 (her miss, last third); MA4 #8', 'last')

# 23 Lower 2 MA #29 classification (her miss, last third, 34% right)
for e in range(2, 41, 2):
    for p in (2, 3, 5, 7, 11, 13):
        assert (e*p) % 2 == 0
assert (2*3) % 4 != 0 and all(not ((e*p) % 2) for e in (2, 4) for p in (3, 5))
add('Classification of Numbers, given a Set',
    'Two numbers are greater than 1. One is an even number and the other is a prime number. What will always describe the product of the two numbers?',
    ['an even number', 'an odd number', 'a prime number', 'a multiple of 4'], 'A',
    'An even number times any whole number is even, so the product is always even. Try 4 &times; 3 = 12 and 2 &times; 5 = 10. B fails because of the even number. C fails: 12 is not prime. D fails: 2 &times; 3 = 6 is not a multiple of 4.',
    'Lower 2 MA #29 (her miss, last third, 34.4% right)', 'last')

# 24 Lower 2 MA #24 divisible by 8 (her miss, last third); traps all divisible by 4
ch24 = [324, 412, 548, 632]
assert [x % 8 == 0 for x in ch24] == [False, False, False, True] and all(x % 4 == 0 for x in ch24)
add('No Remainder when Divided by a given Number',
    'Which number is divisible by 8?',
    ['324', '412', '548', '632'], 'D',
    '632 &divide; 8 = 79 with no remainder. The others can be divided by 4 but not by 8: 324 &divide; 8 = 40 R4, 412 &divide; 8 = 51 R4, 548 &divide; 8 = 68 R4. Checking only "divisible by 4" is not enough.',
    'Lower 2 MA #24 (her miss, last third, 73.3% right)', 'last')

# 25 Lower 2 QR #29 factor arrays (her miss, last third)
arr25 = [(3, 6), (9, 2), (4, 5), (3, 5)]
assert [r*c == 18 and {r, c} != {2, 9} for r, c in arr25] == [True, False, False, False]
add('Comparing Areas',
    'The length and width of the array shown represent two factors of 18. Which array represents two <u>different</u> factors of 18?<div style="margin-top:8px">' + array_svg(2, 9) + '</div>',
    [array_svg(*rc) for rc in arr25], 'A',
    'The array shown is 2 by 9 (2 &times; 9 = 18). A is 3 by 6, and 3 &times; 6 = 18 with different factors. B is 9 by 2, the same factors turned. C is 4 &times; 5 = 20. D is 3 &times; 5 = 15.',
    'Lower 2 QR #29 (her miss, last third, 65.1% right)', 'last')

# 26 Lower 1 MA #25 remaining amount (her miss, last third); MA4 #24 added what was lost
assert 9 - 9*F(2, 3) + 12 - 12*F(3, 4) == 6 and 9*F(2, 3) + 12*F(3, 4) == 15
add('Remaining Amount after Reducing by Fractions',
    f'Ravi had 9 marbles and 12 stickers. He gave away {frac(2,3)} of his marbles and {frac(3,4)} of his stickers. How many marbles and stickers does he have left?',
    ['6', '9', '12', '15'], 'A',
    'Marbles: 2/3 of 9 is 6, so 3 are left. Stickers: 3/4 of 12 is 9, so 3 are left. 3 + 3 = 6. D is what he gave away (6 + 9), the MA4 #24 slip.',
    'Lower 1 MA #25 (her miss, last third); MA4 #24', 'last')

# 27 Lower 1 MA #30 (35.9% right) with one more step: perimeter of the rectangle
side27 = 36 // 4; len27 = side27**2 // 3
assert side27 == 9 and len27 == 27 and 2*(27 + 3) == 60 and 2*27 == 54
add('Finding Area/Perimeter of Rectangle, given Length & Width',
    'The perimeter of a square is 36 centimeters. A rectangle with a width of 3 centimeters has the same area as the square. What is the perimeter of the rectangle in centimeters?',
    ['27', '36', '54', '60'], 'D',
    'Square side: 36 &divide; 4 = 9, so its area is 81. Rectangle length: 81 &divide; 3 = 27. Perimeter: 27 + 3 + 27 + 3 = 60. A stops at the length. B assumes the same perimeter. C adds only the two lengths.',
    'Lower 1 MA #30 (her miss, last third, 35.9% right); QR9 #35', 'last')

# 28 Lower 2 MA #30 triangle area vs height (her miss, last third, 32.1% right)
assert all(F(1, 2)*12*h == 6*h for h in range(1, 30))
add('Area of Triangles',
    f'The base of a triangle is 12 centimeters (cm). Which statement correctly compares the value of A to the height of the triangle? (A = {frac(1,2)} &times; base &times; height)',
    [f'The value of A is always {frac(1,2)} the value of the height.', 'The value of A is always 12 times the value of the height.', 'The value of A can be the same as the value of the height.', 'The value of A is always 6 times the value of the height.'], 'D',
    'Put the base into the formula: A = 1/2 &times; 12 &times; height = 6 &times; height. Check: height 2 gives A = 12, which is 6 times 2. A uses only the 1/2. B uses only the 12.',
    'Lower 2 MA #30 (her miss, last third, 32.1% right); MA4 #17', 'last')

# 29 Lower 5 QR #34 balance scales (her miss, last third; officially tagged pictographs)
# scale 1: tri tri sq = sq cir  -> cir = 2 tri ; scale 2: cir tri = sq sq sq -> 3 tri = 3 sq -> tri = sq
for tri in range(1, 20):
    cir, sq = 2*tri, tri
    assert 2*tri + sq == sq + cir and cir + tri == 3*sq
    assert cir != tri and cir != 3*sq and 2*sq != tri
add('Interpreting Pictographs',
    'The scales shown are balanced. Which set of figures would also make a balanced scale?<div style="margin-top:8px">' + scale(['tri', 'tri', 'sq'], ['sq', 'cir'], 'Scale 1') + scale(['cir', 'tri'], ['sq', 'sq', 'sq'], 'Scale 2') + '</div>',
    ['△ balances □', '○ balances △', '○ balances □ □ □', '□ □ balances △'], 'A',
    'Scale 1: take one □ off both sides, so △ △ balances ○. Scale 2: put △ △ in place of ○, so △ △ △ balances □ □ □, and one △ balances one □. B is false (○ is two △). C is false (○ is two □). D is false (□ □ is two △).',
    'Lower 5 QR #34 (her miss, last third, 63.1% right; retake: "not solid on scale exchange")', 'last')

# 30 Lower 3 QR #32 cube net (last third, 60.5% right; her MA3 #27 miss)
cells30 = {(0, 1): '★', (1, 0): '●', (1, 1): '▲', (1, 2): '♥', (1, 3): '■', (2, 2): '◆'}
f30 = fold(cells30)
opp30 = [s for cell, s in cells30.items() if f30[cell] == OPP[f30[(0, 1)]]]
assert opp30 == ['◆']
add('3D shape from its net (unfolding a solid)',
    'The net shown is folded to make a cube. Which symbol will be on the face opposite the face with the ★?',
    ['▲', '♥', '●', '◆'], 'D',
    'When the net folds, the ★ square folds over the top of the row of four squares and the ◆ square folds under it, so they end up on opposite faces. ▲, ●, and ♥ are all on the row of four, which goes around the sides, so each of them touches the ★ face. A is right under the ★ on the net, but it folds to be next to it, not across from it.',
    'Lower 3 QR #32 (last third, 60.5% right); her MA3 #27 miss', 'last',
    net_svg(cells30))

# ================= checks =================
assert len(P) == 30
L = [p['correct'] for p in P]
cnt = Counter(L); print(cnt, ''.join(L))
assert max(cnt.values()) - min(cnt.values()) <= 1, cnt
assert not any(L[i] == L[i+1] == L[i+2] for i in range(28)), ''.join(L)
tc = Counter(p['topic'] for p in P)
assert max(tc.values()) <= 3, tc
thirds = Counter(MAP[n]['source_third'] for n in MAP); print(thirds)
assert all(MAP[n]['source_third'] == 'last' for n in range(12, 31))
json.dump(P, open(os.path.join(HERE, 'ma5_problems.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(MAP, open(os.path.join(HERE, 'ma5_mapping.json'), 'w'), indent=1, ensure_ascii=False)
print('wrote', len(P), 'diagrams', sum(1 for p in P if p['diagram']))
