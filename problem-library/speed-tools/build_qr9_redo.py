"""QR Set 9 redo (2026-11-04): #5, #8, #9 with fresh numbers, parent request.
#5 is now ADDITION with no carrying in any column (parent: '+' and no advancing
a digit to the next place). Every math claim is asserted below."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

def colsum(rows):
    style = 'display:inline-block;font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',\'Courier New\',monospace;letter-spacing:2px;font-size:1.25rem;text-align:right'
    r = ''.join(f'<div style="padding:2px 6px;line-height:1.5">{x}</div>' for x in rows[:-1])
    return f'<div style="{style}">{r}<div style="padding:7px 6px 2px;margin-top:5px;line-height:1.5;border-top:2px solid currentColor">{rows[-1]}</div></div>'

def ref(orig, her, ok, why):
    return f'Redo of QR Set 9 #{orig} &middot; Her answer on 11/3: {her} (correct {ok}) &middot; {why}'

P = []

# 1 (was #5): T C C + T T = 266, no carrying
sols = [(t, c) for t in range(1, 10) for c in range(1, 10)
        if t != c and (100*t + 11*c) + 11*t == 266]
assert sols == [(2, 4)], sols
t, c = 2, 4
assert c + t < 10                      # ones column: no carry
assert c + t < 10                      # tens column: no carry
assert 100*t + 11*c == 244 and 11*t == 22 and 244 + 22 == 266
P.append(dict(n=1, topic='Cryptarithm / digit substitution',
  q='Each shape shown represents a different digit from 1 through 9. What is the value of ○?',
  diagram=colsum(['△○○', '+&nbsp;△△', '266']),
  choices=dict(A='2', B='4', C='6', D='8'), correct='B',
  key='<b>Answer: B.</b> No column carries, so the hundreds digit of the answer is just △: △ = 2. '
      'Ones column: ○ + △ = 6, so ○ + 2 = 6 and ○ = 4. Check: 244 + 22 = 266. '
      'A is △. C is the digit in the answer. D is 4 + 4 or 6 + 2.',
  ref=ref(5, 'D (8)', 'B', 'now addition with no carrying, per parent')))

# 2 (was #8): $70 decreased by 30%, then a $6 coupon
pct_off = 70 * 30 // 100
assert pct_off == 21 and 70 - 21 == 49 and 49 - 6 == 43
assert round(70 - 0.30 - 6, 2) == 63.70 and 70 - 30 - 6 == 34
P.append(dict(n=2, topic='Percent Increase Decrease basic',
  q='A pair of shoes cost $70. The price was decreased by 30%. Then Leo used a $6 coupon on the new price. How much did Leo pay for the shoes?',
  diagram='',
  choices=dict(A='$34', B='$43', C='$49', D='$63.70'), correct='B',
  key='<b>Answer: B.</b> 30% of 70 is 0.30 &times; 70 = 21, so the new price is 70 &minus; 21 = 49. '
      'After the coupon, 49 &minus; 6 = 43. D subtracts 0.30 instead of 30% of the price. '
      'C stops before the coupon. A takes off $30 instead of 30%.',
  ref=ref(8, 'C ($74.85, subtracted 0.15)', 'A', 'same build, new numbers')))

# 3 (was #9): two shape equations that must be combined
sol = [(o, tr) for o in range(1, 20) for tr in range(1, 20) if 2*o + tr == 17 and o + 2*tr == 13]
assert sol == [(7, 3)], sol
assert 17 + 13 == 30 and 30 // 3 == 10 and 17 - 10 == 7
P.append(dict(n=3, topic='Algebra with Geometric Shapes',
  q='<div>○ + ○ + △ = 17</div><div>○ + △ + △ = 13</div><div style="margin-top:6px">What is the value of ○?</div>',
  diagram='',
  choices=dict(A='3', B='4', C='7', D='10'), correct='C',
  key='<b>Answer: C.</b> Add the two lines: three ○ and three △ make 17 + 13 = 30, so ○ + △ = 10. '
      'The first line is ○ + (○ + △) = 17, so ○ + 10 = 17 and ○ = 7. Check the second line: 7 + 3 + 3 = 13. '
      'Another way: ○ = 13 &minus; 2△, put it in the first line twice: 26 &minus; 4△ + △ = 17, so 3△ = 9 and △ = 3. '
      'A is △. B is the difference ○ &minus; △. D is ○ + △ (stopping one step early).',
  ref=ref(9, 'D (14, ○ + △)', 'C', 'scratch showed a sign slip: &minus;2△ &minus; 2△ + △ written as +△')))

letters = [p['correct'] for p in P]
assert letters == ['B', 'B', 'C']
json.dump(P, open(os.path.join(HERE, 'qr9_redo_problems.json'), 'w'), ensure_ascii=False, indent=1)
print(len(P), 'problems', letters)
