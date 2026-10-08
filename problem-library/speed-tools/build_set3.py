import json, html
S = '/private/tmp/claude-501/-Users-kxieztt-Documents-HannahISEEMath/5e000592-8898-4fa3-a99a-7f35349cf51d/scratchpad/'
REPO = '/Users/kxieztt/Documents/HannahISEEMath-repo/'
plan = json.load(open(S + 'plan3.json'))['slots']

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data"><tr>{th}</tr>{trs}</table>'

def bar(parts, shaded, w=300):
    cell = w // parts
    out = [f'<svg viewBox="0 0 {w} 50" width="{w}" height="50" role="img">']
    for i in range(parts):
        fill = 'var(--accent-soft)' if i < shaded else 'var(--surface)'
        out.append(f'<rect x="{i*cell}" y="5" width="{cell}" height="40" fill="{fill}" stroke="currentColor" stroke-width="1.5"/>')
    out.append('</svg>'); return ''.join(out)

def grid(rows, cols, shaded, w=260):
    cell = w // cols; h = cell * rows
    out = [f'<svg viewBox="0 0 {cols*cell} {h}" width="{cols*cell}" height="{h}" role="img">']
    n = 0
    for r in range(rows):
        for c in range(cols):
            fill = 'var(--accent-soft)' if n < shaded else 'var(--surface)'
            out.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="{fill}" stroke="currentColor" stroke-width="1.5"/>')
            n += 1
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

def net(faces, s=50):
    W = max(c for c,r,l in faces)*s + s + 10; H = max(r for c,r,l in faces)*s + s + 10
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">']
    for c,r,l in faces:
        x,y = c*s+5, r*s+5
        out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>')
        out.append(f'<text x="{x+s/2}" y="{y+s/2+4}" font-size="13" text-anchor="middle" fill="currentColor">{l}</text>')
    out.append('</svg>'); return ''.join(out)

def numberline(n, marks, show_ends=None):
    w, pad = 320, 20
    cell = (w - 2*pad) / n
    out = [f'<svg viewBox="0 0 {w} 60" width="{w}" height="60" role="img">']
    out.append(f'<line x1="{pad}" y1="30" x2="{w-pad}" y2="30" stroke="currentColor" stroke-width="1.5"/>')
    mark_map = dict(marks)
    for i in range(n+1):
        x = pad + i*cell
        out.append(f'<line x1="{x}" y1="22" x2="{x}" y2="38" stroke="currentColor" stroke-width="1.5"/>')
        if show_ends and i == 0: out.append(f'<text x="{x}" y="52" font-size="12" text-anchor="middle" fill="currentColor">{show_ends[0]}</text>')
        if show_ends and i == n: out.append(f'<text x="{x}" y="52" font-size="12" text-anchor="middle" fill="currentColor">{show_ends[1]}</text>')
        if i in mark_map: out.append(f'<text x="{x}" y="14" font-size="13" text-anchor="middle" fill="currentColor">{mark_map[i]}</text>')
    out.append('</svg>'); return ''.join(out)

def triangle_angles(a, b, w=220, h=160):
    # right-ish triangle figure with two angle labels and a "?" at the third vertex
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<polygon points="10,{h-10} {w-10},{h-10} 60,10" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            f'<text x="30" y="{h-20}" font-size="13" fill="currentColor">{a}</text>'
            f'<text x="{w-45}" y="{h-20}" font-size="13" fill="currentColor">{b}</text>'
            f'<text x="55" y="30" font-size="13" fill="currentColor">?</text>'
            f'</svg>')

def sq_area_label(area):
    return (f'<svg viewBox="0 0 140 140" width="140" height="140" role="img">'
            f'<rect x="10" y="10" width="120" height="120" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            f'<text x="70" y="75" font-size="14" text-anchor="middle" fill="currentColor">Area = {area} sq cm</text>'
            f'</svg>')

# P[n] = dict(q, a=correct, d=[3 distractors], diag=optional, why, topic=optional override)
P = {}
P[1] = dict(q="A decimal number has a 6 in the tenths place, a 1 in the hundredths place, and a 4 in the thousandths place. What is the number?", a="0.614", d=["0.641","0.461","0.146"], diag=table(["Place","Digit"],[["Tenths","6"],["Hundredths","1"],["Thousandths","4"]]), why="Tenths, hundredths, thousandths in order give 0.614.")
P[2] = dict(q="Which value is the greatest?", a="11/18", d=["7/12","0.58","3/5"], diag=numberline(2,[(1,"0.5")],show_ends=(0,1)), why="11/18 ≈ 0.611, the largest. 7/12 ≈ 0.583, 3/5 = 0.6, and 0.58 is less than both.")
P[3] = dict(q="What is a reasonable estimation for the value of (58 × 412) ÷ 29?", a="between 800 and 1,000", d=["between 600 and 800","between 1,000 and 1,200","between 400 and 600"], why="Round to 60 × 400 ÷ 30 = 800. Exact: 824, which is between 800 and 1,000.", topic="Estimating Multiplication & Division")
P[4] = dict(q="What value is equivalent to 5/8?", a="62.5%", d=["58%","0.58","85%"], why="5/8 = 0.625 = 62.5%. Trap: 58% and 0.58 reverse the digits.")
P[5] = dict(q="The net shown folds into a cube. Which face is opposite the face labeled Right?", a="Left", d=["Front","Back","Under"], diag=net([(1,0,"Top"),(0,1,"Left"),(1,1,"Front"),(2,1,"Right"),(3,1,"Back"),(1,2,"Under")]), why="In the strip Left-Front-Right-Back, faces two places apart are opposite. Right and Left are opposite.")
P[6] = dict(q="What is the next number in the pattern 5, 11, 23, 47, ___?", a="95", d=["94","71","119"], diag=table(["Term","Value"],[["1","5"],["2","11"],["3","23"],["4","47"],["5","?"]]), why="Differences double: 6, 12, 24, then 48. 47 + 48 = 95. Trap: 94 just doubles the term instead of the difference.")
P[7] = dict(q="The graph shows points scored by 4 players. Which statement is true?", a="Beth scored the most.", d=["Dana scored more than Beth.","Ann and Cara together scored 30.","The range of the scores is 4."], diag=barchart(["Ann","Beth","Cara","Dana"],[8,14,10,9]), why="Beth's 14 is the highest. Trap: Ann (8) + Cara (10) = 18, not 30; the range is 14 − 8 = 6, not 4.", topic="Identifying Correct Conclusions from Bar Graph Data Table")
P[8] = dict(q="The table shows how many points four students scored on a quiz. Which statement is true?", a="Ann and Cara scored the same.", d=["Dana scored more than Ann.","The total of all four scores is 52.","Beth scored more than Dana."], diag=table(["Player","Points"],[["Ann","15"],["Beth","9"],["Cara","15"],["Dana","11"]]), why="Ann and Cara both scored 15. Trap: the true total is 15+9+15+11 = 50, not 52; Dana (11) scored more than Beth (9), not less.", topic="Identifying Correct Conclusions from Bar Graph Data Table")
P[9] = dict(q="A square has a side of 9 cm. What is its area?", a="81 sq cm", d=["36 sq cm","18 sq cm","72 sq cm"], why="Area = side × side = 9 × 9 = 81 sq cm.")
P[10] = dict(q="A square has a perimeter of 28 cm. What is the length of one side?", a="7 cm", d=["14 cm","4 cm","56 cm"], why="Perimeter ÷ 4 = 28 ÷ 4 = 7 cm.")
P[11] = dict(q="Tom has $58 to split equally among 6 friends. About how much does each friend get?", a="about $10", d=["about $5","about $6","about $60"], diag=table(["Item","Amount"],[["Money","$58"],["Friends","6"]]), why="Round $58 to $60. $60 ÷ 6 = $10.", topic="Estimating Division with Money")
P[12] = dict(q="Which list orders 5/9, 0.52, and 7/15 from least to greatest?", a="7/15, 0.52, 5/9", d=["5/9, 0.52, 7/15","0.52, 7/15, 5/9","5/9, 7/15, 0.52"], diag=numberline(2,[(1,"0.5")],show_ends=(0,1)), why="7/15 ≈ 0.467, 0.52, 5/9 ≈ 0.556 — that order is least to greatest.")
P[13] = dict(q="Mia has $82 to split equally among 9 friends. About how much does each friend get?", a="about $9", d=["about $8","about $18","about $90"], why="Round $82 to $81 (a multiple of 9). $81 ÷ 9 = $9.", topic="Estimating Division with Money")
P[14] = dict(q="Lucy has $123 to split equally among 6 friends. About how much does each friend get?", a="about $20", d=["about $12","about $2","about $200"], diag=table(["Item","Amount"],[["Money","$123"],["Friends","6"]]), why="Round $123 to $120. $120 ÷ 6 = $20.", topic="Estimating Division with Money")
P[15] = dict(q="A decimal number has a 3 in the thousandths place, an 8 in the tenths place, and a 0 in the hundredths place. What is the number?", a="0.803", d=["0.830","0.308","0.038"], diag=table(["Place","Digit"],[["Tenths","8"],["Hundredths","0"],["Thousandths","3"]]), why="Tenths, hundredths, thousandths in order give 0.803.")
P[16] = dict(q="The net shown folds into a cube. Which face is opposite the face labeled R?", a="T", d=["Q","S","U"], diag=net([(1,0,"P"),(1,1,"Q"),(2,1,"R"),(3,1,"S"),(4,1,"T"),(3,2,"U")]), why="In the strip Q-R-S-T, faces two places apart are opposite. R and T are opposite.")
P[17] = dict(q="The graph shows the votes for four colors. Which statement is true?", a="Red and Green are tied for the most votes.", d=["Yellow has more votes than Blue.","The total number of votes is 40.","Blue has the fewest votes."], diag=barchart(["Red","Blue","Green","Yellow"],[12,7,12,5]), why="Red and Green both have 12. Trap: the true total is 12+7+12+5 = 36, not 40; Yellow (5) has the fewest, not Blue (7).", topic="Identifying Correct Conclusions from Bar Graph Data Table")
P[18] = dict(q="What is the next number in the pattern 3, 9, 27, 81, ___?", a="243", d=["162","216","324"], why="Each term is 3 times the one before: 81 × 3 = 243.")
P[19] = dict(q="Which value is equivalent to 0.045?", a="9/200", d=["9/20","45%","1/45"], why="0.045 = 45/1,000 = 9/200. Trap: 9/20 and 45% both equal 0.45, ten times too big.")
P[20] = dict(q="Each figure in a pattern has 3 more tiles than the one before. Figure 1 has 4 tiles. How many tiles does Figure 7 have?", a="22", d=["25","21","18"], diag=table(["Figure","Tiles"],[["1","4"],["2","7"],["3","10"],["7","?"]]), why="Figure n has 4 + 3(n − 1) tiles. Figure 7: 4 + 3×6 = 22.")
P[21] = dict(q="A figure is divided into 15 equal parts, and 9 are shaded. What percent of the figure is shaded?", a="60%", d=["40%","67%","90%"], diag=grid(3,5,9), why="9 of 15 parts = 9/15 = 3/5 = 60%.")
P[22] = dict(q="A figure is divided into 24 equal parts. If 5/8 of the figure is shaded, how many parts are shaded?", a="15", d=["19","8","20"], why="5/8 of 24 is 15 parts.")
P[23] = dict(q="Point B lies between points A and C on a number line. A is at 14 and C is at 50. If B is the midpoint of AC, what number is B?", a="32", d=["36","28","25"], why="Midpoint = (14 + 50) ÷ 2 = 32.", topic="Split Line Segments")
P[24] = dict(q="A square has an area of 64 square cm. What is its perimeter?", a="32 cm", d=["16 cm","64 cm","256 cm"], diag=sq_area_label(64), why="Side = √64 = 8 cm. Perimeter = 4 × 8 = 32 cm.")
P[25] = dict(q="A 5-pack of pens costs $12.50. What is the price per pen?", a="$2.50", d=["$2.00","$0.40","$62.50"], diag=table(["Item","Price"],[["5-pack","$12.50"]]), why="$12.50 ÷ 5 = $2.50 per pen. Trap: $62.50 multiplies instead of dividing.")
P[26] = dict(q="What is a reasonable estimation for the value of (83 × 196) ÷ 21?", a="between 700 and 900", d=["between 500 and 700","between 900 and 1,100","between 300 and 500"], diag=table(["Number","Round to"],[["83","80"],["196","200"],["21","20"]]), why="Round to 80 × 200 ÷ 20 = 800. Exact: 774.7, which is between 700 and 900.", topic="Estimating Multiplication & Division")
P[27] = dict(q="In a triangle, one angle measures 90° and another measures 35°. What is the measure of the third angle?", a="55°", d=["45°","65°","125°"], diag=triangle_angles("90°","35°"), why="The angles in a triangle add to 180°. 180 − 90 − 35 = 55°. Trap: 125° just adds the two given angles.")
P[28] = dict(q="Estimate 38.7 + 24.6 − 11.9. Which is the best estimate?", a="about 52", d=["about 42","about 62","about 72"], why="Round each: 39 + 25 − 12 = 52. Exact: 51.4.", topic="Estimating Sums/Differences of Decimal Numbers")
P[29] = dict(q="An 8-ounce bottle of juice costs $3.20. What is the price per ounce?", a="$0.40", d=["$0.04","$4.00","$25.60"], diag=table(["Item","Price"],[["8 oz bottle","$3.20"]]), why="$3.20 ÷ 8 = $0.40 per ounce. Trap: $25.60 multiplies instead of dividing.")
P[30] = dict(q="Which expression means: 7 more than twice a number x?", a="2x + 7", d=["2(x + 7)","7x + 2","2x − 7"], why="Twice x is 2x; 7 more than that is 2x + 7.", topic="Translating Math Expressions")
P[31] = dict(q="Which value is the least?", a="9/16", d=["5/8","0.62","0.58"], diag=bar(16,9), why="9/16 = 0.5625, which is less than 0.58, 0.62, and 5/8 (0.625).")
P[32] = dict(q="Which expression means: 4 less than the product of 5 and a number n?", a="5n − 4", d=["5(n − 4)","4 − 5n","5n + 4"], why="Product of 5 and n is 5n; 4 less than that is 5n − 4. Trap: 5(n − 4) also shows '− 4', but it subtracts before multiplying, not after.", topic="Translating Math Expressions")
P[33] = dict(q="The ratio of cats to dogs at a shelter is 3 : 5. There are 56 animals in all. How many dogs are there?", a="35", d=["21","24","32"], why="3 + 5 = 8 parts. 56 ÷ 8 = 7 per part. Dogs = 5 × 7 = 35. Trap: 21 is the number of cats.", topic="Word Problems with Ratios")
P[34] = dict(q="Each letter represents a different digit from 1 through 9. PP + QQ = RST. What digit does R represent?", a="1", d=["3","7","9"], why="PP and QQ are two-digit repeated digits, so PP + QQ = 11 × (P + Q). The largest possible sum is 11 × 17 = 187, so the hundreds digit R is always 1.")
P[35] = dict(q="What is the value of the digit 4 in 0.462?", a="4 tenths", d=["4 hundredths","4 thousandths","4 ones"], why="0.462: 4 is tenths, 6 is hundredths, 2 is thousandths.")
P[36] = dict(q="Each square in this net is 3 cm by 3 cm. The net folds into a cube. What is its surface area?", a="54 sq cm", d=["36 sq cm","27 sq cm","81 sq cm"], diag=net([(1,0,"3 cm"),(0,1,"3 cm"),(1,1,"3 cm"),(2,1,"3 cm"),(3,1,"3 cm"),(1,2,"3 cm")]), why="6 faces × (3 × 3) = 54 square cm.")
P[37] = dict(q="Use the number line. P is the midpoint between Q and another point R. What is R?", a="50", d=["40","60","45"], diag=numberline(10,[(2,"Q"),(6,"P")]), why="Q = 10, P = 30 (read from the marks, 5 per tick). Midpoint of Q and R equals P, so R = 2 × 30 − 10 = 50.", topic="Split Line Segments")
P[38] = dict(q="What is 7/16 as a decimal?", a="0.4375", d=["0.467","0.4325","0.475"], why="7 ÷ 16 = 0.4375.")

items = []
for s in plan:
    n = s['n']; p = P[n]
    L = s['correct_letter']; i = 'ABCD'.index(L)
    ch = p['d'][:]; ch.insert(i, p['a'])
    assert len(ch) == 4 and ch[i] == p['a'], n
    items.append(dict(n=n, tier=s['tier'], topic=p.get('topic', s['topic']), q=p['q'], ch=ch, ans=L,
                      diag=p.get('diag'), why=p['why'], needs_diag=bool(p.get('diag')), ref=s['reference']))

json.dump(items, open(S + 'set3_items.json', 'w'), indent=1)
print('items', len(items), 'diagrams', sum(1 for it in items if it['needs_diag']))
