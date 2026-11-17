"""QR Set 11 (2026-11-17). Parent 11/17: focus on real-test LAST-third problem types first, then MIDDLE-third types.
Every problem names the official practice-test item it is built like, and the topic's metrics:
last time done, last time wrong, recent error rate (last 5 attempts), from topic_history.py -> qr11_metrics.json.
Problems 1-14 are middle-third types, 15-38 last-third types. Every math claim is asserted. No real item verbatim."""
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
              'ref': f'Tier: Hard &middot; Topic: {topic} &middot; Type: real {third} third &middot; Built like: {model} &middot; {hist}',
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

# ================= MIDDLE-THIRD TYPES (1-14) =================
# 1 pattern product (PT6 QR #18, wrong)
assert [15873*k for k in (7, 14, 21)] == [111111, 222222, 333333] and 15873*63 == 999999
add('Numerical Patterns', 'PAT', 'middle', 'Use the pattern to help answer the question.<div style="margin-top:6px">15,873 &times; 7 = 111,111</div><div>15,873 &times; 14 = 222,222</div><div>15,873 &times; 21 = 333,333</div><div style="margin-top:6px">What is the value of 15,873 &times; 63?</div>',
    ['444,444', '666,666', '888,888', '999,999'], 'D',
    'The repeated digit is how many 7s are in the number you multiply by: 7 = 1 seven, 14 = 2 sevens, 21 = 3 sevens. 63 = 9 sevens, so the answer is 999,999. A is just the next line after 333,333.',
    'PT6 QR #18 (gid 1519): she picked the next line in the list')
# 2 group rule (PT7 QR #19, slow 85 s)
add('Numerical Patterns', 'PAT', 'middle', 'Mr. Diaz is sorting numbers. He puts the numbers 8, 27, and 64 in a group together. Which is another number that belongs in Mr. Diaz&rsquo;s group?',
    ['81', '100', '125', '144'], 'C',
    '8 = 2 &times; 2 &times; 2, 27 = 3 &times; 3 &times; 3, 64 = 4 &times; 4 &times; 4. The next is 5 &times; 5 &times; 5 = 125. 81, 100, and 144 are a number times itself only twice (9 &times; 9, 10 &times; 10, 12 &times; 12), the rule from Practice Test 7.',
    'PT7 QR #19 (gid 1558): squares 4, 9, 16, right but 85 s')
assert all(round(v ** (1/3)) ** 3 != v for v in (81, 100, 144)) and 5**3 == 125
# 3 order fractions (PT3 QR #20 wrong; QR10 #13 wrong)
fr = [F(3, 5), F(2, 3), F(5, 8), F(4, 7)]
assert sorted(fr) == [F(4, 7), F(3, 5), F(5, 8), F(2, 3)]
add('Comparing & Ordering Fractions & Decimals', 'ORDER', 'middle', f'Which list shows {frac(3,5)}, {frac(2,3)}, {frac(5,8)}, and {frac(4,7)} in order from least to greatest?',
    [f'{frac(4,7)}, {frac(3,5)}, {frac(5,8)}, {frac(2,3)}', f'{frac(4,7)}, {frac(5,8)}, {frac(3,5)}, {frac(2,3)}', f'{frac(3,5)}, {frac(2,3)}, {frac(4,7)}, {frac(5,8)}', f'{frac(2,3)}, {frac(3,5)}, {frac(4,7)}, {frac(5,8)}'], 'A',
    'Compare each to a decimal: 4/7 &asymp; 0.57, 3/5 = 0.6, 5/8 = 0.625, 2/3 &asymp; 0.67. Write them down before ordering. B swaps 3/5 and 5/8. C orders by the bottom number. D orders by the bottom number backwards.',
    'PT3 QR #20 (gid 139) and QR10 #13: ordering 4 fractions, both wrong')
# 4 statement to find greater fraction (PT1 QR #22 wrong; PT6 #29)
assert F(5, 8) == F(15, 24) and F(7, 12) == F(14, 24) and F(5, 8) > F(7, 12) and F(10, 16) > F(7, 12)
add('Comparing & Ordering Fractions & Decimals', 'ORDER', 'middle', f'Ana walked {frac(5,8)} of a mile. Ben walked {frac(7,12)} of a mile. Which statement shows how to find the greater distance?',
    [f'{frac(5,8)} = {frac(15,24)} and {frac(7,12)} = {frac(14,24)}, so {frac(5,8)} &gt; {frac(7,12)}', f'{frac(5,8)} = {frac(15,24)} and {frac(7,12)} = {frac(14,24)}, so {frac(5,8)} &lt; {frac(7,12)}', f'{frac(7,12)} has the greater bottom number, so {frac(7,12)} &gt; {frac(5,8)}', f'{frac(5,8)} = {frac(10,16)} and {frac(10,16)} &lt; {frac(7,12)}'], 'A',
    'Make the bottoms the same: 5/8 = 15/24 and 7/12 = 14/24. 15/24 is more, so Ana&rsquo;s 5/8 is greater. B has the right fractions but the wrong sign. C uses the bottom number only. D is false: 10/16 = 0.625 is more than 7/12.',
    'PT1 QR #22 (gid 60, wrong) and PT6 QR #29 (gid 1530)')
# 5 balance scales (PT5 QR #34 wrong; PT7 QR #18 slow 94 s)
circ, sq, hexa = 1, 3, 6
assert 3*circ == sq and 2*sq == hexa
checks = {'A': hexa == 5*circ, 'B': hexa == sq + 3*circ, 'C': 2*hexa == 3*sq, 'D': sq == 2*circ}
assert checks == {'A': False, 'B': True, 'C': False, 'D': False}
add('Interpreting Pictographs', 'PICTO', 'middle', 'The scales are balanced.' + lines('<b>Scale 1:</b> &#9679; &#9679; &#9679; on the left balances &#9632; on the right.', '<b>Scale 2:</b> &#9632; &#9632; on the left balances &#9650; on the right.') + 'Which set of figures would also balance a scale?',
    ['&#9650; = &#9679; &#9679; &#9679; &#9679; &#9679;', '&#9650; = &#9632; &#9679; &#9679; &#9679;', '&#9650; &#9650; = &#9632; &#9632; &#9632;', '&#9632; = &#9679; &#9679;'], 'B',
    'Write each in circles: &#9632; = 3 circles, so &#9650; = 2 &times; 3 = 6 circles. B: &#9632; + 3 circles = 3 + 3 = 6. A adds 3 + 2 = 5 instead of multiplying. C: 12 circles vs 9. D: 3 circles vs 2.',
    'PT5 QR #34 (gid 1490, wrong) and PT7 QR #18 (gid 1557, right but 94 s)')
# 6 shape digits (PT7 QR #16, slow 99 s)
sols = [(s, c) for s in range(1, 10) for c in range(1, 10) if s != c and 3*s == 10*c + s]
assert sols == [(5, 1)], sols
add('Cryptarithm / digit substitution', 'PICTO', 'middle', 'Each shape stands for a different digit from 1 through 9.<table style="margin:8px 0 8px 24px;font-size:1.35em;border-collapse:collapse;text-align:center"><tr><td></td><td></td><td style="width:1.4em">&#9733;</td></tr><tr><td></td><td></td><td>&#9733;</td></tr><tr><td>+</td><td></td><td>&#9733;</td></tr><tr><td colspan="3" style="border-top:2px solid currentColor;padding:0"></td></tr><tr><td></td><td style="width:1.4em">&#9679;</td><td>&#9733;</td></tr></table>What digit does &#9733; stand for?',
    ['1', '3', '5', '7'], 'C',
    'Three &#9733;s add up to a two-digit number that ends in &#9733;. Try them: 3 &times; 5 = 15 ends in 5. So &#9733; = 5 and &#9679; = 1. A is &#9679;, not &#9733;.',
    'PT7 QR #16 (gid 1555): right but 99 s')
# 7 ratio part of total then the rest (PT6 QR #17)
tot = 96 * 8 // 3
assert 96 * 8 % 3 == 0 and tot == 256 and tot - 96 == 160 and F(96, tot) == F(3, 8)
add('Word Problems with Ratios', 'RATIO', 'middle', 'In a library, the ratio of mystery books to the total number of books is 3 : 8. There are 96 mystery books. How many books are NOT mystery books?',
    ['36', '160', '256', '288'], 'B',
    '3 parts = 96, so 1 part = 32 and the total is 8 &times; 32 = 256. Not mystery: 256 &minus; 96 = 160. C stops at the total. A is 3/8 of 96. D is 96 &times; 3.',
    'PT6 QR #17 (gid 1518), with one more step at the end')
# 8 proportional (PT5 QR #21, 85 s)
assert 150 % 25 == 0 and 150 // 25 * 175 == 1050
add('Word Problems with Ratios', 'RATIO', 'middle', 'A bakery uses 150 eggs to make 25 cakes. It uses the same number of eggs in each cake. How many eggs does it need to make 175 cakes?',
    ['300', '875', '1,050', '1,750'], 'C',
    '150 &divide; 25 = 6 eggs per cake. 175 &times; 6 = 1,050. A adds 150 because 175 &minus; 25 = 150. B uses 5 eggs. D uses 10 eggs.',
    'PT5 QR #21 (gid 1477): right but 85 s')
# 9 unit conversion statement (PT6 QR #25 wrong; last 5 attempts 4 wrong)
assert 8*3*12 == 288 < 300 and 8*12 == 96
add('English Unit Conversions', 'UNIT', 'middle', 'A roll has 8 yards of ribbon. There are 3 feet in 1 yard and 12 inches in 1 foot. Mia needs 300 inches of ribbon. Which statement best explains whether Mia has enough ribbon?',
    ['Since 8 &times; 3 &times; 12 is less than 300, Mia does not have enough ribbon.', 'Since 8 &times; 3 &times; 12 is less than 300, Mia has enough ribbon.', 'Since 8 &times; 12 is less than 300, Mia does not have enough ribbon.', 'Since 8 &times; 3 &times; 12 is greater than 300, Mia has enough ribbon.'], 'A',
    'Yards to feet: 8 &times; 3 = 24 feet. Feet to inches: 24 &times; 12 = 288 inches. 288 is less than 300, so she does not have enough. C skips the feet step (12 inches in a yard, the QR10 #11 slip). D is wrong arithmetic.',
    'PT6 QR #25 (gid 1526, wrong) with two steps, like QR10 #11')
# 10 categories (PT6 QR #38 wrong, QR10 #1 wrong)
add('Data Collection & Random Sampling', 'DATA', 'middle', 'Maya watched a bird feeder and listed what she observed in categories or groups.<div style="margin-top:6px">1. Kind of bird: robin, cardinal, sparrow</div><div>2. Color of each bird&rsquo;s feathers</div><div>3. ?</div><div style="margin-top:6px">Which information best completes Maya&rsquo;s list?</div>',
    ['the side of the feeder each bird landed on: left or right', 'the number of seeds each bird ate', 'how many minutes each bird stayed', 'the weight of each bird, in grams'], 'A',
    'Items 1 and 2 are categories (words), not numbers. Only A is a category. B, C, and D are all numbers you count or measure.',
    'PT6 QR #38 (gid 1539, wrong) and QR10 #1 (wrong)')
# 11 divisible by 3 and 8 (PT1 QR #20 wrong; PT2 MA #24 wrong)
ch11 = [312, 316, 328, 333]
assert [x for x in ch11 if x % 3 == 0 and x % 8 == 0] == [312] and 328 % 8 == 0 and 333 % 3 == 0
add('No Remainder when Divided by a given Number', 'DIV', 'middle', 'Which whole number is divisible by both 3 and 8 without a remainder?',
    ['312', '316', '328', '333'], 'A',
    'By 3: the digits add to a multiple of 3. 3 + 1 + 2 = 6, yes. By 8: 312 &divide; 8 = 39, yes. C works for 8 (328 &divide; 8 = 41) but not 3 (digits add to 13). D works for 3 but is odd, so not 8.',
    'PT1 QR #20 (gid 58, wrong) and PT2 MA #24 (divisible by 8, wrong)')
# 12 Venn (What to Expect QR #10, wrong)
add('Solving for Subsets in a Venn Diagram', 'VENN', 'middle', 'Use the Venn diagram. What instrument do the students in the shaded part play?',
    ['piano', 'violin', 'drums', 'piano and drums'], 'B',
    'The shaded part is inside BOTH circles. The only instrument named in both labels is violin. Piano is only in the left label, drums only in the right.',
    'What to Expect QR #10 (gid 10, wrong)', venn_overlap())
# 13 mean of mixed numbers (What to Expect QR #18, wrong)
w = [F(5, 2), F(5, 2), F(7, 2), F(9, 2)]
assert sum(w) / 4 == F(13, 4) and (F(5, 2) + F(7, 2) + F(9, 2)) / 3 == F(7, 2)
add('Averaging Mixed Numbers', 'AVGMIX', 'middle', 'A dog had 4 puppies. Two puppies weighed 2&frac12; pounds each, one weighed 3&frac12; pounds, and one weighed 4&frac12; pounds. What is the mean weight of the puppies?',
    ['3 pounds', '3&frac14; pounds', '3&frac12; pounds', '3&frac34; pounds'], 'B',
    'Add all four: 2&frac12; + 2&frac12; + 3&frac12; + 4&frac12; = 13. Divide by 4 puppies: 13 &divide; 4 = 3&frac14;. C counts 2&frac12; only once and divides by 3.',
    'What to Expect QR #18 (gid 18, wrong)')
# 14 statement about length and width (PT2 QR #25, wrong)
add('Finding Area/Perimeter of Rectangle, given Length & Width', 'RECT', 'middle', 'The length of a rectangle is L feet. The width is W feet, where W = L &divide; 3. Which statement is true?',
    ['The length is always 3 times the width.', 'The width is always 3 times the length.', 'The length is always 1/3 of the width.', 'The perimeter is always 6 times the width.'], 'A',
    'W = L &divide; 3 means the width is one third of the length, so the length is 3 times the width. D: the perimeter is L + W + L + W = 3W + W + 3W + W = 8W, not 6W.',
    'PT2 QR #25 (gid 103, wrong)')
for L in (3, 9, 12): Wd = F(L, 3); assert L == 3*Wd and 2*L + 2*Wd == 8*Wd

# ================= LAST-THIRD TYPES (15-38) =================
# 15 a / b x c range (PT6 QR #36 wrong; MA5 #15 wrong)
v15 = F(75, 11) * 190
assert 1200 < v15 < 1500 and 900 < 6*190 < 1200 and 1200 < 7*200 < 1500
add('Estimating Multiplication & Division', 'EST', 'last', 'Sam did the problem 75 &divide; 11 &times; 190 on a calculator. Approximately what was his answer?',
    ['between 600 and 900', 'between 900 and 1,200', 'between 1,200 and 1,500', 'between 1,500 and 1,800'], 'C',
    'Work left to right. 75 &divide; 11 is about 7 (77 &divide; 11 = 7). 7 &times; 190 is about 7 &times; 200 = 1,400. Exact: about 1,295. B comes from cutting 75 &divide; 11 down to 6.',
    'PT6 QR #36 (gid 1537, wrong) and MA5 #15 (wrong): third time on this type')
# 16 (a x b) / c range (What to Expect QR #33, wrong)
v16 = F(61*482, 30)
assert 900 < v16 < 1200
add('Estimating Multiplication & Division', 'EST', 'last', f'Josh did the problem shown on his calculator: {frac("61 &times; 482", "30")}. What is a reasonable estimate for his answer?',
    ['between 600 and 900', 'between 900 and 1,200', 'between 1,200 and 1,500', 'between 1,500 and 2,000'], 'B',
    '61 &divide; 30 is about 2. 2 &times; 482 is about 960. Exact: about 980. Divide the pair that goes together first.',
    'What to Expect QR #33 (gid 35, wrong)')
# 17 best estimate of a + (b x c) (PT2 QR #24, wrong)
exact17 = 286 + 42*19
assert exact17 == 1084 and min([800, 1100, 1300, 6000], key=lambda e: abs(e - exact17)) == 1100
add('Estimating Multiplication & Division', 'EST', 'last', 'A store had 286 pencils. It got 42 more boxes of pencils with 19 pencils in each box. The expression 286 + (42 &times; 19) is the exact number of pencils now. Which is the best estimate of the number of pencils?',
    ['800', '1,100', '1,300', '6,000'], 'B',
    '42 &times; 19 is about 40 &times; 20 = 800. Add the 286, about 300: 800 + 300 = 1,100. A forgets the 286. D multiplies 300 by 20.',
    'PT2 QR #24 (gid 102, wrong)')
# 18 cube times as wide (PT4 QR #36, wrong)
assert 4**3 == 64
add('Comparing Volume of Cubes', 'CUBE', 'last', 'Two cubes are shown. Cube A has sides of length 3 centimeters. Cube B is 4 times as wide as Cube A. How many Cube A&rsquo;s can fit inside Cube B?',
    ['12', '16', '48', '64'], 'D',
    '4 times as wide means 4 cube A&rsquo;s along each edge: 4 long, 4 wide, 4 tall. 4 &times; 4 &times; 4 = 64. B fills only the bottom layer. A uses 3 &times; 4. The 3 cm does not matter.',
    'PT4 QR #36 (gid 196, wrong)', two_cubes())
# 19 thousands cubes (PT5 QR #38, wrong)
assert 20 * 1000 == 2*10*10*10*10
add('Comparing Volume of Cubes', 'CUBE', 'last', 'The thousands cube shown has a volume of 1,000 cubic centimeters. Exactly 20 of these thousands cubes are used to build a new figure. Which expression shows the volume of the new figure, in cubic centimeters?',
    ['2 &times; 10', '2 &times; 10 &times; 10 &times; 10', '2 &times; 10 &times; 10 &times; 10 &times; 10', '2 &times; 10 &times; 10 &times; 10 &times; 10 &times; 10'], 'C',
    '20 &times; 1,000 = 20,000. 20 = 2 &times; 10 and 1,000 = 10 &times; 10 &times; 10, so 20,000 = 2 &times; 10 &times; 10 &times; 10 &times; 10 (four 10s). B is only 2,000.',
    'PT5 QR #38 (gid 1494, wrong)', thousands_cube())
# 20 symbol story, total from share (PT3 QR #37, wrong; reversed)
add('Matching Stories to Equations', 'STORY', 'last', 'Some friends shared the cost of a pizza equally. The list shows what is known.<div style="margin-top:6px">The number of friends sharing is &#9633;.</div><div>The amount each friend paid is &#9675;.</div><div style="margin-top:6px">Which equation will find &#9651;, the total cost of the pizza?</div>',
    ['&#9651; = &#9675; &divide; &#9633;', '&#9651; = &#9675; + &#9633;', '&#9651; = &#9675; &minus; &#9633;', '&#9651; = &#9675; &times; &#9633;'], 'D',
    'Each friend paid &#9675;, and there are &#9633; friends, so the total is &#9675; &times; &#9633;. Try numbers: 4 friends paid $5 each, total $20 = 5 &times; 4. A is the Practice Test 3 answer, but this time the total is unknown.',
    'PT3 QR #37 (gid 156, wrong), reversed to find the total')
# 21 tiles (PT2 QR #32 wrong; PT7 QR #26)
assert 96 % 8 == 0 and 54 % 6 == 0 and (96//8)*(54//6) == 108 and (96*54) // (8*6) == 108
add('Matching Stories to Equations', 'STORY', 'last', 'Rosa wants to cover a patio with tiles. The patio is 96 inches long and 54 inches wide. Each tile is 8 inches long and 6 inches wide. How can Rosa find how many tiles she needs without laying them all down? (A = l &times; w)',
    ['(96 &divide; 8) &times; (54 &divide; 6)', '(96 &times; 54) &divide; (8 + 6)', '(96 &minus; 8) &times; (54 &minus; 6)', '(96 &minus; 48) &times; (54 &minus; 48)'], 'A',
    'Tiles along the length: 96 &divide; 8 = 12. Along the width: 54 &divide; 6 = 9. 12 &times; 9 = 108 tiles. C and D subtract instead of dividing. B adds the tile sides instead of multiplying them.',
    'PT2 QR #32 (gid 111, wrong) and PT7 QR #26 (gid 1565)')
# 22 quadrilateral: exactly one pair of parallel sides (PT7 MA #18, wrong)
add('Identifying Shapes', 'SHAPES', 'last', 'Which figure could be described as a quadrilateral with exactly one pair of parallel sides?',
    ['square', 'rectangle', 'rhombus', 'trapezoid'], 'D',
    'A trapezoid has exactly ONE pair of parallel sides. A square, a rectangle, and a rhombus each have TWO pairs. (On Practice Test 7 the question asked for two pairs, and the answer was square, not trapezoid.)',
    'PT7 MA #18 (wrong: picked trapezoid for two pairs)')
# 23 always-true statement (PT1 MA #23, wrong; PT5 MA #28, wrong)
add('Identifying Shapes', 'SHAPES', 'last', 'Which statement is always true?',
    ['A rhombus is always a square.', 'A trapezoid always has two pairs of parallel sides.', 'A rectangle always has four sides of equal length.', 'A square is always a rhombus.'], 'D',
    'A rhombus has 4 equal sides. A square has 4 equal sides (and 4 right angles), so every square is a rhombus. A is backwards: a rhombus does not need right angles. B: one pair only. C: only a square.',
    'PT1 MA #23 and PT5 MA #28 (both wrong)')
# 24 rotation (PT7 QR #27, right but 185 s)
add('Identifying Shapes', 'SHAPES', 'last', 'Leo wants to prove that Figure E and Figure F are the same size and shape. What must he do?',
    ['slide Figure E over the dashed line onto Figure F', 'turn Figure E counterclockwise a quarter of a turn', 'turn Figure E clockwise a quarter of a turn and slide it onto Figure F', 'flip Figure E over the dashed line and turn it counterclockwise a quarter of a turn'], 'C',
    'Look at the one square that sticks out. In E it sticks out on the right of the middle column. Turn E clockwise (like a clock) a quarter turn: the long column lies flat and the bump points down, as in F. Then slide it over.',
    'PT7 QR #27 (gid 1566): right but 185 s', rot_fig())
# 25 probability, unknown count (PT7 QR #34, wrong)
known = [5, 7, 4, 8]
sol = [p for p in range(1, 50) if F(p, sum(known) + p) == F(1, 4)]
assert sum(known) == 24 and sol == [8] and sum(known) // 4 == 6
add('Finding Ratios given Probability', 'PROB', 'last', 'The table shows the number of each color of marble in a bag. The probability of picking a purple marble without looking is ' + frac(1, 4) + '. How many purple marbles are in the bag?' +
    table(['Color', 'Number'], [['Red', 5], ['Blue', 7], ['Green', 4], ['Yellow', 8], ['Purple', '?']], 'MARBLES IN THE BAG'),
    ['6', '8', '12', '24'], 'B',
    'The other marbles: 5 + 7 + 4 + 8 = 24. The total must include the purple ones. Check 8: 8 out of 24 + 8 = 32, and 8/32 = 1/4. A is 1/4 of 24, leaving purple out of the total (the Practice Test 7 slip).',
    'PT7 QR #34 (gid 1573, wrong) and PT5 QR #37 (gid 1493, 145 s)')
# 26 probability, find the other group (What to Expect QR #27)
assert F(6, 21) == F(2, 7) and 21 - 6 == 15
add('Finding Ratios given Probability', 'PROB', 'last', 'Mr. Lee put the names of all his students in a hat. The probability of pulling out a boy&rsquo;s name is 2 out of 7. There are 15 girls in the class. How many boys are in the class?',
    ['2', '5', '6', '21'], 'C',
    'Girls are the other 5 out of 7. 5 parts = 15, so 1 part = 3. Boys are 2 parts = 6. Check: 6 boys out of 21 students = 2/7. D is the whole class. B is the girls&rsquo; part number.',
    'What to Expect QR #27 (gid 29)')
# 27 digit rules, hundreds place (PT7 QR #36, wrong)
cands = [int(''.join(p)) for p in permutations('245679') if int(p[-1]) % 2 == 1]
best = min(cands)
assert best == 245679 and str(best)[-3] == '6'
add('Value of Digits', 'DIGIT', 'last', 'Students wrote a new number using the digits 2, 4, 5, 6, 7, and 9 and these rules.' +
    '<div style="border:1px solid var(--border);border-radius:6px;padding:6px 10px;margin:8px 0;max-width:420px"><b>RULES FOR THE NEW NUMBER</b><div>1. The number must have 6 digits.</div><div>2. The number must be odd.</div><div>3. The number must be the smallest number possible.</div><div>4. Each digit can be used only once.</div></div>What digit is in the <b>hundreds</b> place of the new number?',
    ['2', '5', '6', '9'], 'C',
    'Smallest: put the small digits in front. Odd: the ones digit must be 5, 7, or 9; use the biggest odd one (9) at the end so the front stays small: 245,679. Write the places under it: hundreds is 6. A is the first digit.',
    'PT7 QR #36 (gid 1575, wrong) and PT3 QR #31 (gid 150, wrong)')
# 28 digit rules, tens place (PT3 QR #31, wrong)
cands = [int(''.join(p)) for p in permutations('13468') if int(p[-1]) % 2 == 0]
best = max(cands)
assert best == 86314 and str(best)[-2] == '1'
add('Value of Digits', 'DIGIT', 'last', 'Students wrote a new number using the digits 1, 3, 4, 6, and 8 and these rules.' +
    '<div style="border:1px solid var(--border);border-radius:6px;padding:6px 10px;margin:8px 0;max-width:420px"><b>RULES FOR THE NEW NUMBER</b><div>1. The number must have 5 digits.</div><div>2. The number must be even.</div><div>3. The number must be the largest number possible.</div><div>4. Each digit can be used only once.</div></div>What digit is in the <b>tens</b> place of the new number?',
    ['1', '3', '4', '8'], 'A',
    'Largest: big digits in front. Even: the ones digit must be 4, 6, or 8; use the smallest even one (4) at the end so the front stays big: 86,314. Tens place is 1. B is the tens digit of 86,341, which is odd.',
    'PT3 QR #31 (gid 150, wrong) and PT2 QR #35 (gid 114)')
# 29 L-shape perimeter (PT6 QR #30, wrong)
sides = [5, 7, 7, 4, 12, 11]   # top, inner down, inner across, right, bottom, left
assert 12 - 5 == 7 and 11 - 4 == 7 and sum(sides) == 46 == 2*(12+11) and 5+11+12+4 == 32
add('Area and Perimeter of Complex Polygons', 'POLY', 'last', 'The figure is made of straight sides that meet at right angles. What is the perimeter of the figure?',
    ['32 feet', '39 feet', '46 feet', '57 feet'], 'C',
    'Find the two missing sides: across = 12 &minus; 5 = 7, down = 11 &minus; 4 = 7. Add all six: 5 + 7 + 7 + 4 + 12 + 11 = 46. A adds only the four labeled sides. B misses one of the 7s.',
    'PT6 QR #30 (gid 1531, wrong)', l_shape())
# 30 0/1 identities (PT7 QR #32, right but 92 s)
for star in (3, 8):
    for dot in (2, 9):
        dia, tri = 0, 1
        assert star - dia == star and dot * tri == dot
        for sq in (4, 7): assert sq * dia + tri == 1
add('Algebraic Equations with Symbol Variables', 'SYM', 'last', 'If &#9733; &minus; &#9670; = &#9733; and &#9679; &times; &#9650; = &#9679;, what is the value of &#9632; &times; &#9670; + &#9650;?',
    ['0', '1', '&#9632;', '&#9632; + 1'], 'B',
    '&#9733; &minus; &#9670; = &#9733; means &#9670; = 0. &#9679; &times; &#9650; = &#9679; means &#9650; = 1. So &#9632; &times; 0 + 1 = 0 + 1 = 1. D forgets that anything times 0 is 0.',
    'PT7 QR #32 (gid 1571): right but 92 s')
# 31 symbol story (PT4 QR #35, wrong)
def ok31(sq, ci, tr):
    ben_before = tr * (sq - ci) - ci
    return {'A': tr*(sq-ci) - ci, 'B': tr*(sq-ci) + ci, 'C': tr*sq - ci, 'D': tr*(sq-ci)}, ben_before
for sq, ci, tr in ((10, 3, 2), (12, 5, 3)):
    ex, bb = ok31(sq, ci, tr)
    assert [k for k, v in ex.items() if v == bb] == ['A']
add('Algebraic Equations with Symbol Variables', 'SYM', 'last', 'Ava had &#9633; stickers. She gave &#9675; of them to Ben. After that, Ben had &#9651; times as many stickers as Ava had left. Which expression shows how many stickers Ben had before Ava gave him any?',
    ['&#9651; &times; (&#9633; &minus; &#9675;) &minus; &#9675;', '&#9651; &times; (&#9633; &minus; &#9675;) + &#9675;', '&#9651; &times; &#9633; &minus; &#9675;', '&#9651; &times; (&#9633; &minus; &#9675;)'], 'A',
    'Ava has &#9633; &minus; &#9675; left. Ben now has &#9651; times that: &#9651; &times; (&#9633; &minus; &#9675;). Before the gift he had &#9675; fewer, so subtract &#9675;. Try numbers: Ava 10, gave 3, Ben now 2 &times; 7 = 14, before 11. D stops one step early.',
    'PT4 QR #35 (gid 195, wrong)')
# 32 midpoint on a number line (PT2 QR #33)
assert 2*NL_D - NL_C == 44
add('Determining Averages between Points on Number Lines', 'NUMLINE', 'last', 'The tick marks on the number line are evenly spaced. D is the midpoint between C and another point, E. What is the value of E?',
    ['16', '20', '40', '44'], 'D',
    'Each tick is 4 (5 jumps from 0 to 20). C = 12 and D = 28. From C to D is 16, so E is 16 more than D: 28 + 16 = 44. A stops at the distance. C adds C and D.',
    'PT2 QR #33 (gid 112) and What to Expect QR #35 (gid 37)', number_line())
# 33 compare areas and perimeters (PT2 QR #38, wrong)
assert 10*10 == 5*20 and 4*10 < 2*(5+20)
add('Comparing Areas', 'AREAS', 'last', 'The floor of Room A is a square with an area of 100 square feet. The floor of Room B is a rectangle 5 feet wide and 20 feet long. Which statement correctly compares the two floors?',
    ['The area of Room A is greater than the area of Room B.', 'The area of Room A is less than the area of Room B.', 'The perimeter of Room A is equal to the perimeter of Room B.', 'The perimeter of Room A is less than the perimeter of Room B.'], 'D',
    'Room A: 10 &times; 10 = 100, so its sides are 10 and its perimeter is 40. Room B: area 5 &times; 20 = 100 (the same), perimeter 5 + 20 + 5 + 20 = 50. 40 is less than 50.',
    'PT2 QR #38 (gid 117, wrong)')
# 34 hidden rule (PT7 QR #38 and #28)
rule = lambda sides, dots: dots == 2*sides
yes = [(3, 6), (4, 8), (5, 10)]; no = [(3, 3), (6, 8), (4, 6)]
assert all(rule(*x) for x in yes) and not any(rule(*x) for x in no)
opts = {'A': (6, 10), 'B': (8, 16), 'C': (5, 5), 'D': (4, 10)}
assert [k for k, v in opts.items() if rule(*v)] == ['B']
add('Predicting the Next Shapes given Progressive Pattern', 'NEXT', 'last', '<div><b>These are zorbs:</b> a triangle with 6 dots, a square with 8 dots, a pentagon with 10 dots.</div><div><b>These are NOT zorbs:</b> a triangle with 3 dots, a hexagon with 8 dots, a square with 6 dots.</div><div style="margin-top:6px">Which of these is a zorb?</div>',
    ['a hexagon with 10 dots', 'an octagon with 16 dots', 'a pentagon with 5 dots', 'a square with 10 dots'], 'B',
    'Check every zorb: the dots are 2 times the number of sides (3 &rarr; 6, 4 &rarr; 8, 5 &rarr; 10). An octagon has 8 sides: 2 &times; 8 = 16. C fits &ldquo;dots = sides&rdquo;, which the non-zorb triangle with 3 dots rules out.',
    'PT7 QR #38 (gid 1577) and PT7 QR #28 (gid 1567, right but 91 s)')
# 35 mean/median statements (What to Expect QR #29)
data = {'Ana': 15, 'Ben': 30, 'Cai': 40, 'Dev': 19}
vals = sorted(data.values()); mean = F(sum(vals), 4); med = F(vals[1] + vals[2], 2); rng = vals[-1] - vals[0]
assert (mean, med, rng) == (26, F(49, 2), 25)
st = {'A': 24 < mean < 25, 'B': rng > data['Ben'], 'C': data['Cai'] == data['Ana'] + data['Dev'], 'D': med < mean}
assert st == {'A': False, 'B': False, 'C': False, 'D': True}
add('Finding MMMR given Bar Graph Data Table', 'MMMR', 'last', 'Four students recorded the minutes they practiced piano one night.' + table(['Student', 'Minutes'], [[k, v] for k, v in data.items()], 'MINUTES PRACTICED') + 'Which statement is true?',
    ['The mean is between 24 and 25.', 'The range is greater than the number of minutes Ben practiced.', 'Cai practiced as many minutes as Ana and Dev combined.', 'The median is less than the mean.'], 'D',
    'Mean: 15 + 30 + 40 + 19 = 104, and 104 &divide; 4 = 26. Median: in order 15, 19, 30, 40, the middle two are 19 and 30, so the median is 24&frac12;. 24&frac12; is less than 26. A describes the median, not the mean. B: range 40 &minus; 15 = 25, less than 30. C: 15 + 19 = 34.',
    'What to Expect QR #29 (gid 31)')
# 36 percent of a grid (PT2 QR #26, wrong; PT4 QR #37)
assert F(40 - len(WHITE), 40) == F(3, 4)
add('Determining Fraction/Percent of Shaded Area, given Figure', 'EQUIV', 'last', 'The shaded squares show the part of a floor that already has tile. Each small square is the same size. What percent of the floor already has tile?',
    ['10%', '25%', '30%', '75%'], 'D',
    'There are 8 &times; 5 = 40 squares. 10 are white, so 30 are shaded. 30 out of 40 = 3/4 = 75%. B is the white part. A and C are the counts, not percents.',
    'PT2 QR #26 (gid 104, wrong) and PT4 QR #37 (gid 197)', floor_grid(8, 5, WHITE))
# 37 increase then decrease (PT4 QR #38, wrong; percent decrease open from MA5 #8)
p1 = F(50) * F(110, 100); p2 = p1 * F(90, 100)
assert p1 == 55 and p2 == F(99, 2)
add('Percent Increase Decrease basic', 'PCT', 'last', 'A game costs $50. The price is increased by 10%. Later, the new price is decreased by 10%. What is the final price?',
    ['$45.00', '$49.50', '$50.00', '$50.50'], 'B',
    'Up 10% of $50: $5, so $55. Down 10% of the NEW price $55: $5.50, so $55 &minus; $5.50 = $49.50. C thinks the two 10%s cancel out. The second 10% is of a bigger number.',
    'PT4 QR #38 (gid 198, wrong) and MA5 #8 (wrong, percent decrease)')
# 38 minus before a group (PT2 MA #26, MA4 #8, MA5 #21: all wrong)
v38 = 40 - (15 + 9 - 4)
ex38 = {'A': 40 - 15 - 9 + 4, 'B': 40 - 15 + 9 - 4, 'C': 40 - 15 - 9 - 4, 'D': 40 + 15 - 9 + 4}
assert v38 == 20 and [k for k, v in ex38.items() if v == v38] == ['A']
add('Order of Operations and Equivalence', 'OOO', 'last', 'Which expression has the same value as 40 &minus; (15 + 9 &minus; 4)?',
    ['40 &minus; 15 &minus; 9 + 4', '40 &minus; 15 + 9 &minus; 4', '40 &minus; 15 &minus; 9 &minus; 4', '40 + 15 &minus; 9 + 4'], 'A',
    'The minus in front takes away the whole group: 15 + 9 &minus; 4 = 20, and 40 &minus; 20 = 20. Taking away the group flips each sign inside: &minus;15, &minus;9, +4. A = 20. C forgets to flip the &minus;4 (it gives 12).',
    'PT2 MA #26 and MA5 #21 (minus before a bracket, wrong)')

assert len(P) == 38
# order: swap the Venn (12) ahead of the divisibility problem (11) to avoid A-A-A
P[10], P[11] = P[11], P[10]
M2 = {}
for i, p in enumerate(P, 1):
    old = p['n']; p['n'] = i; M2[i] = MAP[old]
MAP = M2
L = [p['correct'] for p in P]
cnt = Counter(L); print(cnt, ''.join(L))
assert max(cnt.values()) - min(cnt.values()) <= 1, cnt
assert not any(L[i] == L[i+1] == L[i+2] for i in range(36)), ''.join(L)
tc = Counter(p['topic'] for p in P)
assert max(tc.values()) <= 3, tc
json.dump(P, open(os.path.join(HERE, 'set11_problems.json'), 'w'), indent=1)
json.dump(MAP, open(os.path.join(HERE, 'set11_mapping.json'), 'w'), indent=1, ensure_ascii=False)
print('wrote', len(P), 'diagrams', sum(1 for p in P if p['diagram']))
