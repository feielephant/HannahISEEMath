import json, html
plan = json.load(open('/tmp/gen/set1_plan.json'))['slots']

def grid(rows, cols, shaded, colors=None, w=260):
    cell = w // cols; h = cell * rows
    out = [f'<svg viewBox="0 0 {cols*cell} {h}" width="{cols*cell}" height="{h}" role="img">']
    n = 0
    for r in range(rows):
        for c in range(cols):
            fill = 'var(--accent-soft)' if n < shaded else 'var(--surface)'
            if colors: fill = colors[n]
            out.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="{fill}" stroke="currentColor" stroke-width="1.5"/>')
            n += 1
    out.append('</svg>'); return ''.join(out)

def bar(parts, shaded, w=300):
    cell = w // parts
    out = [f'<svg viewBox="0 0 {w} 50" width="{w}" height="50" role="img">']
    for i in range(parts):
        fill = 'var(--accent-soft)' if i < shaded else 'var(--surface)'
        out.append(f'<rect x="{i*cell}" y="5" width="{cell}" height="40" fill="{fill}" stroke="currentColor" stroke-width="1.5"/>')
    out.append('</svg>'); return ''.join(out)

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data"><tr>{th}</tr>{trs}</table>'

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

def rects(specs):
    # specs: list of (x, y, w, h, label)
    W = max(x+w for x,y,w,h,l in specs)+10; H = max(y+h for x,y,w,h,l in specs)+10
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">']
    for x,y,w,h,l in specs:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>')
        out.append(f'<text x="{x+w/2}" y="{y+h/2+4}" font-size="13" text-anchor="middle" fill="currentColor">{l}</text>')
    out.append('</svg>'); return ''.join(out)

def lshape(pts, labels):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    W=max(xs)+30; H=max(ys)+30
    d=' '.join(f'{x+10},{y+10}' for x,y in pts)
    out=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"><polygon points="{d}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>']
    for x,y,l in labels: out.append(f'<text x="{x+10}" y="{y+10}" font-size="13" fill="currentColor">{l}</text>')
    out.append('</svg>'); return ''.join(out)

def pie(colors_counts):
    # 12-cell spinner as a grid of sections
    cols=[]
    for color,n in colors_counts: cols += [color]*n
    fills={'red':'#E77563','green':'#4FC4AC','yellow':'#E0AC4E'}
    return grid(3,4,0,colors=[fills[c] for c in cols])

P = {}
P[1] = dict(q="A number is greater than 30 and less than 40. It is a multiple of 4 and also a multiple of 6. What is the number?", ch=["24","32","38","36"], why="Multiples of 12 between 30 and 40: only 36. (Check each: 36÷4=9, 36÷6=6.)")
P[2] = dict(q="A bag has 4 red marbles and 6 blue marbles. One marble is picked at random. What is the probability that it is red?", ch=["3/5","1/2","2/5","1/10"], why="4 red out of 10 total = 4/10 = 2/5. The trap is 3/5, the chance of blue (complement).")
P[3] = dict(q="The bar is split into 4 equal parts, and 3 parts are shaded. Which value is NOT equivalent to the shaded part?", ch=["0.75","75%","3/5","3/4"], diag=bar(4,3), why="3/4 = 0.75 = 75%. 3/5 is not equal. KEY WORD: NOT. Habit: key-word-watch.")
P[4] = dict(q="What percent of the figure is shaded?", ch=["40%","4%","60%","25%"], diag=grid(2,5,4), why="4 of 10 squares shaded = 40%.")
P[5] = dict(q="How many milligrams are in 0.05 kilograms?", ch=["50,000 mg","5,000 mg","500 mg","50 mg"], why="0.05 kg = 50 g (×1,000); 50 g = 50,000 mg (×1,000 again). Two steps, not one. Gap: multi-step conversion.")
P[6] = dict(q="Which value is NOT equivalent to the shaded part of the bar?", ch=["2/10","20%","0.02","1/5"], diag=bar(10,2), why="2/10 = 20% = 1/5 = 0.2. 0.02 is not equal. KEY WORD: NOT.")
P[7] = dict(q="Maya has x apples. Ben has 3 times as many apples as Maya. Chris has 5 fewer apples than Ben. Which expression shows how many apples Chris has?", ch=["3x − 5","3(x − 5)","3x + 5","x − 15"], why="Ben = 3x; Chris = 3x − 5. Trap: 3(x − 5) applies the 5 before the multiplication.")
P[8] = dict(q="Two rectangles are similar. The small rectangle is 4 cm wide and 6 cm long. The large rectangle is 10 cm wide. How long is the large rectangle?", ch=["12 cm","14 cm","16 cm","15 cm"], diag=rects([(10,30,40,60,"4 cm"),(80,10,100,150,"10 cm")]), why="Scale factor 10 ÷ 4 = 2.5. Length 6 × 2.5 = 15 cm.")
P[9] = dict(q="There are 60 squares in a figure, and 15 are shaded. What percent of the figure is shaded?", ch=["25%","15%","40%","75%"], why="15/60 = 1/4 = 25%.")
P[10] = dict(q="The price tags show the cost of each item. About how much will 4 smoothies cost?", ch=["about $8","about $16","about $20","about $24"], diag=table(["Item","Price"],[["Smoothie","$3.92"],["Sandwich","$4.95"],["Soup","$3.10"]]), why="Round $3.92 to $4. Four smoothies ≈ 4 × $4 = $16. (Exact: $15.68.)")
P[11] = dict(q="A small triangle has side lengths 3, 4, and 5 units. A similar large triangle has a shortest side of 9 units. What is its longest side?", ch=["12 units","15 units","20 units","25 units"], why="Scale factor 9 ÷ 3 = 3. Longest side 5 × 3 = 15 units.")
P[12] = dict(q="A number is greater than 40 and less than 50. It is odd and divisible by 3. What is the number?", ch=["42","44","45","48"], why="Odd numbers 41–49: 41, 43, 45, 47, 49. Only 45 is divisible by 3.")
P[13] = dict(q="What percent of the figure is shaded?", ch=["25%","20%","35%","50%"], diag=grid(4,5,5), why="5 of 20 squares = 25%.")
P[14] = dict(q="A pen costs p dollars. Ana buys 6 pens and pays with a $20 bill. Which expression shows her change?", ch=["6p − 20","20 − p","20 − 6p","6(20 − p)"], diag=table(["Item","Price"],[["Pen","p dollars"],["Ana pays","$20"]]), why="Change = money paid − cost = 20 − 6p. Habit: exact-thing-asked (the change, not the total cost).")
P[15] = dict(q="Estimate 19 × 2.9. Which is the best estimate?", ch=["about 60","about 40","about 90","about 120"], diag=table(["Number","Round to"],[["19","20"],["2.9","3"]]), why="20 × 3 = 60. Exact product is 55.1, closest to 60.")
P[16] = dict(q="The bar graph shows boxes of cookies sold each day. How many boxes were sold in all?", ch=["52","56","53","54"], diag=barchart(["Mon","Tue","Wed","Thu"],[12,18,15,9]), why="12 + 18 + 15 + 9 = 54.")
P[17] = dict(q="What is (−4) × (−5)?", ch=["−20","−9","−1","20"], why="Negative × negative = positive: 4 × 5 = 20.")
P[18] = dict(q="How many pints are in 3 gallons?", ch=["6","12","24","48"], diag=table(["Unit","Equal to"],[["1 gallon","4 quarts"],["1 quart","2 pints"]]), why="3 gal × 4 qt × 2 pt = 24 pints. Two hops, not one.")
P[19] = dict(q="A recipe needs 2¾ cups of flour per batch. About how many cups of flour are needed for 7 batches?", ch=["about 21","about 14","about 28","about 35"], why="Round 2¾ to 3. 7 × 3 = 21 cups. (Exact: 19¼.)")
P[20] = dict(q="A 6-foot-tall person casts a 4-foot shadow at the same time a tree casts a 10-foot shadow. How tall is the tree?", ch=["10 ft","15 ft","18 ft","24 ft"], diag=rects([(10,60,60,120,"6 ft"),(90,140,100,40,"4 ft shadow"),(210,40,40,160,"tree"),(260,180,100,20,"10 ft shadow")]), why="Heights scale with shadows: 6/4 = tree/10, so tree = 15 ft.")
P[21] = dict(q="A recipe uses 2 cups of flour for every 3 cups of sugar. If you use 9 cups of sugar, how many cups of flour do you need?", ch=["4","6","9","12"], why="Flour:sugar = 2:3. 9 ÷ 3 = 3, so flour = 2 × 3 = 6.")
P[22] = dict(q="A jar holds 3/4 of a liter. Half of that amount is poured out. How many liters remain?", ch=["1/4","1/2","3/4","3/8"], diag=bar(4,3), why="3/4 × 1/2 = 3/8 liter remains. Trap: 1/4 (subtracting the fraction poured out instead of taking half).")
P[23] = dict(q="Sam has y marbles. Lee has 4 more than twice as many marbles as Sam. Which expression shows how many marbles Lee has?", ch=["2(y + 4)","y + 8","2y + 4","4y + 2"], why="Twice Sam's = 2y; 4 more = 2y + 4.")
P[24] = dict(q="The bar is split into 2 equal parts, and 1 part is shaded. Which value is NOT equivalent to the shaded part?", ch=["0.2","50%","5/10","0.5"], diag=bar(2,1), why="1/2 = 0.5 = 50% = 5/10. 0.2 is not equal. KEY WORD: NOT.")
P[25] = dict(q="What is (−18) ÷ 3?", ch=["−6","6","−15","15"], why="−18 ÷ 3 = −6.")
P[26] = dict(q="A figure is a 5 by 3 rectangle with a 2 by 1 notch removed from one corner. What is the perimeter of the figure?", ch=["14","18","16","20"], why="Perimeter of 5×3 rectangle = 16. Removing a corner notch does not change the outside perimeter.")
P[27] = dict(q="Which number is divisible by both 4 and 9?", ch=["24","27","54","72"], diag=table(["Number","Divisible by 4?","Divisible by 9?"],[["24","yes","no"],["27","no","yes"],["54","no","yes"],["72","yes","yes"]]), why="72 = 4 × 18 = 9 × 8. Habit: check-every-condition (both conditions).")
P[28] = dict(q="The figure is made of two rectangles, one 8 ft by 3 ft and one 5 ft by 2 ft, joined as shown. What is its area?", ch=["30 sq ft","32 sq ft","33 sq ft","34 sq ft"], diag=lshape([(0,0),(200,0),(200,60),(120,60),(120,120),(0,120)], [(60,40,"8 ft × 3 ft"),(60,100,"5 ft × 2 ft")]), why="8 × 3 = 24, plus 5 × 2 = 10. Total 34 sq ft.")
P[29] = dict(q="A large square has sides of 10 units. A 4 by 4 square is cut from one corner. What is the remaining area?", ch=["96","84","60","76"], why="100 − 16 = 84 square units.")
P[30] = dict(q="Tickets: adult $12, child $7. What is the total cost for 2 adults and 3 children?", ch=["$40","$44","$42","$45"], diag=table(["Ticket","Price"],[["Adult","$12"],["Child","$7"]]), why="2 × 12 + 3 × 7 = 24 + 21 = $45.")
P[31] = dict(q="How many seconds are in 2 hours?", ch=["720","7,200","72,000","120"], diag=table(["Unit","Equal to"],[["1 minute","60 seconds"],["1 hour","60 minutes"]]), why="2 × 60 × 60 = 7,200 seconds. Two hops.")
P[32] = dict(q="A pizza is whole. Lia eats 1/3 of it, then 1/4 of the whole pizza. What fraction of the pizza is left?", ch=["1/2","5/12","7/12","1/12"], why="1 − 1/3 − 1/4 = 12/12 − 4/12 − 3/12 = 5/12.")
P[33] = dict(q="Tom buys 4 notebooks at $3 each and pays with a $20 bill. How much change does he get?", ch=["$6","$10","$7","$8"], why="20 − 4 × 3 = 20 − 12 = $8.")
P[34] = dict(q="The ratio of boys to girls in a class is 3 : 5. There are 24 students in all. How many boys are there?", ch=["8","9","15","12"], diag=bar(8,3), why="3 + 5 = 8 parts; 24 ÷ 8 = 3 students per part; boys = 3 × 3 = 9.")
P[35] = dict(q="A spinner has 8 equal sections, and 2 are blue. What is the probability that it does NOT land on blue?", ch=["3/4","1/4","1/2","3/8"], why="6 of 8 sections are not blue: 6/8 = 3/4. Habit: key-word-watch (NOT).")
P[36] = dict(q="A spinner has 12 equal sections: 3 red, 5 green, and 4 yellow. What is the probability it lands on yellow?", ch=["1/4","1/3","5/12","1/2"], diag=grid(3,4,0,colors=['#E77563']*3+['#4FC4AC']*5+['#E0AC4E']*4), why="4 yellow of 12 = 4/12 = 1/3.")
P[37] = dict(q="A tank is 3/5 full. Then half of the water is used. What fraction of the tank is left?", ch=["1/5","2/5","1/2","3/10"], diag=bar(5,3), why="3/5 × 1/2 = 3/10 left.")
P[38] = dict(q="A price is $200. It is increased by 20%, and then the new price is decreased by 20%. What is the final price?", ch=["$200","$192","$196","$180"], diag=table(["Step","Price"],[["Start","$200"],["+20%","$240"],["−20%","?"]]), why="200 × 1.2 = 240; 240 × 0.8 = 192. Not back to $200 — the changes do not cancel (trap: $200).")

# check each answer letter against the plan
letters_plan = [s['correct_letter'] for s in plan]
ok = True
items = []
for s in plan:
    n = s['n']; p = P[n]
    assert len(p['ch']) == 4, n
    items.append(dict(n=n, tier=s['tier'], topic=s['topic'], q=p['q'], ch=p['ch'], ans=s['correct_letter'], diag=p.get('diag'), why=p['why'], needs_diag=s['needs_diagram'], ref=s['reference']))
    if s['needs_diagram'] and not p.get('diag'): print('MISSING DIAGRAM', n); ok=False
    if not s['needs_diagram'] and p.get('diag'): print('EXTRA DIAGRAM', n)
json.dump(items, open('set1_items.json','w'), indent=1)
print('ok' if ok else 'fix', len(items))
