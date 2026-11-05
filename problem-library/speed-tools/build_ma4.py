"""MA Set 4 (2026-11-05). Parent: use the 23 QR9 follow-up problems (from the 11/4 review
with Hannah) and fill to 30 with problems built on her earlier last-third misses on real
practice tests. The follow-up items are read from qr9_followup_problems.json (built and
asserted by build_qr9_followup.py); the 7 extras are asserted here."""
import json, os, re, sys, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'build_set9.py')).read().split('WHO = ')[0])   # helpers + T (tracker topics)
LIB = {i['global_id']: i for i in json.load(open(os.path.join(HERE, '..', 'problem_library.json')))}
MA = json.load(open(os.path.join(HERE, '..', 'ma_library.json')))
S9 = {p['n']: p for p in json.load(open(os.path.join(HERE, 'set9_problems.json')))}
FU = json.load(open(os.path.join(HERE, 'qr9_followup_problems.json')))

def s9_topic(n):
    return S9[n]['topic']

def ref(topic, how, src):
    assert topic in T, topic
    return f'Tier: Hard &middot; Topic: {topic} &middot; {how} &middot; {src}'

FOLLOW = []
for p in FU:
    k = int(re.search(r'Follows QR9 #(\d+)', p['ref']).group(1))
    src = f"Real item used verbatim (gid {p['gid']})" if p.get('gid') else 'New problem'
    FOLLOW.append(dict(q=p['q'], diagram=p['diagram'], choices=p['choices'], correct=p['correct'], key=p['key'],
                       topic=s9_topic(k), gid=p.get('gid'),
                       ref=ref(s9_topic(k), f'Follows QR9 #{k} (parent review 11/4)', src)))

EXTRA = []
def extra(topic, q, ch, ans, key, built_on, diagram='', gid=None, ma_idx=None):
    assert len(set(ch)) == 4 and ans in 'ABCD'
    if gid is not None: assert LIB[gid]['status'] == 'not_done'; src = f'Real item used verbatim (gid {gid})'
    elif ma_idx is not None: assert MA[ma_idx]['status'] == 'not_done'; src = f'Real item used verbatim (ma_library: {MA[ma_idx]["exercise_title"]})'
    else: src = 'New problem'
    EXTRA.append(dict(q=q, diagram=diagram, choices=dict(zip('ABCD', ch)), correct=ans, key=f'<b>Answer: {ans}.</b> {key}',
                      topic=topic, gid=gid, ma_idx=ma_idx, ref=ref(topic, f'Built on her real-test miss: {built_on}', src)))

# E1 counting multiples (Lower 5 MA #29 wrong; QR9 #36 wrong again with the (end - start) / divisor shortcut)
mult = [n for n in range(68, 85) if n % 4 == 0]
assert mult == [68, 72, 76, 80, 84] and (85 - 67) // 4 == 4
extra('Counting Multiples within a Range', LIB[978]['question_text'], ['2', '3', '5', '7'], 'C',
      'List them: 68, 72, 76, 80, 84, so 5. The shortcut (85 &minus; 67) &divide; 4 = 4.5 &rarr; 4 is wrong; write the first and last multiple, then count.',
      'Lower 5 MA #29; QR9 #36', gid=978)

# E2 distributive (Lower 2 MA #26 wrong; parent taught the distributive method on 11/4)
assert 8 * (6 + 3) - 4 == 68 == (8*6) + (8*3) - 4 and (8*6) + (8*3) != 68 and (8*6 + 3) - 4 != 68
extra('Order of Operations and Equivalence', MA[197]['question_text'],
      ['(8 &times; 6 + 3) &minus; 4', '(8 &times; 6) + (8 &times; 3)', '(8 &times; 2) + (8 &times; &minus;1)', '(8 &times; 6) + (8 &times; 3) &minus; 4'], 'D',
      'The 8 multiplies BOTH numbers in the parentheses: (8 &times; 6) + (8 &times; 3). The &minus; 4 is outside, so it stays. Check: 8 &times; 9 &minus; 4 = 68 and 48 + 24 &minus; 4 = 68. B drops the &minus; 4.',
      'Lower 2 MA #26', ma_idx=197)

# E3 classification with the "2 is prime" corner (Lower 2 MA #29 wrong: forgot 2 is prime)
def isprime(n): return n > 1 and all(n % d for d in range(2, n))
pr = [p for p in range(2, 40) if isprime(p)]
prods = [a*b for a, b in itertools.combinations(pr, 2)]
assert all(not isprime(x) for x in prods) and any(x % 2 == 0 for x in prods) and any(x % 2 for x in prods)
extra('Classification of Numbers, given a Set', 'Two different prime numbers are multiplied. What will always describe the product of the two numbers?',
      ['composite number', 'even number', 'odd number', 'prime number'], 'A',
      'The product has at least the two primes as factors, so it is always composite. It is NOT always odd: 2 is a prime number, and 2 &times; 3 = 6 is even. It is not always even either: 3 &times; 5 = 15.',
      'Lower 2 MA #29 (2 is prime)')

# E4 value of digits with rules (Lower 3 #31 wrong; QR9 #24 wrong)
cands = [int(''.join(p)) for p in itertools.permutations('03469') if p[0] != '0' and int(p[-1]) % 2 == 1]
best = min(cands)
assert best == 30469 and str(best)[2] == '4'
rules = ('<div style="border:1.6px solid currentColor;border-radius:6px;padding:8px 12px;display:inline-block">'
         '<div style="font-weight:600;margin-bottom:4px">RULES FOR THE NEW NUMBER</div>'
         '<div>1. The number must have 5 digits.</div><div>2. It must use each of the digits 0, 3, 4, 6, and 9 one time.</div>'
         '<div>3. The number must be odd.</div><div>4. The number must be as small as possible.</div></div>')
extra('Value of Digits', 'Students were asked to write a new number using all the rules shown. What digit is in the hundreds place of the new number?',
      ['0', '4', '6', '9'], 'B',
      'Odd means it ends in 3 or 9. To be as small as possible, the first digit should be the smallest digit that is not 0, which is 3, so it ends in 9: 3 _ _ _ 9, filled smallest first: 30,469. The hundreds digit is 4. '
      'A number cannot start with 0. Write the whole number down before reading the place.',
      'Lower 3 #31; QR9 #24', diagram=rules)

# E5 cube scaling (Lower 4 #36, Lower 5 #38, What to Expect #28, Lower 3 #29 all wrong)
assert (12 // 3) ** 3 == 64
extra('Comparing Volume of Cubes', 'Two cubes are shown. Cube A has sides 3 centimeters long. Cube B is 4 times as wide as Cube A. How many Cube A\'s can fit inside Cube B?',
      ['12', '64', '108', '192'], 'B',
      'Cube B is 4 Cube A\'s wide, 4 long, and 4 tall, so 4 &times; 4 &times; 4 = 64 fit. A is 3 &times; 4 (side times width). C is 4 &times; 27. D is 64 &times; 3: the 3 cm side does not matter, only how many times as wide.',
      'Lower 4 #36 (and three other cube misses)',
      diagram=svg(230, 160, cube(8, 150, 24, 'A') + cube(76, 150, 96, 'B')))

# E6 parentheses in a word problem (Lower 1 #33 wrong: (box + circle) x triangle)
assert (1000 + 2000) / 60 == 50
extra('Matching Stories to Equations', LIB[1053]['question_text'],
      ['t = (2,000 &times; 1,000) &times; 60', 't = (2,000 &times; 1,000) &divide; 60', 't = (1,000 + 2,000) &times; 60', 't = (1,000 + 2,000) &divide; 60'], 'D',
      'First the total words: 1,000 + 2,000 = 3,000. She types 60 a minute, so the minutes are 3,000 &divide; 60 = 50. The parentheses make the adding happen first. C multiplies, which would make the time bigger than the words.',
      'Lower 1 #33', gid=1053)

# E7 remaining amount, two kinds (Lower 1 MA #25 wrong; QR9 #38 slow)
left = 12 - 12 * F(1, 4) + 15 - 15 * F(2, 3)
assert left == 14 and 12 * F(1, 4) + 15 * F(2, 3) == 13 and 12 - 3 == 9 and (12 - 3) + (15 - 5) == 19
extra('Remaining Amount after Reducing by Fractions', 'Sam had 12 marbles and 15 shells. He lost <span class="frac"><span class="n">1</span><span class="d">4</span></span> of his marbles and <span class="frac"><span class="n">2</span><span class="d">3</span></span> of his shells. How many marbles and shells does he have left?',
      ['9', '13', '14', '19'], 'C',
      'Marbles: 1/4 of 12 is 3, so 9 are left. Shells: 2/3 of 15 is 10, so 5 are left. 9 + 5 = 14. '
      'B is how many he LOST. A counts only the marbles. D takes 1/3 of the shells instead of 2/3.',
      'Lower 1 MA #25; QR9 #38')

# ---- order: keep the follow-up order, slot one extra in every 4 problems; pick the extras' order so
# no answer letter shows up 3 times in a row and the letters stay balanced
slots = [3, 7, 11, 15, 19, 23, 27]          # 0-based positions in the final list
def build(order):
    out, fi, ei = [], 0, 0
    for i in range(30):
        if i in slots: out.append(EXTRA[order[ei]]); ei += 1
        else: out.append(FOLLOW[fi]); fi += 1
    return out
def ok(seq):
    L = [p['correct'] for p in seq]
    return all(not (L[i] == L[i+1] == L[i+2]) for i in range(len(L) - 2))
final = next(build(o) for o in itertools.permutations(range(7)) if ok(build(o)))
from collections import Counter
L = [p['correct'] for p in final]
cnt = Counter(L)
assert len(final) == 30 and max(cnt.values()) - min(cnt.values()) <= 1, cnt
# ---- 2026-11-05 parent-approved swap: free 5 duplicate slots, fill with 5 real-test gaps ----
# dropped (coverage kept elsewhere): Ted 1501 (Sally 1497 stays), Tabitha 1054 (Wendy 1053 stays),
# square 1062 and square 1061 (Room A/B below covers square area <-> perimeter), 898 (reminder moved into the Omar key)
NEW = {}
def newp(slot_gid, topic, q, ch, ans, key, built_on, diagram=''):
    assert len(set(ch)) == 4 and ans in 'ABCD'
    NEW[slot_gid] = dict(q=q, diagram=diagram, choices=dict(zip('ABCD', ch)), correct=ans, key=f'<b>Answer: {ans}.</b> {key}',
                         topic=topic, gid=None, ma_idx=None,
                         ref=ref(topic, f'Built on her real-test miss: {built_on}, same difficulty, new numbers', 'New problem'))

# votes prediction -- Lower 2 QR #34 (18/24/3/30 of 75, next 25), and QR9 #31
votes = [('Pretzels', 14), ('Popcorn', 21), ('Grapes', 6), ('Apples', 19)]
tot_v = sum(v for _, v in votes)
assert tot_v == 60 and tot_v // 20 == 3 and F(21, 60) * 20 == 7 and 21 // 3 == 7 and 6 // 3 == 2 and 21 * 3 == 63
newp(1501, s9_topic(31),
     'The table shows the number of votes for different class snacks. Based on the information in the table, what is the most reasonable prediction of the number of votes for popcorn out of the next 20 votes?',
     ['2', '7', '14', '63'], 'B',
     'There are 14 + 21 + 6 + 19 = 60 votes. Popcorn got 21 of 60. The next 20 votes are 1/3 of 60, so popcorn should get 1/3 of 21 = 7. '
     'A is grapes (6 &divide; 3). C is 21 &minus; 7. D multiplies by 3 instead of dividing.',
     'Lower 2 QR #34 (and QR9 #31)', table(['Snack'] + [n for n, _ in votes], [['Number of Votes'] + [v for _, v in votes]], 'VOTES FOR CLASS SNACKS'))

# triangle area vs height -- Lower 2 MA #30 (base 6, A always 3 times h)
assert all(F(1, 2) * 10 * h == 5 * h for h in range(1, 20)) and all(F(1, 2) * 10 * h != h for h in range(1, 20))
newp(1054, 'Area of Triangles',
     'The base of a triangle is 10 meters (m). Which statement correctly compares the value of A to the height of the triangle? (A = <span class="frac"><span class="n">1</span><span class="d">2</span></span> &times; base &times; height)',
     ['The value of A is always <span class="frac"><span class="n">1</span><span class="d">2</span></span> the value of the height.',
      'The value of A is always 10 times the value of the height.',
      'The value of A is always 5 times the value of the height.',
      'The value of A can be the same as the value of the height.'], 'C',
     'A = 1/2 &times; 10 &times; height = 5 &times; height, so A is always 5 times the height. '
     'B forgets the 1/2. D would need 5 &times; height = height, which only happens if the height is 0.',
     'Lower 2 MA #30')

# Room A / Room B -- Lower 2 QR #38 (square area 144 vs 9 x 15: same perimeter), and QR9 #30 / #35
side = 14; assert side * side == 196 and 4 * side == 56 == 2 * (10 + 18) and 10 * 18 == 180 < 196
newp(1061, s9_topic(30),
     'The floor of Room A is in the shape of a square and has an area of 196 feet&sup2;. The floor of Room B is in the shape of a rectangle and has a length of 18 feet and a width of 10 feet. Which statement correctly compares the floors in the two rooms?',
     ['The area of the floor in Room A is the same as the area of the floor in Room B.',
      'The area of the floor in Room A is less than the area of the floor in Room B.',
      'The perimeter of the floor in Room A is equal to the perimeter of the floor in Room B.',
      'The perimeter of the floor in Room A is less than the perimeter of the floor in Room B.'], 'C',
     'Room A: 14 &times; 14 = 196, so each side is 14 and the perimeter is 4 &times; 14 = 56. Room B: area 18 &times; 10 = 180, perimeter 2 &times; (18 + 10) = 56. '
     'The perimeters are equal; the areas are not (196 is more than 180). Check each statement against BOTH numbers.',
     'Lower 2 QR #38 (and QR9 #30, #35)')

# doubling-differences pattern -- Lower 1 MA #21 (2 3 5 9 17 -> 33)
seq = [4, 5, 7, 11, 19]
d = [b - a for a, b in zip(seq, seq[1:])]
assert d == [1, 2, 4, 8] and seq[-1] + 16 == 35 and seq[-1] + 8 == 27 and seq[-1] + 4 == 23 and 19 * 2 == 38
newp(1062, 'Numerical Patterns',
     'Use the number pattern to answer the question.<div style="margin:6px 0;font-size:1.15rem;letter-spacing:2px">4 &nbsp; 5 &nbsp; 7 &nbsp; 11 &nbsp; 19 &nbsp; ___</div>What is the next number in the pattern?',
     ['23', '27', '35', '38'], 'C',
     'Write the differences: 1, 2, 4, 8. Each difference doubles, so the next one is 16: 19 + 16 = 35. '
     'B adds 8 again. D doubles 19. A adds 4.',
     'Lower 1 MA #21')

# cube net, circles must end up OUTSIDE -- MA3 #27 (real Lower 3 #32, gid 151): she folded it with the circles inside
def fold(cells, base):
    """cells: set of (col,row) on the page, row going up. The drawn side faces the reader and becomes the OUTSIDE,
    so faces fold away from the reader. Returns {cell: outward normal}."""
    import numpy as np
    frame = {base: (np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]))}   # u (page right), v (page up), n (out)
    todo = [base]
    while todo:
        c = todo.pop(); u, v, n = frame[c]
        for (dc, dr), (nu, nv, nn) in (((1, 0), (-n, v, u)), ((-1, 0), (n, v, -u)), ((0, 1), (u, -n, v)), ((0, -1), (u, n, -v))):
            k = (c[0] + dc, c[1] + dr)
            if k in cells and k not in frame:
                frame[k] = (nu, nv, nn); todo.append(k)
    assert len(frame) == 6
    normals = {tuple(f[2]) for f in frame.values()}
    assert len(normals) == 6                      # a real cube net
    return {k: f[2] for k, f in frame.items()}
import numpy as np
NET = {(1, 2), (0, 1), (1, 1), (2, 1), (3, 1), (1, 0)}
NRM = fold(NET, (1, 1))
TARGET = np.linalg.det(np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]))     # yellow top, blue front, orange right
def verdict(pl):     # pl: {'Y': cell, 'B': cell, 'O': cell}
    m = np.array([NRM[pl[c]] for c in 'YBO'])
    if any(abs(m[i] @ m[j]) > 0 for i, j in ((0, 1), (0, 2), (1, 2))): return 'opposite'
    return 'ok' if round(np.linalg.det(m)) == round(TARGET) else 'mirror'
CH = [{'Y': (2, 1), 'B': (1, 0), 'O': (3, 1)},     # A correct, not laid out like the picture
      {'Y': (2, 1), 'B': (3, 1), 'O': (1, 0)},     # B mirror of A (blue/orange swapped): only works with the circles inside
      {'Y': (2, 1), 'B': (1, 0), 'O': (0, 1)},     # C yellow and orange on opposite faces
      {'Y': (1, 1), 'B': (2, 1), 'O': (1, 0)}]     # D looks like the picture but is the mirror
assert [verdict(x) for x in CH] == ['ok', 'mirror', 'opposite', 'mirror'], [verdict(x) for x in CH]
assert tuple(NRM[(1, 1)]) == (0, 0, 1) and tuple(NRM[(2, 1)]) == (1, 0, 0) and tuple(NRM[(1, 0)]) == (0, -1, 0) and tuple(NRM[(3, 1)]) == (0, 0, -1)
COL = {'Y': ('#F2C230', 'Y'), 'B': ('#3B7DDD', 'B'), 'O': ('#F08A24', 'O')}
def net_svg(pl, u=26):
    b = ''
    for (c, r) in NET:
        x, y = 4 + c * u, 4 + (2 - r) * u
        b += f'<rect x="{x}" y="{y}" width="{u}" height="{u}" fill="none" {SW}/>'
    for col, (c, r) in pl.items():
        x, y = 4 + c * u + u / 2, 4 + (2 - r) * u + u / 2
        b += f'<circle cx="{x}" cy="{y}" r="8" fill="{COL[col][0]}" stroke="currentColor" stroke-width="1"/>' + f'<text x="{x}" y="{y+3.5}" font-size="9" text-anchor="middle" fill="#111">{COL[col][1]}</text>'
    return svg(4 * u + 8, 3 * u + 8, b)
def cube_svg():
    s, d, x, y = 80, 30, 10, 40
    b = (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="none" {SW}/>'
         f'<polygon points="{x},{y} {x+d},{y-d} {x+s+d},{y-d} {x+s},{y}" fill="none" {SW}/>'
         f'<polygon points="{x+s},{y} {x+s+d},{y-d} {x+s+d},{y+s-d} {x+s},{y+s}" fill="none" {SW}/>')
    for (cx, cy, rx, ry, k) in ((x + s/2, y + s/2, 14, 14, 'B'), (x + s/2 + d/2, y - d/2, 13, 6, 'Y'), (x + s + d/2, y + s/2 - d/2, 6, 13, 'O')):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{COL[k][0]}" stroke="currentColor" stroke-width="1"/><text x="{cx}" y="{cy+4}" font-size="10" text-anchor="middle" fill="#111">{k}</text>'
    return svg(s + d + 24, s + d + 14, b)
newp(898, '3D shape from its net (unfolding a solid)',
     'A cube has three colored circles drawn on it: yellow (Y) on top, blue (B) on the front, and orange (O) on the right side. Which diagram could be folded to make this cube, if the colored circles are on the OUTSIDE of the cube and cannot be seen from the other side?',
     [net_svg(x) for x in CH], 'A',
     'Fold the net so the drawn side stays on the outside: the squares fold AWAY from you. '
     'In A, use the empty middle square as the top. Yellow folds down to become the right side, blue folds down to become the front, and orange (at the end of the row) wraps under to become the bottom. '
     'Now tip the cube to the left so the right side comes up: yellow is on top, blue is still in front, and orange (the bottom) comes around to the right. That is the cube. '
     'B swaps blue and orange: it makes the mirror cube, which only works if the circles end up INSIDE (her MA3 #27 fold). '
     'C puts yellow and orange two squares apart in the row, so they are opposite faces and never touch. D is laid out like the picture but is also the mirror, so it fails the same way as B.',
     'MA3 #27 (real Lower 3 #32, gid 151)', diagram=cube_svg())

REPL = {1501: 1501, 1054: 1054, 1061: 1061, 1062: 1062, 898: 898}
slots_new = [i for i, p in enumerate(final) if p.get('gid') in REPL]
assert len(slots_new) == 5
def place(perm):
    out = list(final)
    for i, g in zip(slots_new, perm): out[i] = NEW[g]
    return out
final = next(place(pm) for pm in itertools.permutations(list(NEW)) if ok(place(pm)))
for p in final:
    if 'Omar' in p['q']:
        p['key'] = p['key'].replace('which means by 3 AND by 5.', 'which means by 3 AND by 5 (the same way 12 means by 3 AND by 4).')
        assert '12 means by 3 AND by 4' in p['key']
L = [p['correct'] for p in final]
cnt = Counter(L)
assert len(final) == 30 and max(cnt.values()) - min(cnt.values()) <= 1, cnt
assert not any(p.get('gid') in (1501, 1054, 1061, 1062, 898) for p in final)

P = []
for i, p in enumerate(final):
    P.append(dict(n=i + 1, tier='Hard', topic=p['topic'], q=p['q'], choices=p['choices'], correct=p['correct'],
                  key=p['key'], ref=p['ref'], diagram=p['diagram'] or '', gid=p.get('gid'), ma_idx=p.get('ma_idx')))
json.dump(P, open(os.path.join(HERE, 'ma4_problems.json'), 'w'), ensure_ascii=False, indent=1)
print(len(P), cnt, ''.join(L))
for p in P: print(p['n'], p['correct'], p['topic'][:45], '|', re.sub('<[^>]+>', ' ', p['q'])[:70])
