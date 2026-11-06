"""QR Set 9 follow-up (2026-11-05), from the parent's review with Hannah on 11/4.
One or two problems per item the parent asked to practice again. Real not-done
items are used verbatim where the library has a match; the rest are new and
say which QR9 problem they follow. Every math claim is asserted below."""
import json, os, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# reuse Set 9's diagram helpers (svg, txt, table, frac, rect_q, floor_grid, colsum, SW)
exec(open(os.path.join(HERE, 'build_set9.py')).read().split('WHO = ')[0])
LIB = {i['global_id']: i for i in json.load(open(os.path.join(HERE, '..', 'problem_library.json')))}

P = []
def add(q, ch, ans, key, follows, diagram='', gid=None):
    assert len(ch) == 4 and len(set(ch)) == 4 and ans in 'ABCD'
    if gid is not None:
        assert LIB[gid]['status'] == 'not_done', gid
    src = f'Real item used verbatim (gid {gid})' if gid else 'New problem'
    P.append(dict(n=len(P) + 1, q=q, diagram=diagram, choices=dict(zip('ABCD', ch)), correct=ans,
                  key=f'<b>Answer: {ans}.</b> {key}', ref=f'Follows QR9 #{follows} &middot; {src}', gid=gid))

def seg(labels_x, w=312):
    b = f'<line x1="14" y1="24" x2="{w-16}" y2="24" stroke="currentColor" stroke-width="2"/>'
    for lab, x in labels_x: b += f'<circle cx="{x}" cy="24" r="4" fill="currentColor"/>' + txt(x, 14, lab, 14)
    return svg(w, 34, b)

def blocks(cells, u=30):
    cols = max(c for _, c in cells) + 1; rows = max(r for r, _ in cells) + 1
    b = ''.join(f'<rect x="{c*u+2}" y="{r*u+2}" width="{u}" height="{u}" fill="none" {SW}/>' for r, c in cells)
    return svg(cols*u+4, rows*u+4, b)

def outside_edges(cells):
    s = set(cells)
    return sum((r+dr, c+dc) not in s for r, c in s for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)))

# 1 -- #1: same rectangle build, but this time it asks for the NEW length, not the increase
short = 26 // 2 - 8                 # the shown 8 is the longer side; the shorter side is 5
long3 = short + 2 * short           # longer than the shorter side BY 2 times the shorter side = 3 times
assert short == 5 and long3 == 15 and 2 * (short + long3) == 40
assert 2 * (short + 2 * short) == 30 and short + long3 == 20      # traps: "2 times" only; one length + one width
add('Nina builds picture frames. The first rectangular frame she builds has a perimeter of 26 inches. The length of one of the sides is shown. '
    'For her next frame, she keeps the shorter side the same length. The longer side is longer than the shorter side by 2 times the length of the shorter side. What is the perimeter of the next frame?',
    ['15 inches', '20 inches', '30 inches', '40 inches'], 'D',
    'Two sides of 8 use 16 inches, so the other two sides share 26 &minus; 16 = 10, and each is 5. So 8 is the longer side and 5 is the shorter side. '
    'In the next frame the shorter side stays 5. The longer side is 5 PLUS 2 &times; 5 more: 5 + 10 = 15, which is 3 times the shorter side. Perimeter: 2 &times; (5 + 15) = 40. '
    'C makes the longer side only 2 times the shorter side (10), missing the "longer than ... by" part. A is the new longer side. B is one length plus one width.',
    1, rect_q(150, 70, '8', '?'))

# 2 -- #3: bigger table, Jun/Jul and Mar/May next to each other
months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
names = ['Rosa', 'Sam', 'Tess', 'Uma', 'Vic']
D = {'Mar': [14,11,17,16,12], 'Apr': [17,15,16,10,18], 'May': [21,13,17,19,15], 'Jun': [18,22,11,20,16],
     'Jul': [26,19,14,23,21], 'Aug': [23,16,19,15,24], 'Sep': [15,20,13,18,14], 'Oct': [12,17,10,13,19]}
def dif(ms): return sum(D[m][0] for m in ms) - sum(D[m][2] for m in ms)
assert [D[m][0] - D[m][2] for m in ('Mar','Jun','Aug')] == [-3, 7, 4]      # Tess ran more in March
assert dif(['Mar','Jun','Aug']) == 8 and dif(['Mar','Jun','Apr']) == 5 and dif(['Mar','Jul','Aug']) == 13
assert sum(abs(D[m][0] - D[m][2]) for m in ('Mar','Jun','Aug')) == 14
add('The table shows the number of miles five friends ran each month. How many more miles did Rosa run than Tess in March, June, and August combined?',
    ['5', '8', '13', '14'], 'B',
    'Rosa: 14 + 18 + 23 = 55. Tess: 17 + 11 + 19 = 47. 55 &minus; 47 = 8. '
    'Month by month works too, but watch March: Tess ran MORE (17 vs 14), so March counts as &minus;3: &minus;3 + 7 + 4 = 8. '
    'D adds 3 + 7 + 4, treating March as if Rosa ran more. A reads April instead of August (her Lower 5 mix-up). C reads July instead of June.',
    3, table(['Month'] + names, [[m] + D[m] for m in months], 'MILES RUN'))

# 3 -- #5: addition WITH carrying this time
sols = [(t, c) for t in range(1, 10) for c in range(1, 10) if t != c and 100*t + 11*c + 11*t == 521]
assert sols == [(4, 7)] and 7 + 4 >= 10 and 477 + 44 == 521 and 388 + 33 == 421
add('Each shape shown represents a different digit from 1 through 9. What is the value of ○?',
    ['8', '4', '5', '7'], 'D',
    'The hundreds digit of the answer is 5, but △ + something carried could make 5, so start with the ones column: ○ + △ ends in 1, so ○ + △ = 11 and 1 carries. '
    'Tens column: ○ + △ + 1 = 12, so 2 is written and 1 carries. Hundreds: △ + 1 = 5, so △ = 4 and ○ = 11 &minus; 4 = 7. Check: 477 + 44 = 521. '
    'C forgets the carry (△ = 5). B is △. A does not work: ○ = 8 would need △ = 3 (8 + 3 = 11), and 388 + 33 = 421, not 521.',
    5, colsum(['△○○', '+&nbsp;△△', '521']))

# 4 -- #9: two shape equations again, this time asking for △
sol = [(o, t) for o in range(1, 30) for t in range(1, 30) if 2*o + t == 22 and o + 2*t == 20]
assert sol == [(8, 6)] and (22 + 20) // 3 == 14
add('<div>○ + ○ + △ = 22</div><div>○ + △ + △ = 20</div><div style="margin-top:6px">What is the value of △?</div>',
    ['2', '6', '8', '14'], 'B',
    'Add the two lines: three ○ and three △ make 42, so ○ + △ = 14. The second line is (○ + △) + △ = 20, so 14 + △ = 20 and △ = 6. Check the first line: 8 + 8 + 6 = 22. '
    'A is ○ &minus; △. C is ○. D is ○ + △ (one step early).',
    9)

# 5 -- #10: count the outside edges (real, U-shape)
U = [(0,0),(1,0),(0,3),(1,3),(2,0),(2,1),(2,2),(2,3)]
assert len(U) == 8 and outside_edges(U) == 18 and 36 / 18 == 2 and 8 * 2 * 2 == 32
add(LIB[1060]['question_text'].replace('centimeters²', 'centimeters&sup2;'),
    ['28 centimeters&sup2;', '32 centimeters&sup2;', '36 centimeters&sup2;', '40 centimeters&sup2;'], 'B',
    'Go around the outside and count the square sides: there are 18. 36 &divide; 18 = 2, so each square is 2 by 2 with area 4. Eight squares: 8 &times; 4 = 32. '
    'Mark each side with a tick as you count it. On QR9 #10 she counted 11 sides where there were 10.',
    10, blocks(U), gid=1060)

# 6 -- #12: hours to minutes, the 60-times-each-part method
assert 60 * F(7, 3) + 60 * F(7, 4) == 245
add('Leo practiced piano for 2 <span class="frac"><span class="n">1</span><span class="d">3</span></span> hours on Saturday and 1 <span class="frac"><span class="n">3</span><span class="d">4</span></span> hours on Sunday. How many minutes did Leo practice in all? (1 hour = 60 minutes)',
    ['215', '235', '245', '255'], 'C',
    'Change each part to minutes first: 2 hours = 120, 1/3 hour = 20, so 140. 1 hour = 60, 3/4 hour = 45, so 105. 140 + 105 = 245. '
    'No fraction adding needed. D uses 1/3 hour = 30. A uses 3/4 hour = 15.',
    12)

# 7 -- #13: fraction and decimal together
assert F('3.2') - F(3, 4) == F('2.45') and F('3.2') - F(3, 4) - F('1.15') == F('1.3') and F('3.2') - F('1.15') == F('2.05') and F('3.2') - F('0.34') - F('1.15') == F('1.71')
add('A ribbon is 3.2 meters long. Kim cuts off <span class="frac"><span class="n">3</span><span class="d">4</span></span> meter and then 1.15 meters. How many meters of ribbon are left?',
    ['1.3', '1.71', '2.05', '2.45'], 'A',
    '3/4 = 0.75. 3.2 &minus; 0.75 = 2.45, and 2.45 &minus; 1.15 = 1.3. Line up the decimal points (3.20). '
    'B reads 3/4 as 0.34. C forgets the 3/4 cut. D stops after the first cut.',
    13)

# 8, 9 -- #15: many conditions (real Who Am I items)
c1497 = [p for p in (11, 13, 17, 19) if all(p % d for d in range(2, p)) and all((20-p) % d for d in range(2, 20-p)) and 20-p > 1 and 20 % (p//10 + p%10) == 0]
assert c1497 == [13]
add(LIB[1497]['question_text'], ['11', '13', '17', '19'], 'B',
    'Check each choice against every rule, one at a time, and cross it out as soon as one rule fails. All four are prime. 20 &minus; 11 = 9 and 20 &minus; 19 = 1 are not prime, so 11 and 19 are out. '
    'Digit sums: 13 &rarr; 4 and 17 &rarr; 8. 20 &divide; 4 = 5, but 20 &divide; 8 is not whole, so the answer is 13.',
    15, gid=1497)
def prime(n): return n > 1 and all(n % d for d in range(2, n))
c1501 = [p for p in (11, 13, 23, 31) if prime(p) and p//10 < p%10 and prime(p%10 - p//10) and (p//10 + p%10) % (p%10 - p//10) == 0 and p%10 - p//10 < 6 and p//10 + p%10 < 6]
assert c1501 == [13]
add(LIB[1501]['question_text'], ['11', '13', '23', '31'], 'B',
    'First digit less than second: 11 (equal) and 31 are out. 13: difference 2 (prime), sum 4, 2 is a factor of 4, both less than 6. '
    '23: difference 1, which is not prime. So 13. Test every rule on every choice that is left.',
    15, gid=1501)

# 10 -- #16: two percent changes, this time the result is an increase
assert 100 * F(150, 100) * F(80, 100) == 120
add('The price of a game is increased by 50%. The new price is then decreased by 20%. What is the overall percent increase or percent decrease from the original price?',
    ['percent decrease by 10%', 'percent increase by 30%', 'percent increase by 70%', 'percent increase by 20%'], 'D',
    'Start with $100. Up 50%: 100 + 50 = 150. Down 20% of 150: 150 &minus; 30 = 120. 120 is 20 more than 100, so it is a 20% increase. '
    'B just subtracts the percents (50 &minus; 20). C adds them.',
    16)

# 11 -- #17: big grid, count slowly
cells = {(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(3,0),(3,1),(4,0),(4,1),(0,7),(0,8),(1,8),(0,9)}
assert len(cells) == 18 and 10 * 5 == 50 and F(18, 50) == F(36, 100) and F(18, 40) == F(45, 100)
add('The shaded area on the grid represents the part of a rectangular garden that has been planted. Each small square is the same size. What percentage of the garden has been planted?',
    ['18%', '30%', '36%', '45%'], 'C',
    'The grid is 10 squares across and 5 down, so there are 50 squares. 18 are shaded. 18/50 = 36/100 = 36%. '
    'A reads the count as the percent. D counts only 8 columns (18/40). Count the rows and columns of the whole grid first, then the shaded squares, writing each number down.',
    17, floor_grid(10, 5, cells))

# 12, 13 -- #19: expressions at real-test level (real Lower 4 #35 asks "times as many as he HAD")
# check with numbers: box=10, circle=3, tri=5 -> Ben now has 10 + 5 = 15, had 12
assert 10 + 5 - 3 == 12
add('Ava had □ stickers and then she gave ○ of them to Ben. Now, Ben has △ more stickers than Ava had. Which expression represents the number of stickers Ben had to begin with?',
    ['□ + △ &minus; ○', '□ + △ + ○', '△ &minus; □ &minus; ○', '□ &minus; ○ &minus; △'], 'A',
    'Ava HAD □. Ben now has △ more than that: □ + △. Before Ava gave him ○, he had ○ fewer: □ + △ &minus; ○. '
    'Try numbers: □ = 10, ○ = 3, △ = 5. Ben now has 15, so he started with 12. Only A gives 12.',
    19)
add(LIB[1054]['question_text'], ['(□ &minus; ○) &divide; ◇', '(○ &minus; □) &divide; ◇', '(□ &divide; ◇) &minus; ○', '(○ &divide; ◇) &minus; □'], 'A',
    'Start with □, give away ○: □ &minus; ○ are left. Sort those into ◇ containers: (□ &minus; ○) &divide; ◇. The parentheses make the giving away happen first.',
    19, gid=1054)

# 14 -- #22: compare, then map back to names
vals = {'Kai': F(3, 4), 'Hannah': F(7, 10), 'Natalie': F(5, 8), 'Sophia': F(72, 100)}
assert sorted(vals, key=lambda k: -vals[k]) == ['Kai', 'Sophia', 'Hannah', 'Natalie']
add('Four students ran on the same track. Kai ran <span class="frac"><span class="n">3</span><span class="d">4</span></span> of a mile, Hannah ran 0.7 of a mile, Natalie ran <span class="frac"><span class="n">5</span><span class="d">8</span></span> of a mile, and Sophia ran 72% of a mile. Which list shows the students in order from the longest run to the shortest?',
    ['Kai, Sophia, Hannah, Natalie', 'Natalie, Hannah, Sophia, Kai', 'Kai, Hannah, Sophia, Natalie', 'Sophia, Kai, Hannah, Natalie'], 'A',
    'Write each as a decimal next to the name: Kai 0.75, Hannah 0.70, Natalie 0.625, Sophia 0.72. Longest to shortest: 0.75, 0.72, 0.70, 0.625, which is Kai, Sophia, Hannah, Natalie. '
    'B is shortest to longest. C puts 0.7 before 0.72.',
    22)

# 15 -- #26: nth term from a later term
assert 65 + (25 - 9) * 7 == 177 and 65 + 15*7 == 170 and 65 + 17*7 == 184
add('In a sequence, each number is 7 more than the number before it. The 9th number in the sequence is 65. What is the 25th number in the sequence?',
    ['112', '170', '175', '177'], 'D',
    'From the 9th to the 25th number is 25 &minus; 9 = 16 steps. 16 &times; 7 = 112, and 65 + 112 = 177. '
    'A is 16 &times; 7, one step early: it still needs adding to 65. B uses 15 steps. C is 25 &times; 7.',
    26)

# 16, 17 -- #27: split line with parentheses
A_, B_, C_, D_ = 0, 4, 9, 15        # check with real positions
x, y = B_ - A_, D_ - C_
assert C_ - B_ == 15 - (x + y) == 15 - x - y and 15 - x + y != C_ - B_
add('The length of AD is 15. The length of AB is x. The length of CD is y. What is the length of BC?',
    ['15 &minus; x + y', 'x + y &minus; 15', '15 + x &minus; y', '15 &minus; (x + y)'], 'D',
    'BC is what is left of AD after taking away AB and CD: 15 &minus; x &minus; y. Taking away x and then y is the same as taking away (x + y), so 15 &minus; (x + y). '
    'A is the parentheses removed wrong: a minus sign in front of the parentheses changes the sign of EVERYTHING inside, so &minus;(x + y) = &minus;x &minus; y, not &minus;x + y.',
    27, seg((('A', 14), ('B', 80), ('C', 214), ('D', 296))))
x2, y2 = C_ - A_, D_ - B_            # AC = 9, BD = 11
assert x2 + y2 - 15 == C_ - B_ == x2 - (15 - y2) and x2 - 15 - y2 != C_ - B_ and 15 - x2 - y2 != C_ - B_
add('The length of AC is x. The length of BD is y. The length of AD is 15. What is the length of BC?',
    ['x &minus; (15 &minus; y)', '15 &minus; x &minus; y', 'x &minus; 15 &minus; y', 'x + y + 15'], 'A',
    'AC and BD together cover all of AD plus BC a second time, so x + y = 15 + BC and BC = x + y &minus; 15. '
    'A is the same thing: x &minus; (15 &minus; y) = x &minus; 15 + y, because the minus in front of the parentheses flips &minus;y to +y. '
    'C removes the parentheses without flipping the sign. Check with A = 0, B = 4, C = 9, D = 15: x = 9, y = 11, BC = 5, and A gives 9 &minus; 4 = 5.',
    27, seg((('A', 14), ('B', 80), ('C', 214), ('D', 296))))

# 18 -- #34: equal-difficulty jug problem
def tot(n): return F(n, 8) + F(1, 3)
# same four statement types as QR9 #34 / Lower 2 #36: two "less than" (false), two "will not all fit" (only the bigger n true)
truth = [tot(1) < F(1, 3), tot(2) < F(1, 2), tot(5) > 1, tot(6) > 1]
assert truth == [False, False, False, True]
add('Max has two equal-sized buckets of sand. The first bucket is <span class="frac"><span class="n">n</span><span class="d">8</span></span> full. The second bucket is <span class="frac"><span class="n">1</span><span class="d">3</span></span> full. The sand from the first bucket is poured into the second bucket. Which statement best describes the amount of sand once the buckets are combined?',
    ['If n = 1, then the amount of sand is less than <span class="frac"><span class="n">1</span><span class="d">3</span></span> of a bucket.',
     'If n = 2, then the amount of sand is less than <span class="frac"><span class="n">1</span><span class="d">2</span></span> of a bucket.',
     'If n = 5, then the sand will not all fit in 1 bucket.',
     'If n = 6, then the sand will not all fit in 1 bucket.'], 'D',
    'Use 24ths: 1/3 = 8/24 and n/8 = 3n/24. n = 1: 11/24, more than 8/24, so A is false (the second bucket alone is already 1/3). '
    'n = 2: 14/24, more than 12/24, so B is false. n = 5: 23/24, which still fits, so C is false. n = 6: 26/24, more than 1 bucket, so D is true.',
    34)

# 19, 20 -- #35: perimeter and area together (real)
assert (16//4)**2 - (12//4)**2 == 7 and 4 * int((25 + 11) ** 0.5) == 24
add(LIB[1061]['question_text'], ['4 centimeters&sup2;', '6 centimeters&sup2;', '7 centimeters&sup2;', '9 centimeters&sup2;'], 'C',
    'Perimeter 12 means a side of 3, area 9. Perimeter 16 means a side of 4, area 16. The area grows by 16 &minus; 9 = 7. A is the change in perimeter, not area.',
    35, gid=1061)
add(LIB[1062]['question_text'].replace('feet²', 'feet&sup2;'), ['16 feet', '20 feet', '24 feet', '28 feet'], 'C',
    'The second square has area 25 + 11 = 36, so its side is 6 and its perimeter is 4 &times; 6 = 24. B is the first square\'s perimeter.',
    35, gid=1062)

# 21, 22 -- #37: divisible by 12 = by 3 and by 4; "and 14 others" = 15
add(LIB[898]['question_text'], ['6', '15', '24', '40'], 'C',
    '24 &divide; 3 = 8 and 24 &divide; 4 = 6. A number divisible by both 3 and 4 is divisible by 12. That is the reminder for the next problem type.',
    37, gid=898)
def ok15(n): return n % 3 == 0 and n % 5 == 0
assert [n for n in (1245, 1246, 1250, 1251) if ok15(n)] == [1245] and 1246 % 14 == 0 and 1250 % 5 == 0 and 1251 % 3 == 0
add('Omar and 14 other students each collected the same number of cans. Which number could be the total number of cans the students collected?',
    ['1,245', '1,246', '1,250', '1,251'], 'A',
    'Omar and 14 others is 15 students, so the total must divide by 15, which means by 3 AND by 5. 1,245: ends in 5, and 1 + 2 + 4 + 5 = 12 divides by 3. '
    'B divides by 14 (forgot Omar). C divides by 5 but not 3. D divides by 3 but not 5.',
    37)

# 23 -- #32: three-way ratio (real), the gap she was taught on 11/4
assert 42 % 21 == 0 and (42 // 21) * 15 == 30
add(LIB[1136]['question_text'], ['24', '27', '30', '35'], 'C',
    'Let basketball be 1 part. Football is 5 parts and soccer is 3 &times; 5 = 15 parts: 1 + 5 + 15 = 21 parts = 42, so 1 part = 2. Soccer = 15 &times; 2 = 30.',
    32, gid=1136)

order = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,14,16,19,17,20,18,23,21,22]
assert sorted(order) == list(range(1, len(P) + 1))
P = [P[i-1] for i in order]
for i, p in enumerate(P): p['n'] = i + 1
from collections import Counter
L = [p['correct'] for p in P]
print(len(P), Counter(L), ''.join(L))
assert max(Counter(L).values()) - min(Counter(L).values()) <= 1
assert all(not (L[i] == L[i+1] == L[i+2]) for i in range(len(L)-2))
json.dump(P, open(os.path.join(HERE, 'qr9_followup_problems.json'), 'w'), ensure_ascii=False, indent=1)
