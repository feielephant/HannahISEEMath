"""MA Set 6 (built 2026-11-19, for Friday 11/20). Plan agreed with the parent 11/19 after QR11 grading:
- one problem per skill, no repeats inside the set (parent 11/19);
- each skill chosen from her difficulty-matched history: only attempts with the same construction count
  (easier, fewer-step or whole-number versions of a topic do not count);
- secured skills (right on the last 3+ comparable tries) are rested; 9 dropped skills replaced by her open ones;
- the asked target is rotated against earlier copies of each type (feedback 11/18: she memorizes formats);
- 6 middle-third sources at positions 1-6, 24 last-third sources at 7-30.
Every problem names the real item(s) it is built on, her comparable last-5 (oldest -> newest), and whether it is
harder, the same or easier than the most recent comparable instance. Every math claim is asserted."""
import json, os, sys
from fractions import Fraction as F
from collections import Counter
from itertools import permutations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from joined_prism_diagram import joined_prisms_svg
T = {x['topic']: x for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}
SW = 'stroke="currentColor" stroke-width="1.6"'
def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def svg(w, h, body): return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{body}</svg>'
def txt(x, y, s, size=13, anchor='middle', weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="currentColor">{s}</text>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def lines(*ls): return ''.join(f'<div>{l}</div>' for l in ls)

P, MAP = [], {}
def add(topic, q, ch, right, key, built_on, third, last5, counted, vs, diagram=None):
    """right = the text of the correct choice; last5 = her comparable results oldest->newest; vs = harder/same/easier note."""
    assert topic in T, topic
    assert len(set(ch)) == 4 and right in ch
    ans = 'ABCD'[ch.index(right)]
    n = len(P) + 1
    wrong = last5.lower().count('x')
    tries = len(last5.replace(' ', '').replace('*', ''))
    P.append({'n': n, 'tier': 'Hard', 'topic': topic, 'q': q, 'choices': dict(zip('ABCD', ch)), 'correct': ans,
              'key': f'<b>Answer: {ans}.</b> {key}',
              'ref': (f'Topic: {topic} &middot; Built on: {built_on} &middot; Her comparable tries (oldest &rarr; newest): '
                      f'<b>{last5}</b> ({counted}) &middot; Compared with the latest: {vs}'),
              'diagram': diagram, 'gid': None, 'ma_idx': None})
    MAP[n] = dict(topic=topic, built_on=built_on, source_third=third, last5=last5, counted=counted,
                  comparable_wrong=f'{wrong}/{tries}', vs_latest=vs)

# ================= diagrams =================
def grouped_bars(cats, a, b, ymax, title, la, lb, ylab):
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
    g += txt(W/2, 16, title, 13, weight='600') + f'<text x="14" y="{(B+TOP)/2}" font-size="11" text-anchor="middle" fill="currentColor" transform="rotate(-90 14 {(B+TOP)/2})">{ylab}</text>'
    g += f'<rect x="{W-170}" y="{B+28}" width="12" height="12" fill="#4A86C5"/>' + txt(W-154, B+38, la, 11, 'start')
    g += f'<rect x="{W-90}" y="{B+28}" width="12" height="12" fill="#D08B3C"/>' + txt(W-74, B+38, lb, 11, 'start')
    return svg(W, H + 2, g)

def hundreds_flat(n=10, s=13):
    # a 10 x 10 x 1 base-ten flat: grid top face, thin front and right faces
    d = s*0.5; W = n*s; x0, y0 = 10, 10 + n*d
    b = ''
    for i in range(n+1):
        b += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s+n*d}" y2="{y0-n*d}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+i*d}" y1="{y0-i*d}" x2="{x0+W+i*d}" y2="{y0-i*d}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s}" y2="{y0+s}" stroke="currentColor" stroke-width="1"/>'
        b += f'<line x1="{x0+W+i*d}" y1="{y0-i*d}" x2="{x0+W+i*d}" y2="{y0-i*d+s}" stroke="currentColor" stroke-width="1"/>'
    b += f'<line x1="{x0}" y1="{y0+s}" x2="{x0+W}" y2="{y0+s}" stroke="currentColor" stroke-width="1"/>'
    b += f'<line x1="{x0+W}" y1="{y0+s}" x2="{x0+W+n*d}" y2="{y0+s-n*d}" stroke="currentColor" stroke-width="1"/>'
    return svg(int(x0+W+n*d+12), int(y0+s+12), b)

def colsum(rows):
    style = 'display:inline-block;font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',\'Courier New\',monospace;letter-spacing:2px;font-size:1.25rem;text-align:right'
    r = ''.join(f'<div style="padding:2px 6px;line-height:1.5">{x}</div>' for x in rows[:-1])
    return f'<div style="{style}">{r}<div style="padding:7px 6px 2px;margin-top:5px;line-height:1.5;border-top:2px solid currentColor">{rows[-1]}</div></div>'

def rules_box(*rules):
    return ('<div style="border:1.5px solid currentColor;border-radius:6px;padding:8px 12px;max-width:340px"><div style="font-weight:700;margin-bottom:4px">RULES FOR THE NEW NUMBER</div>'
            + ''.join(f'<div>{i}. {r}</div>' for i, r in enumerate(rules, 1)) + '</div>')

# ================= positions 1-6: middle-third sources =================
# 1 scale with a decimal per-unit value, asked the OTHER direction (QR11 #8 asked real distance; this asks map length)
assert F(27)*4/10 == F('10.8') and F(27)*10/4 == F('67.5') and F(27)/4 == F('6.75')
add('Measurement Scaling',
    'On a map, 4 centimeters stand for 10 kilometers. Two lakes are really 27 kilometers apart. How far apart are the lakes on the map?',
    ['6.75 centimeters', '10.8 centimeters', '67.5 centimeters', '108 centimeters'], '10.8 centimeters',
    '10 kilometers for every 4 centimeters means 1 centimeter stands for 10 &divide; 4 = 2.5 kilometers. 27 &divide; 2.5 = 10.8 centimeters. Check: 10.8 &times; 2.5 = 27. C multiplies 27 by 2.5 (that finds a real distance, but 27 is already the real distance). A divides 27 by 4. D drops the decimal point.',
    'WTE QR #26 (middle third, 1.2 in = 10 mi); QR11 #8 (her miss, decimal per-unit)', 'middle',
    'o x o x', 'WTE QR #26, QR2 #25, QR7 #34, QR11 #8',
    'Slightly harder: same steps, but it asks the map length (the other direction) and the answer is a decimal')

# 2 two packs, price per item, and say which is cheaper (QR11 #24 asked only the difference)
assert F('3.40')/5 == F('0.68') and F('5.20')/8 == F('0.65') and F('0.68') - F('0.65') == F('0.03') and F('5.20') - F('3.40') == F('1.80')
add('Finding Unit Price',
    'Store A sells 5 pens for $3.40. Store B sells 8 of the same pens for $5.20. Which store has the lower price for one pen, and by how much?',
    ['Store A, by $0.03 per pen', 'Store B, by $0.65 per pen', 'Store A, by $1.80 per pen', 'Store B, by $0.03 per pen'], 'Store B, by $0.03 per pen',
    'Find the price of one pen at each store. Store A: 3.40 &divide; 5 = $0.68. Store B: 5.20 &divide; 8 = $0.65. Store B is lower by 0.68 &minus; 0.65 = $0.03. A has the right amount but the wrong store. B is the price of one pen at Store B, not the difference. C subtracts the pack prices (her QR11 #24 slip).',
    'Lower 5 QR #21 (middle third, price per item); QR8 #12 and QR11 #24 (her misses)', 'middle',
    'x x', 'QR8 #12, QR11 #24',
    'Slightly harder: same two divisions and a subtraction, and she must also say which store is lower')

# 3 "decreased by 14%" in a non-store story (her habit: subtract 0.14 or 14)
assert 3500*F(14, 100) == 490 and 3500 - 490 == 3010 and 3500 - 14 == 3486 and 3500 + 490 == 3990
add('Evaluating Percents of Numbers',
    'A lake had 3,500 fish. After a dry summer, the number of fish decreased by 14%. How many fish are in the lake now?',
    ['490', '3,010', '3,486', '3,990'], '3,010',
    '14% of 3,500: 10% is 350 and 4% is 140, so 14% is 490. Decreased by 14% means take 490 away: 3,500 &minus; 490 = 3,010. A stops at the amount of the decrease. C subtracts 14 instead of 14% of 3,500 (the "decreased by" slip). D increases instead.',
    'Official ISEE exercise gid 1108 (her MA3 #3 miss); QR8 #14 and MA5 #8 (her misses)', 'middle',
    'x x', 'QR8 #14, MA5 #8',
    'Same: one percent and one subtraction, in a story with no money so it does not look like the last two')

# 4 digit puzzle with a borrow; asks the OTHER symbol (QR9 #5 asked the circle)
sol4 = [(t, c) for t in range(1, 10) for c in range(1, 10) if t != c and (110*t + c) - (10*c + t) == 573]
assert sol4 == [(6, 9)] and 669 - 96 == 573
add('Cryptarithm / digit substitution',
    'Each shape shown represents a different digit from 1 through 9. What is the value of △?<div style="margin-top:8px">' + colsum(['△△○', '&minus; ○△', '573']) + '</div>',
    ['3', '5', '6', '9'], '6',
    'Ones: ○ &minus; △ ends in 3. Tens: △ &minus; ○ ends in 7, so the tens must borrow (○ is bigger than △). Because of the borrow, the hundreds digit is △ &minus; 1 = 5, so △ = 6. Then ○ = 9: 669 &minus; 96 = 573. B reads the hundreds digit without the borrow. D is ○.',
    'Lower 3 QR #38 (gid 157, 40% right; same subtraction layout); Lower 4 QR #24 (her miss); QR9 #5 (her miss)', 'middle',
    'x x x o o', 'Lower 4 QR #24, QR8 #30, QR9 #5, MA4 #3, QR10 #12',
    'Same: same layout as QR9 #5 with a borrow, but it asks for the other symbol')

# 5 yards + feet to inches, asks the LEFTOVER (earlier copies asked pieces or "enough")
inch5 = 4*36 + 2*12
assert inch5 == 168 and divmod(168, 10) == (16, 8) and divmod(4*36 + 2, 10) == (14, 6) and divmod(4*12 + 24, 10) == (7, 2)
add('English Unit Conversions',
    'A rope is 4 yards 2 feet long. Kai cuts it into as many 10-inch pieces as he can. There are 3 feet in 1 yard and 12 inches in 1 foot. How many inches of rope are left over?',
    ['8', '16', '24', '168'], '8',
    '1 yard = 3 &times; 12 = 36 inches, so 4 yards = 144 inches. 2 feet = 24 inches. The rope is 144 + 24 = 168 inches. 168 &divide; 10 = 16 R8: 16 pieces and 8 inches left over. B is the number of pieces. C treats the 2 feet (24 inches) as the leftover piece. D is the whole rope in inches.',
    'Lower 6 QR #25 (middle third, her miss); QR10 #11, MA5 #7, MA5 #23, QR11 #9', 'middle',
    'x x x o o*', 'Lower 6 QR #25, QR10 #11, MA5 #23, MA5 #7, QR11 #9 (245 s)',
    'Harder: yards and feet mixed, and it asks the leftover instead of the number of pieces')

# 6 remainder with two divisors; every wrong choice fits exactly one condition
r6 = lambda k: (k % 4 == 3, k % 6 == 3)
assert r6(27) == (True, True) and r6(23) == (True, False) and r6(33) == (False, True) and r6(36) == (False, False)
add('Remainder when Divided by a given Number',
    'Which number leaves a remainder of 3 when it is divided by 4 and also leaves a remainder of 3 when it is divided by 6?',
    ['23', '27', '33', '36'], '27',
    'Check both divisions for each choice. 27 &divide; 4 = 6 R3 and 27 &divide; 6 = 4 R3. 23 &divide; 4 = 5 R3, but 23 &divide; 6 = 3 R5. 33 &divide; 6 = 5 R3, but 33 &divide; 4 = 8 R1. 36 divides evenly by both.',
    'Lower 3 MA #16 (middle third, her miss)', 'middle',
    'x', 'Lower 3 MA #16',
    'Slightly harder: same check, but each wrong choice passes one of the two tests, so she must check both')

# ================= positions 7-30: last-third sources =================
# 7 NOT a statistical question (Lower 5 MA #30, 18.8% right, her miss, 282 s)
add('Data Collection & Random Sampling',
    'The table shows some of the data a scientist gathered about a type of frog. Which question is NOT a valid statistical question based on the data in the table?',
    ['How long was each frog?', 'What mass did each frog have?', 'How far did each frog jump?', 'How many toes did each front foot have?'], 'How many toes did each front foot have?',
    'A statistical question expects answers that vary. Length (4 to 7), mass (20 to 45), and jump distance (30 to 90) all vary from frog to frog. Every frog has 4 toes on each front foot, so that question always has the same answer.',
    'Lower 5 MA #30 (her miss, last third, 18.8% right, 282 s)', 'last',
    'x', 'Lower 5 MA #30 (282 s)',
    'Same: same table format, different animal and different row that does not vary',
    table(['Characteristic', 'Data'], [['Length', '4 to 7 (cm)'], ['Mass', '20 to 45 (g)'], ['Jump distance', '30 to 90 (cm)'], ['Number of toes on each front foot', '4']], 'FROG DATA'))

# 8 part of a group as a decimal; two groups combined, total 25 (Official MA #23 was 3 of 10, 158 s)
assert F(7 + 8, 25) == F(6, 10) and F(10, 25) == F('0.4')
add('Equivalent Fractions Decimals and Percents',
    'Mr. Diaz has 25 plants in his classroom. He has 7 tulips, 10 daisies, and 8 ferns. Which number represents the part of his plants that are tulips or ferns?',
    ['0.15', '0.4', '0.6', '15'], '0.6',
    'Tulips or ferns: 7 + 8 = 15 out of 25. 15/25 = 60/100 = 0.6. B is the daisies (10/25). A writes 15 as hundredths without using the 25. D is the count, not the part.',
    'Official MA #23 (last third, 158 s); Lower 2 QR #26 (her miss)', 'last',
    'x o o o*', 'Lower 2 QR #26, Lower 4 QR #37, Lower 6 QR #27, Official MA #23 (158 s)',
    'Harder: total is 25 (not 10) and two groups must be added first')

# 9 estimate a sum of 6 decimals; round-each-down trap (Lower 2 MA #27, her miss)
w9 = [F('2.87'), F('4.12'), F('3.49'), F('5.91'), F('1.68'), F('4.36')]
assert sum(w9) == F('22.43') and sum(int(x) for x in w9) == 19 and sum(round(float(x)) for x in w9) == 22
add('Estimating Sums Differences of Decimal Numbers',
    'Six packages weigh 2.87 kg, 4.12 kg, 3.49 kg, 5.91 kg, 1.68 kg, and 4.36 kg. Which is the closest estimate of the total weight of the six packages?',
    ['19 kg', '20 kg', '21 kg', '22 kg'], '22 kg',
    'Round each to the nearest whole number: 3 + 4 + 3 + 6 + 2 + 4 = 22. The exact total is 22.43 kg. A drops every decimal part (rounds everything down).',
    'Lower 2 MA #27 (her miss, last third, 55.3% right)', 'last',
    'o x o o o', 'Lower 1 MA #20, Lower 2 MA #27, QR2 #4, QR6 #26, MA2 #12',
    'Slightly harder: 6 values instead of 5; last practiced 10/21')

# 10 double bar graph: one category against two others combined (Official MA #26 compared two, 127 s)
cats10, g4, g5 = ['Soccer', 'Basketball', 'Tennis', 'Swimming'], [7, 4, 2, 6], [8, 3, 3, 5]
tot10 = [a + b for a, b in zip(g4, g5)]
assert tot10 == [15, 7, 5, 11] and 15 - (7 + 5) == 3 and 15 - 7 == 8 and 15 - 5 == 10
add('Comparing Adding Subtracting Bar Graph Data Table Values',
    'Students in Grade 4 and Grade 5 voted for their favorite sport. The graph shows the results. How many more students in the two grades together voted for soccer than voted for basketball and tennis combined?',
    ['2', '3', '8', '10'], '3',
    'Add the two bars for each sport. Soccer: 7 + 8 = 15. Basketball: 4 + 3 = 7. Tennis: 2 + 3 = 5. Basketball and tennis combined: 7 + 5 = 12. 15 &minus; 12 = 3. C compares soccer with basketball only. D compares soccer with tennis only. A uses only the Grade 5 bars (8 &minus; 6).',
    'Official MA #26 (last third, 127 s); Lower 5 MA #6 and QR9 #3 (her misses)', 'last',
    'x x o o o*', 'Lower 5 MA #6, QR9 #3, MA4 #2, MA5 #1, Official MA #26 (127 s)',
    'Harder: one sport against two others combined (one more step)',
    grouped_bars(cats10, g4, g5, 9, 'FAVORITE SPORT', 'Grade 4', 'Grade 5', 'Number of Students'))

# 11 percent chain: discount amount at 15% -> price -> sale price -> how much more she needs (QR11 #15 was 25% and change)
orig11 = F(12) / F(15, 100)
assert orig11 == 80 and orig11 - 12 == 68 and 68 - 50 == 18 and 80 - 50 == 30 and 50 - 12 == 38
add('Percent Word Problems',
    'A store has 15% off every lamp. The discount on one lamp is $12. Lia has $50. How much more money does she need to buy the lamp at the sale price?',
    ['$18', '$30', '$38', '$68'], '$18',
    'The $12 discount is 15% of the regular price. 15% is $12, so 5% is $4 and 100% is $80. The sale price is 80 &minus; 12 = $68. She needs 68 &minus; 50 = $18 more. D stops at the sale price (the step she skipped on QR11 #15). B uses the regular price. C subtracts the discount from her $50.',
    'Lower 6 MA #28 (her miss, last third); QR9 #8, QR10 #22, QR11 #15', 'last',
    'x o x', 'QR9 #8, QR10 #22, QR11 #15',
    'Slightly harder: 15% (not 25%) to find the whole, then two more steps')

# 12 order 4 numbers, fractions and decimals mixed, greatest to least (QR11 #1 was least to greatest, fractions only)
v12 = {'5/7': F(5, 7), '0.7': F(7, 10), '0.68': F(68, 100), '2/3': F(2, 3)}
assert sorted(v12, key=v12.get, reverse=True) == ['5/7', '0.7', '0.68', '2/3']
fm = lambda s: frac(*s.split('/')) if '/' in s else s
order = lambda *xs: ', &nbsp;'.join(fm(x) for x in xs)
add('Comparing & Ordering Fractions & Decimals',
    f'Which list shows {frac(5,7)}, 0.7, {frac(2,3)}, and 0.68 in order from greatest to least?',
    [order('5/7', '0.7', '0.68', '2/3'), order('0.7', '0.68', '5/7', '2/3'), order('2/3', '0.68', '0.7', '5/7'), order('0.7', '5/7', '2/3', '0.68')], order('5/7', '0.7', '0.68', '2/3'),
    'Change each to a decimal: 5/7 &asymp; 0.714, 0.7, 0.68, 2/3 &asymp; 0.667. Greatest to least: 5/7, 0.7, 0.68, 2/3. Placing them on a number line helps. C is least to greatest. B puts the decimals first because they are written differently.',
    'Lower 6 QR #31 (last third, 98 s, greatest to least); QR10 #13 (her miss)', 'last',
    'o* x o o', 'Lower 6 QR #31 (98 s), QR10 #13, MA5 #6, QR11 #1',
    'Same: four close numbers like QR11 #1, now with decimals mixed in and in the greatest-to-least direction')

# 13 about 3/4 filled -> how many EMPTY (Official MA #25 asked 1/3 of the total, 207 s)
assert 79920 / 4 == 19980 and abs(79920/4 - 20000) < 100
add('Multiplying and Dividing Whole Numbers',
    'A stadium has 79,920 seats. About {} of the seats were filled for a game. About how many seats were empty?'.format(frac(3, 4)),
    ['2,000', '20,000', '60,000', '80,000'], '20,000',
    '79,920 is close to 80,000. If 3/4 were filled, 1/4 were empty. 1/4 of 80,000 is 20,000. C is the number filled. A is off by a zero. D is all the seats.',
    'Official MA #25 (last third, 207 s); Lower 5 MA #10 (186 s); Lower 2 MA #15 (her miss)', 'last',
    'x o o* o o*', 'Lower 2 MA #15, Lower 2 MA #5, Lower 5 MA #10 (186 s), Lower 6 MA #19, Official MA #25 (207 s)',
    'Harder: 3/4 is given but she must find the other 1/4 (empty seats)')

# 14 joined prisms: compute the volume (Lower 1 QR #36 asked for the expression, 37.2% right)
assert 2*4*7 + 7*4*3 == 140 and 2*4*10 + 7*4*3 == 164 and 7*4*10 == 280 and 7*7*4 == 196
add('Volume of Solids',
    'The figure shown was made by joining two rectangular prisms. The side lengths are measured in feet. What is the total volume of the figure, in cubic feet? (V = lwh, where V = volume, l = length, w = width, and h = height.)',
    ['140', '164', '196', '280'], '140',
    'Top prism: 2 by 4 by 7 = 56. Bottom prism: 7 by 4 by 3 = 84. 56 + 84 = 140 cubic feet. B uses the full height 10 for the top prism, which counts the bottom part twice. D treats the shape as one full box (7 &times; 4 &times; 10). C uses 7 for both the width and the height.',
    'Lower 1 QR #36 (her miss, last third, 37.2% right); QR4 #19, QR5 #20, QR9 #6', 'last',
    'x o o', 'Lower 1 QR #36, QR4 #19, QR5 #20',
    'Harder: she must compute the volume, not just choose the expression; last practiced 10/18',
    joined_prisms_svg(2, 7, 7, 3, 4, sc=15))

# 15 symbols story -> expression, "more than she has LEFT" and the gift counted twice (MA4 #15 said "more than Ava had")
for sq, ci, tr in ((20, 5, 3), (40, 12, 7), (9, 2, 10)):
    ella_left = sq - ci; max_now = ella_left + tr; max_start = max_now - ci
    assert max_start == sq + tr - ci - ci
add('Translating Math Expressions',
    'Ella had □ cards. Then she gave ○ of her cards to Max. Now Max has △ more cards than Ella has left. Which expression represents the number of cards Max had to begin with?',
    ['□ &minus; ○ + △', '□ + △ + ○', '△ &times; (□ &minus; ○) &minus; ○', '□ + △ &minus; ○ &minus; ○'], '□ + △ &minus; ○ &minus; ○',
    'Ella has □ &minus; ○ left. Max now has △ more than that: □ &minus; ○ + △. Max got ○ of those from Ella, so to begin with he had □ &minus; ○ + △ &minus; ○. Try numbers: Ella 20, gives 5, Max now has 3 more than 15, so 18; he had 18 &minus; 5 = 13 = 20 + 3 &minus; 5 &minus; 5. A is what Max has now. C reads "more" as "times".',
    'Lower 4 QR #35 (her miss, last third, 47.4% right); QR9 #19, MA4 #15 (her misses), QR10 #19', 'last',
    'x x x o', 'Lower 4 QR #35, QR9 #19, MA4 #15, QR10 #19',
    'Harder: "more than she has left" and the gift must be taken away twice')

# 16 nth term from TWO given terms (QR11 #33 gave the step)
d16 = (48 - 23) // (9 - 4)
assert d16 == 5 and 23 + (30 - 4)*5 == 153 and 23 + 25*5 == 148 and 23 + 27*5 == 158 and 30*5 == 150
add('Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.',
    'In a sequence, each number is the same amount more than the number before it. The 4th number is 23 and the 9th number is 48. What is the 30th number in the sequence?',
    ['148', '150', '153', '158'], '153',
    'From the 4th to the 9th number is 5 steps, and it grows 48 &minus; 23 = 25, so each step is 25 &divide; 5 = 5. From the 4th to the 30th number is 26 steps: 23 + 26 &times; 5 = 153. A takes 25 steps and D takes 27 (off by one). B is 30 &times; 5 with no starting number.',
    'No real test item asks a far term; closest official: Lower 1 QR #6 (gid 44, given the 2nd/3rd/4th numbers) and the official Nth Term exercises (gids 903-907); QR9 #26, MA4 #18, QR11 #23 (her misses), QR11 #33', 'last',
    'x x o x o', 'QR9 #26, MA4 #18, MA5 #18, QR11 #23, QR11 #33',
    'Harder: she must first find the step from two given numbers')

# 17 range of 10 three-digit values in a table (Lower 6 MA #25, 9 two-digit values, 264 s)
v17 = [148, 213, 176, 129, 205, 231, 162, 139, 190, 218]
assert max(v17) - min(v17) == 102 and 231 - 139 == 92 and 218 - 129 == 89
add('Finding Range, given Sets of Numbers, Data Tables or Graphs',
    'The table shows the number of visitors to a museum on each of 10 days. What is the range of this set of data?',
    ['89', '92', '102', '129'], '102',
    'Range = greatest &minus; least. Greatest: 231 (Day 6). Least: 129 (Day 4). 231 &minus; 129 = 102. B misses the least value (uses 139). A misses the greatest value (uses 218). D is the least value itself.',
    'Lower 6 MA #25 (last third, 264 s)', 'last',
    'o o o*', 'Lower 4 MA #26, QR6 #12, Lower 6 MA #25 (264 s)',
    'Harder: 10 three-digit values in a table (in for speed: she took 264 s on the real one)',
    table(['Day'] + [str(i) for i in range(1, 6)], [['Visitors'] + v17[:5]], 'MUSEUM VISITORS') + '<div style="height:6px"></div>' + table(['Day'] + [str(i) for i in range(6, 11)], [['Visitors'] + v17[5:]]))

# 18 mixed hours with THREE parts, one given in minutes; asks the third part (QR11 #30 had two parts)
assert F(11, 4)*60 == 165 and F(7, 6)*60 == 70 and 165 - 70 - 40 == 55 and 165 - 10 - 40 == 115 and 165 + 70 + 40 == 275
add('Multi-step unit conversion (off-by-10, multi-step)',
    f'Ken spent 2 {frac(3,4)} hours on homework. He spent 1 {frac(1,6)} hours on math and 40 minutes on reading. He spent the rest of the time on science. How many minutes did Ken spend on science? (1 hour = 60 minutes)',
    ['55', '65', '115', '275'], '55',
    '2 3/4 hours = 120 + 45 = 165 minutes. 1 1/6 hours = 60 + 10 = 70 minutes. 165 &minus; 70 &minus; 40 = 55. B is off by 10. C forgets the 1 whole hour in 1 1/6. D adds everything.',
    'Official ISEE exercise gid 1005; Lower 1 QR #29 (her miss, last third, "left"); QR9 #12, QR11 #30 (her misses)', 'last',
    'x o x', 'QR9 #12, MA5 #19, QR11 #30',
    'Harder: three parts, one already in minutes (one more step)')

# 19 differences double; asks a MISSING MIDDLE number (Lower 1 MA #21 asked the next one)
seq19 = [4, 5, 7, 11, 19, 35]
assert [b - a for a, b in zip(seq19, seq19[1:])] == [1, 2, 4, 8, 16]
add('Numerical Patterns',
    'What number is missing from the pattern?<div style="margin-top:6px;font-size:1.15em;letter-spacing:2px">4, &nbsp;5, &nbsp;7, &nbsp;11, &nbsp;___, &nbsp;35</div>',
    ['15', '19', '22', '23'], '19',
    'Look at the differences: 5 &minus; 4 = 1, 7 &minus; 5 = 2, 11 &minus; 7 = 4. They double, so the next differences are 8 and 16: 11 + 8 = 19, and 19 + 16 = 35 checks. A adds 4 again. C doubles 11. D is halfway between 11 and 35.',
    'Lower 1 MA #21 (her miss, last third, 67.1% right); MA4 #25 (her miss), QR10 #34', 'last',
    'x x x x o', 'Lower 1 MA #21, QR3 #6, MA1 #4, MA4 #25, QR10 #34',
    'Slightly harder: a missing middle number, which must be checked against the number after it')

# 20 a / b x c estimate, left to right
ex20 = F(47, 6)*98
assert 600 < ex20 < 900 and F(47, 6*98) < 1 and 50/5*100 == 1000
add('Estimating Multiplication & Division',
    'Ana did the problem 47 &divide; 6 &times; 98 on a calculator. Approximately what was her answer?',
    ['less than 1', 'between 400 and 600', 'between 600 and 900', 'between 900 and 1,200'], 'between 600 and 900',
    'Work left to right: 47 &divide; 6 first. 48 &divide; 6 = 8, so 47 &divide; 6 is a little less than 8. 98 is a little less than 100. 8 &times; 100 = 800, and the real answer is a little less (about 768): between 600 and 900. A does 6 &times; 98 first, as if there were parentheses. D rounds too much (50 &divide; 5 &times; 100 = 1,000).',
    'Lower 6 QR #36 (her miss, last third); QR10 #8, MA5 #15 (her misses), QR11 #11', 'last',
    'x x x o*', 'Lower 6 QR #36, QR10 #8, MA5 #15, QR11 #11 (136 s)',
    'Same: same left-to-right estimate with new numbers')

# 21 probability 2/5 with a missing count; asks the TOTAL (QR11 #22 asked the missing count with 1/4)
others21 = 4 + 6 + 5 + 3
purple21 = F(2, 3)*others21
assert others21 == 18 and purple21 == 12 and F(12, 30) == F(2, 5) and 18*F(5, 2) == 45
add('Probability of 1 Event, given a List of Items',
    f'The table shows the number of each color of marble in a bag. The probability of picking a purple marble without looking is {frac(2,5)}. How many marbles are in the bag in all?',
    ['12', '18', '30', '45'], '30',
    '2/5 purple means 3/5 are not purple. The 4 + 6 + 5 + 3 = 18 marbles that are not purple are 3/5 of the bag, so 1/5 is 6 and the whole bag is 30. (Purple = 12, and 12/30 = 2/5.) A is the purple marbles. B is the marbles that are not purple. D treats 18 as 2/5 of the bag.',
    'Official QR #34 (her miss, last third, 57.6% right); QR11 #22', 'last',
    'o* x o', 'Lower 5 QR #37 (145 s), Official QR #34, QR11 #22',
    'Harder: 2/5 is not a unit fraction, and it asks for the total instead of the missing count',
    table(['Color', 'Number'], [['Red', 4], ['Blue', 6], ['Green', 5], ['Yellow', 3], ['Purple', '?']], 'MARBLES IN THE BAG'))

# 22 fraction, then a fraction of what is LEFT; asks the DIFFERENCE between the two sales (QR11 #36 asked what was left)
am22 = 120*F(3, 8); pm22 = (120 - am22)*F(2, 5)
assert am22 == 45 and pm22 == 30 and am22 - pm22 == 15 and 120*F(2, 5) - am22 == 3 and am22 + pm22 == 75
add('Remaining Amount after Reducing by Fractions',
    f'A farm stand had 120 apples. In the morning, {frac(3,8)} of the apples were sold. In the afternoon, {frac(2,5)} of the apples that were left were sold. How many more apples were sold in the morning than in the afternoon?',
    ['3', '15', '30', '75'], '15',
    'Morning: 3/8 of 120 = 45 sold, so 75 are left. Afternoon: 2/5 of the 75 left = 30 sold. 45 &minus; 30 = 15. A takes 2/5 of all 120 apples (48) instead of the apples that were left. C is the afternoon only. D is the total sold.',
    'Official exercise gid 849 (Fractional Parts Word Problems #1 #5, 59.4% right: 1/5, then 1/5 of the rest); Lower 1 MA #25 (her miss, last third); QR9 #38 (her miss), QR11 #36', 'last',
    'o x o', 'QR8 #21, QR9 #38, QR11 #36 (right only on paper after time)',
    'Same: same two fraction steps as QR11 #36, but it asks for a difference instead of what is left')

# 23 rules box: SMALLEST EVEN, asks the THOUSANDS place; ending in the smallest even digit is the trap
digs23 = [1, 3, 4, 5, 8, 9]
c23 = sorted(int(''.join(map(str, p))) for p in permutations(digs23) if p[-1] % 2 == 0)
best23 = c23[0]
assert best23 == 134598 and (best23 // 1000) % 10 == 4 and (135894 // 1000) % 10 == 5 and 135894 > best23
add('Value of Digits',
    'Students wrote a new number using the digits 1, 3, 4, 5, 8, and 9 and these rules. What digit is in the thousands place of the new number?<div style="margin-top:8px">' +
    rules_box('The number must have 6 digits.', 'The number must be even.', 'The number must be the smallest number possible.', 'Each digit can be used only once.') + '</div>',
    ['3', '4', '5', '9'], '4',
    'It must end in 4 or 8. Ending in 8 leaves 1, 3, 4, 5, 9 for the front: 134598. Ending in 4 gives 135894, which is bigger, because the 4 is needed near the front. The smallest is 134598. Places: 1 hundred-thousands, 3 ten-thousands, 4 thousands, 5 hundreds, 9 tens, 8 ones. The thousands digit is 4. C comes from ending in the smallest even digit (135894). Write the number and label every place before answering.',
    'Lower 3 QR #31 (her miss, last third, 61.6% right); Official QR #36 (her miss), QR11 #35 (her miss)', 'last',
    'o o x o x', 'MA4 #16, MA5 #20, Official QR #36, QR11 #31, QR11 #35',
    'Harder: asks the thousands place, and ending in the smallest even digit gives the wrong number')

# 24 quadrilateral from a description (Official MA #18 asked about parallel sides; this asks about angles)
add('Identifying Shapes',
    'Which figure could be described as a quadrilateral that always has four right angles, but whose four sides do NOT always have the same length?',
    ['rectangle', 'rhombus', 'square', 'trapezoid'], 'rectangle',
    'A rectangle always has four right angles; its length and width can be different. A square always has four equal sides. A rhombus has four equal sides and does not need right angles. A trapezoid does not need right angles.',
    'Lower 6 MA #27 (last third, 171 s); Official MA #18 (her miss)', 'last',
    'o* o x o o', 'Lower 6 MA #27 (171 s), QR10 #16, Official MA #18, QR11 #12, QR11 #28',
    'Same: same kind of description, but about angles instead of parallel sides')

# 25 value with a minus in front of a bracket with + inside (QR11 #16 asked for an equivalent expression)
assert 300 - 6*(25 + 8) == 102 and 300 - 6*25 + 8 == 158 and 300 - 6*25 + 6*8 == 198 and (300 - 6)*(25 + 8) == 9702
add('Order of Operations and Equivalence',
    'What is the value of 300 &minus; 6 &times; (25 + 8)?',
    ['102', '158', '198', '9,702'], '102',
    'Brackets first: 25 + 8 = 33. Then 6 &times; 33 = 198. Then 300 &minus; 198 = 102. Or: 300 &minus; 150 &minus; 48 = 102 (the minus goes to both parts). C flips the second part to + (300 &minus; 150 + 48), or stops at 6 &times; 33. B multiplies only the 25. D subtracts first.',
    'Lower 2 MA #26 (her miss, last third); MA4 #8, MA5 #21 (her misses), QR10 #3, QR11 #16', 'last',
    'x o x o', 'MA4 #8, QR10 #3, MA5 #21, QR11 #16',
    'Same: same bracket, but she finds the value instead of the matching expression')

# 26 fractions and decimals mixed, statement choices (MA5 #16 and QR11 #10 asked one difference)
m26, w26, o26 = F(3, 4), F(6, 10), F(2, 5)
assert m26 - w26 == F(15, 100) and m26 + w26 + o26 == F(175, 100) and w26 + o26 == 1 > m26 and m26 + o26 == F(115, 100)
add('Converting to a Decimal',
    f'A recipe uses {frac(3,4)} cup of milk, 0.6 cup of water, and {frac(2,5)} cup of oil. Which statement is true?',
    ['The three amounts add up to more than 2 cups.', 'The water and the oil together are less than the milk.', 'The milk and the oil together are exactly 1 cup.', 'The milk is 0.15 cup more than the water.'], 'The milk is 0.15 cup more than the water.',
    '3/4 = 0.75 and 2/5 = 0.4. Milk &minus; water: 0.75 &minus; 0.6 = 0.15, true. A: 0.75 + 0.6 + 0.4 = 1.75, less than 2. B: 0.6 + 0.4 = 1.0, more than 0.75. C: 0.75 + 0.4 = 1.15, not 1.',
    'Lower 1 QR #29 (her miss, last third); QR9 #13, QR10 #14, MA5 #16 (her misses), QR11 #10, QR11 #27', 'last',
    'x o x x o', 'QR9 #13, MA4 #9, QR10 #14, MA5 #16, QR11 #10 (QR11 #27 right only on paper)',
    'Slightly harder: four statements to check instead of one difference')

# 27 numbers with both 4 and 6 as factors: multiples of 12, not 24 (QR11 #5 was 2 and 3, 183 s)
m27 = [k for k in range(36, 145) if k % 4 == 0 and k % 6 == 0]
assert m27 == list(range(36, 145, 12)) and len(m27) == 10 and len([k for k in range(36, 145) if k % 24 == 0]) == 5 and (145 - 35) // 12 == 9
add('Counting Multiples within a Range',
    'How many whole numbers between 35 and 145 have both 4 and 6 as factors?',
    ['5', '9', '10', '11'], '10',
    'A number with both 4 and 6 as factors is a multiple of 12 (the smallest number both go into), not of 4 &times; 6 = 24. Multiples of 12 from 36 to 144: 12 &times; 3 up to 12 &times; 12, which is 12 &minus; 3 + 1 = 10 numbers. A counts multiples of 24. B is the shortcut (145 &minus; 35) &divide; 12, which misses one.',
    'Lower 5 MA #29 (her miss, last third); QR9 #36 (her miss), QR11 #5 (183 s)', 'last',
    'x o o o o*', 'QR9 #36, MA4 #4, QR10 #17, MA5 #12, QR11 #5 (183 s)',
    'Harder: 4 and 6 share a factor, so multiplying them (24) is wrong (in for speed: 183 s on QR11)')

# 28 matching gift at $3 for every $2 (Lower 6 MA #30 was $1 for $1, 210 s; QR11 #25)
wk28 = [18, 24, 14, 20]
store28 = F(sum(wk28), 2)*3
assert sum(wk28) == 76 and store28 == 114 and 76 + 114 == 190 and 76*3 == 228 and 76*2 == 152
add('Determining Total Cost',
    'A class collected money for a food bank for 4 weeks. The table shows how much the class collected each week. A grocery store promised that for every $2 the class collected, the store would give $3 more. How much money did the food bank receive in all from the class and the store?',
    ['$76', '$114', '$152', '$190'], '$190',
    'The class collected 18 + 24 + 14 + 20 = $76. That is 76 &divide; 2 = 38 groups of $2, and the store gives $3 for each: 38 &times; 3 = $114. In all: 76 + 114 = $190. A is the class&rsquo;s part only. B is the store&rsquo;s part only. C doubles the class money (a $1-for-$1 match).',
    'Lower 6 MA #30 (her miss, last third, 210 s); QR11 #25', 'last',
    'x o', 'Lower 6 MA #30 (210 s), QR11 #25',
    'Harder: a $3-for-$2 match instead of $1 for $1',
    table(['Week', 'Money collected'], [['Week 1', '$18'], ['Week 2', '$24'], ['Week 3', '$14'], ['Week 4', '$20']], 'MONEY FOR THE FOOD BANK'))

# 29 rectangle: width is one fourth of the length; asks the LENGTH (QR11 #17 asked the area)
W29 = F(50, 2) / 5
assert W29 == 5 and 4*W29 == 20 and 2*(20 + 5) == 50 and F(50, 4) == F('12.5') and 50 // 5 == 10
add('Finding Area/Perimeter of Rectangle, given Length & Width',
    'The width of a rectangle is one fourth of its length. The perimeter of the rectangle is 50 meters. What is the length of the rectangle?',
    ['5 meters', '10 meters', '20 meters', '100 meters'], '20 meters',
    'Width : length = 1 : 4, so one width and one length make 5 equal parts. One width + one length = half the perimeter = 25 meters. Each part is 25 &divide; 5 = 5, so the width is 5 and the length is 4 &times; 5 = 20 meters. Check: 2 &times; (20 + 5) = 50. A is the width. B divides the whole perimeter by 5. D is the area (20 &times; 5), not the length.',
    'Lower 1 MA #30 (her miss, last third, 35.9% right); QR8 #9, QR9 #35, QR11 #17 (her misses)', 'last',
    'x x o o x', 'QR8 #9, QR9 #35, QR10 #31, MA5 #27, QR11 #17',
    'Same: same ratio-in-words idea as QR11 #17 (her language miss), and it asks the length instead of the area')

# 30 200 hundreds flats of 100 cubic cm (parent 11/18: "give 200 but with only 100", change the story)
assert 200*100 == 20000 == 2*10*10*10*10
add('Comparing Volume of Cubes',
    'The hundreds flat shown has a volume of 100 cubic centimeters. A class stacks exactly 200 of these flats to build a tower. Which expression shows the volume of the tower, in cubic centimeters?<div style="margin-top:8px">' + hundreds_flat() + '</div>',
    ['2 &times; 10', '2 &times; 10 &times; 10', '2 &times; 10 &times; 10 &times; 10', '2 &times; 10 &times; 10 &times; 10 &times; 10'], '2 &times; 10 &times; 10 &times; 10 &times; 10',
    '200 &times; 100 = 20,000. 200 = 2 &times; 10 &times; 10 and 100 = 10 &times; 10, so 20,000 = 2 &times; 10 &times; 10 &times; 10 &times; 10 (four 10s). B is only 200 (it forgets the 100 in each flat, like the 20 she forgot on QR11 #14). C is 2,000. A is 20.',
    'Lower 5 QR #38 (her miss, last third); QR9 #29, QR11 #14 (her miss)', 'last',
    'x o x', 'Lower 5 QR #38, QR9 #29, QR11 #14',
    'Same: same steps as QR11 #14, with 200 flats of 100 instead of 20 cubes of 1,000 (parent 11/18)')

# ================= checks =================
assert len(P) == 30
L = [p['correct'] for p in P]
cnt = Counter(L); print(cnt, ''.join(L))
assert max(cnt.values()) - min(cnt.values()) <= 2, cnt
assert not any(L[i] == L[i+1] == L[i+2] for i in range(28)), ''.join(L)
tc = Counter(p['topic'] for p in P)
assert max(tc.values()) == 1, tc
thirds = Counter(MAP[n]['source_third'] for n in MAP); print(thirds)
assert thirds == {'middle': 6, 'last': 24} and all(MAP[n]['source_third'] == 'middle' for n in range(1, 7))
json.dump(P, open(os.path.join(HERE, 'ma6_problems.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(MAP, open(os.path.join(HERE, 'ma6_mapping.json'), 'w'), indent=1, ensure_ascii=False)
print('wrote', len(P), 'diagrams', sum(1 for p in P if p['diagram']))
