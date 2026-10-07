import json, random, html
random.seed(202)
REPO = '/Users/kxieztt/Documents/HannahISEEMath-repo/'

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data"><tr>{th}</tr>{trs}</table>'

def numberline(lo, hi, step, marks):
    # evenly spaced ticks from lo to hi; only the two ends are numbered; marks is a list of (tick_index, label)
    n = (hi - lo) // step
    w, pad = 320, 20
    cell = (w - 2*pad) / n
    out = [f'<svg viewBox="0 0 {w} 60" width="{w}" height="60" role="img">']
    out.append(f'<line x1="{pad}" y1="30" x2="{w-pad}" y2="30" stroke="currentColor" stroke-width="1.5"/>')
    mark_map = dict(marks)
    for i in range(n+1):
        x = pad + i*cell
        out.append(f'<line x1="{x}" y1="22" x2="{x}" y2="38" stroke="currentColor" stroke-width="1.5"/>')
        if i == 0: out.append(f'<text x="{x}" y="52" font-size="12" text-anchor="middle" fill="currentColor">{lo}</text>')
        if i == n: out.append(f'<text x="{x}" y="52" font-size="12" text-anchor="middle" fill="currentColor">{hi}</text>')
        if i in mark_map: out.append(f'<text x="{x}" y="14" font-size="13" text-anchor="middle" fill="currentColor">{mark_map[i]}</text>')
    out.append('</svg>'); return ''.join(out)

def coordplane(xmin, xmax, ymin, ymax, points, s=20):
    pad = 24
    w = (xmax - xmin) * s + 2*pad; h = (ymax - ymin) * s + 2*pad
    def px(x): return pad + (x - xmin) * s
    def py(y): return h - pad - (y - ymin) * s
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
    for gx in range(xmin, xmax+1):
        out.append(f'<line x1="{px(gx)}" y1="{py(ymin)}" x2="{px(gx)}" y2="{py(ymax)}" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>')
    for gy in range(ymin, ymax+1):
        out.append(f'<line x1="{px(xmin)}" y1="{py(gy)}" x2="{px(xmax)}" y2="{py(gy)}" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>')
    out.append(f'<line x1="{px(xmin)}" y1="{py(0)}" x2="{px(xmax)}" y2="{py(0)}" stroke="currentColor" stroke-width="1.5"/>')
    out.append(f'<line x1="{px(0)}" y1="{py(ymin)}" x2="{px(0)}" y2="{py(ymax)}" stroke="currentColor" stroke-width="1.5"/>')
    for x, y, lab in points:
        out.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="3.5" fill="var(--accent)"/>')
        out.append(f'<text x="{px(x)+6}" y="{py(y)-6}" font-size="13" fill="currentColor">{lab}</text>')
    out.append('</svg>'); return ''.join(out)

def barchart(labels, values):
    w, h, pad = 300, 170, 28
    mx = max(values)
    bw = (w - pad) // len(values)
    out = [f'<svg viewBox="0 0 {w} {h+24}" width="{w}" height="{h+24}" role="img">']
    out.append(f'<line x1="{pad}" y1="{h}" x2="{w}" y2="{h}" stroke="currentColor"/>')
    for i,(l,v) in enumerate(zip(labels, values)):
        bh = int((h-20) * v / mx)
        x = pad + i*bw + 8
        out.append(f'<rect x="{x}" y="{h-bh}" width="{bw-16}" height="{bh}" fill="var(--accent)" opacity="0.75"/>')
        out.append(f'<text x="{x+(bw-16)/2}" y="{h+14}" font-size="12" text-anchor="middle" fill="currentColor">{l}</text>')
        out.append(f'<text x="{x+(bw-16)/2}" y="{h-bh-4}" font-size="11" text-anchor="middle" fill="currentColor">{v}</text>')
    out.append('</svg>'); return ''.join(out)

# (question, correct, [d1,d2,d3], tier, topic, diagram_html_or_None, why)
P = [
("Use the number line. The hash marks are evenly spaced. What number does M stand for?", "40", ["35","45","30"], "Easy", "number line (evenly spaced marks)", numberline(20,50,5,[(4,"M")]), "6 equal steps of 5 from 20 to 50. M is the 4th mark after 20: 20 + 4×5 = 40."),
("Which number is divisible by 7?", "77", ["74","81","92"], "Easy", "divisibility by 7", None, "77 ÷ 7 = 11. The others leave a remainder."),
("A machine changes numbers by one rule. Input 2 gives output 9, and input 5 gives output 18. What is the output for input 8?", "27", ["24","30","21"], "Medium", "function machine rule (output = 3 × input + 3)", table(["Input","Output"],[["2","9"],["5","18"],["8","?"]]), "Rule: output = 3 × input + 3. 3 × 8 + 3 = 27."),
("Find the mode of 5, 12, 8, 12, 19, 3, 12.", "12", ["5","19","8"], "Easy", "mode", None, "12 appears three times, more than any other value."),
("The range of a set of numbers is 34. The smallest number is 9. What is the largest number?", "43", ["25","34","52"], "Medium", "range (missing value)", None, "Range = largest − smallest, so largest = 34 + 9 = 43."),
("What is the median of 6, 10, 3, 15, 8, 12?", "9", ["8","10","11"], "Medium", "median (even count)", None, "In order: 3, 6, 8, 10, 12, 15. With six numbers, average the two middle values: (8 + 10) ÷ 2 = 9."),
("The average of four numbers is 15. Three of the numbers are 10, 18, and 20. What is the fourth number?", "12", ["8","18","22"], "Medium", "average (missing value)", None, "Four numbers averaging 15 sum to 60. 60 − (10 + 18 + 20) = 12."),
("Points P, Q, R, and S are plotted on the grid. If all four points are connected in order, what shape do they form?", "rectangle", ["square","trapezoid","rhombus"], "Hard", "classifying a quadrilateral from coordinates", coordplane(-3,4,-2,4,[(-2,-1,"P"),(-2,3,"Q"),(3,3,"R"),(3,-1,"S")]), "P to Q is 4 units up, Q to R is 5 units right: the sides are not equal, but opposite sides are equal and all angles are right angles, so it is a rectangle."),
("Points P, Q, R, and S are plotted on the grid. What is the perimeter of quadrilateral PQRS?", "24 units", ["35 units","12 units","17 units"], "Medium", "perimeter from coordinates", coordplane(0,10,0,7,[(2,1,"P"),(2,6,"Q"),(9,6,"R"),(9,1,"S")]), "The sides are 5 units and 7 units. Perimeter = 2 × (5 + 7) = 24 units. Trap: 35 is the area, not the perimeter."),
("What value is equivalent to 35%?", "7/20", ["3/5","0.035","3.5"], "Medium", "percent equivalence", None, "35% = 35/100 = 7/20. Trap: 0.035 (moved the decimal the wrong way)."),
("A hiker starts at an elevation of −45 m. She climbs up 120 m, then climbs down 30 m. What is her new elevation?", "45 m", ["−75 m","15 m","195 m"], "Hard", "signed numbers (elevation, multi-step)", None, "−45 + 120 = 75. 75 − 30 = 45."),
("Which number is divisible by both 6 and 8?", "48", ["36","32","54"], "Medium", "divisibility by 6 and 8", None, "48 ÷ 6 = 8 and 48 ÷ 8 = 6. Each other choice fails one of the two conditions."),
("Which number is a multiple of both 4 and 9?", "36", ["27","32","45"], "Easy", "multiples (common multiple)", None, "36 = 4 × 9. 27 and 45 are multiples of 9 but not 4; 32 is a multiple of 4 but not 9."),
("Which fraction is greater than 0.75?", "7/9", ["3/4","5/8","2/3"], "Hard", "comparing fraction to decimal", None, "7/9 ≈ 0.778, which is greater than 0.75. 3/4 equals 0.75 exactly; the others are less."),
("What is the value of the digit 5 in 12.456?", "5 hundredths", ["5 tenths","5 thousandths","5 ones"], "Medium", "decimal place value", None, "12.456: 4 is tenths, 5 is hundredths, 6 is thousandths."),
("Which list orders 5/8, 1/2, and 3/5 from least to greatest?", "1/2, 3/5, 5/8", ["5/8, 3/5, 1/2","3/5, 1/2, 5/8","1/2, 5/8, 3/5"], "Medium", "ordering fractions (unlike denominators)", None, "1/2 = 0.5, 3/5 = 0.6, 5/8 = 0.625."),
("A rectangle has an area of 48 square cm and a width of 6 cm. What is its perimeter?", "28 cm", ["14 cm","48 cm","96 cm"], "Medium", "perimeter from area", None, "Length = 48 ÷ 6 = 8 cm. Perimeter = 2 × (6 + 8) = 28 cm."),
("Marco has 25 marbles. He gives away 2/5 of them. How many marbles does he have left?", "15", ["10","20","5"], "Medium", "fraction of a quantity", None, "2/5 of 25 is 10. 25 − 10 = 15 left. Trap: 10 is how many he gave away, not how many are left."),
("A spinner has 10 equal sections: 4 green, 3 yellow, and 3 purple. What is the probability of landing on yellow?", "3/10", ["4/10","3/7","7/10"], "Easy", "probability of one event", None, "3 yellow out of 10 sections = 3/10."),
("It is 2:00 PM in Chicago. London is 6 hours ahead of Chicago. What time is it in London?", "8:00 PM", ["8:00 AM","4:00 PM","2:00 AM"], "Medium", "time zones (ahead)", None, "2:00 PM + 6 hours = 8:00 PM."),
("Nora spent $27.85 on bracelets. Each bracelet cost $4.10. Which expression best estimates how many bracelets she bought?", "28 ÷ 4", ["28 ÷ 5","27 ÷ 4","30 ÷ 4"], "Medium", "estimating with money (expression)", table(["Item","Amount"],[["Total spent","$27.85"],["Each bracelet","$4.10"]]), "Round $27.85 to 28 and $4.10 to 4: 28 ÷ 4. Exact: about 6.8 bracelets."),
("The graph shows books sold each day. How many more books were sold on the busiest day than the slowest day?", "12", ["7","19","26"], "Medium", "reading a bar graph (difference)", barchart(["Mon","Tue","Wed","Thu"],[12,19,7,15]), "Busiest: Tuesday, 19. Slowest: Wednesday, 7. 19 − 7 = 12."),
("Which statement is always true?", "Every rhombus is a parallelogram.", ["Every parallelogram is a rhombus.","Every trapezoid has 4 equal sides.","A pentagon has 4 sides."], "Medium", "always-true statement about shapes", None, "A rhombus has two pairs of parallel sides, so it is always a parallelogram. The reverse is not always true."),
("Which expression is equivalent to 24 × (31 − 12)?", "(24 × 31) − (24 × 12)", ["(24 × 31) − 12","24 − (31 × 12)","24 × 31 × 12"], "Hard", "distributive property (subtraction)", None, "Multiply 24 by each part of the difference, then subtract."),
("On Monday, Elena read 84 pages. On Tuesday, she read one third as many pages as Monday. How many pages did she read over the two days?", "112", ["28","56","140"], "Hard", "multi-step word problem (fraction then sum)", None, "Tuesday: 84 ÷ 3 = 28 pages. Total: 84 + 28 = 112 pages. Trap: 28 is only Tuesday's pages."),
("What is the standard form for four hundred twelve thousand, seven?", "412,007", ["412,700","421,007","412,070"], "Easy", "number words to standard form", None, "Four hundred twelve thousand is 412,000. Plus seven ones: 412,007."),
("A quadrilateral has exactly one pair of parallel sides. What is it called?", "trapezoid", ["parallelogram","rhombus","pentagon"], "Easy", "identifying shapes by properties", None, "A parallelogram and rhombus both have two pairs of parallel sides; a trapezoid has only one."),
("Use the number line. P is the average of Q and another number R. What is R?", "32", ["24","40","16"], "Medium", "average using a number line (missing point)", numberline(0,40,4,[(2,"Q"),(5,"P")]), "Q = 8, P = 20 (read from the marks). Average of Q and R equals P, so R = 2 × 20 − 8 = 32."),
("A board that is 72 inches long is cut into sixths. What is the length of each piece, in inches?", "12", ["6","18","24"], "Easy", "dividing a whole number into equal parts", None, "72 ÷ 6 = 12 inches per piece."),
("A pattern of square tiles: Figure 1 has 1 tile, Figure 2 has 4 tiles, Figure 3 has 9 tiles. If the pattern continues, how many tiles will Figure 6 have?", "36", ["25","49","30"], "Hard", "pattern (square numbers)", None, "Figure n has n² tiles. Figure 6: 6² = 36."),
]
assert len(P) == 30, len(P)
letters = ['A']*8 + ['B']*8 + ['C']*7 + ['D']*7
for _ in range(2000):
    random.shuffle(letters)
    if not any(letters[i] == letters[i+1] == letters[i+2] for i in range(28)): break
items = []
for i, (q, cor, dis, tier, topic, diag, why) in enumerate(P):
    L = letters[i]; idx = 'ABCD'.index(L)
    ch = list(dis); ch.insert(idx, cor)
    items.append(dict(n=i+1, q=q, ch=ch, ans=L, tier=tier, topic=topic, diag=diag, why=why,
                       needs_diag=bool(diag), ref={"times_practised_before": 0, "wrong_so_far": None, "graded_so_far": None}))

from collections import Counter
print(Counter(letters), 'diagrams:', sum(1 for x in items if x['diag']), 'tiers:', Counter(x['tier'] for x in items))
json.dump(items, open('/private/tmp/claude-501/-Users-kxieztt-Documents-HannahISEEMath/5e000592-8898-4fa3-a99a-7f35349cf51d/scratchpad/ma2_items.json', 'w'), indent=1)
