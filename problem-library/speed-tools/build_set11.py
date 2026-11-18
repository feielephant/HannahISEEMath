"""QR Set 11 (2026-11-17), rebuilt the same day per the parent:
- 30 real-test LAST-third type problems (more steps, more information) + 8 MIDDLE-third type, no easy problems;
- topics chosen only by her data (topic_history.py -> group_metrics.py -> qr11_metrics.json):
  high error rate; or high error earlier, later secured, but not practiced for 3+ weeks; or still missed in recent sets/tests.
Every problem names the real or practice item it is built like. Every math claim is asserted. No real item verbatim."""
import json, os
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
T = {x['topic']: x for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}
MET = json.load(open(os.path.join(HERE, 'qr11_metrics.json')))
SW = 'stroke="currentColor" stroke-width="1.6"'
def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def svg(w, h, body): return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{body}</svg>'
def txt(x, y, s, size=13, anchor='middle', style=''): return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="currentColor" {style}>{s}</text>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def lines(*ls): return ''.join(f'<div>{l}</div>' for l in ls)

P, MAP = [], {}
def add(topic, group, third, q, ch, ans, key, model, diagram=None):
    assert topic in T, topic
    assert len(set(ch)) == 4 and ans in 'ABCD'
    n = len(P) + 1
    m = MET[group]
    hist = (f"Real tests: {m['real_mid']} middle-third + {m['real_last']} last-third items &middot; "
            f"Last done: {m['last_done']} &middot; Last wrong: {m['last_wrong']} &middot; Last 5: {m['last5']} wrong &middot; Since 10/25: {m['since1025']} wrong")
    P.append({'n': n, 'tier': 'Hard', 'topic': topic, 'q': q, 'choices': dict(zip('ABCD', ch)), 'correct': ans,
              'key': f'<b>Answer: {ans}.</b> {key}',
              'ref': f'Tier: Hard &middot; Topic: {topic} &middot; Type: real {third} third &middot; Why chosen: {WHY[group]} &middot; Built like: {model} &middot; {hist}',
              'diagram': diagram, 'needs_diagram': bool(diagram)})
    MAP[n] = dict(group=group, topic=topic, third=third, model=model, **m)

# ---------------- diagrams ----------------
def cube(x0, y0, s, label=None, side=None):
    d = s * 0.45
    b = f'<polygon points="{x0},{y0} {x0+s},{y0} {x0+s},{y0+s} {x0},{y0+s}" fill="none" {SW}/>'
    b += f'<polygon points="{x0},{y0} {x0+d},{y0-d} {x0+s+d},{y0-d} {x0+s},{y0}" fill="none" {SW}/>'
    b += f'<polygon points="{x0+s},{y0} {x0+s+d},{y0-d} {x0+s+d},{y0+s-d} {x0+s},{y0+s}" fill="none" {SW}/>'
    if label: b += txt(x0 + s/2, y0 + s/2 + 5, label, 15, style='font-weight="600"')
    if side: b += txt(x0 + s/2, y0 + s + 18, side, 13)
    return b
def two_cubes():
    return svg(310, 235, cube(20, 176, 32, 'A', '3 cm') + cube(100, 80, 128, 'B'))

def thousands_cube(n=10, s=11):
    d = s*0.5; W = n*s; x0, y0 = 10, 10 + n*d
    b = ''
    for i in range(n+1):
        b += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s}" y2="{y0+W}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0}" y1="{y0+i*s}" x2="{x0+W}" y2="{y0+i*s}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s+n*d}" y2="{y0-n*d}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+i*d}" y1="{y0-i*d}" x2="{x0+W+i*d}" y2="{y0-i*d}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+W+i*d}" y1="{y0-i*d}" x2="{x0+W+i*d}" y2="{y0+W-i*d}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+W}" y1="{y0+i*s}" x2="{x0+W+n*d}" y2="{y0+i*s-n*d}" stroke="currentColor" stroke-width="1"/>'
    return svg(int(x0+W+n*d+12), int(y0+W+12), b)

# rotation: E on the left of a dashed line, F = E turned clockwise a quarter turn, on the right
E_CELLS = {(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)}          # (col, row), row grows downward
def norm(cells):
    mx, my = min(c for c, r in cells), min(r for c, r in cells)
    return frozenset((c - mx, r - my) for c, r in cells)
def cw(cells): return norm({(-r, c) for c, r in cells})      # screen clockwise
def ccw(cells): return norm({(r, -c) for c, r in cells})
def flipv(cells): return norm({(-c, r) for c, r in cells})   # flip over a vertical line
F_CELLS = cw(E_CELLS)
assert F_CELLS != norm(E_CELLS)                 # A: a slide alone does not work
assert F_CELLS != ccw(E_CELLS)                  # B: counterclockwise turn does not work
assert F_CELLS != ccw(flipv(E_CELLS))           # D: flip then counterclockwise does not work
assert F_CELLS != flipv(E_CELLS)                # a flip alone does not work either
def rot_fig():
    u = 28; b = ''
    for c, r in E_CELLS: b += f'<rect x="{20+c*u}" y="{30+r*u}" width="{u}" height="{u}" fill="var(--ink-muted)" fill-opacity="0.35" {SW}/>'
    for c, r in F_CELLS: b += f'<rect x="{200+c*u}" y="{30+r*u}" width="{u}" height="{u}" fill="var(--ink-muted)" fill-opacity="0.35" {SW}/>'
    b += '<line x1="150" y1="10" x2="150" y2="140" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 5"/>'
    b += txt(62, 135, 'Figure E', 13) + txt(242, 135, 'Figure F', 13)
    return svg(300, 145, b)

def l_shape():  # top arm 5 wide, full height 11, bottom 12 wide, right lower side 4
    s = 14; x0, y0 = 40, 20
    pts = [(0, 0), (5, 0), (5, 7), (12, 7), (12, 11), (0, 11)]
    poly = ' '.join(f'{x0+x*s},{y0+y*s}' for x, y in pts)
    b = f'<polygon points="{poly}" fill="none" {SW}/>'
    b += txt(x0+2.5*s, y0-6, '5 ft') + txt(x0-6, y0+5.5*s+4, '11 ft', anchor='end') + txt(x0+6*s, y0+11*s+18, '12 ft') + txt(x0+12*s+6, y0+9*s+4, '4 ft', anchor='start')
    return svg(260, 200, b)

def venn_overlap():
    b = ('<defs><clipPath id="v11l"><circle cx="120" cy="95" r="80"/></clipPath></defs>'
         '<circle cx="210" cy="95" r="80" fill="var(--ink-muted)" fill-opacity="0.45" clip-path="url(#v11l)"/>')
    b += f'<circle cx="120" cy="95" r="80" fill="none" {SW}/><circle cx="210" cy="95" r="80" fill="none" {SW}/>'
    b += txt(85, 192, 'Play piano or violin', 12) + txt(250, 192, 'Play violin or drums', 12)
    return svg(330, 200, b)

def number_line():
    # ticks every 4 from 0 to 40; labels only at 0 and 20; C at 12, D at 28
    x = lambda v: 20 + v * 7
    b = f'<line x1="{x(0)-8}" y1="50" x2="{x(40)+18}" y2="50" {SW}/><polygon points="{x(40)+22},50 {x(40)+12},45 {x(40)+12},55" fill="currentColor"/>'
    for v in range(0, 41, 4): b += f'<line x1="{x(v)}" y1="43" x2="{x(v)}" y2="57" {SW}/>'
    b += txt(x(0), 75, '0', 14) + txt(x(20), 75, '20', 14)
    for v, L in ((12, 'C'), (28, 'D')): b += f'<circle cx="{x(v)}" cy="50" r="5" fill="currentColor"/>' + txt(x(v), 33, L, 15, style='font-style="italic"')
    return svg(330, 85, b)
NL_C, NL_D = 12, 28

def floor_grid(cols, rows, white):
    u, b = 28, ''
    for r in range(rows):
        for c in range(cols):
            fill = 'var(--surface,#fff)' if (r, c) in white else 'var(--ink-muted)'
            b += f'<rect x="{c*u+2}" y="{r*u+2}" width="{u}" height="{u}" fill="{fill}" {SW}/>'
    return svg(cols*u+4, rows*u+4, b)
WHITE = {(0, 3), (1, 1), (1, 6), (2, 2), (2, 4), (3, 0), (3, 5), (4, 3), (4, 7), (0, 7)}
assert len(WHITE) == 10 and all(r < 5 and c < 8 for r, c in WHITE)


def segment():
    # points only, as on the real tests; left to right B, A, D, C
    X = [('B', 20), ('A', 95), ('D', 215), ('C', 300)]
    b = f'<line x1="20" y1="40" x2="300" y2="40" {SW}/>'
    for k, v in X: b += f'<circle cx="{v}" cy="40" r="4" fill="currentColor"/>' + txt(v, 26, k, 15, style='font-style="italic"')
    return svg(320, 55, b)

WHY = {
 'ORDER': 'high error rate, 4 of 10 wrong since 10/25 (last wrong QR10 #13)',
 'DATA': 'high error rate, 3 of 6 wrong since 10/25 (last wrong QR10 #1)',
 'DIV': 'high error rate overall (7 of 23), divisible-by-8 still owed',
 'MULT': 'high error rate (3 of 8), missed QR9 #36 and Lower 5 MA #29',
 'IO': 'recent misses (QR10 #5, #26)',
 'WHO': 'missed on Lower 3; not practiced since 10/14 (3+ weeks)',
 'SCALE': 'missed in QR2; not practiced since 10/6 (3+ weeks)',
 'UNIT': '4 of her last 5 wrong',
 'DEC': '4 of her last 5 wrong',
 'EST': '2 of last 5 wrong; a / b x c estimate missed 3 times in a row',
 'LINEQ': 'missed Lower 1 QR #33 and MA4 #28 (a group times an amount each); symbol version never practiced since',
 'TOTALCOST': 'missed Lower 6 MA #30 (11/8), the last problem on that test',
 'SHAPES': 'missed on the Official Lower test (MA #18)',
 'SPLIT': 'high error rate (3 of 8), last wrong QR9 #27',
 'CUBE': 'high error rate (4 of 11), 4 of 7 real-test items wrong',
 'PCTWORD': 'high error rate (5 of 11), last wrong QR10 #6',
 'NUMPROP': 'missed MA5 #21 (minus before a group)',
 'RECT': '2 of last 5 wrong',
 'AVGMIX': 'missed before; not practiced since 10/27 (3 weeks)',
 'TRI': 'missed MA4 #17',
 'NUMLINE': '4 real last-third items; not practiced since 10/25 (3+ weeks)',
 'PROB': 'missed on the Official Lower test (QR #34)',
 'NTH': '3 of her last 5 wrong',
 'UNITPRICE': '2 of 4 wrong; not practiced since 10/27 (3 weeks)',
 'AREAS': 'high error rate (4 of 9)',
 'GEOFORM': '2 of last 5 wrong',
 'MSUNIT': 'high error rate (6 of 16), last wrong QR9 #12',
 'DIGIT': 'sticky: 3 of 6 wrong, 2 of 3 real tests (last: Official QR #36)',
 'PCT': '3 of her last 5 wrong',
 'REMFRAC': 'high error rate (5 of 15), 2 of last 5 wrong',
 'OOO': '2 of last 5 wrong (minus before a group)',
}

# ================= MIDDLE-THIRD TYPES (1-8) =================
# 3 order fractions (Lower 3 QR #20 wrong; QR10 #13 wrong)
fr = [F(3, 5), F(2, 3), F(5, 8), F(4, 7)]
assert sorted(fr) == [F(4, 7), F(3, 5), F(5, 8), F(2, 3)]
add('Comparing & Ordering Fractions & Decimals', 'ORDER', 'middle', f'Which list shows {frac(3,5)}, {frac(2,3)}, {frac(5,8)}, and {frac(4,7)} in order from least to greatest?',
    [f'{frac(4,7)}, {frac(3,5)}, {frac(5,8)}, {frac(2,3)}', f'{frac(4,7)}, {frac(5,8)}, {frac(3,5)}, {frac(2,3)}', f'{frac(3,5)}, {frac(2,3)}, {frac(5,8)}, {frac(4,7)}', f'{frac(2,3)}, {frac(3,5)}, {frac(4,7)}, {frac(5,8)}'], 'A',
    'Compare each to a decimal: 4/7 &asymp; 0.57, 3/5 = 0.6, 5/8 = 0.625, 2/3 &asymp; 0.67. Write them down before ordering. B swaps 3/5 and 5/8. C is just the order they were given in. D orders them by the bottom number (3, 5, 7, 8).',
    'Lower 3 QR #20 (gid 139) and QR10 #13: ordering 4 fractions, both wrong')
# 4 statement to find greater fraction (Lower 1 QR #22 wrong; PT6 #29)
assert F(5, 8) == F(15, 24) and F(7, 12) == F(14, 24) and F(5, 8) > F(7, 12) and F(10, 16) > F(7, 12)
add('Comparing & Ordering Fractions & Decimals', 'ORDER', 'middle', f'Ana walked {frac(5,8)} of a mile. Ben walked {frac(7,12)} of a mile. Which statement shows how to find the greater distance?',
    [f'{frac(5,8)} = {frac(15,24)} and {frac(7,12)} = {frac(14,24)}, so {frac(5,8)} &gt; {frac(7,12)}', f'{frac(5,8)} = {frac(15,24)} and {frac(7,12)} = {frac(14,24)}, so {frac(5,8)} &lt; {frac(7,12)}', f'{frac(7,12)} has the greater bottom number, so {frac(7,12)} &gt; {frac(5,8)}', f'{frac(5,8)} = {frac(10,16)} and {frac(10,16)} &lt; {frac(7,12)}'], 'A',
    'Make the bottoms the same: 5/8 = 15/24 and 7/12 = 14/24. 15/24 is more, so Ana&rsquo;s 5/8 is greater. B has the right fractions but the wrong sign. C uses the bottom number only. D is false: 10/16 = 0.625 is more than 7/12.',
    'Lower 1 QR #22 (gid 60, wrong) and Lower 6 QR #29 (gid 1530)')
# 10 categories (Lower 6 QR #38 wrong, QR10 #1 wrong)
add('Data Collection & Random Sampling', 'DATA', 'middle', 'Maya watched a bird feeder and listed what she observed in categories or groups.<div style="margin-top:6px">1. Kind of bird: robin, cardinal, sparrow</div><div>2. Color of each bird&rsquo;s feathers</div><div>3. ?</div><div style="margin-top:6px">Which information best completes Maya&rsquo;s list?</div>',
    ['the side of the feeder each bird landed on: left or right', 'the number of seeds each bird ate', 'how many minutes each bird stayed', 'the weight of each bird, in grams'], 'A',
    'Items 1 and 2 are categories (words), not numbers. Only A is a category. B, C, and D are all numbers you count or measure.',
    'Lower 6 QR #38 (gid 1539, wrong) and QR10 #1 (wrong)')
# 11 divisible by 3 and 8 (Lower 1 QR #20 wrong; Lower 2 MA #24 wrong)
ch11 = [312, 316, 328, 333]
assert [x for x in ch11 if x % 3 == 0 and x % 8 == 0] == [312] and 328 % 8 == 0 and 333 % 3 == 0
add('No Remainder when Divided by a given Number', 'DIV', 'middle', 'Which whole number is divisible by both 3 and 8 without a remainder?',
    ['312', '316', '328', '333'], 'A',
    'By 3: the digits add to a multiple of 3. 3 + 1 + 2 = 6, yes. By 8: 312 &divide; 8 = 39, yes. C works for 8 (328 &divide; 8 = 41) but not 3 (digits add to 13). D works for 3 but is odd, so not 8.',
    'Lower 1 QR #20 (gid 58, wrong) and Lower 2 MA #24 (divisible by 8, wrong)')

# counting multiples in a range (QR9 #36 wrong, Lower 5 MA #29 wrong)
cnt6 = [k for k in range(39, 95) if k % 2 == 0 and k % 3 == 0]
assert len(cnt6) == 9 and cnt6[0] == 42 and cnt6[-1] == 90
add('Counting Multiples within a Range', 'MULT', 'middle', 'How many whole numbers between 38 and 95 have both 2 and 3 as factors?',
    ['8', '9', '10', '15'], 'B',
    'Having both 2 and 3 as factors means being a multiple of 6. The first one after 38 is 42 (6 &times; 7) and the last before 95 is 90 (6 &times; 15). From 7 to 15 is 15 &minus; 7 + 1 = 9 numbers. 8 forgets the +1. 15 is just the last multiplier.',
    'QR9 #36 (wrong) and Lower 5 MA #29 (wrong)')

# input/output: the rule must fit EVERY row (QR10 #26 wrong, QR10 #5 wrong)
rows_io = [(2, 5), (3, 10), (5, 26), (7, 50)]
rules = {'A': lambda t: t*t + 1, 'B': lambda t: t*2 + 1, 'C': lambda t: t*5 - 5, 'D': lambda t: t + 3}
assert [k for k, f in rules.items() if all(f(a) == b for a, b in rows_io)] == ['A']
assert rules['C'](2) == 5 and rules['C'](3) == 10 and rules['C'](5) != 26
add('Input Output Tables', 'IO', 'middle', 'The table shows how a number machine changes each input number (&#9651;) into an output number (&#9632;). Which equation shows the rule for the number machine?' +
    table(['Input (&#9651;)', 'Output (&#9632;)'], rows_io),
    ['&#9651; &times; &#9651; + 1 = &#9632;', '&#9651; &times; 2 + 1 = &#9632;', '&#9651; &times; 5 &minus; 5 = &#9632;', '&#9651; + 3 = &#9632;'], 'A',
    'Check a rule on EVERY row, not just the first one. &#9651; &times; &#9651; + 1: 2&rarr;5, 3&rarr;10, 5&rarr;26, 7&rarr;50, all work. &#9651; &times; 5 &minus; 5 works for the first two rows but gives 20 for 5. &#9651; &times; 2 + 1 and &#9651; + 3 work only for 2.',
    'QR10 #26 (wrong: checked one row) and QR10 #5 (wrong)')

# "who am I" (Lower 3 QR #11 wrong) - not practiced since 10/14
cands_who = [k for k in range(51, 80) if k > 63 and k % 2 == 0 and k % 9 == 0]
assert cands_who == [72]
add('Whole Number Who am I', 'WHO', 'middle', 'Lena picked a whole number greater than 50 and less than 80. When Max guessed 63, Lena said her number is greater than 63, is even, and is divisible by 9. What is Lena&rsquo;s number?',
    ['63', '66', '72', '81'], 'C',
    'Multiples of 9 between 63 and 80: 72 only (81 is too big). 72 is even. 66 is even but not divisible by 9 (6 + 6 = 12). 63 is not greater than 63.',
    'Lower 3 QR #11 (wrong), Lower 4 QR #13, Lower 1 QR #2')

# map scale (QR2 #25 wrong) - not practiced since 10/6
d_scale = F(9, 2) * 15
assert d_scale == F(135, 2)
add('Measurement Scaling', 'SCALE', 'middle', 'On a map, 2 centimeters stand for 15 kilometers. Two towns are 9 centimeters apart on the map. How far apart are the real towns?',
    ['18 kilometers', '67.5 kilometers', '135 kilometers', '270 kilometers'], 'B',
    '1 centimeter stands for 15 &divide; 2 = 7.5 kilometers. 9 &times; 7.5 = 67.5 kilometers. 135 uses 15 km for each centimeter (forgets the 2). 18 is 9 &times; 2.',
    'QR2 #24-#25 scale problems (#25 wrong)')

# ================= LAST-THIRD TYPES (9-38) =================
# 9 unit conversion statement (Lower 6 QR #25 wrong; last 5 attempts 4 wrong)
assert 8*3*12 == 288 < 300 and 8*12 == 96
add('English Unit Conversions', 'UNIT', 'last', 'A roll has 8 yards of ribbon. There are 3 feet in 1 yard and 12 inches in 1 foot. Mia needs 300 inches of ribbon. Which statement best explains whether Mia has enough ribbon?',
    ['Since 8 &times; 3 &times; 12 is less than 300, Mia does not have enough ribbon.', 'Since 8 &times; 3 &times; 12 is less than 300, Mia has enough ribbon.', 'Since 8 &times; 12 is less than 300, Mia does not have enough ribbon.', 'Since 8 &times; 3 &times; 12 is greater than 300, Mia has enough ribbon.'], 'A',
    'Yards to feet: 8 &times; 3 = 24 feet. Feet to inches: 24 &times; 12 = 288 inches. 288 is less than 300, so she does not have enough. C skips the feet step (12 inches in a yard, the QR10 #11 slip). D is wrong arithmetic.',
    'Lower 6 QR #25 (gid 1526, wrong) with two steps, like QR10 #11')

# fractions and decimals mixed: longest minus shortest (QR10 #14 wrong, MA5 #16 wrong)
runs = {'Monday': F(3, 5), 'Tuesday': F(65, 100), 'Wednesday': F(5, 8)}
assert max(runs.values()) - min(runs.values()) == F(5, 100) and F(65, 100) - F(5, 8) == F(25, 1000)
add('Converting to a Decimal', 'DEC', 'last', f'Lisa ran {frac(3,5)} mile on Monday, 0.65 mile on Tuesday, and {frac(5,8)} mile on Wednesday. How much farther did she run on her longest day than on her shortest day?',
    ['0.025 mile', '0.05 mile', '0.075 mile', '0.25 mile'], 'B',
    'Write every distance as a decimal first: 3/5 = 0.6, 0.65, 5/8 = 0.625. Longest is 0.65 (Tuesday), shortest is 0.6 (Monday). 0.65 &minus; 0.6 = 0.05. 0.025 compares Tuesday with Wednesday instead of the shortest day.',
    'QR10 #14 and MA5 #16 (both wrong)')
# 15 a / b x c range (Lower 6 QR #36 wrong; MA5 #15 wrong)
v15 = F(75, 11) * 190
assert 1200 < v15 < 1500 and 900 < 6*190 < 1200 and 1200 < 7*200 < 1500
add('Estimating Multiplication & Division', 'EST', 'last', 'Sam did the problem 75 &divide; 11 &times; 190 on a calculator. Approximately what was his answer?',
    ['between 600 and 900', 'between 900 and 1,200', 'between 1,200 and 1,500', 'between 1,500 and 1,800'], 'C',
    'Work left to right. 75 &divide; 11 is about 7 (77 &divide; 11 = 7). 7 &times; 190 is about 7 &times; 200 = 1,400. Exact: about 1,295. B comes from cutting 75 &divide; 11 down to 6.',
    'Lower 6 QR #36 (gid 1537, wrong) and MA5 #15 (wrong): third time on this type')

# quadrilateral: properties to name (Official MA #18 wrong)
add('Identifying Shapes', 'SHAPES', 'last', 'A quadrilateral has exactly one pair of parallel sides. Its other two sides are equal in length. Which statement about this quadrilateral is true?',
    ['It is a parallelogram, because two of its sides are equal.', 'It is a rhombus, because it has parallel sides.', 'It is a trapezoid, because it has exactly one pair of parallel sides.', 'It is a rectangle, because its opposite sides are equal.'], 'C',
    'Exactly ONE pair of parallel sides is the trapezoid rule. A parallelogram, a rhombus, and a rectangle all have TWO pairs. (On the Official Lower test she called a shape with two pairs a trapezoid.)',
    'Official MA #18 (wrong), Lower 5 MA #28 (wrong)')

# split segment (QR9 #27 wrong)
for xv, yv in ((20, 6), (31, 9)):
    bc = xv - 5 - yv
    assert bc == xv - 5 - yv and bc != xv - 5 + yv and bc != xv + 5 + yv
add('Split Line Segments', 'SPLIT', 'last', 'Use the figure. The length of BC is x. The length of AB is 5. The length of CD is y. What is the length of AD?',
    ['x &minus; 5 &minus; y', 'x &minus; 5 + y', 'x + 5 + y', '5 + y &minus; x'], 'A',
    'Read the order from the picture: B, A, D, C. The whole segment is BC = x. AD is what is left after taking away AB (5) and DC (y): x &minus; 5 &minus; y. Try numbers: if BC = 20, AB = 5, CD = 6, then AD = 9 = 20 &minus; 5 &minus; 6. x &minus; 5 + y adds CD back. Label each piece on the picture before choosing.',
    'QR9 #27 (wrong), MA4 #21, QR10 #18', segment())
# 19 thousands cubes (Lower 5 QR #38, wrong)
assert 20 * 1000 == 2*10*10*10*10
add('Comparing Volume of Cubes', 'CUBE', 'last', 'The thousands cube shown has a volume of 1,000 cubic centimeters. Exactly 20 of these thousands cubes are used to build a new figure. Which expression shows the volume of the new figure, in cubic centimeters?',
    ['2 &times; 10', '2 &times; 10 &times; 10 &times; 10', '2 &times; 10 &times; 10 &times; 10 &times; 10', '2 &times; 10 &times; 10 &times; 10 &times; 10 &times; 10'], 'C',
    '20 &times; 1,000 = 20,000. 20 = 2 &times; 10 and 1,000 = 10 &times; 10 &times; 10, so 20,000 = 2 &times; 10 &times; 10 &times; 10 &times; 10 (four 10s). B is only 2,000.',
    'Lower 5 QR #38 (gid 1494, wrong)', thousands_cube())

# find the regular price from the discount, then one more step (QR10 #6 wrong, Lower 6 MA #28 wrong)
reg = 9 * 4; sale = reg - 9
assert F(9, reg) == F(25, 100) and sale == 27 and 40 - sale == 13
add('Percent Word Problems', 'PCTWORD', 'last', 'A store has 25% off everything. The discount on a backpack is $9. Rosa buys the backpack at the sale price and pays with a $40 bill. How much change does Rosa get?',
    ['$4', '$9', '$13', '$31'], 'C',
    '$9 is 25% (one fourth) of the regular price, so the regular price is 4 &times; $9 = $36. Sale price: $36 &minus; $9 = $27. Change: $40 &minus; $27 = $13. $31 takes only the discount from $40. $4 uses the regular price. $9 stops at the discount.',
    'QR10 #6 and Lower 6 MA #28 (both wrong: finding the whole from the discount)')

# minus in front of a times-group (MA5 #21 wrong)
v_np = 400 - 8*(30 - 4)
ex_np = {'A': 400 - 8*30 - 4, 'B': 400 - 8*30 - 8*4, 'C': 400 - 8*30 + 8*4, 'D': (400 - 8)*(30 - 4)}
assert v_np == 192 and [k for k, v in ex_np.items() if v == v_np] == ['C']
add('Identifying Number Properties', 'NUMPROP', 'last', 'Which expression is equivalent to 400 &minus; 8 &times; (30 &minus; 4)?',
    ['400 &minus; (8 &times; 30) &minus; 4', '400 &minus; (8 &times; 30) &minus; (8 &times; 4)', '400 &minus; (8 &times; 30) + (8 &times; 4)', '(400 &minus; 8) &times; (30 &minus; 4)'], 'C',
    '8 &times; (30 &minus; 4) = 8 &times; 30 &minus; 8 &times; 4 = 240 &minus; 32 = 208, and 400 &minus; 208 = 192. Taking away the whole group flips the inside minus to a plus: 400 &minus; 240 + 32 = 192. The second choice keeps the minus (it gives 128).',
    'MA5 #21 (wrong: the same type, she had the right answer and changed it)')

# rectangle with W = L / 3 and a perimeter (Lower 2 QR #25 wrong; QR9 #35 wrong)
Lr, Wr = 18, 6
assert Wr == Lr / 3 and 2*(Lr + Wr) == 48 and Lr*Wr == 108
add('Finding Area/Perimeter of Rectangle, given Length & Width', 'RECT', 'last', 'The width of a rectangle is the length divided by 3. The perimeter of the rectangle is 48 feet. What is the area of the rectangle?',
    ['36 square feet', '72 square feet', '108 square feet', '144 square feet'], 'C',
    'Length = 3 widths. Perimeter = width + 3 widths + width + 3 widths = 8 widths = 48, so the width is 6 and the length is 18. Area = 18 &times; 6 = 108. 144 treats it as a 12 by 12 square. 36 is 6 &times; 6.',
    'Lower 2 QR #25 (gid 103, wrong) and QR9 #35 (wrong)')
# 13 mean of mixed numbers (What to Expect QR #18, wrong)
w = [F(5, 2), F(5, 2), F(7, 2), F(9, 2)]
assert sum(w) / 4 == F(13, 4) and (F(5, 2) + F(7, 2) + F(9, 2)) / 3 == F(7, 2)
add('Averaging Mixed Numbers', 'AVGMIX', 'last', 'A dog had 4 puppies. Two puppies weighed 2&frac12; pounds each, one weighed 3&frac12; pounds, and one weighed 4&frac12; pounds. What is the mean weight of the puppies?',
    ['3 pounds', '3&frac14; pounds', '3&frac12; pounds', '3&frac34; pounds'], 'B',
    'Add all four: 2&frac12; + 2&frac12; + 3&frac12; + 4&frac12; = 13. Divide by 4 puppies: 13 &divide; 4 = 3&frac14;. C counts 2&frac12; only once and divides by 3.',
    'What to Expect QR #18 (gid 18, wrong)')

# triangle area vs height (MA4 #17 wrong)
for h in (2, 5, 9): assert F(1, 2) * 14 * h == 7 * h
add('Area of Triangles', 'TRI', 'last', 'The base of a triangle is 14 centimeters. Which statement correctly compares the area, A, to the height of the triangle? (A = ' + frac(1, 2) + ' &times; base &times; height)',
    ['The value of A is always 7 times the value of the height.', 'The value of A is always 14 times the value of the height.', f'The value of A is always {frac(1,2)} the value of the height.', 'The value of A is always 28 times the value of the height.'], 'A',
    'A = 1/2 &times; 14 &times; height = 7 &times; height. The second choice forgets the 1/2. The third uses only the 1/2. The last doubles instead of halving.',
    'MA4 #17 (wrong), QR10 #20, MA5 #28')
# 32 midpoint on a number line (Lower 2 QR #33)
assert 2*NL_D - NL_C == 44
add('Determining Averages between Points on Number Lines', 'NUMLINE', 'last', 'The tick marks on the number line are evenly spaced. D is the midpoint between C and another point, E. What is the value of E?',
    ['16', '20', '40', '44'], 'D',
    'Each tick is 4 (5 jumps from 0 to 20). C = 12 and D = 28. From C to D is 16, so E is 16 more than D: 28 + 16 = 44. 16 stops at the distance between C and D. 40 adds C and D.',
    'Lower 2 QR #33 (gid 112) and What to Expect QR #35 (gid 37)', number_line())

# yards, feet, inches statements (QR8 #6 wrong)
def inches(yd, ft, inch): return yd*36 + ft*12 + inch
r1, r2, r3 = inches(2, 2, 5), inches(3, 0, 1), inches(1, 5, 5)
assert (r1, r2, r3) == (101, 109, 101)
st_e = {'A': r1 > r3, 'B': r3 > r2, 'C': r1 == r3, 'D': r1 > r2}
assert st_e == {'A': False, 'B': False, 'C': True, 'D': False}
add('English Unit Conversions', 'UNIT', 'last', 'Sam cut three pieces of rope.<div style="margin-top:6px">Rope 1: 2 yards, 2 feet, 5 inches</div><div>Rope 2: 3 yards, 1 inch</div><div>Rope 3: 1 yard, 5 feet, 5 inches</div><div style="margin-top:6px">Which statement is true? (1 yard = 3 feet; 1 foot = 12 inches)</div>',
    ['Rope 1 is longer than Rope 3.', 'Rope 3 is longer than Rope 2.', 'Rope 1 and Rope 3 are the same length.', 'Rope 1 is longer than Rope 2.'], 'C',
    'Change each to inches. Rope 1: 72 + 24 + 5 = 101. Rope 2: 108 + 1 = 109. Rope 3: 36 + 60 + 5 = 101. Ropes 1 and 3 are both 101 inches. Rope 3 looks shorter only because it has 1 yard, but its 5 feet make up for it.',
    'QR8 #6 (wrong) and Lower 3 QR #25 (gid 144)')
# 25 probability, unknown count (Official QR #34, wrong)
known = [5, 7, 4, 8]
sol = [p for p in range(1, 50) if F(p, sum(known) + p) == F(1, 4)]
assert sum(known) == 24 and sol == [8] and sum(known) // 4 == 6
add('Finding Ratios given Probability', 'PROB', 'last', 'The table shows the number of each color of marble in a bag. The probability of picking a purple marble without looking is ' + frac(1, 4) + '. How many purple marbles are in the bag?' +
    table(['Color', 'Number'], [['Red', 5], ['Blue', 7], ['Green', 4], ['Yellow', 8], ['Purple', '?']], 'MARBLES IN THE BAG'),
    ['4', '6', '8', '12'], 'C',
    'The other marbles: 5 + 7 + 4 + 8 = 24. The total must include the purple ones. Check 8: 8 out of 24 + 8 = 32, and 8/32 = 1/4. 6 is 1/4 of 24, leaving purple out of the total (the Official Lower test slip).',
    'Official QR #34 (gid 1573, wrong) and Lower 5 QR #37 (gid 1493, 145 s)')

# nth term from the start (QR8 #23 wrong)
seq = [7 + 4*k for k in range(25)]
assert seq[:4] == [7, 11, 15, 19] and seq[24] == 103 and 7 + 25*4 == 107
add('Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.', 'NTH', 'last', 'A sequence begins 7, 11, 15, 19, &hellip; What is the 25th number in the sequence?',
    ['99', '103', '107', '111'], 'B',
    'The 1st number is 7. To reach the 25th you add 4 only 24 times (one fewer than 25). 7 + 24 &times; 4 = 7 + 96 = 103. 107 adds 4 twenty-five times, the off-by-one slip.',
    'QR8 #23 (wrong) and QR7 #6')

# unit price difference (QR8 #12 wrong, QR4 #1 wrong) - not practiced since 10/27
a_each, b_each = F(420, 6), F(650, 10)   # cents
assert (a_each, b_each, a_each - b_each) == (70, 65, 5)
add('Finding Unit Price', 'UNITPRICE', 'last', 'Pack A has 6 granola bars for $4.20. Pack B has 10 granola bars for $6.50. How much more does one bar in Pack A cost than one bar in Pack B?',
    ['$0.05', '$0.65', '$0.70', '$2.30'], 'A',
    'Pack A: $4.20 &divide; 6 = $0.70 per bar. Pack B: $6.50 &divide; 10 = $0.65 per bar. $0.70 &minus; $0.65 = $0.05. $2.30 subtracts the pack prices. $0.70 and $0.65 stop at one price.',
    'QR8 #12 and QR4 #1 (both wrong)')
# total with a partial 2-for-1 match (Lower 6 MA #30 wrong: employer matches every dollar; she picked $106 not $212)
wk = {'Week 1': 15, 'Week 2': 20, 'Week 3': 12, 'Week 4': 18}
class_total = sum(wk.values()); store = 2 * (wk['Week 3'] + wk['Week 4'])
assert (class_total, store, class_total + store) == (65, 60, 125)
assert class_total + (wk['Week 3'] + wk['Week 4']) == 95 and 2 * class_total == 130 and 3 * class_total == 195
add('Determining Total Cost', 'TOTALCOST', 'last', 'Mia&rsquo;s class collected money for an animal shelter for 4 weeks. The table shows how much the class collected each week.' +
    table(['Week', 'Money collected'], [[k, f'${v}'] for k, v in wk.items()], 'MONEY FOR THE SHELTER') +
    'A pet store promised that for every $1 the class collected in Week 3 and Week 4, the store would give $2 more to the shelter. What was the total amount of money the shelter received?',
    ['$95', '$125', '$130', '$195'], 'B',
    'Class total: 15 + 20 + 12 + 18 = $65. The store only matches Weeks 3 and 4: 12 + 18 = $30, and $2 for every $1 is 2 &times; 30 = $60. The shelter gets both: 65 + 60 = $125. $95 gives only $1 for each $1. $130 matches every week $1 for $1. $195 matches every week with $2.',
    'Lower 6 MA #30 (wrong, 11/8: the match was left out of the total)')
# 33 compare areas and perimeters (Lower 2 QR #38, wrong)
assert 10*10 == 5*20 and 4*10 < 2*(5+20)
add('Comparing Areas', 'AREAS', 'last', 'The floor of Room A is a square with an area of 100 square feet. The floor of Room B is a rectangle 5 feet wide and 20 feet long. Which statement correctly compares the two floors?',
    ['The area of Room A is greater than the area of Room B.', 'The area of Room A is less than the area of Room B.', 'The perimeter of Room A is equal to the perimeter of Room B.', 'The perimeter of Room A is less than the perimeter of Room B.'], 'D',
    'Room A: 10 &times; 10 = 100, so its sides are 10 and its perimeter is 40. Room B: area 5 &times; 20 = 100 (the same), perimeter 5 + 20 + 5 + 20 = 50. 40 is less than 50.',
    'Lower 2 QR #38 (gid 117, wrong)')

# pour out a fraction and a decimal, estimate what is left (QR9 #13 wrong)
left = F(32, 10) - F(3, 4) - F(16, 10)
assert left == F(85, 100) and F(3, 4) < left < 1 and F(32, 10) - F(34, 100) - F(16, 10) > 1
add('Converting to a Decimal', 'DEC', 'last', f'A jug holds 3.2 liters of juice. Ben pours {frac(3,4)} liter into one pitcher and 1.6 liters into another pitcher. How much juice is left in the jug?',
    [f'less than {frac(1,2)} liter', f'more than {frac(1,2)} liter and less than {frac(3,4)} liter', f'more than {frac(3,4)} liter and less than 1 liter', f'more than 1 liter and less than 1{frac(1,2)} liters'], 'C',
    '3/4 = 0.75. 3.2 &minus; 0.75 &minus; 1.6 = 0.85 liter, which is between 3/4 (0.75) and 1. The last choice comes from reading 3/4 as 0.34.',
    'QR9 #13 (wrong) and MA4 #9')
# shape from several conditions (Official MA #18 wrong, Lower 5 MA #28 wrong; Lower 6 MA #27 right but 171 s)
PROPS = {'trapezoid': dict(par=1, eq=False, right=False), 'rectangle': dict(par=2, eq=False, right=True),
         'rhombus': dict(par=2, eq=True, right=False), 'square': dict(par=2, eq=True, right=True)}
# "always two pairs parallel, always 4 equal sides, does NOT always have right angles"
assert [k for k, v in PROPS.items() if v['par'] == 2 and v['eq'] and not v['right']] == ['rhombus']
add('Identifying Shapes', 'SHAPES', 'last', 'Which shape ALWAYS has two pairs of parallel sides and four sides of equal length, but does NOT always have four right angles?',
    ['trapezoid', 'rectangle', 'rhombus', 'square'], 'C',
    'Check all three conditions. A rhombus has two pairs of parallel sides and 4 equal sides, and its angles do not have to be right angles. A square always has right angles. A rectangle does not always have 4 equal sides. A trapezoid has only one pair of parallel sides.',
    'Official MA #18 and Lower 5 MA #28 (both wrong), Lower 6 MA #27 (171 s)')

# formula rearranged (QR7 #37 wrong)
for w in (2, 3, 4, 6):
    assert (F(12) / w) * w * 5 == 60 and (12 * w) * w * 5 != 60 and (F(55) / w) * w * 5 != 60 and (F(300) / w) * w * 5 != 60
add('Solving Problems with Geometric Formulas', 'GEOFORM', 'last', 'The volume of a rectangular prism is 60 cubic inches. Its height is 5 inches. Which equation can be used to find the length, l, of the prism? (V = l &times; w &times; h)',
    ['l = 12 &divide; w', 'l = 12 &times; w', 'l = 55 &divide; w', 'l = 300 &divide; w'], 'A',
    '60 = l &times; w &times; 5. Divide both sides by 5: 12 = l &times; w. Then l = 12 &divide; w. 55 subtracts the height instead of dividing. 300 multiplies by the height.',
    'QR7 #37 (wrong) and QR7 #1 (wrong)')

# mixed-number hours to minutes, then subtract (QR9 #12 wrong) - numbers changed from MA5 #19
total_m = 3*60 + 60 // 3; off_m = 60 + 60*2 // 5
assert (total_m, off_m, total_m - off_m) == (200, 84, 116) and total_m - 24 == 176
add('Multi-step unit conversion (off-by-10, multi-step)', 'MSUNIT', 'last', f'Nora spent 3{frac(1,3)} hours at the park. Of that time, 1{frac(2,5)} hours were spent eating lunch and riding the bus. How many minutes did Nora spend playing? (1 hour = 60 minutes)',
    ['84', '116', '176', '200'], 'B',
    '3 1/3 hours = 180 + 20 = 200 minutes. 2/5 of an hour = 60 &divide; 5 &times; 2 = 24 minutes, so 1 2/5 hours = 84 minutes. 200 &minus; 84 = 116. 176 forgets the 1 whole hour in 1 2/5. 84 is the lunch-and-bus time. 200 is the whole park time.',
    'QR9 #12 (wrong), MA5 #19, MA4 #7')
# 27 digit rules, hundreds place (Official QR #36, wrong)
cands = [int(''.join(p)) for p in permutations('245679') if int(p[-1]) % 2 == 1]
best = min(cands)
assert best == 245679 and str(best)[-3] == '6'
add('Value of Digits', 'DIGIT', 'last', 'Students wrote a new number using the digits 2, 4, 5, 6, 7, and 9 and these rules.' +
    '<div style="border:1px solid var(--border);border-radius:6px;padding:6px 10px;margin:8px 0;max-width:420px"><b>RULES FOR THE NEW NUMBER</b><div>1. The number must have 6 digits.</div><div>2. The number must be odd.</div><div>3. The number must be the smallest number possible.</div><div>4. Each digit can be used only once.</div></div>What digit is in the <b>hundreds</b> place of the new number?',
    ['2', '5', '6', '9'], 'C',
    'Smallest: put the small digits in front. Odd: the ones digit must be 5, 7, or 9; use the biggest odd one (9) at the end so the front stays small: 245,679. Write the places under it: hundreds is 6. A is the first digit.',
    'Official QR #36 (gid 1575, wrong) and Lower 3 QR #31 (gid 150, wrong)')

# overall percent change (QR9 #16 wrong, MA4 #13 wrong)
assert F(150, 100) * F(60, 100) == F(90, 100)
add('Percent Increase Decrease basic', 'PCT', 'last', 'The price of a scooter is increased by 50%. The new price is then decreased by 40%. What is the overall percent increase or percent decrease from the original price?',
    ['percent decrease by 10%', 'percent increase by 10%', 'no change', 'percent decrease by 40%'], 'A',
    'Try a price of $100. Up 50%: $150. Down 40% of $150 is $60, so $90. $90 is 10% less than $100. &ldquo;Increase by 10%&rdquo; comes from 50 &minus; 40, which forgets that the 40% is taken from the bigger price.',
    'QR9 #16 and MA4 #13 (both wrong), Lower 4 QR #38 (wrong)')

# nth term from a middle term (QR9 #26 wrong, MA4 #18 wrong)
t22 = 61 + (22 - 7) * 8
assert t22 == 181 and 61 + 14*8 == 173 and 61 + 16*8 == 189 and 61 + 22*8 == 237
add('Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.', 'NTH', 'last', 'In a sequence, each number is 8 more than the number before it. The 7th number in the sequence is 61. What is the 22nd number in the sequence?',
    ['173', '181', '189', '237'], 'B',
    'From the 7th number to the 22nd number is 22 &minus; 7 = 15 jumps. 15 &times; 8 = 120. 61 + 120 = 181. 173 uses 14 jumps, 189 uses 16 jumps, and 237 uses 22 jumps (counting from the start instead of from the 7th).',
    'QR9 #26 and MA4 #18 (both wrong), MA5 #18')

# percent, then a fraction of what is left (QR8 #31 wrong)
sold = 300 * 40 // 100; unsold = 300 - sold; blue = unsold // 3
assert (sold, unsold, blue) == (120, 180, 60) and sold // 3 == 40 and 300 // 3 == 100
add('Percent Word Problems', 'PCTWORD', 'last', 'A shop had 300 bracelets. On Saturday, 40% of the bracelets were sold. Of the bracelets that were NOT sold, ' + frac(1, 3) + ' were blue. How many of the unsold bracelets were blue?',
    ['40', '60', '100', '120'], 'B',
    '40% of 300 = 120 sold, so 300 &minus; 120 = 180 were not sold. 1/3 of 180 = 60. 40 takes 1/3 of the sold bracelets. 100 takes 1/3 of all 300. 120 stops at the number sold.',
    'QR8 #31 (wrong)')
# 28 digit rules, tens place (Lower 3 QR #31, wrong)
cands = [int(''.join(p)) for p in permutations('13468') if int(p[-1]) % 2 == 0]
best = max(cands)
assert best == 86314 and str(best)[-2] == '1'
add('Value of Digits', 'DIGIT', 'last', 'Students wrote a new number using the digits 1, 3, 4, 6, and 8 and these rules.' +
    '<div style="border:1px solid var(--border);border-radius:6px;padding:6px 10px;margin:8px 0;max-width:420px"><b>RULES FOR THE NEW NUMBER</b><div>1. The number must have 5 digits.</div><div>2. The number must be even.</div><div>3. The number must be the largest number possible.</div><div>4. Each digit can be used only once.</div></div>What digit is in the <b>tens</b> place of the new number?',
    ['1', '3', '4', '8'], 'A',
    'Largest: big digits in front. Even: the ones digit must be 4, 6, or 8; use the smallest even one (4) at the end so the front stays big: 86,314. Tens place is 1. C (4) is the tens digit of 86,341, which is odd.',
    'Lower 3 QR #31 (gid 150, wrong) and Lower 2 QR #35 (gid 114)')

# fraction of what is left, then add (QR9 #38 wrong, MA4 #24 wrong)
c1 = 96 - 96 // 4; c2 = c1 - c1 // 3; c3 = c2 + 10
assert (c1, c2, c3) == (72, 48, 58) and 96 - 24 - 32 + 10 == 50 and 96 - 24 + 10 == 82
add('Remaining Amount after Reducing by Fractions', 'REMFRAC', 'last', f'A library cart had 96 books. In the morning, {frac(1,4)} of the books were put on the shelves. In the afternoon, {frac(1,3)} of the books still on the cart were put on the shelves. Then 10 new books were added to the cart. How many books are on the cart now?',
    ['48', '50', '58', '82'], 'C',
    'Morning: 1/4 of 96 = 24, so 72 are left. Afternoon: 1/3 of 72 = 24, so 48 are left. Add 10: 58. 48 forgets the 10 new books. 50 takes 1/3 of all 96 instead of the 72 left.',
    'QR9 #38 and MA4 #24 (both wrong), QR8 #21')
# grouped story -> expression with symbols (Lower 1 QR #33 wrong: (calls + emails) x minutes each; MA4 #28 wrong: (1,000 + 2,000) / 60)
EXPR = {'A': lambda sq, ci, tr, st: (sq + ci) * tr * st, 'B': lambda sq, ci, tr, st: sq + ci * tr * st,
        'C': lambda sq, ci, tr, st: (sq + ci) * tr + st, 'D': lambda sq, ci, tr, st: sq * ci * tr * st}
for vals in ((3, 5, 20, 2), (4, 2, 30, 3)):
    right = (vals[0] + vals[1]) * vals[2] * vals[3]          # lessons x minutes x dollars per minute
    assert [k for k, f in EXPR.items() if f(*vals) == right] == ['A']
add('Interpreting Linear Equations from Word Problems', 'LINEQ', 'last', 'A tutor taught &#9633; lessons on Monday and &#9675; lessons on Tuesday. Each lesson lasted &#9651; minutes. She was paid &#9734; dollars for every minute she taught. Which expression shows how many dollars she earned on Monday and Tuesday?',
    ['(&#9633; + &#9675;) &times; &#9651; &times; &#9734;', '&#9633; + &#9675; &times; &#9651; &times; &#9734;', '(&#9633; + &#9675;) &times; &#9651; + &#9734;', '&#9633; &times; &#9675; &times; &#9651; &times; &#9734;'], 'A',
    'Build it step by step. Lessons in all: &#9633; + &#9675; (keep them together in brackets). Minutes: (&#9633; + &#9675;) &times; &#9651;. Dollars: that many minutes &times; &#9734;. Try numbers: 3 + 5 = 8 lessons, &times; 20 minutes = 160 minutes, &times; $2 = $320. The choice without brackets multiplies only the Tuesday lessons. Adding &#9734; treats the pay as one extra dollar amount instead of a rate.',
    'Lower 1 QR #33 (gid 71, wrong) and MA4 #28 (wrong)')
# 38 minus before a group (Lower 2 MA #26, MA4 #8, MA5 #21: all wrong)
v38 = 40 - (15 + 9 - 4)
ex38 = {'A': 40 - 15 - 9 + 4, 'B': 40 - 15 + 9 - 4, 'C': 40 - 15 - 9 - 4, 'D': 40 + 15 - 9 + 4}
assert v38 == 20 and [k for k, v in ex38.items() if v == v38] == ['A']
add('Order of Operations and Equivalence', 'OOO', 'last', 'Which expression has the same value as 40 &minus; (15 + 9 &minus; 4)?',
    ['40 &minus; 15 &minus; 9 + 4', '40 &minus; 15 + 9 &minus; 4', '40 &minus; 15 &minus; 9 &minus; 4', '40 + 15 &minus; 9 + 4'], 'A',
    'The minus in front takes away the whole group: 15 + 9 &minus; 4 = 20, and 40 &minus; 20 = 20. Taking away the group flips each sign inside: &minus;15, &minus;9, +4, which gives 20. C forgets to flip the &minus;4 (it gives 12).',
    'Lower 2 MA #26 and MA5 #21 (minus before a bracket, wrong)')

assert len(P) == 38
M2 = {}
for i, p in enumerate(P, 1):
    old = p['n']; p['n'] = i; M2[i] = MAP[old]
MAP = M2
# balance answer letters: problems whose choices are plain numbers keep number order; the others may have
# the right choice swapped into another slot, and letter mentions in the explanation are swapped to match.
import random, re as _re
NUM = _re.compile(r'^\$?[0-9][0-9,]*(\.[0-9]+)?( [a-z ]+)?$')
def _plain(v): return _re.sub(r'&frac[0-9]+;|&[a-z]+;', '', _re.sub('<[^>]+>', '', v)).strip()
def numeric(ch):
    vals = [_plain(v) for v in ch.values()]
    growing = all(vals[i] in vals[i+1] for i in range(3))   # e.g. 2 x 10, 2 x 10 x 10, ...
    return growing or all(NUM.match(v) for v in vals) or all(v.startswith(('between', 'less than', 'more than')) for v in vals)
REF = _re.compile(r'(?<![A-Za-z&;])(?<!Room )(?<!Rope )(?<!Pack )(?<!Cube )(?<!Figure )(?<!Scale )(?<!Point )(?<!Patio )(?<!Garden )([ABCD])(?=[ :,.)])(?! (square|rhombus|rectangle|trapezoid|parallelogram|number|whole|price|store)\b)(?! =)')
def swap_refs(text, a, b):
    head, body = text.split('</b>', 1)
    body = REF.sub(lambda m: {a: b, b: a}.get(m.group(1), m.group(1)), body)
    return head + '</b>' + body
movable = [i for i, p in enumerate(P) if not numeric(p['choices'])]
def ok(L):
    c = Counter(L); return max(c.values()) - min(c.values()) <= 1 and not any(L[i] == L[i+1] == L[i+2] for i in range(36))
rng = random.Random(11)
base = [p['correct'] for p in P]
best = None
for _ in range(50000):
    L = base[:]
    for i in movable: L[i] = rng.choice('ABCD')
    if ok(L):
        moved = sum(1 for x, y in zip(L, base) if x != y)
        if best is None or moved < best[0]: best = (moved, L)
if best is None: raise SystemExit('no balanced assignment; movable=%s' % [i+1 for i in movable])
L = best[1]
for i, p in enumerate(P):
    old, new = p['correct'], L[i]
    if old != new:
        ch = p['choices']; ch[old], ch[new] = ch[new], ch[old]
        p['correct'] = new
        p['key'] = swap_refs(p['key'].replace(f'<b>Answer: {old}.</b>', f'<b>Answer: {new}.</b>', 1), old, new)
        print('moved', i+1, old, '->', new, '|', _re.sub('<[^>]+>', '', p['key'])[:150])
print('movable', [i+1 for i in movable])
L = [p['correct'] for p in P]
cnt = Counter(L); print(cnt, ''.join(L))
assert max(cnt.values()) - min(cnt.values()) <= 1, cnt
assert not any(L[i] == L[i+1] == L[i+2] for i in range(36)), ''.join(L)
tc = Counter(p['topic'] for p in P)
assert max(tc.values()) <= 3, tc
json.dump(P, open(os.path.join(HERE, 'set11_problems.json'), 'w'), indent=1)
json.dump(MAP, open(os.path.join(HERE, 'set11_mapping.json'), 'w'), indent=1, ensure_ascii=False)
print('wrote', len(P), 'diagrams', sum(1 for p in P if p['diagram']))
