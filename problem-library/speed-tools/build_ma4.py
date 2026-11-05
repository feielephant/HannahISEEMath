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
# the 898 reminder must come right before the Omar problem
i898 = next(i for i, p in enumerate(final) if p.get('gid') == 898)
assert 'Omar' in final[i898 + 1]['q']

P = []
for i, p in enumerate(final):
    P.append(dict(n=i + 1, tier='Hard', topic=p['topic'], q=p['q'], choices=p['choices'], correct=p['correct'],
                  key=p['key'], ref=p['ref'], diagram=p['diagram'] or '', gid=p.get('gid'), ma_idx=p.get('ma_idx')))
json.dump(P, open(os.path.join(HERE, 'ma4_problems.json'), 'w'), ensure_ascii=False, indent=1)
print(len(P), cnt, ''.join(L))
for p in P: print(p['n'], p['correct'], p['topic'][:45], '|', re.sub('<[^>]+>', ' ', p['q'])[:70])
