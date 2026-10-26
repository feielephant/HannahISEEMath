import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WS = os.path.join(os.path.dirname(REPO), 'worksheets')

def frac(n, d):
    return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'

def venn(labelA, labelB):
    return ('<svg viewBox="0 0 220 120" width="220" height="120" role="img">'
            '<circle cx="85" cy="60" r="50" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<circle cx="135" cy="60" r="50" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<text x="45" y="20" font-size="11" fill="currentColor">{labelA}</text>'
            f'<text x="130" y="20" font-size="11" fill="currentColor">{labelB}</text>'
            '</svg>')

def numline(lo, hi):
    w = 280
    return (f'<svg viewBox="0 0 {w} 60" width="{w}" height="60" role="img">'
            f'<line x1="20" y1="30" x2="{w-20}" y2="30" stroke="currentColor" stroke-width="2"/>'
            f'<line x1="20" y1="22" x2="20" y2="38" stroke="currentColor" stroke-width="2"/>'
            f'<line x1="{w-20}" y1="22" x2="{w-20}" y2="38" stroke="currentColor" stroke-width="2"/>'
            f'<text x="20" y="52" font-size="12" text-anchor="middle" fill="currentColor">{lo}</text>'
            f'<text x="{w-20}" y="52" font-size="12" text-anchor="middle" fill="currentColor">{hi}</text>'
            '</svg>')

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data"><tr>{th}</tr>{trs}</table>'

def shaded_grid(cols, rows, shaded_n):
    cw, ch = 32, 32
    cells = []
    i = 0
    for r in range(rows):
        for c in range(cols):
            fill = 'var(--accent-soft)' if i < shaded_n else 'var(--surface)'
            cells.append(f'<rect x="{c*cw}" y="{r*ch}" width="{cw}" height="{ch}" fill="{fill}" stroke="currentColor" stroke-width="1.5"/>')
            i += 1
    w, h = cols*cw, rows*ch
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">' + ''.join(cells) + '</svg>'

def tile_grid(cols, rows):
    cw, ch = 28, 28
    cells = []
    for r in range(rows):
        for c in range(cols):
            cells.append(f'<rect x="{c*cw}" y="{r*ch}" width="{cw}" height="{ch}" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    w, h = cols*cw, rows*ch
    label = (f'<text x="{w/2}" y="-8" font-size="12" text-anchor="middle" fill="currentColor">{cols} m</text>'
             f'<text x="-10" y="{h/2}" font-size="12" text-anchor="middle" fill="currentColor" transform="rotate(-90,-10,{h/2})">{rows} m</text>')
    return f'<svg viewBox="-30 -24 {w+30} {h+24}" width="{w+40}" height="{h+34}" role="img">' + ''.join(cells) + label + '</svg>'

def array_split(a, b1, b2):
    # a x (b1+b2) split rectangle, unit=14px. The second (unknown) part is
    # labeled "?" not its value -- labeling it with b2 would hand the
    # question's answer straight to the diagram (never do that).
    u = 12
    w1, w2, h = b1*u, b2*u, a*u
    ty = h + (-6 if h > 20 else h/2)
    svg = (f'<svg viewBox="0 0 {w1+w2+4} {h+14}" width="{w1+w2+4}" height="{h+14}" role="img">'
           f'<rect x="0" y="0" width="{w1}" height="{h}" fill="var(--accent-soft)" stroke="currentColor" stroke-width="1.5"/>'
           f'<rect x="{w1+4}" y="0" width="{w2}" height="{h}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
           f'<text x="{w1/2}" y="{ty+12}" font-size="11" text-anchor="middle" fill="currentColor">{a}&times;{b1}</text>'
           f'<text x="{w1+4+w2/2}" y="{ty+12}" font-size="11" text-anchor="middle" fill="currentColor">{a}&times;?</text>'
           '</svg>')
    return svg

def bar_model(part1, part2, label=""):
    u = 18
    w1, w2 = part1*u, part2*u
    h = 36
    return (f'<svg viewBox="0 0 {w1+w2} {h}" width="{w1+w2}" height="{h}" role="img">'
            f'<rect x="0" y="0" width="{w1}" height="{h}" fill="var(--accent-soft)" stroke="currentColor" stroke-width="1.5"/>'
            f'<rect x="{w1}" y="0" width="{w2}" height="{h}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            '</svg>')

def pattern_plus(step_cells):
    # step_cells: list of (x,y) grid cells for a plus-shape, draw 3 small panels
    pass

def arrow_chain(labels):
    boxes = ''
    x = 0
    for i, lab in enumerate(labels):
        boxes += f'<rect x="{x}" y="10" width="70" height="34" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
        boxes += f'<text x="{x+35}" y="31" font-size="11" text-anchor="middle" fill="currentColor">{lab}</text>'
        if i < len(labels)-1:
            boxes += f'<line x1="{x+70}" y1="27" x2="{x+90}" y2="27" stroke="currentColor" stroke-width="2" marker-end="url(#ah)"/>'
        x += 90
    w = x - 20
    defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="currentColor"/></marker></defs>'
    return f'<svg viewBox="0 0 {w} 54" width="{w}" height="54" role="img">{defs}{boxes}</svg>'

def pct_chain(labels):
    return arrow_chain(labels)

def frac_pct_dec_diagram():
    return ('<svg viewBox="0 0 240 90" width="240" height="90" role="img">'
            '<text x="20" y="20" font-size="13" fill="currentColor">Fraction</text>'
            '<text x="170" y="20" font-size="13" fill="currentColor">Decimal</text>'
            '<text x="95" y="80" font-size="13" fill="currentColor">Percent</text>'
            '<line x1="75" y1="15" x2="160" y2="15" stroke="currentColor" stroke-width="1.5"/>'
            '<line x1="35" y1="30" x2="90" y2="65" stroke="currentColor" stroke-width="1.5"/>'
            '<line x1="190" y1="30" x2="135" y2="65" stroke="currentColor" stroke-width="1.5"/>'
            '</svg>')

def thermometer(rise_label):
    return ('<svg viewBox="0 0 70 140" width="70" height="140" role="img">'
            '<line x1="35" y1="10" x2="35" y2="110" stroke="currentColor" stroke-width="3"/>'
            '<circle cx="35" cy="118" r="10" fill="none" stroke="currentColor" stroke-width="3"/>'
            + ''.join(f'<line x1="28" y1="{18+i*12}" x2="35" y2="{18+i*12}" stroke="currentColor" stroke-width="1.5"/>' for i in range(8))
            + f'<text x="55" y="60" font-size="11" fill="currentColor">{rise_label}</text>'
            '</svg>')

def plus_pattern():
    # Classic growing-cross pattern: step k has a center cell plus an arm of
    # length (k-1) in each of the 4 directions -> 4(k-1)+1 cells (1, 5, 9, 13, ...),
    # so the picture's growth rule visually matches the "+4 each step" arithmetic
    # instead of degenerating into a solid square.
    s = 14
    radius = 2  # largest arm length drawn (step 3)
    grid = 2*radius + 1
    vb = grid * s

    def cross_cells(arm):
        cells = [(0, 0)]
        for d in range(1, arm + 1):
            cells += [(d, 0), (-d, 0), (0, d), (0, -d)]
        return cells

    def mk(arm):
        cells = cross_cells(arm)
        boxes = ''.join(
            f'<rect x="{(x+radius)*s}" y="{(y+radius)*s}" width="{s}" height="{s}" '
            f'fill="var(--accent-soft)" stroke="currentColor" stroke-width="1"/>'
            for x, y in cells)
        return f'<svg viewBox="0 0 {vb} {vb}" width="{vb}" height="{vb}">{boxes}</svg>'

    st1, st2, st3 = mk(0), mk(1), mk(2)
    return ('<div style="display:flex;gap:16px;align-items:flex-end;">'
            f'<div style="text-align:center;">{st1}<div style="font-size:0.78rem;color:var(--ink-muted);">Step 1</div></div>'
            f'<div style="text-align:center;">{st2}<div style="font-size:0.78rem;color:var(--ink-muted);">Step 2</div></div>'
            f'<div style="text-align:center;">{st3}<div style="font-size:0.78rem;color:var(--ink-muted);">Step 3</div></div>'
            '</div>')

def grouping_diagram(total, group_size):
    full_groups = total // group_size
    rem = total % group_size
    boxes = ''
    x = 0
    s = 13
    for g in range(full_groups):
        gw = group_size * s + 6
        dots = ''.join(f'<circle cx="{x+3+i*s+s/2}" y="12" cy="12" r="{s/2-2}" fill="var(--accent-ink)"/>' for i in range(group_size))
        boxes += f'<rect x="{x}" y="2" width="{gw}" height="20" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>' + dots
        x += gw + 6
    if rem:
        dots = ''.join(f'<circle cx="{x+3+i*s+s/2}" cy="12" r="{s/2-2}" fill="var(--ink-muted)"/>' for i in range(rem))
        boxes += f'<rect x="{x}" y="2" width="{rem*s+6}" height="20" fill="none" stroke="currentColor" stroke-dasharray="3,2" stroke-width="1.2" rx="3"/>' + dots
        x += rem*s+6
    return f'<svg viewBox="0 0 {x+4} 26" width="{min(x+4,560)}" height="26" role="img">{boxes}</svg>'

# ---- problem data ----
P = []
def add(n, tier, topic, q, choices, correct, key, habit_note, ref, diagram=None, needs_diagram=False):
    P.append(dict(n=n, tier=tier, topic=topic, q=q, choices=choices, correct=correct, key=key,
                   habit_note=habit_note, ref=ref, diagram=diagram, needs_diagram=needs_diagram or (diagram is not None)))

add(1, "Easy", "Tools for Measuring",
    "Which tool would be the best choice for measuring the amount of liquid in a water bottle?",
    {"A": "Ruler", "B": "Thermometer", "C": "Scale", "D": "Measuring cup"}, "D",
    "<b>Answer: D.</b> A measuring cup (or graduated cylinder) measures liquid volume. A ruler measures length, a thermometer measures temperature, and a scale measures weight/mass.",
    None, "Tier: Easy &middot; Topic: Tools for Measuring &middot; Diagram: no &middot; Never tracked before (0 graded instances) -- coverage-floor pick, no data yet to judge.")

add(2, "Medium", "Estimating Multiplication & Division",
    "A charity raised money to split evenly among its volunteers, as shown. Which is the best estimate of how much each volunteer receives?",
    {"A": "$200", "B": "$150", "C": "$175", "D": "$100"}, "A",
    "<b>Answer: A.</b> Round $7,850 to $8,000 and 39 volunteers to 40: $8,000 &divide; 40 = $200. (Exact value is about $201.28, so $200 is the best estimate -- don't compute the exact division when an estimate is asked for.)",
    "compute-both-sides / estimation-division-number-sense",
    "Tier: Medium &middot; Topic: Estimating Multiplication &amp; Division &middot; Diagram: yes &middot; Wrong so far: 2/13 &middot; Times practised before: 8 (last: set 6)",
    diagram=table(["Total raised", "Number of volunteers"], [["$7,850", "39"]]))

add(3, "Hard", "Converting to a Decimal",
    "Which decimal is equivalent to " + frac(11,16) + "?",
    {"A": "0.611", "B": "0.65", "C": "0.586", "D": "0.6875"}, "D",
    f"<b>Answer: D.</b> 11 &divide; 16 = 0.6875 (long division: 11.0000 &divide; 16). The wrong choices come from stopping the long division too early or misplacing a digit.",
    "proper-fraction-long-division",
    "Tier: Hard &middot; Topic: Converting to a Decimal &middot; Diagram: no &middot; Wrong so far: 6/34 &middot; Times practised before: 3 (last: set 6)")

add(4, "Easy", "Remainder when Divided by a given Number",
    "A florist has 53 roses to arrange into bouquets of 6 roses each. After making as many full bouquets as possible, how many roses are left over?",
    {"A": "5", "B": "6", "C": "3", "D": "2"}, "A",
    "<b>Answer: A.</b> 53 &divide; 6 = 8 full bouquets (48 roses) with 5 roses left over.",
    None, "Tier: Easy &middot; Topic: Remainder when Divided by a given Number &middot; Diagram: yes &middot; Wrong so far: 3/6 &middot; Times practised before: 4 (last: set 7)",
    diagram=grouping_diagram(53, 6))

add(5, "Medium", "Numerical Patterns",
    "A number pattern begins 2, 5, 10, 17, 26, .... What is the 6th number in the pattern?",
    {"A": "35", "B": "36", "C": "37", "D": "38"}, "C",
    "<b>Answer: C.</b> The differences between terms are 3, 5, 7, 9 -- each difference is 2 more than the last (not constant). The next difference is 11, so the 6th term is 26 + 11 = 37. Checking only the first difference (3) and assuming it stays constant is the trap here.",
    "first-order-only pattern reading",
    "Tier: Medium &middot; Topic: Numerical Patterns &middot; Diagram: no &middot; Wrong so far: 4/9 &middot; Times practised before: 6 (last: set 7)")

add(6, "Easy", "English Unit Conversions",
    "A piece of ribbon is 5 feet long. How many inches long is the ribbon?",
    {"A": "48", "B": "55", "C": "60", "D": "72"}, "C",
    "<b>Answer: C.</b> 5 feet &times; 12 inches/foot = 60 inches.",
    None, "Tier: Easy &middot; Topic: English Unit Conversions &middot; Diagram: yes &middot; Wrong so far: 0/1 &middot; Times practised before: 1 (last: set 4)",
    diagram=table(["Unit", "Equals"], [["1 foot", "12 inches"]]))

add(7, "Medium", "Predicting the Next Shapes given Progressive Pattern",
    "The figure shows a pattern growing in steps. If the pattern continues, how many small squares will be in Step 4?",
    {"A": "12", "B": "13", "C": "16", "D": "17"}, "B",
    "<b>Answer: B.</b> Each step adds 4 squares to the plus-shape: Step 1 = 1, Step 2 = 5, Step 3 = 9, so Step 4 = 9 + 4 = 13.",
    None, "Tier: Medium &middot; Topic: Predicting the Next Shapes given Progressive Pattern &middot; Diagram: yes &middot; Wrong so far: 1/5 &middot; Times practised before: 2 (last: set 5)",
    diagram=plus_pattern())

add(8, "Medium", "Identifying Number Properties",
    "Priya solves 7 &times; 13 using the expression (7 &times; 10) + (7 &times; ?). What number completes the expression?",
    {"A": "13", "B": "10", "C": "7", "D": "3"}, "D",
    "<b>Answer: D.</b> 13 = 10 + 3, so (7&times;10) + (7&times;3) = 70 + 21 = 91 = 7&times;13. This is the distributive property.",
    None, "Tier: Medium &middot; Topic: Identifying Number Properties &middot; Diagram: yes &middot; Wrong so far: 1/6 &middot; Times practised before: 2 (last: set 6)",
    diagram=array_split(7, 10, 3))

add(9, "Easy", "Finding Area/Perimeter of Rectangle, given Length & Width",
    "A rectangular garden is 14 feet long and 9 feet wide. What is the area of the garden, in square feet?",
    {"A": "126", "B": "46", "C": "23", "D": "63"}, "A",
    "<b>Answer: A.</b> Area = length &times; width = 14 &times; 9 = 126 square feet. (B is the perimeter.)",
    None, "Tier: Easy &middot; Topic: Finding Area/Perimeter of Rectangle, given Length &amp; Width &middot; Diagram: no &middot; Wrong so far: 1/10 &middot; Times practised before: 2 (last: set 5)")

add(10, "Hard", "Area and Perimeter of Complex Polygons",
    "The figure is made of a square and a triangle that share one side. The perimeter of the whole figure (the largest polygon) is 40 centimeters. The perimeter of the square alone is 28 centimeters. What is the perimeter of the triangle alone?",
    {"A": "19", "B": "33", "C": "26", "D": "12"}, "C",
    "<b>Answer: C.</b> The square's perimeter is 28, so each side is 7 cm. Three of the square's sides are on the outside of the figure (3 &times; 7 = 21 cm); the shared 4th side is internal and NOT part of the whole figure's perimeter. So the triangle's two outer sides total 40 &minus; 21 = 19 cm. The triangle's own perimeter adds back the shared side: 19 + 7 = 26 cm.",
    "check-every-condition",
    "Tier: Hard &middot; Topic: Area and Perimeter of Complex Polygons &middot; Diagram: yes &middot; Wrong so far: 6/15 &middot; Times practised before: 8 (last: set 7)",
    diagram='<svg viewBox="0 0 220 120" width="220" height="120" role="img"><rect x="20" y="20" width="80" height="80" fill="none" stroke="currentColor" stroke-width="2"/><polygon points="100,20 180,60 100,100" fill="none" stroke="currentColor" stroke-width="2"/><text x="60" y="65" font-size="12" text-anchor="middle" fill="currentColor">square</text><text x="128" y="64" font-size="12" text-anchor="middle" fill="currentColor">triangle</text></svg>')

add(11, "Medium", "Percent Increase Decrease basic",
    "A gym membership fee is increased by 20%, and then the new fee is decreased by 20%. What is the overall percent change from the original fee?",
    {"A": "No change", "B": "4% decrease", "C": "4% increase", "D": "20% decrease"}, "B",
    "<b>Answer: B.</b> Let the original fee be 100. After a 20% increase: 100 &times; 1.2 = 120. After a 20% decrease: 120 &times; 0.8 = 96. That's a net change of 100 &rarr; 96, a 4% decrease. The two 20% changes do NOT cancel out, because the second 20% is taken from a larger (then smaller) base.",
    None, "Tier: Medium &middot; Topic: Percent Increase Decrease basic &middot; Diagram: yes &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick.",
    diagram=pct_chain(["Start", "+20%", "&minus;20%"]))

add(12, "Easy", "Finding Unit Price",
    "The table shows two juice-box pack options. What is the unit price of Pack B, in dollars per juice box?",
    {"A": "$0.40", "B": "$0.45", "C": "$0.50", "D": "$0.54"}, "B",
    "<b>Answer: B.</b> Pack B: $5.40 &divide; 12 boxes = $0.45 per box. (Pack A is $4.00 &divide; 8 = $0.50 per box, so Pack B is actually the better deal, but the question only asks for Pack B's unit price.)",
    None, "Tier: Easy &middot; Topic: Finding Unit Price &middot; Diagram: yes &middot; Wrong so far: 1/4 &middot; Times practised before: 3 (last: set 4)",
    diagram=table(["", "Juice boxes", "Price"], [["Pack A", "8", "$4.00"], ["Pack B", "12", "$5.40"]]))

add(13, "Medium", "No Remainder when Divided by two given Numbers",
    "If z can be divided by both 4 and 9 without leaving a remainder, then 2z can also be divided by which number without leaving a remainder?",
    {"A": "24", "B": "16", "C": "27", "D": "20"}, "A",
    "<b>Answer: A.</b> z must be a multiple of 36 (since 4 and 9 share no common factor, the smallest number divisible by both is 4&times;9=36). So 2z is a multiple of 72. 24 divides 72 evenly (72 &divide; 24 = 3), so 24 always divides 2z. 16, 27, and 20 do not divide 72 evenly.",
    None, "Tier: Medium &middot; Topic: No Remainder when Divided by two given Numbers &middot; Diagram: no &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick.")

add(14, "Medium", "Evaluating Percents of Numbers",
    "What is 30% of 70?",
    {"A": "21", "B": "23", "C": "24", "D": "18"}, "A",
    "<b>Answer: A.</b> 30% of 70 = 0.3 &times; 70 = 21. (Deliberately a 20%/30%-type percent, not a 10%/25% shortcut percent -- this is the confirmed slower, more error-prone case.)",
    None, "Tier: Medium &middot; Topic: Evaluating Percents of Numbers &middot; Diagram: no &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick; targets the confirmed 20%/30% percent-method gap (see project_percent_calc_method).")

add(15, "Medium", "Word Problems with Ratios",
    "In a parking lot, the ratio of sedans to trucks is 5:3. If there are 48 vehicles total, how many trucks are there?",
    {"A": "30", "B": "6", "C": "18", "D": "48"}, "C",
    "<b>Answer: C.</b> 5 + 3 = 8 parts total. 48 &divide; 8 = 6 vehicles per part. Trucks = 3 parts &times; 6 = 18. (A is the number of sedans -- re-read which group the question asks for before finalizing.)",
    "ratio-partition-forgotten / exact-thing-asked",
    "Tier: Medium &middot; Topic: Word Problems with Ratios &middot; Diagram: yes &middot; Wrong so far: 3/7 &middot; Times practised before: 8 (last: set 7)",
    diagram=bar_model(5, 3))

add(16, "Easy", "Multiplying and Dividing Whole Numbers",
    "A theater has 342 seats arranged into 9 equal sections. How many seats are in each section?",
    {"A": "42", "B": "36", "C": "38", "D": "41"}, "C",
    "<b>Answer: C.</b> 342 &divide; 9 = 38.",
    None, "Tier: Easy &middot; Topic: Multiplying and Dividing Whole Numbers &middot; Diagram: no &middot; Wrong so far: 1/6 &middot; Times practised before: 3 (last: set 6)")

add(17, "Easy", "Perimeter",
    "A regular pentagon has a side length of 11 cm. What is its perimeter?",
    {"A": "44", "B": "33", "C": "66", "D": "55"}, "D",
    "<b>Answer: D.</b> A regular pentagon has 5 equal sides: 5 &times; 11 = 55 cm.",
    None, "Tier: Easy &middot; Topic: Perimeter &middot; Diagram: no &middot; Wrong so far: 0/6 &middot; Maintain priority (keep this skill fresh).")

add(18, "Easy", "Adding and Subtracting Integers",
    "At 6 a.m., the temperature was &minus;4&deg;F. By noon, it had risen 15&deg;F. What was the temperature at noon?",
    {"A": "19", "B": "11", "C": "&minus;11", "D": "&minus;19"}, "B",
    "<b>Answer: B.</b> &minus;4 + 15 = 11&deg;F.",
    None, "Tier: Easy &middot; Topic: Adding and Subtracting Integers &middot; Diagram: yes &middot; Wrong so far: 0/9 &middot; Times practised before: 1 (last: set 6)",
    diagram=thermometer("+15&deg;"))

add(19, "Medium", "Estimation (sums, products, money, ranges)",
    "Nina tracked her weekly grocery spending for four weeks, as shown. Which is the best estimate of her total spending?",
    {"A": "between $190 and $210", "B": "between $215 and $230", "C": "between $260 and $280", "D": "between $230 and $250"}, "D",
    "<b>Answer: D.</b> $62.80 + $47.15 + $71.40 + $55.90 = $237.25, which falls between $230 and $250. Don't compute the exact total when an estimate (rounded range) is asked for -- rounding each amount to the nearest $10 first (63+47+71+56 &asymp; 237) gets there faster.",
    "compute-both-sides",
    "Tier: Medium &middot; Topic: Estimation (sums, products, money, ranges) &middot; Diagram: yes &middot; Wrong so far: 4/14 &middot; Times practised before: 7 (last: set 7) &middot; Note: biggest gap by count on official tests",
    diagram=table(["Week 1", "Week 2", "Week 3", "Week 4"], [["$62.80", "$47.15", "$71.40", "$55.90"]]))

add(20, "Easy", "Identifying Numbers, Standard Form Word Form",
    "What is the standard form for four hundred sixteen thousand, seventy-two?",
    {"A": "416,072", "B": "416,720", "C": "46,072", "D": "4,160,072"}, "A",
    "<b>Answer: A.</b> Four hundred sixteen thousand = 416,000. Seventy-two = 72. Together: 416,072.",
    None, "Tier: Easy &middot; Topic: Identifying Numbers, Standard Form Word Form &middot; Diagram: no &middot; Wrong so far: 0/5 &middot; Maintain priority (keep this skill fresh).")

add(21, "Medium", "Remaining Amount after Reducing by Fractions",
    "Omar had $240 in savings. He spent " + frac(1,3) + " of it on a bike helmet, then spent " + frac(1,4) + " of what remained on a lock. How much money does Omar have left?",
    {"A": "$160", "B": "$40", "C": "$80", "D": "$120"}, "D",
    f"<b>Answer: D.</b> Helmet: {frac(1,3)} of $240 = $80, leaving $160. Lock: {frac(1,4)} of $160 = $40, leaving $160 &minus; $40 = $120.",
    None, "Tier: Medium &middot; Topic: Remaining Amount after Reducing by Fractions &middot; Diagram: yes &middot; Wrong so far: 3/7 &middot; Times practised before: 6 (last: set 7)",
    diagram=bar_model(8,16))

add(22, "Medium", "Algebra with Geometric Shapes",
    'Two equations are shown.<div style="margin-top:6px;">&#9651; + &#9651; + &#9675; = 19</div><div>&#9651; + &#9675; + &#9675; = 17</div>What is the value of &#9675;?',
    {"A": "4", "B": "5", "C": "6", "D": "7"}, "B",
    "<b>Answer: B.</b> Let &#9651;=triangle, &#9675;=circle. 2&#9651;+&#9675;=19 and &#9651;+2&#9675;=17. Doubling the first: 4&#9651;+2&#9675;=38. Subtracting the second: 3&#9651;=21, so &#9651;=7. Then &#9675;=19&minus;2(7)=5.",
    None, "Tier: Medium &middot; Topic: Algebra with Geometric Shapes &middot; Diagram: yes (symbolic) &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick.",
    needs_diagram=True)

add(23, "Easy", "Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.",
    "An arithmetic sequence begins 9, 14, 19, 24, .... What is the 15th term?",
    {"A": "74", "B": "75", "C": "79", "D": "84"}, "C",
    "<b>Answer: C.</b> Common difference = 5. 15th term = 9 + (15&minus;1)&times;5 = 9 + 70 = 79. (D=84 comes from using 15&times;5 instead of (15&minus;1)&times;5 -- an off-by-one error in the term count.)",
    None, "Tier: Easy &middot; Topic: Nth Term, given Arithmetic Sequence, Progressive Pattern, etc. &middot; Diagram: no &middot; Wrong so far: 2/9 &middot; Times practised before: 3 (last: set 7)")

add(24, "Medium", "No Remainder when Divided by a given Number",
    "Which whole number is divisible by both 4 and 5 without leaving a remainder?",
    {"A": "60", "B": "45", "C": "32", "D": "50"}, "A",
    "<b>Answer: A.</b> 60 &divide; 4 = 15 and 60 &divide; 5 = 12, both whole numbers. 45 is divisible by 5 but not 4. 32 is divisible by 4 but not 5. 50 is divisible by 5 but not 4. Only 60 satisfies BOTH conditions.",
    "check-every-condition",
    "Tier: Medium &middot; Topic: No Remainder when Divided by a given Number &middot; Diagram: yes &middot; Wrong so far: 4/11 &middot; Times practised before: 6 (last: set 7)",
    diagram=venn("multiples of 4", "multiples of 5"))

add(25, "Medium", "Multi-step unit conversion (off-by-10, multi-step)",
    "4 zips = 6 bons. 1 bon = 5 crons. How many crons equal 10 zips?",
    {"A": "60", "B": "75", "C": "90", "D": "50"}, "B",
    "<b>Answer: B.</b> 4 zips = 6 bons, so 1 zip = 1.5 bons. 10 zips = 15 bons. Each bon = 5 crons, so 15 bons = 75 crons.",
    "exact-thing-asked",
    "Tier: Medium &middot; Topic: Multi-step unit conversion (off-by-10, multi-step) &middot; Diagram: yes &middot; Wrong so far: 5/8 &middot; Times practised before: 11 (last: set 7)",
    diagram=arrow_chain(["zips", "bons", "crons"]))

add(26, "Medium", "Divisibility / number constraints (Serena/Who am I style)",
    "Felix picked a whole number greater than 60 but less than 75. The number is even and is divisible by 7. What is Felix's number?",
    {"A": "63", "B": "66", "C": "70", "D": "72"}, "C",
    "<b>Answer: C.</b> Multiples of 7 between 60 and 75: 63 and 70. 63 is odd, so it fails the 'even' condition. 70 is even and divisible by 7 -- it satisfies every condition. (66 and 72 are even and in range, but neither is divisible by 7.)",
    "check-every-condition / use-all-data",
    "Tier: Medium &middot; Topic: Divisibility / number constraints (Serena/Who am I style) &middot; Diagram: yes &middot; Wrong so far: 4/19 &middot; Times practised before: 10 (last: set 6)",
    diagram=numline(60, 75))

add(27, "Medium", "Comparing & Ordering Fractions & Decimals",
    "Which statement is true?",
    {"A": frac(5,8) + " &gt; 0.6", "B": frac(3,4) + " &lt; 0.7", "C": frac(2,5) + " &gt; 0.5", "D": frac(7,10) + " &gt; " + frac(3,4)}, "A",
    f"<b>Answer: A.</b> {frac(5,8)} = 0.625, which is greater than 0.6 -- true. {frac(3,4)} = 0.75, which is NOT less than 0.7. {frac(2,5)} = 0.4, which is NOT greater than 0.5. {frac(7,10)} = 0.7, which is NOT greater than {frac(3,4)} = 0.75.",
    "decimal-vs-nonnice-fraction / benchmark-0.5-fluency",
    "Tier: Medium &middot; Topic: Comparing &amp; Ordering Fractions &amp; Decimals &middot; Diagram: no &middot; Wrong so far: 7/18 &middot; Times practised before: 10 (last: set 7)")

add(28, "Hard", "Equivalent Fractions Decimals and Percents",
    "Which statement is true?",
    {"A": "0.6 = 6%", "B": frac(3,20) + " = 15%", "C": "0.45 = 4.5%", "D": frac(1,8) + " = 1.8%"}, "B",
    f"<b>Answer: B.</b> {frac(3,20)} = 0.15 = 15% -- true. 0.6 = 60% (not 6% -- a decimal-to-percent shift error). 0.45 = 45% (not 4.5%). {frac(1,8)} = 0.125 = 12.5% (not 1.8%). Watch the decimal point when converting between decimals and percents -- it's easy to be off by a factor of 10.",
    "key-word-watch / off-by-10",
    "Tier: Hard &middot; Topic: Equivalent Fractions Decimals and Percents &middot; Diagram: yes &middot; Wrong so far: 4/24 &middot; Times practised before: 3 (last: set 7)",
    diagram=frac_pct_dec_diagram())

add(29, "Medium", "Probability (simple, equally likely outcomes)",
    "A spinner is divided into 8 equal sections: 3 red, 2 blue, and 3 yellow. If the spinner is spun once, what is the probability it lands on blue?",
    {"A": frac(1,8), "B": frac(1,4), "C": frac(3,8), "D": frac(1,2)}, "B",
    f"<b>Answer: B.</b> 2 blue sections out of 8 total = {frac(2,8)} = {frac(1,4)}.",
    None, "Tier: Medium &middot; Topic: Probability (simple, equally likely outcomes) &middot; Diagram: no &middot; Wrong so far: 0/2 &middot; Times practised before: 2 (last: set 5)")

add(30, "Hard", "Finding Ratios given Probability",
    "A bag contains only red and green marbles. The probability of picking a red marble at random is " + frac(3,7) + ". If there are 12 red marbles, how many green marbles are in the bag?",
    {"A": "7", "B": "12", "C": "9", "D": "16"}, "D",
    f"<b>Answer: D.</b> If {frac(3,7)} of the marbles are red and there are 12 red marbles, the total is 12 &divide; {frac(3,7)} = 12 &times; {frac(7,3)} = 28 marbles. Green = 28 &minus; 12 = 16.",
    "check-every-condition",
    "Tier: Hard &middot; Topic: Finding Ratios given Probability &middot; Diagram: no &middot; Wrong so far: 2/13 &middot; Times practised before: 1 (last: set 4)")

add(31, "Hard", "Percent Word Problems",
    "A bookstore had 240 novels in stock. During a sale, 35% of the novels were sold. Of the novels that were NOT sold, " + frac(1,4) + " were paperbacks. How many of the unsold novels were paperbacks?",
    {"A": "39", "B": "84", "C": "60", "D": "21"}, "A",
    f"<b>Answer: A.</b> Sold: 35% of 240 = 84. Unsold: 240 &minus; 84 = 156. Paperbacks (unsold only): {frac(1,4)} of 156 = 39. (B=84 is the number SOLD, not the quantity asked for -- re-read which group the question is about before finalizing.)",
    "check-every-condition / exact-thing-asked",
    "Tier: Hard &middot; Topic: Percent Word Problems &middot; Diagram: yes &middot; Wrong so far: 10/31 &middot; Times practised before: 7 (last: set 7)",
    diagram=bar_model(7,13))

add(32, "Medium", "Comparing Areas",
    "The floor of Room A is a square with area 196 ft&sup2;. The floor of Room B is a rectangle that is 10 ft by 22 ft. Which room has the larger floor area, and by how much?",
    {"A": "Room A, by 24 ft&sup2;", "B": "Room A, by 44 ft&sup2;", "C": "Room B, by 24 ft&sup2;", "D": "Room B, by 44 ft&sup2;"}, "C",
    "<b>Answer: C.</b> Room B's area = 10 &times; 22 = 220 ft&sup2;. Room A's area = 196 ft&sup2; (since 14 &times; 14 = 196). 220 &minus; 196 = 24 ft&sup2; -- Room B is larger by 24 ft&sup2;.",
    None, "Tier: Medium &middot; Topic: Comparing Areas &middot; Diagram: no &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick.")

add(33, "Hard", "Fractional Parts Word Problems",
    "A choir has 60 members. " + frac(2,5) + " of the members are altos, and " + frac(1,3) + " of the remaining members are sopranos. How many members are sopranos?",
    {"A": "12", "B": "24", "C": "36", "D": "20"}, "A",
    f"<b>Answer: A.</b> Altos: {frac(2,5)} of 60 = 24. Remaining: 60 &minus; 24 = 36. Sopranos: {frac(1,3)} of 36 = 12. (B=24 is the number of ALTOS, not sopranos.)",
    "exact-thing-asked",
    "Tier: Hard &middot; Topic: Fractional Parts Word Problems &middot; Diagram: no &middot; Wrong so far: 1/7 &middot; Times practised before: 1 (last: set 5)")

add(34, "Medium", "Total Shaded Area given Figure with Equal Divisions",
    "The grid shown is divided into equal squares. What fraction of the grid, in lowest terms, is shaded?",
    {"A": frac(5,16), "B": frac(3,4), "C": frac(5,8), "D": frac(3,8)}, "C",
    f"<b>Answer: C.</b> 10 of the 16 squares are shaded: {frac(10,16)} = {frac(5,8)} in lowest terms. (D={frac(3,8)} is the UNshaded fraction -- 6 of 16 squares.)",
    "decimal-vs-nonnice-fraction",
    "Tier: Medium &middot; Topic: Total Shaded Area given Figure with Equal Divisions &middot; Diagram: yes &middot; Wrong so far: 1/6 &middot; Times practised before: 6 (last: set 7)",
    diagram=shaded_grid(4,4,10))

add(35, "Medium", "Finding Area/Perimeter of Rectangle, given Length & Width",
    "The diagram shows a rectangular patio made of square tiles, each tile 1 meter by 1 meter. What is the perimeter of the patio, in meters?",
    {"A": "24", "B": "20", "C": "10", "D": "16"}, "B",
    "<b>Answer: B.</b> The patio is 6 m by 4 m. Perimeter = 2 &times; (6 + 4) = 20 m. (A=24 is the AREA, not the perimeter.)",
    None, "Tier: Medium &middot; Topic: Finding Area/Perimeter of Rectangle, given Length &amp; Width &middot; Diagram: yes &middot; Wrong so far: 1/10 &middot; Times practised before: 2 (last: set 5)",
    diagram=tile_grid(6,4))

add(36, "Easy", "Key-word NOT in equivalence questions",
    "Which of the following is <b>NOT</b> equivalent to " + frac(3,4) + "?",
    {"A": "75%", "B": "0.75", "C": frac(6,8), "D": frac(4,3)}, "D",
    f"<b>Answer: D.</b> {frac(4,3)} is the RECIPROCAL of {frac(3,4)}, not an equivalent value (1.33 &ne; 0.75). 75%, 0.75, and {frac(6,8)} are all equal to {frac(3,4)}.",
    "key-word-watch",
    "Tier: Easy &middot; Topic: Key-word NOT in equivalence questions &middot; Diagram: no &middot; Wrong so far: 4/7 &middot; Times practised before: 6 (last: set 5) &middot; Note: 4/4 wrong on 'Which value is NOT equivalent' drill -- only NOT-style item in this set.")

add(37, "Hard", "No Remainder when Divided by a given Number",
    "A number is divisible by both 6 and 8 without a remainder. Which of the following must also divide that number without a remainder?",
    {"A": "16", "B": "9", "C": "18", "D": "12"}, "D",
    "<b>Answer: D.</b> The smallest number divisible by both 6 and 8 is their LCM, 24 -- so the number is a multiple of 24. 12 divides 24 evenly (24 &divide; 12 = 2), so 12 always divides a multiple of 24. 16, 9, and 18 do not divide 24 evenly, so they are not guaranteed to work.",
    None, "Tier: Hard &middot; Topic: No Remainder when Divided by a given Number &middot; Diagram: yes &middot; Wrong so far: 4/11 &middot; Times practised before: 6 (last: set 7)",
    diagram=venn("multiples of 6", "multiples of 8"))

add(38, "Medium", "Estimating Sums Differences of Decimal Numbers",
    "Which expression gives the best estimate of 38.7 &minus; 11.2?",
    {"A": "30 &minus; 10", "B": "40 &minus; 10", "C": "40 &minus; 20", "D": "30 &minus; 20"}, "B",
    "<b>Answer: B.</b> Rounding to the nearest ten: 38.7 rounds up to 40 (since .7 rounds up), and 11.2 rounds down to 10 (since .2 rounds down). 40 &minus; 10 is the best estimate. The other choices round at least one number the wrong direction.",
    "compute-both-sides",
    "Tier: Medium &middot; Topic: Estimating Sums Differences of Decimal Numbers &middot; Diagram: no &middot; Wrong so far: 1/11 &middot; Times practised before: 2 (last: set 6)")

assert len(P) == 38
letters = [p["correct"] for p in P]
from collections import Counter
print("letter balance:", Counter(letters))
assert not any(letters[i]==letters[i+1]==letters[i+2] for i in range(len(letters)-2)), "3 identical letters in a row"

json.dump(P, open(os.path.join(HERE, 'set8_problems.json'), 'w'), indent=1)
print("wrote set8_problems.json,", len(P), "problems")
