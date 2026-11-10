"""QR Set 10 (2026-11-10). Plan agreed with the parent 11/10:
- every Practice Test 6 miss (QR 18, 25, 36, 38; MA 12, 13, 28, 30), re-read after the parent talked with Hannah;
- real last-third misses she got wrong again the last time we practiced them;
- real last-third misses not practiced since; a few thin real-test topics.
Every problem is built like the real last third (feedback_hard_means_construction). Every math claim is asserted.
COMPARE holds the original-vs-new difficulty comparison the parent asked for; it is written to set10_mapping.json."""
import json, os, math
from fractions import Fraction as F
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
T = {x['topic']: x for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}
SW = 'stroke="currentColor" stroke-width="1.6"'
def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def svg(w, h, body): return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{body}</svg>'
def txt(x, y, s, size=13, anchor='middle'): return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="currentColor">{s}</text>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def lines(*ls): return ''.join(f'<div>{l}</div>' for l in ls)

P, COMPARE = [], {}
def add(topic, q, ch, ans, key, model, cmp, diagram=None, habit=None):
    assert topic in T, topic
    assert len(set(ch)) == 4 and ans in 'ABCD'
    n = len(P) + 1
    t = T[topic]
    hist = f"Wrong so far: {t.get('wrong')}/{t.get('graded')}" if t.get('graded') else 'Few graded instances so far'
    P.append({'n': n, 'tier': 'Hard', 'topic': topic, 'q': q, 'choices': dict(zip('ABCD', ch)), 'correct': ans,
              'key': f'<b>Answer: {ans}.</b> {key}', 'habit_note': habit,
              'ref': f'Topic: {topic} &middot; Diagram: {"yes" if diagram else "no"} &middot; {hist} &middot; New problem &middot; Built like: {model}',
              'diagram': diagram, 'needs_diagram': bool(diagram)})
    COMPARE[n] = dict(model=model, **cmp)

def C(orig, lang, steps, conds, verdict):
    return dict(orig=orig, lang=lang, steps=steps, conds=conds, verdict=verdict)

# ---------- diagrams ----------
def floor_grid(cols, rows, white):
    u, b = 30, ''
    for r in range(rows):
        for c in range(cols):
            b += f'<rect x="{c*u+2}" y="{r*u+2}" width="{u}" height="{u}" fill="{"#ffffff" if (r,c) in white else "#7d8c87"}" {SW}/>'
    return svg(cols*u+4, rows*u+4, b)

def square_triangle():  # square on the left, right triangle on the right sharing the square's right side
    return svg(250, 130, f'<polygon points="10,10 120,10 230,120 10,120" fill="none" {SW}/>'
               f'<line x1="120" y1="10" x2="120" y2="120" {SW}/>' + txt(65, 70, 'square', 13) + txt(150, 95, 'triangle', 13))

# symmetry figure: rectangle, a half-circle bump OUT on the top edge, a half-circle notch IN on the bottom edge, both centered
W0, H0, R0 = 220, 110, 22
def sym_boundary(n=400):
    pts = []
    for i in range(n):  # top edge with bump, left to right (y up = positive)
        x = -W0/2 + W0*i/n
        y = H0/2 + (math.sqrt(max(0, R0*R0 - x*x)) if abs(x) < R0 else 0)
        pts.append((x, y))
    for i in range(n):  # bottom edge with notch (goes up into the shape)
        x = -W0/2 + W0*i/n
        y = -H0/2 + (math.sqrt(max(0, R0*R0 - x*x)) if abs(x) < R0 else 0)
        pts.append((x, y))
    for i in range(n):
        y = -H0/2 + H0*i/n
        pts += [(-W0/2, y), (W0/2, y)]
    return pts
def is_sym(f):
    pts = sym_boundary(); S = set((round(x), round(y)) for x, y in pts)
    def near(p): return any((round(p[0])+dx, round(p[1])+dy) in S for dx in (-1,0,1) for dy in (-1,0,1))
    return all(near(f(x, y)) for x, y in pts[::7])
SYM = {'p': is_sym(lambda x, y: (x, -y)), 'q': is_sym(lambda x, y: (-x, y)), 'r': is_sym(lambda x, y: (y, x))}
assert SYM == {'p': False, 'q': True, 'r': False}, SYM
def sym_fig():
    ox, oy = 150, 105  # center
    L, Rt, Tp, Bt = ox-W0/2, ox+W0/2, oy-H0/2, oy+H0/2
    d = (f'M{L},{Tp} L{ox-R0},{Tp} A{R0},{R0} 0 0 1 {ox+R0},{Tp} L{Rt},{Tp} L{Rt},{Bt} L{ox+R0},{Bt} '
         f'A{R0},{R0} 0 0 0 {ox-R0},{Bt} L{L},{Bt} Z')
    dash = 'stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 5"'
    b = f'<path d="{d}" fill="none" {SW}/>'
    b += f'<line x1="{L-24}" y1="{oy}" x2="{Rt+24}" y2="{oy}" {dash}/>' + txt(Rt+34, oy+5, 'p', 15)
    b += f'<line x1="{ox}" y1="{Tp-46}" x2="{ox}" y2="{Bt+30}" {dash}/>' + txt(ox+12, Tp-40, 'q', 15)
    b += f'<line x1="{ox-95}" y1="{oy+95}" x2="{ox+95}" y2="{oy-95}" {dash}/>' + txt(ox+104, oy-96, 'r', 15)
    return svg(300, 215, b)

def big_cube(n=5, s=26):
    d = s*0.5; W = n*s; x0, y0 = 10, 10 + n*d
    b = ''
    for i in range(n+1):  # front face grid
        b += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s}" y2="{y0+W}" {SW}/>'
        b += f'<line x1="{x0}" y1="{y0+i*s}" x2="{x0+W}" y2="{y0+i*s}" {SW}/>'
    for i in range(n+1):  # top face
        b += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s+n*d}" y2="{y0-n*d}" {SW}/>'
        b += f'<line x1="{x0+i*d}" y1="{y0-i*d}" x2="{x0+W+i*d}" y2="{y0-i*d}" {SW}/>'
    for i in range(n+1):  # right face
        b += f'<line x1="{x0+W+i*d}" y1="{y0-i*d}" x2="{x0+W+i*d}" y2="{y0+W-i*d}" {SW}/>'
        b += f'<line x1="{x0+W}" y1="{y0+i*s}" x2="{x0+W+n*d}" y2="{y0+i*s-n*d}" {SW}/>'
    return svg(int(x0+W+n*d+10), int(y0+W+10), b)

def venn():
    # left circle = multiples of 3, right = even numbers; shaded = left circle only (not the overlap)
    clip = '<defs><clipPath id="v10l"><circle cx="120" cy="100" r="80"/></clipPath><mask id="v10m"><rect x="0" y="0" width="340" height="210" fill="white"/><circle cx="220" cy="100" r="80" fill="black"/></mask></defs>'
    b = clip + '<rect x="0" y="0" width="340" height="210" fill="var(--ink-muted)" opacity="0.45" clip-path="url(#v10l)" mask="url(#v10m)"/>'
    b += f'<circle cx="120" cy="100" r="80" fill="none" {SW}/><circle cx="220" cy="100" r="80" fill="none" {SW}/>'
    b += txt(90, 200, 'Multiples of 3', 13) + txt(250, 200, 'Even numbers', 13)
    return svg(340, 210, b)

# ================= problems =================
# 1  PT6 QR #38, reversed: the list is numbers, three choices are categories
add('Data Collection & Random Sampling',
    'Lena volunteers at an animal shelter and records information about each dog. She made a list of the information that is measured or counted with numbers.<div style="margin-top:6px">1. Weight of each dog, in pounds</div><div>2. Age of each dog, in months</div><div>3. ?</div><div style="margin-top:6px">Which information best completes Lena&rsquo;s list?</div>',
    ['the number of walks each dog gets per day', 'the breed of each dog', 'the color of each dog&rsquo;s collar', 'the name of each dog&rsquo;s favorite toy'], 'A',
    'Weight and age are numbers. Only A is a number (a count of walks). B, C, and D are all categories (words), so the one choice that is different from the other three is the answer.',
    'Lower #6 #38 (reversed: the list is numbers, not categories)',
    C('Lower 6 QR #38, 18.4% right', 'Same "find the one choice unlike the other three"; reversed so the answer is the number, not the category', '1 = 1', '2 list items, 4 choices = same', 'Same'))
# 2  PT6 QR #18 format 1
assert [37*k for k in (3, 6, 9, 18)] == [111, 222, 333, 666] and 18 == 3*6
add('Numerical Patterns', 'Use the pattern to help answer the question.<div style="margin-top:6px">37 &times; 3 = 111</div><div>37 &times; 6 = 222</div><div>37 &times; 9 = 333</div><div style="margin-top:6px">What is the value of 37 &times; 18?</div>',
    ['444', '666', '888', '999'], 'B',
    '3 gives 111, 6 gives 222, 9 gives 333: the digit is how many 3s are in the number you multiply by. 18 = 3 &times; 6, so 37 &times; 18 = 666. A is just the next line after 333. D comes from 1 + 8 = 9.',
    'Lower #6 #18, new numbers',
    C('Lower 6 QR #18, 79% right', 'Same layout (3 lines given, then a jump)', '2 = 2 (see the multiplier is 3 &times; k, use k)', 'same', 'Same'))
# 3  distributive, minus in front (Lower 2 MA #26, MA4 #8, QR9 #27 x - (3 + y))
v = 60 - 3*(8+2)
assert v == 30 and 60-3*8-3*2 == v and 60-3*8+2 != v and 60-3*8+3*2 != v and (60-3)*(8+2) != v
add('Order of Operations and Equivalence', 'Which expression is equal to 60 &minus; 3 &times; (8 + 2)?',
    ['60 &minus; 3 &times; 8 &minus; 3 &times; 2', '60 &minus; 3 &times; 8 + 2', '60 &minus; 3 &times; 8 + 3 &times; 2', '(60 &minus; 3) &times; (8 + 2)'], 'A',
    'The 3 multiplies both numbers inside: 3 &times; 8 and 3 &times; 2. Both are taken away, because the minus is in front of the whole group: 60 &minus; 24 &minus; 6 = 30. B multiplies only the 8. C changes the second minus to plus. D subtracts first.',
    'Lower 2 MA #26 and MA4 #8, with a minus in front of a + group (QR9 #27)',
    C('Lower 2 MA #26, 69.1% right', 'Harder on purpose: the minus in front of the group (her QR9 #27 confusion)', '1 &rarr; 2 (distribute, then keep both minus signs)', 'same', 'Harder (by design)'))
# 4  PT6 MA #12
assert 96 // 8 == 12 and 8*12 == 96
add('Matching Stories to Equations', 'A baker has 96 cookies. She puts the same number of cookies into each of 8 boxes. If c represents the number of cookies in each box, which equation can be used to find c?',
    ['96 &times; c = 8', 'c = 96 &minus; 8', 'c + 8 = 96', '8 &times; c = 96'], 'D',
    '8 boxes with c cookies each make 96 cookies: 8 &times; c = 96. That is the same as c = 96 &divide; 8 = 12. A is backwards, the mistake on Practice Test 6 MA #12.',
    'Lower #6 MA #12',
    C('Lower 6 MA #12, 93.3% right', 'Same story type; the right choice is written as a multiplication, so she has to see 8 &times; c = 96 means c = 96 &divide; 8', '1 &rarr; 2', 'same', 'Slightly harder'))
# 5  input/output, a = 1/2, b = 3, find output
rule5 = lambda x: F(x, 2) + 3
rows5 = [(4, 5), (10, 8), (16, 11), (22, 14)]
assert all(rule5(a) == b for a, b in rows5) and rule5(30) == 18 and rule5(28) == 17
add('Input Output Tables', 'The number machine performs the same operation on each input to create an output. What is the output for an input of 30?',
    ['17', '18', '19', '33'], 'B',
    'Inputs go up by 6 while outputs go up by 3, so the output grows half as fast: try input &divide; 2 + 3. Check: 4 &divide; 2 + 3 = 5, 22 &divide; 2 + 3 = 14. So 30 &divide; 2 + 3 = 18. A treats 30 as the next row (that would be 28). D is 30 + 3, leaving out the half.',
    'Lower #6 MA #13, rule a &times; input + b with a fraction',
    C('Lower 6 MA #13, 93.4% right', 'Same wording', '1 (subtract 7) &rarr; 2 (halve, then add 3)', 'same 4 rows', 'Harder (parent asked for a fraction rule)'),
    table(['Input', 'Output'], rows5, 'NUMBER MACHINE'))
# 6  PT6 MA #28
assert F(7) / F(20, 100) == 35
add('Percent Word Problems', 'A store gave a 20% discount off the regular price of a jacket. The amount of the discount was $7. What was the regular price of the jacket?',
    ['$14', '$28', '$35', '$42'], 'C',
    '$7 is 20% of the regular price. 20% = 0.2, so the price is 7 &divide; 0.2 = 35 (or: 20% is one fifth, so 7 &times; 5). A is 7 &times; 2. B is the sale price, 35 &minus; 7.',
    'Lower #6 MA #28',
    C('Lower 6 MA #28, 74.6% right', 'Same', '1 = 1 (part &divide; 0.2)', 'same', 'Same'))
# 7  composite perimeter, square + triangle (Lower 1 #38)
side = 20 // 4; tri = 27 - 3*side + side
assert side == 5 and tri == 17 and 27 - 3*side == 12
add('Area and Perimeter of Complex Polygons', 'The perimeter of the whole figure is 27 centimeters. The perimeter of the square is 20 centimeters. What is the perimeter of the triangle?',
    ['12 centimeters', '17 centimeters', '22 centimeters', '27 centimeters'], 'B',
    'The square&rsquo;s side is 20 &divide; 4 = 5. The whole figure&rsquo;s outline uses 3 sides of the square (15), so the triangle&rsquo;s two outside sides are 27 &minus; 15 = 12. The triangle also has the shared side, 5: 12 + 5 = 17. A leaves out the shared side. C is 27 &minus; 5.',
    'Lower #1 #38',
    C('Lower 1 QR #38, 33.8% right', 'Same wording', '3 = 3 (side, outside sides, add the shared side)', 'same', 'Same'),
    square_triangle(), 'shared-side')
# 8  PT6 QR #36 format 1: a / b * c, band edge + order trap
e = F(50, 12)*182
assert 600 < e < 900 and F(50, 10)*180 == 900 and F(50, 12*182) < 1
add('Estimating Multiplication & Division', 'Nina did the problem 50 &divide; 12 &times; 182. Approximately what was her answer?',
    ['less than 1', 'between 300 and 600', 'between 600 and 900', 'between 900 and 1,200'], 'C',
    'Work left to right: 50 &divide; 12 first. 48 &divide; 12 = 4, so 50 &divide; 12 is a little more than 4. 4 &times; 182 is about 730, and the exact answer is about 758: between 600 and 900. A comes from doing 12 &times; 182 first. Rounding 12 down to 10 and 182 to 180 gives exactly 900, which sits on the line between C and D, so that rounding is too rough here.',
    'Lower #6 #36, same two traps',
    C('Lower 6 QR #36, 50.1% right', 'Same; both traps kept (left-to-right order, rough rounding lands on a band edge)', '2 = 2', 'same', 'Same'))
# 9  remaining two kinds (Lower 1 MA #25, MA4 #24)
ap, orng = 12 - 12//4, 9 - 9*2//3
assert (ap, orng) == (9, 3) and ap + orng == 12 and 12//4 + 9*2//3 == 9
add('Remaining Amount after Reducing by Fractions', f'Tia had 12 apples and 9 oranges. She gave away {frac(1,4)} of her apples and {frac(2,3)} of her oranges. How many apples and oranges does she have left?',
    ['3', '6', '9', '12'], 'D',
    'Apples: 1/4 of 12 is 3, so 9 are left. Oranges: 2/3 of 9 is 6, so 3 are left. 9 + 3 = 12. C is the number she gave away (3 + 6), and B mixes apples given with oranges left.',
    'Lower 1 MA #25 and MA4 #24',
    C('Lower 1 MA #25, 64.9% right', 'Same "how many left"', '4 = 4', '2 items, 2 fractions = same', 'Same (fraction 2/3 a bit harder than 1/3)'))
# 10 (swapped 11/10) compare areas, mixing perimeter and area (QR8 #32, QR9 #30: direction swapped)
sideA = 36 // 4; wB = (36 - 2*12) // 2
assert sideA == 9 and wB == 6 and 2*(12 + wB) == 36 and sideA**2 == 81 and 12*wB == 72 and 81 - 72 == 9
add('Comparing Areas', 'Garden A is a square with a perimeter of 36 feet. Garden B is a rectangle with a length of 12 feet. Garden B has the same perimeter as Garden A. Which statement correctly compares the two gardens?',
    ['The area of Garden A is 9 square feet greater than the area of Garden B.', 'The area of Garden B is 9 square feet greater than the area of Garden A.', 'The two gardens have the same area because they have the same perimeter.', 'The area of Garden A is 3 square feet greater than the area of Garden B.'], 'A',
    'Garden A: each side is 36 &divide; 4 = 9 ft, so the area is 9 &times; 9 = 81 square feet. Garden B: the two lengths use 12 + 12 = 24 ft, so the two widths share 36 &minus; 24 = 12 ft, and each width is 6 ft. Its area is 12 &times; 6 = 72 square feet. 81 &minus; 72 = 9, and Garden A is the bigger one. B has the right number in the wrong direction (her QR9 #30 slip). C thinks the same perimeter means the same area. D compares the sides (9 &minus; 6), not the areas.',
    'QR8 #32 and QR9 #30 (wrong both times, last third), now mixed with perimeter',
    C('QR9 #30 / QR8 #32 (her misses, last third)', 'Same "which statement compares" choices; both directions offered; same-perimeter trap added', '4 &rarr; 5 (side, area, width from perimeter, area, compare)', '2 shapes, 1 shared perimeter', 'Slightly harder'),
    None, 'verbose-choices')
# 11 PT6 QR #25 type: long statement choices with extra information
assert 4*36 == 144 and 15*10 == 150 and 144 < 150 and 15*2 <= 40
add('English Unit Conversions', 'Mia has a roll with 4 yards of ribbon and a box of 40 beads. She wants to make 15 bows. Each bow uses 10 inches of ribbon and 2 beads. There are 3 feet in 1 yard and 12 inches in 1 foot. Which statement best explains whether Mia has enough ribbon?',
    ['Since 4 &times; 12 = 48 is less than 150, Mia does not have enough ribbon.', 'Since 4 &times; 36 = 144 is less than 150, Mia does not have enough ribbon.', 'Since 4 &times; 36 = 144 is less than 150, Mia does have enough ribbon.', 'Since 40 beads is more than 15 &times; 2 = 30 beads, Mia does have enough ribbon.'], 'B',
    '1 yard = 3 &times; 12 = 36 inches, so 4 yards = 144 inches. 15 bows need 15 &times; 10 = 150 inches. 144 is less than 150, so she does not have enough. A uses 12 inches in a yard. C has the right numbers and the wrong conclusion. D is about beads, which the question does not ask.',
    'Lower #6 #25, with more steps and extra information',
    C('Lower 6 QR #25, 83.5% right', 'Same "Since &hellip;, &hellip;" statement choices; extra information (beads) added on purpose', '1 &rarr; 3 (yards to inches is 2 steps, plus bows &times; 10)', '1 &rarr; 2 (one is a distractor)', 'Harder'),
    None, 'verbose-choices')
# 12 (swapped 11/10) cryptarithm, subtraction with NO borrow (QR3 #34, QR6 #34, QR8 #30 wrong, last third)
sol12 = [(p_, q_) for p_ in range(1, 10) for q_ in range(1, 10) if p_ != q_ and (100*p_ + 10*q_ + 9) - (300 + 10*p_ + q_) == 123]
assert sol12 == [(4, 6)] and 9 >= 6 and 6 >= 4 and 4 >= 3  # unique; no column needs a borrow
add('Cryptarithm / digit substitution', 'P and Q are different digits from 1 through 9. What digit does P represent?',
    ['2', '4', '6', '8'], 'B',
    'Work from the ones column. 9 &minus; Q = 3, so Q = 6. Tens column: Q &minus; P = 2, so 6 &minus; P = 2 and P = 4. Hundreds column check: P &minus; 3 = 4 &minus; 3 = 1. So 469 &minus; 346 = 123. No column needs a borrow. C is Q, not P. D adds 6 + 2 instead of subtracting.',
    'QR8 #30 (her miss, last third), now with no borrow as the parent asked',
    C('QR8 #30 / QR6 #34 / QR3 #34 (her misses, last third)', 'Same "different digits" wording; subtraction, no borrow', '3 = 3 (one column at a time)', '2 letters, 3 columns', 'Same (borrow removed, one more column)'),
    '<div style="font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',\'Courier New\',monospace;letter-spacing:2px;max-width:140px;margin:0 auto;font-size:1.1em;"><div style="padding:2px 6px;line-height:1.5;text-align:right;">PQ9</div><div style="padding:2px 6px;line-height:1.5;text-align:right;">&minus;3PQ</div><div style="padding:2px 6px;line-height:1.5;text-align:right;border-top:1.5px solid currentColor;margin-top:5px;padding-top:5px;">123</div></div>',
    'write-it-down')
# 13 (swapped 11/10) order 4 fractions greatest to least, one close pair (QR2 #38, QR6 #32, QR8 #27 wrong, last third)
fr13 = [F(4, 7), F(2, 3), F(5, 9), F(3, 5)]
assert sorted(fr13, reverse=True) == [F(2, 3), F(3, 5), F(4, 7), F(5, 9)] and 4*9 - 5*7 == 1
fl = lambda *xs: ', &nbsp;'.join(frac(*x) for x in xs)
add('Comparing & Ordering Fractions & Decimals', f'Which list shows the fractions {frac(4,7)}, {frac(2,3)}, {frac(5,9)}, and {frac(3,5)} ordered from greatest to least?',
    [fl((5,9),(4,7),(3,5),(2,3)), fl((2,3),(3,5),(5,9),(4,7)), fl((3,5),(2,3),(4,7),(5,9)), fl((2,3),(3,5),(4,7),(5,9))], 'D',
    'As decimals: 2/3 &asymp; 0.667, 3/5 = 0.6, 4/7 &asymp; 0.571, 5/9 &asymp; 0.556. The close pair is 4/7 and 5/9: cross-multiply, 4 &times; 9 = 36 and 5 &times; 7 = 35, so 4/7 is bigger. A is least to greatest (bigger numbers do not mean a bigger fraction). B swaps the close pair. C swaps 2/3 and 3/5.',
    'QR8 #27, QR6 #32, QR2 #38 (her misses, last third)',
    C('QR8 #27 (her miss, last third)', 'Same "ordered from greatest to least" wording', '3 comparisons = same', '4 fractions = same', 'Same (close pair 36 vs 35 is closer)'),
    None, 'write-it-down')
# 14 converting to decimals, order three, subtract
x = sorted([F(7, 8), F(85, 100), F(4, 5)])
assert x[-1] - x[0] == F(75, 1000) and F(7, 8) - F(85, 100) == F(25, 1000)
add('Converting to a Decimal', f'Lisa ran {frac(7,8)} mile on Monday, 0.85 mile on Tuesday, and {frac(4,5)} mile on Wednesday. How much farther did she run on her longest day than on her shortest day?',
    ['0.025 mile', '0.05 mile', '0.075 mile', '0.125 mile'], 'C',
    '7/8 = 0.875 and 4/5 = 0.8. In order: 0.8, 0.85, 0.875. Longest minus shortest: 0.875 &minus; 0.8 = 0.075. A is Monday minus Tuesday. B is Tuesday minus Wednesday. D is 1 &minus; 0.875.',
    'Lower #1 #29 (decimal word problem) and her order-three gap',
    C('Lower 1 QR #29, real last third', 'Similar', '3 &rarr; 4 (2 conversions, order 3 numbers, subtract)', '3 values', 'Slightly harder'),
    None, 'write-it-down')
# 15 two percent changes (Lower 4 #38)
assert F(100)*F(125, 100)*F(80, 100) == 100
add('Percent Increase Decrease basic', 'The price of a bike is increased by 25%. The new price is then decreased by 20%. What is the overall percent increase or percent decrease from the original price?',
    ['no change', 'percent increase by 5%', 'percent decrease by 5%', 'percent increase by 45%'], 'A',
    'Start with $100. 25% more is $125. 20% of 125 is 25, so the price goes back to $100: no change. B just subtracts 25 &minus; 20, but the 20% is taken from the bigger new price.',
    'Lower #4 #38',
    C('Lower 4 QR #38, 40.6% right', 'Same wording', '3 = 3 (start at 100, two changes)', 'same', 'Same'), None, 'percent-language')
# 16 quadrilateral "always" statements (Lower 1 MA #23)
add('Identifying Shapes', 'Which statement is true?',
    ['A rhombus is always a square.', 'A rectangle is always a rhombus.', 'A rhombus is always a rectangle.', 'A square is always a rhombus.'], 'D',
    'A rhombus has 4 equal sides. A square has 4 equal sides (and 4 right angles), so every square is a rhombus. A rhombus does not need right angles, so A and C are false. A rectangle does not need equal sides, so B is false.',
    'Lower 1 MA #23 and Lower 5 MA #28 (rhombus)',
    C('Lower 1 MA #23, 67.3% right', 'Same format', '1 = 1', '4 statements = same', 'Same'))
# 17 (swapped 11/10) counting multiples between two numbers, "has 6 as a factor" wording (QR6 #28, QR9 #36 wrong, last third)
m17 = [k for k in range(42, 91) if k % 6 == 0]
assert len(m17) == 9 and m17[0] == 42 and m17[-1] == 90 and (91 - 41) // 6 == 8
add('Counting Multiples within a Range', 'How many whole numbers between 41 and 91 have 6 as a factor?',
    ['7', '8', '9', '10'], 'C',
    '"Has 6 as a factor" means the number can be divided by 6 with no remainder, so these are the multiples of 6. The first one after 41 is 42 = 6 &times; 7. The last one before 91 is 90 = 6 &times; 15. Count 7, 8, &hellip;, 15: that is 15 &minus; 7 + 1 = 9 numbers. B is her shortcut (91 &minus; 41) &divide; 6 = 8 R2, which misses one.',
    'QR9 #36 and QR6 #28 (her misses, last third), new "factor" wording',
    C('QR9 #36 / QR6 #28 (her misses, last third)', 'Different words: "has 6 as a factor" instead of "divisible by"', '3 = 3 (first, last, count)', '2 ends = same', 'Same (harder words)'),
    None, 'key-word-watch')
# 18 (swapped 11/10) split line segments, letters (QR3 #37, QR9 #27 wrong, last third)
x_, y_ = 20, 9
assert x_ - 4 - y_ == 7 and x_ - 4 + y_ != 7
seg = svg(300, 50, f'<line x1="10" y1="25" x2="290" y2="25" {SW}/>' + ''.join(
    f'<line x1="{px}" y1="19" x2="{px}" y2="31" {SW}/>' + txt(px, 46, lab, 14) for px, lab in ((10, 'A'), (75, 'B'), (190, 'C'), (290, 'D'))))
add('Split Line Segments', 'The length of AD is x. The length of AB is 4. The length of BC is y. What is the length of CD?',
    ['x &minus; 4 + y', 'x + 4 + y', '4 + y &minus; x', 'x &minus; 4 &minus; y'], 'D',
    'CD is what is left of AD after taking away AB and BC: x &minus; 4 &minus; y. Check with numbers: if AD = 20 and BC = 9, then CD = 20 &minus; 4 &minus; 9 = 7. A adds y back (her QR9 #27 change). C takes the whole line away from the parts.',
    'QR9 #27 and QR3 #37 (her misses, last third), new layout: the end piece is asked',
    C('QR9 #27 (her miss, last third); real Lower 5 #30, WTE #20', 'Same wording; asks for the end piece, not the middle', '2 = 2', '3 lengths = same', 'Same'),
    seg)
# 19 (11/10: parent kept the Mila stamps problem; replaces the grocery estimate, 2/11 wrong, last wrong 10/14)
# Lower 4 #35 real wording "as many as she had"
sq, ci, tr = 10, 2, 3
assert tr*sq - ci == 28 and tr*(sq-ci) - ci != 28
add('Algebra with Geometric Shapes', 'Mila had □ stamps and then she gave ○ of them to Jon. Now, Jon has △ times as many stamps as Mila had. Which expression represents the number of stamps Jon had to begin with?',
    ['△ &times; □ &minus; ○', '△ &times; ○ + □', '△ &times; □ + ○', '△ &times; (□ &minus; ○) &minus; ○'], 'A',
    '"As many as Mila HAD" means her starting number, □. So Jon now has △ &times; □. He got ○ from Mila, so before that he had △ &times; □ &minus; ○. Try □ = 10, ○ = 2, △ = 3: Jon now has 30 and started with 28. D uses what Mila has left, which is a different question.',
    'Lower #4 #35, same wording',
    C('Lower 4 QR #35, 47.4% right', 'Same wording ("as many as she had"); D added for the "has left" reading', '2 = 2', '3 symbols = same', 'Same'))
# 20 triangle area vs height (Lower 2 MA #30)
assert all(F(1, 2)*8*h == 4*h for h in range(1, 20))
add('Area of Triangles', f'The base of a triangle is 8 meters (m). Which statement correctly compares the value of A to the height of the triangle? (A = {frac(1,2)} &times; base &times; height)',
    ['The value of A is always 4 times the value of the height.', f'The value of A is always {frac(1,2)} the value of the height.', 'The value of A is always 8 times the value of the height.', 'The value of A can be the same as the value of the height.'], 'A',
    'Put the base into the formula: A = 1/2 &times; 8 &times; height = 4 &times; height. Check: height 3 gives A = 12, which is 4 times 3. B uses only the 1/2. C uses only the 8.',
    'Lower 2 MA #30 and MA4 #17',
    C('Lower 2 MA #30, 32.1% right', 'Same', '2 = 2', 'same', 'Same'))
# 21 (swapped 11/10) remainder: divide what is LEFT, then round up (QR6 #33 wrong, last third: used the full goal)
assert (300 - 130) / 8 == 21.25 and 22*8 >= 170 > 21*8 and 300 / 8 == 37.5
add('Remainder when Divided by a given Number', 'A soccer team needs to sell 300 raffle tickets. They have already sold 130 tickets. The 8 players will sell the rest, and each player will sell the same number of tickets. What is the fewest number of tickets each player must sell for the team to reach its goal?',
    ['21', '22', '37', '38'], 'B',
    'Tickets still to sell: 300 &minus; 130 = 170. 170 &divide; 8 = 21 R2. If each player sells 21, that is only 168, 2 short, so each must sell 22. A forgets the 2 left over. C and D divide the whole goal, 300 &divide; 8, and forget the 130 already sold (her QR6 #33 slip).',
    'QR6 #33 (her miss, last third)',
    C('QR6 #33 (her miss, last third)', 'Same "how much more each" idea; adds a remainder', '2 &rarr; 3 (subtract, divide, round up)', '3 values = same', 'Slightly harder'),
    None, 'exact-thing-asked')
# 22 "decreased by X%" language, plus change
assert F(45)*F(80, 100) == 36 and 50 - 36 == 14 and 50 - (45 - F('0.2')) == F('5.2')
add('Percent Increase Decrease basic', 'A pair of shoes cost $45. The price was decreased by 20%. Sam paid for the shoes at the new price with a $50 bill. How much change did Sam get?',
    ['$5.20', '$9', '$14', '$36'], 'C',
    '20% of 45 is 9, so the new price is 45 &minus; 9 = $36. Change from $50: 50 &minus; 36 = $14. A takes 0.20 off the price instead of 20% of it. B is the discount, D is the new price.',
    'QR9 #8 language (Lower 4 #38 wording)',
    C('real platform drill gid 1106 ("decreased by 20%", 1 step)', 'Same "decreased by" wording', '1 &rarr; 3 (20% of 45, subtract, then change)', '1 &rarr; 2', 'Harder (multi-step build)'), None, 'percent-language')
# 23 floor grid percent (Lower 2 #26)
white = {(0, 1), (0, 4), (1, 2), (1, 5), (2, 0), (2, 3), (3, 1), (3, 4), (4, 2)}
assert len(white) == 9 and F(30 - 9, 30) == F(70, 100)
add('Total Shaded Area given Figure with Equal Divisions', 'The shaded area on the grid represents the part of a rectangular floor that has tile already installed. Each small square on the floor has the same dimensions. What percentage of the floor has tile already installed?',
    ['21%', '30%', '70%', '79%'], 'C',
    'There are 6 &times; 5 = 30 squares. 9 are white, so 21 are tiled. 21/30 = 7/10 = 70%. A reads the count 21 as a percent. B is the part with no tile.',
    'Lower 2 #26',
    C('Lower 2 QR #26, 68.1% right', 'Same wording', '3 = 3 (count, make a fraction, to percent)', 'same', 'Same'), floor_grid(6, 5, white))
# 24 ratio chain (MA4 #27, QR9 #32)
h = 65 // (1 + 4 + 8)
assert h == 5 and 4*h == 20 and 8*h == 40
add('Word Problems with Ratios', 'A pet store has fish, birds, and hamsters. There are 2 times as many fish as birds and 4 times as many birds as hamsters. There are 65 of these animals in all. How many fish are there?',
    ['5', '13', '20', '40'], 'D',
    'Hamsters = 1 part, birds = 4 parts, fish = 2 &times; 4 = 8 parts. 13 parts = 65, so 1 part = 5. Fish = 8 &times; 5 = 40. A is hamsters, C is birds, B is the number of parts.',
    'MA4 #27 and QR9 #32 (real drill gid 1140)',
    C('real drill gid 1140 / MA4 #27', 'Same', '4 = 4', '2 ratio links + total = same', 'Same'), None, 'exact-thing-asked')
# 25 line symmetry (What to Expect #24)
add('Shape Construction & Symmetry in 2-D Figures', 'The figure shown may be folded along one or more of the dotted lines. Which line or lines, when folded, will make the two halves match exactly?',
    ['line p only', 'line q only', 'both line p and line q', 'line p, line q, and line r'], 'B',
    'Fold on q (up and down): the left and right halves match. Fold on p (across): the top half has a bump going out, but the bottom half has a dent going in, so they do not match. Line r is not a line of symmetry of a rectangle that is not a square.',
    'What to Expect #24',
    C('What to Expect QR #24, 41.4% right', 'Same "which line or pair of lines" format', '1 per line, 3 lines = same', 'same', 'Same'), sym_fig())
# 26 input/output, pick the rule, square rule
rows26 = [(2, 5), (3, 10), (5, 26), (6, 37)]
ok = lambda f: [f(a) == b for a, b in rows26]
assert all(ok(lambda a: a*a + 1)) and ok(lambda a: a + 3) == [True, False, False, False]
assert ok(lambda a: 5*a - 5) == [True, True, False, False] and ok(lambda a: 6*a + 1) == [False, False, False, True]
add('Input Output Tables', 'The table shows how a number machine changes each input number (△) into an output number (■). Which equation shows the rule for the number machine?',
    ['△ &times; △ + 1 = ■', '△ + 3 = ■', '△ &times; 5 &minus; 5 = ■', '△ &times; 6 + 1 = ■'], 'A',
    'Check every row, not just the first one. B works only for 2. C works for 2 and 3 but gives 20 for 5. D works only for 6. A: 2 &times; 2 + 1 = 5, 3 &times; 3 + 1 = 10, 5 &times; 5 + 1 = 26, 6 &times; 6 + 1 = 37.',
    'Lower #6 #6 (pick the rule) and Lower 5 MA (square rule)',
    C('Lower 6 QR #6, 95.6% right', 'Same "which equation shows the rule"', '1 &rarr; 2 (rule is a square plus 1)', '4 rows, each wrong choice fits 1 or 2 rows', 'Harder (parent asked for a square rule)'),
    table(['Input (△)', 'Output (■)'], rows26, 'NUMBER MACHINE'), 'check-every-condition')
# 27 combining two equations (MA4 #5)
sol = [(s, t) for s in range(1, 30) for t in range(1, 30) if 2*s + t == 26 and s - t == 4]
assert sol == [(10, 6)]
add('Algebra with Geometric Shapes', lines('□ + □ + △ = 26', '□ &minus; △ = 4') + '<div style="margin-top:6px">What is the value of △?</div>',
    ['4', '6', '10', '13'], 'B',
    'The second line says □ is 4 more than △. Replace each □ in the first line with △ + 4: △ + 4 + △ + 4 + △ = 26, so three △ = 18 and △ = 6. Then □ = 10. C is □. D is 26 &divide; 2.',
    'MA4 #5 and Lower 1 #37',
    C('Lower 1 QR #37 / MA4 #5', 'Same', '3 = 3', '2 equations = same', 'Same'), None, 'write-it-down')
# 28 pavers (Lower 2 #32)
assert (96//8)*(60//6) == 120 and 96 % 8 == 0 and 60 % 6 == 0
add('Matching Stories to Equations', 'Ana wants to cover a wall with rectangular tiles. The wall is 96 inches long and 60 inches high. Each tile is 8 inches long and 6 inches high. If she knows how to find the area of a rectangle, how can Ana find how many tiles she needs without putting them all on the wall? (A = l &times; w)',
    ['(96 &minus; 8) &times; (60 &minus; 6)', '(96 &divide; 6) &times; (60 &divide; 8)', '(96 &times; 60) &minus; (8 &times; 6)', '(96 &divide; 8) &times; (60 &divide; 6)'], 'D',
    'Along the length, 96 &divide; 8 = 12 tiles fit. Up the height, 60 &divide; 6 = 10 tiles fit. 12 &times; 10 = 120 tiles. B divides the length by the tile&rsquo;s height, so the tiles are turned the wrong way.',
    'Lower 2 #32',
    C('Lower 2 QR #32, 59.4% right', 'Same', '2 = 2', 'same', 'Same'))
# 29 hidden divisor 9 (Lower 1 MA #29, MA L1 #24 digit-sum rule)
ch29 = [1512, 1516, 1605, 1608]
assert [n % 9 == 0 for n in ch29] == [True, False, False, False] and 1608 % 8 == 0 and 1605 % 3 == 0
add('No Remainder when Divided by a given Number', 'Kofi and 8 other students each sold the same number of raffle tickets. Which number could be the total number of tickets the students sold?',
    ['1,512', '1,516', '1,605', '1,608'], 'A',
    'Kofi and 8 others is 9 students, so the total must divide by 9: its digits add to a multiple of 9. 1 + 5 + 1 + 2 = 9, and 1,512 &divide; 9 = 168. D divides by 8, which comes from counting only 8 students. C divides by 3 but not 9.',
    'Lower 1 MA #29 (and the digit-sum rule from Lower 1 MA #24)',
    C('Lower 1 MA #29, 39.1% right', 'Same "and 8 other" wording trap', '2 = 2', 'same', 'Same'), None, 'exact-thing-asked')
# 30 PT6 MA #30 format 2: half match, more information
c30 = {'Ali': 18, 'Bea': 24, 'Cal': 15, 'Dot': 23}
s30 = sum(c30.values())
assert s30 == 80 and s30 // 2 == 40 and s30 + s30 // 2 == 120
add('Determining Total Cost', 'Four students are collecting cans for a food bank. A grocery store promised that for every 2 cans the students collect, the store will add 1 more can. The table shows how many cans each student collected. How many cans will the food bank get in all from the students and the store?',
    ['40', '80', '120', '160'], 'C',
    'The students collected 18 + 24 + 15 + 23 = 80 cans. The store adds 1 for every 2, so 80 &divide; 2 = 40 more. Total 80 + 40 = 120. B stops before the store&rsquo;s part. D doubles, as if the store matched every can.',
    'Lower #6 MA #30, a second format',
    C('Lower 6 MA #30, 50.2% right', 'Same "promised to add" sentence before the table', '2 &rarr; 3 (add, halve, add)', '4 table values (was 3)', 'Slightly harder'),
    table(['Student', 'Cans'], [[k, v] for k, v in c30.items()], 'CANS COLLECTED'), 'exact-thing-asked')
# 31 square perimeter -> area -> rectangle length (Lower 1 MA #30)
s31 = 32 // 4
assert s31 == 8 and s31*s31 // 4 == 16
add('Finding Area/Perimeter of Rectangle, given Length & Width', 'The perimeter of a square is 32 centimeters. If a rectangle with a width of 4 centimeters has the same area as the square, what is the length of the rectangle in centimeters?',
    ['8', '16', '28', '64'], 'B',
    'Square side: 32 &divide; 4 = 8, area 8 &times; 8 = 64. Rectangle: 64 &divide; 4 = 16 long. A stops at the square&rsquo;s side, D at the area.',
    'Lower 1 MA #30',
    C('Lower 1 MA #30, 35.9% right', 'Same wording', '3 = 3', 'same', 'Same'), None, 'exact-thing-asked')
# 32 symbols, total then divide (Lower 1 #33, MA4 #28)
add('Translating Math Expressions', 'A baker made □ muffins in the morning and ○ muffins in the afternoon. She puts △ muffins in each box. Which expression represents the number of boxes she fills with all the muffins?',
    ['(□ + ○) &divide; △', '(□ + ○) &times; △', '□ + ○ &divide; △', '(□ &times; ○) &divide; △'], 'A',
    'All the muffins: □ + ○. Boxes: that total &divide; △. The parentheses matter: C divides only ○. Try 20 + 16 muffins, 6 per box: 36 &divide; 6 = 6 boxes.',
    'Lower 1 #33 and MA4 #28',
    C('Lower 1 QR #33, 54.4% right', 'Same', '2 = 2', 'same', 'Same'))
# 33 PT6 QR #36 format 2: word problem, truncation trap + order trap
e33 = F(47, 18)*63
assert 150 < e33 < 200 and (47//18)*63 == 126 and F(18*63, 47) < 50
add('Estimating Multiplication & Division', 'A pack of 18 batteries costs $47. At the same price for each battery, about how much would 63 batteries cost?',
    ['less than $50', 'between $100 and $150', 'between $150 and $200', 'between $200 and $250'], 'C',
    'One battery: 47 &divide; 18. 2 &times; 18 = 36 and 3 &times; 18 = 54, so it is about 2.6, not 2. 2.6 &times; 63 is about 164, between $150 and $200. B comes from dropping the 0.6 (2 &times; 63 = 126). A comes from 18 &times; 63 &divide; 47.',
    'Lower #6 #36, word-problem version',
    C('Lower 6 QR #36, 50.1% right', 'Different presentation (story, the order is not written for her); same band trap', '2 = 2', 'same', 'Same'))
# 34 doubling differences, 7th term (Lower 1 MA #21, MA4 #25)
s34 = [3, 5, 9, 17, 33]
while len(s34) < 7: s34.append(s34[-1] + 2*(s34[-1] - s34[-2]))
assert s34 == [3, 5, 9, 17, 33, 65, 129]
add('Numerical Patterns', 'Use the number pattern to answer the question.<div style="margin-top:6px">3, &nbsp;5, &nbsp;9, &nbsp;17, &nbsp;33, &nbsp;...</div><div style="margin-top:6px">What is the 7th number in the pattern?</div>',
    ['65', '97', '129', '130'], 'C',
    'Write the differences: 2, 4, 8, 16. Each difference doubles, so the next ones are 32 and 64. 6th: 33 + 32 = 65. 7th: 65 + 64 = 129. A stops at the 6th. B adds 32 again. D doubles the number 65 instead of the difference (the MA4 #25 slip).',
    'Lower 1 MA #21 and MA4 #25',
    C('Lower 1 MA #21, 67.1% right', 'Same', '2 &rarr; 3 (asks the 7th, not the next)', 'same', 'Harder (same as MA4 #25)'), None, 'write-it-down')
# 35 volume with gaps (Lower 3 #29)
assert 50*2 == 100
add('Volume of Solids', 'A jar is filled with 50 marbles. Each marble takes up 2 cubic centimeters of space. There are gaps between the marbles in the jar. Which statement best describes the volume of the jar?',
    ['The volume of the jar is exactly 50 cubic centimeters.', 'The volume of the jar is exactly 100 cubic centimeters.', 'The volume of the jar is less than 100 cubic centimeters.', 'The volume of the jar is more than 100 cubic centimeters.'], 'D',
    'The marbles take up 50 &times; 2 = 100 cubic centimeters. The jar holds the marbles AND the gaps, so its volume is more than 100. B forgets the gaps.',
    'Lower 3 #29',
    C('Lower 3 QR #29, 72.2% right', 'Same 4 statements', '1 &rarr; 2 (multiply first)', 'same', 'Slightly harder'), None, 'verbose-choices')
# 36 fractional parts of the rest
walk = 32*3//8; rest = 32 - walk; bike = rest//4
assert (walk, rest, bike, rest - bike) == (12, 20, 5, 15) and 32//4 == 8 and 32 - 12 - 32//4 == 12
add('Fractional Parts Word Problems', f'A class has 32 students. {frac(3,8)} of the students walk to school. {frac(1,4)} of the remaining students ride bikes. The rest take the bus. How many students take the bus?',
    ['5', '8', '12', '15'], 'D',
    'Walk: 3/8 of 32 = 12, so 20 remain. Bikes: 1/4 of 20 = 5. Bus: 20 &minus; 5 = 15. B takes 1/4 of all 32 instead of the remaining students (8 bikes), and C is the bus count that follows from it (32 &minus; 12 &minus; 8). A is the bikes.',
    'Lower 5 #33 step chain (fraction of the rest)',
    C('real "fraction of the rest" items', 'Same "of the remaining" wording', '3 = 3', '2 fractions = same', 'Same'), None, 'exact-thing-asked')
# 37 cube count (What to Expect #28)
assert 5**3 == 125 and 3*25 == 75 and 6*25 == 150
add('Comparing Volume of Cubes', 'Use the diagram of the cube to answer the question. How many small cubes are being used to build the large cube?',
    ['25', '75', '125', '150'], 'C',
    'Each edge is 5 small cubes: 5 &times; 5 &times; 5 = 125. A counts one face. B counts the 3 faces you can see. D counts 6 faces.',
    'What to Expect #28',
    C('What to Expect QR #28, 65.1% right', 'Same', '1 = 1', 'same', 'Same (5 &times; 5 &times; 5 instead of 4 &times; 4 &times; 4)'), big_cube())
# 38 phrase for an expression (Lower 2 #28)
add('Translating Math Expressions', 'Which phrase is represented by the expression 3 &times; (n &minus; 4)?',
    ['3 times the difference of n and 4', '4 less than 3 times n', 'the difference of 4 and n, times 3', '3 more than the difference of n and 4'], 'A',
    'The parentheses come first: the difference of n and 4 is n &minus; 4, then 3 times it. B is 3 &times; n &minus; 4, with no parentheses. C is 3 &times; (4 &minus; n), in the wrong order.',
    'Lower 2 #28',
    C('Lower 2 QR #28, 72.4% right', 'Same', '1 = 1', 'same', 'Same'), None, 'key-word-watch')

assert len(P) == 38
L = [p['correct'] for p in P]
cnt = Counter(L); print(cnt, ''.join(L))
assert max(cnt.values()) - min(cnt.values()) <= 1, cnt
assert not any(L[i] == L[i+1] == L[i+2] for i in range(36)), ''.join(L)
tc = Counter(p['topic'] for p in P)
assert max(tc.values()) <= 3, tc
json.dump(P, open(os.path.join(HERE, 'set10_problems.json'), 'w'), indent=1)
json.dump(COMPARE, open(os.path.join(HERE, 'set10_mapping.json'), 'w'), indent=1, ensure_ascii=False)
print('wrote', len(P), 'diagrams', sum(1 for p in P if p['diagram']))
