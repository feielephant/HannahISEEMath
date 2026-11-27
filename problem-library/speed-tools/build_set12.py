"""QR Set 12 (built 2026-11-27, after the vacation drills). Parent rules (11/27):
- every problem is built on a REAL practice-test problem from the LAST THIRD (QR #26-38 / MA #21-30); nothing invented
  without a real reference;
- topics only from her data: high error rate, recent misses, or a miss followed by 3+ weeks without practice; plus (parent
  approved 11/27) types she missed often before and has got right since, 1-2 weeks unpracticed, including 4 the parent had
  rested on 11/19 (divisible-by-8 story, prime x composite, triangle area vs height, share-a-total equation);
- difficulty AND trap level match the real problem she missed: same steps, same kind of numbers, and the same kinds of
  wrong choices the real test offered (including the one she picked). Numbers, story and sometimes the asked part change,
  because she memorizes formats;
- ordered from the highest real % right to the lowest, like the real test's rising difficulty.
Every math claim is asserted."""
import json, os, sys, re
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from joined_prism_diagram import joined_prisms_svg
T = {x['topic'] for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}

def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def rules_box(*rules, title='GUIDELINES FOR THE NEW NUMBER'):
    return (f'<div style="border:1.5px solid currentColor;border-radius:6px;padding:8px 12px;max-width:360px"><div style="font-weight:700;margin-bottom:4px">{title}</div>'
            + ''.join(f'<div>{i}. {r}</div>' for i, r in enumerate(rules, 1)) + '</div>')
def stem_plot(title, stems):
    rows = ''.join(f'<tr><td style="padding:5px 12px 5px 18px;text-align:right;border-right:2px solid currentColor">{k}</td>'
                   f'<td style="padding:5px 28px 5px 12px;white-space:nowrap">{"&nbsp;&nbsp;&nbsp;".join(map(str, ls))}</td></tr>' for k, ls in stems.items())
    return (f'<div style="display:inline-block;text-align:center;margin-left:12px"><div style="font-weight:600;letter-spacing:0.03em;margin-bottom:8px">{title}</div>'
            f'<table style="border-collapse:collapse;border-top:2px solid currentColor;font-variant-numeric:lining-nums tabular-nums;font-size:1.15em;margin:0 auto 10px">{rows}</table></div>')
SW = 'stroke="currentColor" stroke-width="2" fill="none"'
def svg(w, h, body): return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{body}</svg>'
def txt(x, y, s, size=14, anchor='middle'): return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="currentColor">{s}</text>'
def grid_array(rows, cols, cell=10):
    w, h = cols*cell, rows*cell
    g = ''.join(f'<line x1="{c*cell}" y1="0" x2="{c*cell}" y2="{h}" stroke="currentColor" stroke-width="1"/>' for c in range(cols + 1))
    g += ''.join(f'<line x1="0" y1="{r*cell}" x2="{w}" y2="{r*cell}" stroke="currentColor" stroke-width="1"/>' for r in range(rows + 1))
    return f'<svg viewBox="-1 -1 {w+2} {h+2}" width="{w+2}" height="{h+2}" role="img" style="vertical-align:middle">{g}</svg>'
def thousands_cube(n=10, s=11):
    """A cube built from n x n x n unit cubes, drawn with three gridded faces (front, top, right)."""
    dx, dy = s*0.5, s*0.4            # receding offset per unit of depth
    ox, oy = 4, n*dy + 4
    L = []
    for i in range(n + 1):           # front face grid
        L.append(f'<line x1="{ox+i*s}" y1="{oy}" x2="{ox+i*s}" y2="{oy+n*s}"/>')
        L.append(f'<line x1="{ox}" y1="{oy+i*s}" x2="{ox+n*s}" y2="{oy+i*s}"/>')
    for i in range(n + 1):           # top face grid
        L.append(f'<line x1="{ox+i*s}" y1="{oy}" x2="{ox+i*s+n*dx}" y2="{oy-n*dy}"/>')
        L.append(f'<line x1="{ox+i*dx}" y1="{oy-i*dy}" x2="{ox+n*s+i*dx}" y2="{oy-i*dy}"/>')
    for i in range(n + 1):           # right face grid
        L.append(f'<line x1="{ox+n*s+i*dx}" y1="{oy-i*dy}" x2="{ox+n*s+i*dx}" y2="{oy+n*s-i*dy}"/>')
        L.append(f'<line x1="{ox+n*s}" y1="{oy+i*s}" x2="{ox+n*s+n*dx}" y2="{oy+i*s-n*dy}"/>')
    W, H = ox + n*s + n*dx + 4, oy + n*s + 4
    return f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" role="img"><g stroke="currentColor" stroke-width="1" fill="none">{"".join(L)}</g></svg>'
def shape(kind, x, y, r=11):
    if kind == 'C': return f'<circle cx="{x}" cy="{y-r}" r="{r}" {SW}/>'
    if kind == 'S': return f'<rect x="{x-r}" y="{y-2*r}" width="{2*r}" height="{2*r}" {SW}/>'
    if kind == 'T': return f'<polygon points="{x-r},{y} {x+r},{y} {x},{y-2*r}" {SW}/>'
def balance(left, right, scale=1.0):
    W, H = 300, 110
    g = f'<polygon points="150,{H-6} 138,{H-30+30} 162,{H-30+30}" fill="none"/>'
    g = (f'<line x1="150" y1="58" x2="150" y2="{H-6}" stroke="currentColor" stroke-width="2"/>'
         f'<polygon points="136,{H-4} 164,{H-4} 150,{H-20}" {SW}/>'
         f'<line x1="20" y1="58" x2="280" y2="58" stroke="currentColor" stroke-width="3"/>')
    for side, items in ((0, left), (1, right)):
        cx = 75 if side == 0 else 225
        n = len(items); start = cx - (n - 1)*14
        for i, k in enumerate(items): g += shape(k, start + i*28, 56)
    w, h = int(W*scale), int(H*scale)
    return f'<svg viewBox="0 0 {W} {H}" width="{w}" height="{h}" role="img" style="vertical-align:middle">{g}</svg>'

P, MAP = [], {}
def add(topic, ref, pct, her, record, q, ch, right, tags, asks, key, vs, diagram=None, free=False):
    """ref/pct/her: the real last-third problem, its % right, and her result on it; record: her wrong/tries + last 6 + last miss.
    tags: {choice: cause} for the 3 wrong choices; free=True lets the builder reorder the choices to balance answer letters."""
    assert topic in T, topic
    assert len(set(ch)) == 4 and right in ch and set(tags) == set(ch) - {right}, (ref, ch)
    P.append(dict(topic=topic, ref=ref, pct=pct, her=her, record=record, q=q, ch=list(ch), right=right, tags=tags, asks=asks,
                  key=key, vs=vs, diagram=diagram, free=free))

# ---------------- A. open weaknesses ----------------
add('Percent Increase Decrease basic', 'Lower 4 QR #38', 40.6, 'x', '6/11 &middot; x o o o x o &middot; last miss 11/20',
    'The price of a bicycle was decreased by 30%. Then the new price was increased by 30%. What is the percent increase or percent decrease from the original price?',
    ['percent decrease by 30%', 'percent decrease by 9%', 'percent increase by 9%', 'percent increase by 30%'], 'percent decrease by 9%',
    {'percent decrease by 30%': 'Used only the first change', 'percent increase by 9%': 'Right size, wrong direction (her pick on the real one)', 'percent increase by 30%': 'Used only the last change'},
    'percent change from the original',
    'Start with $100. Down 30%: $70. Up 30% of $70 = $21: $91. $91 is $9 less than $100, a 9% decrease. The 30% increase is taken of a smaller number, so it does not undo the decrease.',
    'Same: two opposite changes of the same percent, answer is a percent change (30% instead of 20%; decrease first)')
assert F(100) * F(70, 100) * F(130, 100) == 91
add('Percent Increase Decrease basic', 'Lower 6 MA #28', 74.6, 'x (92 s)', '6/11 &middot; x o o o x o &middot; last miss 11/20',
    'A coupon gives 20% off the regular price of a jacket. The coupon saves Mia $4. What is the regular price of the jacket?',
    ['$8', '$12', '$20', '$24'], '$20',
    {'$8': 'Known trap (her pick on the real one): doubled the $4 instead of finding 100%', '$12': 'Tripled the $4', '$24': 'Added the $4 to the regular price'},
    'regular price',
    '20% is $4. 100% is 5 times 20%, so the regular price is 5 &times; $4 = $20. (Whole = part &divide; percent: 4 &divide; 0.2 = 20.)',
    'Same: 20% of the price is given in dollars, find the whole; same kinds of wrong choices')
assert F(4) / F(20, 100) == 20
mult = [k for k in range(51, 90) if k % 4 == 0]
assert len(mult) == 10 and mult[0] == 52 and mult[-1] == 88
add('Counting Multiples within a Range', 'Lower 5 MA #29', 63.7, 'x (134 s)', '6/12 &middot; o o o x x x &middot; last miss 11/25',
    'How many numbers between 50 and 90 are divisible by 4?', ['7', '8', '9', '10'], '10',
    {'7': 'Missed several: counted by 4s from 60', '8': 'Off by two: missed both ends', '9': 'Off by one: missed the first (52) or the last (88)'},
    'how many numbers',
    'The first multiple of 4 after 50 is 52 and the last before 90 is 88. List or count by 4s: 52, 56, ..., 88. (88 &minus; 52) &divide; 4 + 1 = 10.',
    'Same: one divisor, a range whose ends are not multiples; off-by-one choices like the real one')
add('Comparing Volume of Cubes', 'Lower 4 QR #36', 48.2, 'x', '6/15 &middot; o o x o x o &middot; last miss 11/24',
    'Cube A has sides that are 3 centimeters long. Cube B is 4 times as wide as Cube A. How many Cube A\'s can fit inside Cube B?',
    ['12', '16', '64', '96'], '64',
    {'12': 'Multiplied 4 by the 3 sides', '16': 'Squared the scale (one face only)', '96': 'Counted 16 per face times 6 faces (like 150 on the real one, her pick)'},
    'how many Cube A\'s',
    'Cube B is 4 times as long, 4 times as wide and 4 times as tall, so 4 &times; 4 &times; 4 = 64 Cube A\'s fit.',
    'Same: scale factor cubed; the same kinds of wrong choices (&times;3, squared, faces)')
assert 4**3 == 64 and 4**2*6 == 96
add('Comparing Volume of Cubes', 'Lower 5 QR #38', 39.6, 'x (66 s)', '6/15 &middot; o o x o x o &middot; last miss 11/24',
    'The thousands cube shown has a volume of 1,000 cubic inches. Exactly 70 of these thousands cubes are used to make a new three-dimensional figure. Which expression represents the volume of the new figure in cubic inches?',
    ['7 &times; 10', '7 &times; 10 &times; 10 &times; 10', '7 &times; 10 &times; 10 &times; 10 &times; 10', '7 &times; 10 &times; 10 &times; 10 &times; 10 &times; 10'],
    '7 &times; 10 &times; 10 &times; 10 &times; 10',
    {'7 &times; 10': 'Known trap (her pick on the real one): wrote only the 70', '7 &times; 10 &times; 10 &times; 10': 'Wrote 7,000: forgot that 70 is 7 &times; 10',
     '7 &times; 10 &times; 10 &times; 10 &times; 10 &times; 10': 'One 10 too many'},
    'volume (expression)',
    '70 &times; 1,000 = 70,000 = 7 &times; 10,000 = 7 &times; 10 &times; 10 &times; 10 &times; 10.',
    'Same: thousands cubes, count to a power of 10 (70 instead of 30)', thousands_cube())
assert 70 * 1000 == 7 * 10**4
fr6 = {'3/10': F(3, 10), '2/5': F(2, 5), '1/6': F(1, 6)}
assert sorted(fr6, key=fr6.get) == ['1/6', '3/10', '2/5']
add('Comparing & Ordering Fractions & Decimals', 'Lower 6 QR #31', 64.4, 'o (98 s)', '13/35 &middot; o x o o o x &middot; last miss 11/20',
    'Which list shows the fractions ' + frac(3, 10) + ', ' + frac(2, 5) + ', ' + frac(1, 6) + ' in order from least to greatest?',
    [f'{frac(1,6)}, {frac(3,10)}, {frac(2,5)}', f'{frac(2,5)}, {frac(3,10)}, {frac(1,6)}', f'{frac(3,10)}, {frac(1,6)}, {frac(2,5)}', f'{frac(1,6)}, {frac(2,5)}, {frac(3,10)}'],
    f'{frac(1,6)}, {frac(3,10)}, {frac(2,5)}',
    {f'{frac(2,5)}, {frac(3,10)}, {frac(1,6)}': 'Right order, wrong direction (greatest to least; the real trap D, and her MA6 #12 slip)',
     f'{frac(3,10)}, {frac(1,6)}, {frac(2,5)}': 'Compared numerators only', f'{frac(1,6)}, {frac(2,5)}, {frac(3,10)}': 'Compared denominators only'},
    'least to greatest',
    'As decimals: 1/6 is about 0.17, 3/10 = 0.3, 2/5 = 0.4. Least to greatest: 1/6, 3/10, 2/5. Read the direction words before choosing.',
    'Same: three fractions with different denominators; asks least to greatest instead of greatest to least', free=True)
seq7 = [2, 6, 18, 54]
assert seq7[-1]*3 == 162 and 162*3 == 486 and 54*2 == 108
add('Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.', 'Lower 3 MA #21', 80.0, 'x', '6/17 &middot; o x x o x o &middot; last miss 11/17',
    'Use the number pattern to answer the question.<div style="margin:8px 0;font-size:1.15em">2&nbsp;&nbsp;&nbsp;6&nbsp;&nbsp;&nbsp;18&nbsp;&nbsp;&nbsp;54&nbsp;&nbsp;&nbsp;?&nbsp;&nbsp;&nbsp;?</div>What is the sixth number in the pattern?',
    ['108', '162', '486', '1,458'], '486',
    {'108': 'Known trap (like 54 on the real one, her pick): doubled the last number', '162': 'Stopped early: this is the fifth number', '1,458': 'One step too far (the seventh number)'},
    'the sixth number',
    'Each number is 3 times the one before: 54 &times; 3 = 162 (fifth), 162 &times; 3 = 486 (sixth).',
    'Same as the real one: four numbers then two ? marks, asks the sixth; same kinds of wrong choices')
add('Volume of Solids', 'Lower 1 QR #36', 37.2, 'x', '2/6 &middot; x o o o x o &middot; last miss 11/20',
    'The figure shown was made by joining two rectangular prisms. The side lengths are measured in feet. Which expression can be used to find the total volume of the figure? (V = lwh, where V = volume, l = length, w = width, and h = height.)',
    ['(2 &times; 5 &times; 4) + (6 &times; 5 &times; 3)', '(2 &times; 5 &times; 7) + (6 &times; 5 &times; 3)', '6 &times; 5 &times; 7', '(6 &times; 5 &times; 4) + (2 &times; 5 &times; 3)'],
    '(2 &times; 5 &times; 4) + (6 &times; 5 &times; 3)',
    {'(2 &times; 5 &times; 7) + (6 &times; 5 &times; 3)': 'Used the full height 7 for the top prism (counts the bottom twice)', '6 &times; 5 &times; 7': 'Treated it as one box',
     '(6 &times; 5 &times; 4) + (2 &times; 5 &times; 3)': 'Mixed up which width goes with which height (like C on the real one, her pick)'},
    'total volume (expression)',
    'Top prism: 2 wide, 5 deep, 4 tall. Bottom prism: 6 wide, 5 deep, 3 tall. Total = (2 &times; 5 &times; 4) + (6 &times; 5 &times; 3) = 40 + 90 = 130.',
    'Same: choose the expression for two joined prisms', joined_prisms_svg(2, 4, 6, 3, 5, sc=17).replace('font-size="11"', 'font-size="14"'), free=True)
add('Translating Math Expressions', 'Lower 4 QR #35', 47.4, 'x', '7/21 &middot; o o o x x x &middot; last miss 11/25',
    'Maya had &square; stickers, and then she gave &#9675; of them to Ben. Now Ben has &#9651; times as many stickers as Maya had. Which expression represents the number of stickers Ben had to begin with?',
    ['&#9651; &times; &#9675; + &square;', '&#9651; &times; &#9675; &minus; &square;', '&#9651; &times; &square; + &#9675;', '&#9651; &times; &square; &minus; &#9675;'],
    '&#9651; &times; &square; &minus; &#9675;',
    {'&#9651; &times; &#9675; + &square;': 'Multiplied the gift instead of what Maya had', '&#9651; &times; &#9675; &minus; &square;': 'Multiplied the gift (her pick on the real one)',
     '&#9651; &times; &square; + &#9675;': 'Stopped at Ben NOW plus the gift again: went the wrong way in time'},
    'Ben, at the beginning',
    'Before | gift | now. Now Ben has &#9651; times what Maya HAD: &#9651; &times; &square;. That includes the &#9675; she gave him, so before the gift he had &#9651; &times; &square; &minus; &#9675;.',
    'Same as the real one (times as many as she HAD); new story')
add('Finding Area/Perimeter of Rectangle, given Length & Width', 'Lower 1 MA #30', 35.9, 'x', '6/20 &middot; x o o x x o &middot; last miss 11/20',
    'The perimeter of a square is 40 centimeters. If a rectangle with a width of 5 centimeters has the same area as the square, what is the length of the rectangle in centimeters?',
    ['8', '10', '15', '20'], '20',
    {'8': 'Known trap (like 8 on the real one, her pick): divided the perimeter by the width (40 &divide; 5)', '10': 'Stopped early: this is the square\'s side',
     '15': 'Added the width to the side (10 + 5)'},
    'length of the rectangle',
    'Square side = 40 &divide; 4 = 10, so its area is 10 &times; 10 = 100. The rectangle has area 100 and width 5: length = 100 &divide; 5 = 20.',
    'Same chain as the real one (perimeter &rarr; side &rarr; area &rarr; missing side), new numbers')
assert 40 // 4 == 10 and 100 // 5 == 20
pat = [4, 5, 7, 11, 19]
assert [b - a for a, b in zip(pat, pat[1:])] == [1, 2, 4, 8] and 19 + 16 == 35
add('Numerical Patterns', 'Lower 1 MA #21', 67.1, 'x', '8/30 &middot; o o o o x o &middot; last miss 11/20',
    'Use the number pattern to answer the question.<div style="margin:8px 0;font-size:1.15em;letter-spacing:0.15em">4&nbsp; 5&nbsp; 7&nbsp; 11&nbsp; 19&nbsp; __</div>What is the next number in the pattern?',
    ['23', '27', '35', '38'], '35',
    {'23': 'Added 4 again', '27': 'Known trap (like 27 on the real one, her pick): added the last jump (8) again', '38': 'Doubled the last number'},
    'the next number',
    'Jumps: +1, +2, +4, +8. Each jump doubles, so the next jump is +16: 19 + 16 = 35.',
    'Same: doubling jumps, next number')
est12 = F(39*812, 20)
assert 1200 < est12 < 2000 and F(40*800, 20) == 1600
add('Estimating Multiplication & Division', 'WTE QR #33', 49.0, 'x', '9/36 &middot; x o o o x o &middot; last miss 11/20',
    'Josh did the problem shown with his calculator. What is a reasonable estimation for his answer?<div style="margin:8px 0;font-size:1.2em">' + frac('39 &times; 812', '20') + '</div>',
    ['between 1,000 and 1,200', 'between 1,200 and 2,000', 'between 2,000 and 2,500', 'between 2,500 and 3,000'], 'between 1,200 and 2,000',
    {'between 1,000 and 1,200': 'Rounded too far down (35 &times; 700 &divide; 20)', 'between 2,000 and 2,500': 'Known trap (her pick on the real one): rounded 20 down to 15 (40 &times; 800 &divide; 15)',
     'between 2,500 and 3,000': 'Divided by 10 or 12 instead of 20'},
    'about how much',
    'Round to friendly numbers: 40 &times; 800 = 32,000, and 32,000 &divide; 20 = 1,600. (Exactly 1,583.4.)',
    'Same: (a &times; b) &divide; c with the same four ranges; new numbers')
est13 = F(85, 11) * 162
assert 1200 < est13 < 1500 and F(88, 11)*160 == 1280 and 7*160 == 1120
add('Estimating Multiplication & Division', 'Lower 6 QR #36', 50.1, 'x (107 s)', '9/36 &middot; x o o o x o &middot; last miss 11/20',
    'Ella did the problem 85 &divide; 11 &times; 162. Approximately what was her answer?',
    ['between 600 and 900', 'between 900 and 1,200', 'between 1,200 and 1,500', 'between 1,500 and 1,800'], 'between 1,200 and 1,500',
    {'between 600 and 900': 'Rounded 85 &divide; 11 down to 5', 'between 900 and 1,200': 'Known trap (her pick on the real one was the range below): rounded 85 &divide; 11 down to 7',
     'between 1,500 and 1,800': 'Rounded 85 &divide; 11 up to 10'},
    'about how much',
    'Left to right. 85 is close to 88, and 88 &divide; 11 = 8. Then 8 &times; 160 = 1,280. (Exactly about 1,252.)',
    'Same: a &divide; b &times; c with four ranges; new numbers')
left14 = F('3.4') - F(3, 4)
assert F(5, 2) < left14 < 3
add('Adding and Subtracting Decimals', 'Lower 1 QR #29', 56.9, 'x', '3/12 &middot; not practiced since 11/1 &middot; last miss 10/6',
    'A pitcher holds 3.4 liters of juice. Maria pours three cups of juice, totaling ' + frac(3, 4) + ' liter. How much juice is left in the pitcher?',
    ['less than ' + frac(3, 4) + ' liter', 'more than 2 and less than 2' + frac(1, 2) + ' liters', 'more than 2' + frac(1, 2) + ' and less than 3 liters', 'more than 3 liters'],
    'more than 2' + frac(1, 2) + ' and less than 3 liters',
    {'less than ' + frac(3, 4) + ' liter': 'Read the 3/4 as what is left (her pick on the real one)', 'more than 2 and less than 2' + frac(1, 2) + ' liters': 'Took away 1 whole liter instead of 3/4',
     'more than 3 liters': 'Took away 0.34 or 0.4'},
    'how much is left',
    '3/4 liter = 0.75 liter. 3.4 &minus; 0.75 = 2.65 liters, which is more than 2.5 and less than 3.',
    'Same: a decimal amount minus a fraction amount, answer as a range')
digs15 = [0, 2, 3, 4, 6, 8]
best15 = max(int(''.join(map(str, p))) for p in permutations(digs15) if p[0] != 0 and p[-1] % 2 == 1)
plain15 = max(int(''.join(map(str, p))) for p in permutations(digs15) if p[0] != 0)
assert best15 == 864203 and (best15 // 100) % 10 == 2 and (plain15 // 100) % 10 == 3 and (best15 // 10) % 10 == 0
add('Value of Digits', 'Official QR #36', 57.0, 'x (36 s)', '4/16 &middot; o x o x o o &middot; last miss 11/17',
    'Students were asked to write a new number using all the guidelines below and the digits 0, 2, 3, 4, 6, and 8. What digit is in the hundreds place for the new number?',
    ['0', '2', '3', '8'], '2',
    {'0': 'Read the tens place', '3': 'Forgot the number must be odd (864,320)', '8': 'Read the first digit (like 9 on the real one, her pick)'},
    'the hundreds digit',
    'Odd: 3 is the only odd digit, so it must be last. Largest: the other digits go biggest first: 8, 6, 4, 2, 0. The number is 864,203. Hundreds place: 2.',
    'Same: one digit is forced last by odd/even, largest number, a middle place asked',
    rules_box('The number must have 6 digits.', 'The number must be odd.', 'The number must be the largest possible number.'))
sq16 = 36 // 4; others16 = 54 - 3*sq16
assert sq16 == 9 and others16 == 27 and others16 + sq16 == 36 and 12 + 15 == 27 and 9**2 + 12**2 == 15**2
fig16 = svg(250, 140, f'<polygon points="20,20 110,20 110,110 20,110" {SW}/><polygon points="110,20 110,110 230,110" {SW}/>')
add('Area and Perimeter of Complex Polygons', 'Lower 1 QR #38', 33.8, 'x', '8/40 &middot; o o o o o x &middot; last miss 11/25',
    'The figure shown is made of a square and a triangle. The perimeter of the largest polygon is 54 centimeters. The perimeter of the square is 36 centimeters. What is the perimeter of the triangle?',
    ['9 centimeters', '18 centimeters', '27 centimeters', '36 centimeters'], '36 centimeters',
    {'9 centimeters': 'Gave the square\'s side', '18 centimeters': 'Subtracted the perimeters (54 &minus; 36)', '27 centimeters': 'Stopped early: only the two outside sides of the triangle (her pick on the real one)'},
    'perimeter of the triangle',
    'Square side = 36 &divide; 4 = 9. The largest polygon\'s outside has 3 square sides (27) and the triangle\'s 2 outside sides, so those two add to 54 &minus; 27 = 27. The triangle also has the shared side: 27 + 9 = 36.',
    'Same: square + triangle sharing a side, two perimeters given', fig16)
unk17 = (30 - 2*11) // 2
assert unk17 == 4 and 2*unk17 - unk17 == 4
fig17 = svg(230, 120, f'<rect x="20" y="15" width="165" height="70" {SW}/>' + txt(102, 106, '11 cm') + txt(206, 55, '?', 16))
add('Perimeter', 'Lower 5 QR #33', 66.1, 'x (145 s)', '8/40 &middot; o o o o o x &middot; last miss 11/25',
    'Ben builds picture frames. The first rectangular frame he builds has a perimeter of 30 centimeters (cm). The length of one of the sides is shown. If the unknown side length of the next frame he builds is doubled, by what amount will he increase the unknown side length of the next frame?',
    ['4', '8', '15', '19'], '4',
    {'8': 'Gave the new side length, not the increase', '15': 'Half the perimeter (the two sides together)', '19': 'Subtracted only one side (30 &minus; 11)'},
    'the increase',
    'Two 11 cm sides use 22 cm, so the two unknown sides use 30 &minus; 22 = 8 cm: each is 4 cm. Doubled, it becomes 8 cm, an increase of 4 cm.',
    'Same as the real one, new numbers', fig17)
fig18 = svg(330, 185, f'<polygon points="80,22 155,22 155,112 260,112 260,157 80,157" {SW}/>' + txt(118, 16, '5 miles') + txt(72, 94, '8 miles', 14, 'end')
            + txt(170, 177, '12 miles') + txt(268, 139, '3 miles', 14, 'start'))
assert 2*(12 + 8) == 40 and 5 + 8 + 12 + 3 == 28 and (12 - 5) == 7 and (8 - 3) == 5
add('Area and Perimeter of Complex Polygons', 'Lower 6 QR #30', 69.5, 'x (13 s)', '8/40 &middot; o o o o o x &middot; last miss 11/25',
    'What is the perimeter of the figure?', ['28 miles', '33 miles', '35 miles', '40 miles'], '40 miles',
    {'28 miles': 'Known trap (like 27 on the real one, her pick): added only the labeled sides', '33 miles': 'Added only one unlabeled side (5)', '35 miles': 'Added only one unlabeled side (7)'},
    'perimeter (all 6 sides)',
    'The two unlabeled sides: across = 12 &minus; 5 = 7, up = 8 &minus; 3 = 5. Perimeter = 5 + 8 + 12 + 3 + 7 + 5 = 40. (Shortcut: 2 &times; (12 + 8) = 40.)',
    'Same: L-shape with two unlabeled inner sides', fig18)
oth19 = 6 + 2 + 4
assert F(oth19) / F(3, 4) == 16 and 16 - oth19 == 4 and oth19 // 4 == 3
add('Probability of 1 Event, given a List of Items', 'Official QR #34', 57.6, 'x (59 s)', '3/28 &middot; o o x o x o &middot; last miss 11/20',
    'The table shows the number of each color of marble Nina has in a bag. If the probability of randomly taking a purple marble out of the bag on the first try is ' + frac(1, 4) + ', how many purple marbles are in the bag?',
    ['3', '4', '5', '6'], '4',
    {'3': 'Known trap (like her pick on the real one): took 1/4 of the other 12 marbles', '5': 'Guessed one more than the answer', '6': 'Matched the biggest color count'},
    'how many purple',
    'Purple is 1/4 of the bag, so the other colors are 3/4. Red + green + blue = 6 + 2 + 4 = 12 = 3/4 of the bag. 1/4 is 4, so purple = 4. Check: 4 out of 16 = 1/4.',
    'Same: unit fraction, unknown count in a table (1/4 instead of 1/3)',
    table(['Color', 'Number of Marbles'], [['Red', 6], ['Green', 2], ['Blue', 4], ['Purple', '?']], 'NINA\'S MARBLES'))
for a, b in ((2, 7), (4, 10), (4, 14), (6, 14)):
    assert (F(a, a + b) == F(2, 7)) == ((a, b) == (4, 10))
add('Finding Ratios given Probability', 'Lower 1 QR #34', 42.4, 'o', '3/28 &middot; o o x o x o &middot; last miss 11/20',
    'Ana has a bag of marbles in different colors: blue, red, green, and yellow. The probability of picking a blue marble is 2 out of 7. What combination of marbles reflects this probability?',
    ['2 blue marbles and 7 other marbles', '4 blue marbles and 10 other marbles', '4 blue marbles and 14 other marbles', '6 blue marbles and 14 other marbles'],
    '4 blue marbles and 10 other marbles',
    {'2 blue marbles and 7 other marbles': 'Known trap (39.5% picked this on the real one): used 7 as the OTHER marbles, not the total',
     '4 blue marbles and 14 other marbles': 'Doubled the 2 and the 7 but used 14 as the others', '6 blue marbles and 14 other marbles': '6 out of 20 = 3/10, not 2/7'},
    'blue out of ALL the marbles',
    '2 out of 7 means 2 blue for every 7 marbles in all, so 2 blue and 5 others. 4 blue and 10 others is 4 out of 14 = 2/7.',
    'Same: probability as "out of", choose the combination', free=True)
def fits(n): return F(n, 6) + F(1, 3) <= 1
assert F(1, 6) + F(1, 3) == F(1, 2) and F(3, 6) + F(1, 3) == F(5, 6) > F(3, 4) and F(4, 6) + F(1, 3) == 1 and not fits(5)
add('Adding and Subtracting Fractions', 'Lower 2 QR #36', 43.6, 'x', '1/13 &middot; not practiced since 11/6 &middot; last miss 9/13',
    'Lily has two equal-sized jars of rice. The first jar is ' + frac('n', 6) + ' full. The second jar is ' + frac(1, 3) + ' full. The rice from these jars will be combined by pouring the rice from the first jar into the second jar. Which statement best describes the amount of rice once the jars are combined?',
    ['If n = 1, then the amount of rice is less than ' + frac(1, 2) + ' of a jar.', 'If n = 3, then the amount of rice is less than ' + frac(3, 4) + ' of a jar.',
     'If n = 4, then the rice will not all fit in 1 jar.', 'If n = 5, then the rice will not all fit in 1 jar.'],
    'If n = 5, then the rice will not all fit in 1 jar.',
    {'If n = 1, then the amount of rice is less than ' + frac(1, 2) + ' of a jar.': 'It is exactly 1/2, not less',
     'If n = 3, then the amount of rice is less than ' + frac(3, 4) + ' of a jar.': '3/6 + 1/3 = 5/6, more than 3/4',
     'If n = 4, then the rice will not all fit in 1 jar.': 'Known trap (like her pick on the real one): 4/6 + 1/3 is exactly 1 jar, so it fits'},
    'which statement is true',
    'Use sixths: 1/3 = 2/6. n = 5: 5/6 + 2/6 = 7/6, more than 1 jar, so it will not all fit. (n = 1 gives exactly 1/2; n = 3 gives 5/6; n = 4 gives exactly 1 jar.)',
    'Same: n/denominator + a fraction, check four statements')
# ---------------- B. missed often before, right since ----------------
assert 10*10 == 100 and 8*12 == 96 and 4*10 == 2*(8 + 12)
add('Comparing Areas', 'Lower 2 QR #38', 41.1, 'x', '4/10 &middot; x o o o o o &middot; last miss 11/3',
    'The floor of Room A is in the shape of a square and has an area of 100 feet&sup2;. The floor of Room B is in the shape of a rectangle and has a length of 12 feet and a width of 8 feet. Which statement correctly compares the floors in the two rooms?',
    ['The area of the floor in Room A is the same as the area of the floor in Room B.', 'The area of the floor in Room A is less than the area of the floor in Room B.',
     'The perimeter of the floor in Room A is less than the perimeter of the floor in Room B.', 'The perimeter of the floor in Room A is equal to the perimeter of the floor in Room B.'],
    'The perimeter of the floor in Room A is equal to the perimeter of the floor in Room B.',
    {'The area of the floor in Room A is the same as the area of the floor in Room B.': '100 vs 96: not the same',
     'The area of the floor in Room A is less than the area of the floor in Room B.': 'Room A is larger (100 &gt; 96)',
     'The perimeter of the floor in Room A is less than the perimeter of the floor in Room B.': 'Known trap (her pick on the real one): both are 40 feet'},
    'which statement is true',
    'Room A: side = 10 (10 &times; 10 = 100), perimeter 40. Room B: area 96, perimeter 2 &times; (12 + 8) = 40. The perimeters are equal.',
    'Same: square from its area vs a rectangle, compare area and perimeter', free=True)
assert 4*15 == 6*10 == 60 and 7*8 != 60 and 4*16 != 60 and 6*11 != 60
add('Comparing Areas', 'Lower 2 QR #29', 65.1, 'x', '4/10 &middot; x o o o o o &middot; last miss 11/3',
    'The length and width of the array shown represent two factors of a number.<div style="margin:8px 0">' + grid_array(4, 15) + '</div>Which array represents two different factors of the same number?',
    [grid_array(6, 10), grid_array(7, 8), grid_array(6, 11), grid_array(4, 16)], grid_array(6, 10),
    {grid_array(7, 8): '7 by 8 = 56, not 60', grid_array(6, 11): '6 by 11 = 66, not 60 (a close shape, like her pick on the real one)', grid_array(4, 16): '4 by 16 = 64: same width, not the same number'},
    'same number (60), different factors',
    'The array shown is 4 rows of 15 = 60. Count each choice: 6 &times; 10 = 60 (the same number, with different factors), 7 &times; 8 = 56, 6 &times; 11 = 66, 4 &times; 16 = 64.',
    'Same: a factor-pair array, find another array with the same product; near-miss arrays as choices', free=True)
add('Data Collection & Random Sampling', 'Lower 6 QR #38', 18.4, 'x (135 s)', '3/9 &middot; x x o o o o &middot; last miss 11/10',
    'Ms. Ortiz\'s class watched a bird feeder and collected data. They listed what they observed in categories or groups.<div style="margin:8px 0 8px 12px">1. Kinds of birds seen: robin, blue jay, cardinal, sparrow<br>2. Color of each bird\'s feathers<br>3. ?</div>Which information best completes the class\'s observation list?',
    ['the number of minutes each bird stayed at the feeder', 'how many seeds each bird ate', 'how many of each kind of bird visited', 'the type of food each bird ate'],
    'the type of food each bird ate',
    {'the number of minutes each bird stayed at the feeder': 'A number (measure), not a category like the list', 'how many seeds each bird ate': 'A number (count), not a category',
     'how many of each kind of bird visited': 'A count, not a category (her pick type on the real one)'},
    'a category like the other two',
    'Items 1 and 2 are categories (kinds of birds, colors). Three choices ask for a number; only "the type of food" is a category. Find the one choice that is different from the other three.',
    'Same: complete a list of categories; three numeric choices and one category', free=True)
assert (6 - 3) + (9 - 3) == 9 and 3 + 3 == 6 and 15 - 3 == 12 and F(2, 3)*15 == 10
add('Remaining Amount after Reducing by Fractions', 'Lower 1 MA #25', 64.9, 'x', '5/17 &middot; x x o o o o &middot; last miss 11/6',
    'Leo had 6 markers and 9 crayons. He lost half of his markers and a third of his crayons. How many markers and crayons does he have remaining?',
    ['6', '9', '10', '12'], '9',
    {'6': 'Stopped early: this is how many he lost', '10': 'Took 2/3 of the total 15 instead of each group', '12': 'Took away only the 3 crayons (15 &minus; 3)'},
    'how many are left',
    'Markers: half of 6 is 3 lost, 3 left. Crayons: a third of 9 is 3 lost, 6 left. 3 + 6 = 9 left.',
    'Same: a different unit fraction of each of two groups, how many left')
def dsum(n): return sum(map(int, str(n)))
assert 5103 % 9 == 0 and 5129 % 9 and 5127 % 9 and 5127 % 3 == 0 and 5919 % 9 and dsum(5103) == 9
add('No Remainder when Divided by a given Number', 'Lower 1 MA #24', 68.1, 'x', '7/24 &middot; o o o o o o &middot; last miss 11/3',
    'Which whole number is divisible by 9?', ['5,103', '5,127', '5,129', '5,919'], '5,103',
    {'5,127': 'Known trap (like her pick on the real one): digit sum 15 is divisible by 3, not by 9', '5,129': 'Digit sum 17', '5,919': 'Ends in 9, but digit sum 24 is not a multiple of 9'},
    'divisible by 9',
    'A number is divisible by 9 when its digits add to a multiple of 9. 5 + 1 + 0 + 3 = 9, so 5,103 &divide; 9 = 567.',
    'Same: four 4-digit numbers, digit-sum rule for 9; one choice divisible by 3 only')
# balance: scale 1: T C C = T S -> C C = S ; scale 2: C C S = T T -> S S = T T -> S = T
add('Interpreting Pictographs', 'Lower 5 QR #34', 63.1, 'x (24 s)', '8/30 &middot; o o o o o o &middot; last miss 11/3',
    'The scales shown are balanced.<div style="margin:8px 0">' + balance('TCC', 'TS') + '<br>' + balance('CCS', 'TT') + '</div>Which set of figures would create a balanced scale?',
    [balance('S', 'TT', 0.6), balance('T', 'SS', 0.6), balance('S', 'T', 0.6), balance('S', 'C', 0.6)], balance('S', 'T', 0.6),
    {balance('S', 'TT', 0.6): 'Read the second scale as square = 2 triangles', balance('T', 'SS', 0.6): 'Known trap (like her pick on the real one): one shape = two of the other',
     balance('S', 'C', 0.6): 'A square balances TWO circles, not one'},
    'which scale balances',
    'Scale 1: take one triangle off each side, so 2 circles = 1 square. Scale 2: replace the 2 circles with 1 square: square + square = triangle + triangle, so 1 square = 1 triangle.',
    'Same: two balanced scales, substitute between them', free=True)
assert (120 // 6) * (60 // 5) == 240
add('Matching Stories to Equations', 'Lower 2 QR #32', 59.4, 'x', '5/22 &middot; o o o o o o &middot; last miss 11/10',
    'Dana wants to cover a patio with tiles. Her patio is 120 inches long and 60 inches wide. Each tile is 6 inches long and 5 inches wide. If she knows how to find the area of a rectangle, how can Dana determine how many tiles she will need without laying them all on the patio? (A = l &times; w)',
    ['(120 &minus; 36) &times; (60 &minus; 25)', '(120 &minus; 6) &times; (60 &minus; 5)', '(120 &divide; 36) &times; (60 &divide; 25)', '(120 &divide; 6) &times; (60 &divide; 5)'],
    '(120 &divide; 6) &times; (60 &divide; 5)',
    {'(120 &minus; 36) &times; (60 &minus; 25)': 'Subtracted squares of the tile sides (her pick type on the real one)', '(120 &minus; 6) &times; (60 &minus; 5)': 'Subtracted instead of divided',
     '(120 &divide; 36) &times; (60 &divide; 25)': 'Divided by the squares of the tile sides'},
    'number of tiles (expression)',
    'Tiles along the length: 120 &divide; 6 = 20. Tiles along the width: 60 &divide; 5 = 12. Total tiles = (120 &divide; 6) &times; (60 &divide; 5) = 240.',
    'Same: tiles along length &times; tiles along width; same four forms', free=True)
don = [38, 52, 29]
assert sum(don) == 119 and 2*sum(don) == 238
add('Determining Total Cost', 'Lower 6 MA #30', 50.2, 'x (210 s)', '2/14 &middot; o o x o o o &middot; last miss 11/8',
    'Kofi\'s aunt matches all of the money he donates in June. This means that for every dollar Kofi donates to a charity, his aunt will also donate a dollar to that charity. The table shows how much money Kofi donated in June. What was the total amount of money these charities received?',
    ['$117', '$119', '$234', '$238'], '$238',
    {'$117': 'Addition slip', '$119': 'Stopped early: this is Kofi\'s donations only (her pick on the real one)', '$234': 'Doubled the addition slip'},
    'total the charities received',
    'Kofi gave 38 + 52 + 29 = $119. His aunt gave the same, $119. Total = $119 &times; 2 = $238.',
    'Same: 1-for-1 match of a table total',
    table(['Charity', 'Amount Donated'], [['Food Bank', '$38'], ['Animal Shelter', '$52'], ['Library Fund', '$29']], 'KOFI\'S DONATIONS IN JUNE'))
stem30 = {3: [2, 5, 5, 8], 4: [0, 4, 4, 4, 7], 5: [1, 6, 9], 6: [0, 3]}
v30 = [10*k + l for k, ls in stem30.items() for l in ls]
assert len(v30) == 14 and v30.count(32) == 1 and min(v30) == 32 and v30.count(51) == 1 and sum(x >= 51 for x in v30) == 5
add('Identifying Correct Conclusions from Bar Graph Data Table', 'Lower 2 QR #37', 41.7, 'x', 'x o o (same build: MA5 #13, MA6 #2)',
    'The stem-and-leaf plot shows the heights of 14 plants in a garden, where 4 | 7 represents 47 centimeters. Based on the data in the stem-and-leaf plot, which conclusion is true?',
    ['A height of 32 centimeters was measured 2 times.', 'Every plant was at least 35 centimeters tall.', 'Three plants were 51 centimeters tall.', 'Exactly 5 plants were at least 51 centimeters tall.'],
    'Exactly 5 plants were at least 51 centimeters tall.',
    {'A height of 32 centimeters was measured 2 times.': '32 appears once', 'Every plant was at least 35 centimeters tall.': 'One plant was 32 cm',
     'Three plants were 51 centimeters tall.': 'Known trap (like her pick on the real one): counted the whole 5 row as 51s'},
    'which conclusion is true',
    'Values: 32, 35, 35, 38, 40, 44, 44, 44, 47, 51, 56, 59, 60, 63. At least 51: 51, 56, 59, 60, 63 = 5 plants.',
    'Same: 14 values on 4 stems, an "at least ... exactly" count is true', stem_plot('PLANT HEIGHTS (CM)', stem30))
add('Identifying Shapes', 'Lower 5 MA #28', 62.0, 'x (18 s)', '3/24 &middot; o o o o o o &middot; last miss 11/15',
    'Which figure best describes a quadrilateral with all four sides equal and angles that are not right angles?',
    ['parallelogram', 'rhombus', 'square', 'trapezoid'], 'rhombus',
    {'parallelogram': 'Known trap (her pick on the real one): a parallelogram\'s sides need not all be equal', 'square': 'A square has four right angles', 'trapezoid': 'Only one pair of parallel sides'},
    'name of the shape',
    'Four equal sides is a rhombus. A square is a rhombus with right angles, so a rhombus without right angles is not a square.',
    'Same: describe a quadrilateral, choose its name (rhombus, as on the real one)')
add('Interpreting Linear Equations from Word Problems', 'Lower 1 QR #33', 54.4, 'x', '1/7 &middot; x o o o o o &middot; last miss 8/30',
    'A baker frosted &square; cupcakes in the morning and &#9675; cupcakes in the afternoon. She used &#9651; grams of frosting on each cupcake. Which expression represents the total amount of frosting, in grams, the baker used?',
    ['(&square; + &#9675;) &divide; &#9651;', '(&square; + &#9675;) + &#9651;', '(&square; + &#9675;) &times; &#9651;', '&square; + &#9675; &times; &#9651;'],
    '(&square; + &#9675;) &times; &#9651;',
    {'(&square; + &#9675;) &divide; &#9651;': 'Divided instead of multiplied', '(&square; + &#9675;) + &#9651;': 'Added the grams once (her pick on the real one)',
     '&square; + &#9675; &times; &#9651;': 'No parentheses: only the afternoon cupcakes get frosting'},
    'total frosting (expression)',
    'Total cupcakes: &square; + &#9675;. Each uses &#9651; grams: (&square; + &#9675;) &times; &#9651;.',
    'Same: (&square; + &#9675;) &times; &#9651;; one choice drops the parentheses', free=True)
amts = ['27.85', '43.12', '36.49', '52.91', '39.70']
assert abs(sum(map(float, amts)) - 200.07) < 1e-9 and sum(round(float(a)) for a in amts) == 200
add('Estimating Sums Differences of Decimal Numbers', 'Lower 2 MA #27', 55.3, 'x', '2/13 &middot; o x o o o o &middot; last miss 10/14',
    'During a 5-month period, Sam\'s phone bills were $27.85, $43.12, $36.49, $52.91, and $39.70. What is the closest approximation of the total cost of Sam\'s phone bills during the 5-month period?',
    ['$190', '$200', '$210', '$215'], '$200',
    {'$190': 'Rounded every bill down', '$210': 'Rounded every bill up', '$215': 'Rounded every bill up to the next $5 (like her pick on the real one)'},
    'closest total',
    'Round each bill to the nearest dollar: 28 + 43 + 36 + 53 + 40 = 200. (Exactly $200.07.)',
    'Same: five money amounts, closest total among four nearby choices')
add('Comparing Volume of Cubes', 'Lower 3 QR #29', 72.2, 'x', '6/15 &middot; o o x o x o &middot; last miss 11/24',
    'Volume is the space an object takes up. A box is packed with 64 one-inch cubes. There is empty space between some of the cubes in the box. Which statement best describes the volume of the box?',
    ['The volume of the box is exactly 64 cubic inches.', 'The volume of the box is less than 64 cubic inches.', 'The volume of the box is greater than 64 cubic inches.', 'The volume of the box is exactly two times 64 cubic inches.'],
    'The volume of the box is greater than 64 cubic inches.',
    {'The volume of the box is exactly 64 cubic inches.': 'Counted only the cubes, not the empty space', 'The volume of the box is less than 64 cubic inches.': 'Known trap (her pick on the real one): the gaps make the box bigger, not smaller',
     'The volume of the box is exactly two times 64 cubic inches.': 'No reason for exactly double'},
    'volume of the box',
    'The box holds the 64 cubic inches of cubes AND the empty space, so its volume is more than 64 cubic inches.',
    'Same as the real one, new numbers', free=True)
# --- the 4 the parent had rested on 11/19, approved again 11/27 ---
ch35 = [2104, 2140, 2330, 2500]
assert [c % 8 == 0 for c in ch35] == [True, False, False, False] and 2140 % 4 == 0 and 2500 % 4 == 0 and 2330 % 2 == 0
add('No Remainder when Divided by a given Number', 'Lower 1 MA #29', 39.1, 'x', '7/24 &middot; o o o o o o &middot; last miss 11/3',
    'Ava and 7 other students have each sold an equal number of raffle tickets. Which number could represent the total number of raffle tickets the students have sold?',
    ['2,104', '2,140', '2,330', '2,500'], '2,104',
    {'2,140': 'Known trap (like her pick on the real one): divisible by 4, not by 8', '2,330': 'Divisible by 2 only', '2,500': 'Divisible by 4, not by 8'},
    'divisible by 8 (Ava + 7 = 8 students)',
    'Ava and 7 others make 8 students, so the total must be divisible by 8. 2,104 &divide; 8 = 263. (Check the last three digits: 104 &divide; 8 = 13.)',
    'Same: "and 7 others" = 8, choose the multiple of 8; two choices divisible by 4 only')
for p_, c_ in ((2, 4), (3, 9), (5, 6), (2, 9)):
    pr = p_ * c_
    assert any(pr % d == 0 for d in range(2, pr)) and pr > 1
assert 3*9 % 2 == 1 and 2*4 % 2 == 0
add('Classification of Numbers, given a Set', 'Lower 2 MA #29', 34.4, 'x', '1/14 &middot; o o o o o o &middot; last miss 9/13',
    'Two numbers are greater than 1. One is a prime number and the other is a composite number. What will always describe the product of the two numbers?',
    ['odd number', 'even number', 'prime number', 'composite number'], 'composite number',
    {'odd number': 'Known trap (her pick on the real one): true for 3 &times; 9 = 27, but 2 &times; 4 = 8 is even', 'even number': 'True for 2 &times; 4 = 8, but 3 &times; 9 = 27 is odd',
     'prime number': 'A product of two numbers greater than 1 is never prime'},
    'always true',
    'Try examples: 2 &times; 4 = 8 (even), 3 &times; 9 = 27 (odd). Odd and even both fail once. Both factors are greater than 1, so the product always has those factors: it is always composite.',
    'Same: classify a product of two kinds of numbers; prime &times; composite instead of prime &times; odd')
add('Area of Triangles', 'Lower 2 MA #30', 32.1, 'x', '2/8 &middot; o o x o o o &middot; last miss 11/6',
    'The base of a triangle is 10 meters (m). Which statement correctly compares the value of A to the base and height of the triangle? (A = ' + frac(1, 2) + ' &times; base &times; height)',
    ['The value of A is always ' + frac(1, 2) + ' the value of the height.', 'The value of A is always 5 times the value of the height.', 'The value of A is always 10 times the value of the height.', 'The value of A can be the same as the value of the height.'],
    'The value of A is always 5 times the value of the height.',
    {'The value of A is always ' + frac(1, 2) + ' the value of the height.': 'Used only the 1/2', 'The value of A is always 10 times the value of the height.': 'Forgot the 1/2',
     'The value of A can be the same as the value of the height.': 'Known trap (her pick on the real one): A = 5 &times; height, never equal (unless 0)'},
    'how A compares with the height',
    'A = 1/2 &times; 10 &times; height = 5 &times; height. So A is always 5 times the height.',
    'Same: fixed base, compare A to the height (base 10 instead of 6)')
add('Matching Stories to Equations', 'Lower 3 QR #37', 48.0, 'x', '5/22 &middot; o o o o o o &middot; last miss 11/10',
    'A group of friends shared the cost of a pizza equally. The list shows what is known.<div style="margin:8px 0 8px 12px">The number of friends is &square;.<br>Each friend paid &#9651; dollars.</div>Which equation will determine &#9675;, the total cost of the pizza?',
    ['&#9675; = &#9651; &divide; &square;', '&#9675; = &#9651; + &square;', '&#9675; = &#9651; &minus; &square;', '&#9675; = &#9651; &times; &square;'],
    '&#9675; = &#9651; &times; &square;',
    {'&#9675; = &#9651; &divide; &square;': 'Known trap: divided as in the real one, but this asks the total, not each share', '&#9675; = &#9651; + &square;': 'Added',
     '&#9675; = &#9651; &minus; &square;': 'Subtracted'},
    'the total cost',
    'Each of &square; friends paid &#9651;, so the total is &#9651; &times; &square;. (The real one asked each share: total &divide; people. This asks the other way.)',
    'Same one-step equation, asked the other way (the total instead of each share)', free=True)

assert len(P) == 38, len(P)
# ---- order by the real problem's % right, highest first (rising difficulty, like the real test) ----
P.sort(key=lambda p: -p['pct'])
# ---- balance answer letters: numeric/ordered choices stay put; "free" ones may be rotated ----
for p in P:
    p['correct'] = 'ABCD'[p['ch'].index(p['right'])]
cnt = Counter(p['correct'] for p in P if not p['free'])
for i, p in enumerate(P):
    if not p['free']: continue
    def ok(L):
        s_ = [q['correct'] for q in P]; s_[i] = L
        return all(not (s_[j] == s_[j+1] == s_[j+2]) for j in range(max(0, i-2), min(i+1, len(P)-2)))
    opts = sorted(range(4), key=lambda r: cnt['ABCD'[(p['ch'].index(p['right']) - r) % 4]])
    for r in opts:
        c2 = p['ch'][r:] + p['ch'][:r]; L = 'ABCD'[c2.index(p['right'])]
        if ok(L): break
    p['ch'] = c2; p['correct'] = L; cnt[L] += 1
cnt = Counter(p['correct'] for p in P)
# break any run of three equal letters by swapping with the next problem of a different letter (order by % right is approximate)
for _ in range(10):
    sq = [p['correct'] for p in P]
    bad = [i for i in range(len(sq) - 2) if sq[i] == sq[i+1] == sq[i+2]]
    if not bad: break
    i = bad[0] + 2
    j = next(k for k in range(i + 1, len(P)) if P[k]['correct'] != sq[i])
    P[i], P[j] = P[j], P[i]
seq = ''.join(p['correct'] for p in P)
assert max(cnt.values()) - min(cnt.values()) <= 2, (cnt, seq)
assert all(not (seq[i] == seq[i+1] == seq[i+2]) for i in range(len(seq) - 2)), seq
for p in P:
    if re.search(r'shown|the table|guidelines below|stem-and-leaf plot shows|scales shown', p['q'], re.I):
        assert p['diagram'] or '<svg' in p['q'] or '<div' in p['q'], p['ref']
out = []
for n, p in enumerate(P, 1):
    tagline = ' &middot; '.join(f'<b>{"ABCD"[p["ch"].index(c)]}</b>: {v}' for c, v in p['tags'].items())
    out.append({'n': n, 'tier': 'Hard', 'topic': p['topic'], 'q': p['q'], 'choices': dict(zip('ABCD', p['ch'])), 'correct': p['correct'],
                'key': f'<b>Answer: {p["correct"]}.</b> <i>The question asks for: {p["asks"]}.</i> {p["key"]} <br>Wrong choices: {tagline}',
                'ref': f'Topic: {p["topic"]} &middot; Built on: {p["ref"]} (last third, {p["pct"]}% right; her result: {p["her"]}) &middot; Her record: {p["record"]} &middot; Compared with the real one: {p["vs"]}',
                'diagram': p['diagram'], 'gid': None, 'ma_idx': None, 'tags': {"ABCD"[p['ch'].index(c)]: v for c, v in p['tags'].items()}})
json.dump(out, open(os.path.join(HERE, 'set12_problems.json'), 'w'), indent=1)
json.dump({str(o['n']): dict(topic=o['topic'], built_on=f"{P[o['n']-1]['ref']} ({P[o['n']-1]['pct']}%, her {P[o['n']-1]['her']})", last5=P[o['n']-1]['record'],
           comparable_wrong='', vs_latest=P[o['n']-1]['vs'], asks=P[o['n']-1]['asks'],
           stop_early=[L for L, v in o['tags'].items() if v.startswith('Stopped early')]) for o in out},
          open(os.path.join(HERE, 'set12_mapping.json'), 'w'), indent=1)
print(cnt, seq)
