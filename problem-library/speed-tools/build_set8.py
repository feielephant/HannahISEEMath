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

def l_shape_outline(cols, rows, unit_label="m&sup2;"):
    # Matches the real item's actual presentation (gid163, verified against the
    # source screenshot): NOT a fully-filled grid -- only the top row (cols unit
    # cells) and left column (rows unit cells) are subdivided, with a bare outer
    # rectangle everywhere else, plus a small separate legend square. She reads
    # the two edge counts off the tick marks and multiplies -- a filled grid lets
    # her just count cells instead, which is a different and easier task.
    cw, ch = 24, 24
    w, h = cols*cw, rows*ch
    lines = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-width="2"/>']
    for c in range(1, cols):
        lines.append(f'<line x1="{c*cw}" y1="0" x2="{c*cw}" y2="{ch}" stroke="currentColor" stroke-width="1.5"/>')
    for r in range(1, rows):
        lines.append(f'<line x1="0" y1="{r*ch}" x2="{cw}" y2="{r*ch}" stroke="currentColor" stroke-width="1.5"/>')
    legend = (f'<rect x="0" y="{h+14}" width="{cw}" height="{ch}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
              f'<text x="{cw+10}" y="{h+14+ch/2+4}" font-size="13" fill="currentColor">= 1 {unit_label}</text>')
    return f'<svg viewBox="-4 -4 {w+90} {h+ch+28}" width="{w+90}" height="{h+ch+28}" role="img">' + ''.join(lines) + legend + '</svg>'

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

IMG_163_B64 = open(os.path.join(HERE, 'gid163_b64.txt')).read().strip()
img_tag = ('<img src="data:image/png;base64,' + IMG_163_B64 + '" '
           'alt="L-shaped unit grid showing a rectangle\'s length and width, with a legend square = 1 square meter" '
           'style="max-width:220px;display:block;" />')

# ---- problem data ----
P = []
def add(n, tier, topic, q, choices, correct, key, habit_note, ref, diagram=None, needs_diagram=False):
    P.append(dict(n=n, tier=tier, topic=topic, q=q, choices=choices, correct=correct, key=key,
                   habit_note=habit_note, ref=ref, diagram=diagram, needs_diagram=needs_diagram or (diagram is not None)))

add(1, "Easy", "Prime Numbers",
    "Which is the product of two prime numbers?",
    {"A": "12", "B": "13", "C": "16", "D": "14"}, "D",
    "<b>Answer: D.</b> 14 = 2 &times; 7, both prime. 12 = 2 &times; 2 &times; 3 (three prime factors, not two). 13 is itself prime, not a product. 16 = 2 &times; 2 &times; 2 &times; 2 (four prime factors).",
    None, "Tier: Easy &middot; Topic: Prime Numbers &middot; Diagram: no &middot; Real, unused not_done library item (global_id 1103), used verbatim. Swapped 2026-10-26 for 'Tools for Measuring' -- that topic had zero real examples in either library, and the invented version (identify which tool measures liquid) was pure vocabulary recall with no actual reasoning in it, not a good use of a coverage-floor slot. This item at least requires checking each choice's prime factorization.")

add(2, "Medium", "Estimating Multiplication & Division",
    "A charity raised $7,850 to split evenly among 39 volunteers. Which is the best estimate of how much each volunteer receives?",
    {"A": "$200", "B": "$150", "C": "$175", "D": "$100"}, "A",
    "<b>Answer: A.</b> Round $7,850 to $8,000 and 39 volunteers to 40: $8,000 &divide; 40 = $200. (Exact value is about $201.28, so $200 is the best estimate -- don't compute the exact division when an estimate is asked for.)",
    "compute-both-sides / estimation-division-number-sense",
    "Tier: Medium &middot; Topic: Estimating Multiplication &amp; Division &middot; Diagram: no &middot; Wrong so far: 2/13 &middot; Times practised before: 8 (last: set 6) &middot; Fixed 2026-10-26: the real model items (gid21/27) are plain text, no table/image -- dropped the invented table and folded the numbers into the question.")

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
    None, "Tier: Easy &middot; Topic: Remainder when Divided by a given Number &middot; Diagram: no &middot; Wrong so far: 3/6 &middot; Times practised before: 4 (last: set 7) &middot; Fixed 2026-10-26: no real example of this topic (in either library) uses a diagram -- dropped the invented grouping graphic.")

add(5, "Medium", "Numerical Patterns",
    "A number pattern begins 2, 5, 10, 17, 26, .... What is the 7th number in the pattern?",
    {"A": "44", "B": "48", "C": "50", "D": "53"}, "C",
    "<b>Answer: C.</b> The differences between terms are 3, 5, 7, 9 -- each difference is 2 more than the last (not constant), so the next two differences are 11 and 13: 6th term = 26 + 11 = 37, 7th term = 37 + 13 = 50. (A=44 comes from wrongly reusing the LAST given difference, 9, for both remaining steps -- 26+9+9=44 -- instead of letting the differences keep growing by 2.)",
    "first-order-only pattern reading",
    "Tier: Medium &middot; Topic: Numerical Patterns &middot; Diagram: no &middot; Wrong so far: 4/9 &middot; Times practised before: 6 (last: set 7) &middot; Extended to the 7th term 2026-10-26 (one extra extrapolation step past the 5 given terms) at the user's request.")

add(6, "Easy", "English Unit Conversions",
    "Mia cut three lengths of ribbon. Ribbon 1 measured 2 yards, 2 feet, 4 inches. Ribbon 2 measured 4 yards, 1 inch. Ribbon 3 measured 1 yard, 7 feet, 2 inches. Which statement is true? (1 yard = 3 feet; 1 foot = 12 inches)",
    {"A": "Ribbon 1 is longer than Ribbon 3.", "B": "Ribbon 3 is longer than Ribbon 2.",
     "C": "Ribbon 2 is longer than Ribbon 1.", "D": "Ribbon 1 and Ribbon 3 are the same length."}, "C",
    "<b>Answer: C.</b> Convert each to inches. Ribbon 1: 2 yd = 72 in, + 2 ft (24 in) + 4 in = 100 in. "
    "Ribbon 2: 4 yd = 144 in, + 1 in = 145 in. Ribbon 3: 7 ft = 84 in = 2 yd 1 ft, so 1 yd + 7 ft = 3 yd 1 ft; "
    "total = 108 in + 12 in + 2 in = 122 in. So Ribbon 1 = 100 in, Ribbon 3 = 122 in, Ribbon 2 = 145 in. "
    "Ribbon 2 (145) is longer than Ribbon 1 (100) -- true. The other three statements are all false once everything is converted to the same unit.",
    None, "Tier: Easy &middot; Topic: English Unit Conversions &middot; Diagram: no &middot; Wrong so far: 0/1 &middot; Times practised before: 1 (last: set 4) &middot; Upgraded 2026-10-26 from a single-step multiply -- a real official item for this exact topic (3-way mixed-unit comparison) was available and unused; too easy to waste one of her only 2 data points on this topic.")

add(7, "Medium", "Predicting the Next Shapes given Progressive Pattern",
    "The figure shows a pattern growing in steps. If the pattern continues, how many small squares will be in Step 4?",
    {"A": "12", "B": "13", "C": "16", "D": "17"}, "B",
    "<b>Answer: B.</b> Each step adds 4 squares to the plus-shape: Step 1 = 1, Step 2 = 5, Step 3 = 9, so Step 4 = 9 + 4 = 13.",
    None, "Tier: Medium &middot; Topic: Predicting the Next Shapes given Progressive Pattern &middot; Diagram: yes &middot; Wrong so far: 1/5 &middot; Times practised before: 2 (last: set 5)",
    diagram=plus_pattern())

add(8, "Medium", "Identifying Number Properties",
    "Which expression is equivalent to 12 &times; (15 + 8)?",
    {"A": "(12 &times; 15) + 8", "B": "(15 &times; 8) + 12", "C": "(12 + 15) + (12 + 8)", "D": "(12 &times; 15) + (12 &times; 8)"}, "D",
    "<b>Answer: D.</b> Distribute the 12 into BOTH terms: 12 &times; (15 + 8) = (12&times;15) + (12&times;8). (A distributes into only the first term and leaves the second term bare -- this is her exact real-test error, ISEE Lower #2 Q26: 'Which expression is equivalent to 16 &times; (13 + 19)?', she picked (16&times;13)+19 instead of (16&times;13)+(16&times;19).)",
    None, "Tier: Medium &middot; Topic: Identifying Number Properties &middot; Diagram: no &middot; Wrong so far: 1/6 (tracker figure; a fuller history check found 4 generated-set instances all right plus a real-test miss on ISEE Lower #2, not yet reconciled into this count) &middot; Times practised before: 2 (last: set 6) &middot; Swapped 2026-10-26 to the harder real-test format (identify the fully-expanded equivalent expression, no fill-in-blank scaffold) after a full history check found she's 4/4 on the EASIER fill-in-blank version across 4 practice sets but has never been retested on this exact harder format since missing it for real on 9/13 -- the two formats test a meaningfully different level of independence (supplying one missing piece vs. remembering to distribute into both terms unprompted).")

add(9, "Easy", "Finding Area/Perimeter of Rectangle, given Length & Width",
    "The perimeter of the rectangle shown is 78 cm. What is the area of the rectangle?",
    {"A": "380 cm&sup2;", "B": "760 cm&sup2;", "C": "741 cm&sup2;", "D": "399 cm&sup2;"}, "A",
    "<b>Answer: A.</b> Step 1: find the missing side. Perimeter = 2(19 + width) = 78, so 19 + width = 39, width = 20. Step 2: area = 19 &times; 20 = 380 cm&sup2;. (B=760 skips the final halving step -- it uses 78&minus;38=40 as the side directly instead of 40&divide;2=20. C=741 skips subtracting the given side -- it uses half the perimeter, 39, as the other side directly. D=399 is a computed-side slip, 19&times;21 instead of 19&times;20.)",
    None, "Tier: Easy &middot; Topic: Finding Area/Perimeter of Rectangle, given Length &amp; Width &middot; Diagram: yes &middot; Wrong so far: 1/10 &middot; Times practised before: 2 (last: set 5) &middot; Real official item (gid367/gid431, both DONE -- she answered this exact scenario, 8cm/24cm, on a real test, so used fresh (and, at the user's request, bigger) numbers per the done-item rule, not verbatim). Her real answer was circled correctly both times.",
    diagram='<svg viewBox="-10 0 150 70" width="150" height="70" role="img"><rect x="10" y="10" width="120" height="40" fill="none" stroke="currentColor" stroke-width="2"/><text x="70" y="7" font-size="11" text-anchor="middle" fill="currentColor">19 cm</text></svg>')

add(10, "Hard", "Area and Perimeter of Complex Polygons",
    "The figure is composed of a rectangle and a triangle. The side lengths are measured in feet (ft). What is the perimeter of the figure?",
    {"A": "30 ft", "B": "34 ft", "C": "40 ft", "D": "44 ft"}, "C",
    "<b>Answer: C.</b> The dashed 4 ft segment is the triangle's base, shared with the rectangle's bottom edge -- it's internal, not part of the outer perimeter. The rectangle's full bottom width is 3 + 4 + 3 = 10 ft, which equals its top edge too (also unlabeled but equal, since it's a rectangle). Add up only the OUTER edges: top (10) + left side (4) + right side (4) + the two exposed 3 ft bottom segments (3 + 3 = 6) + the two triangle slant sides (8 + 8 = 16) = 10 + 4 + 4 + 6 + 16 = 40 ft.",
    "check-every-condition",
    "Tier: Hard &middot; Topic: Area and Perimeter of Complex Polygons &middot; Diagram: yes &middot; Wrong so far: 6/15 &middot; Times practised before: 8 (last: set 7) &middot; Real, unused library item (global_id 736, verified directly against the source screenshot). Redesigned 2026-10-26: the first draft was a near-exact repeat of set 7 #3 (same square+triangle shared-perimeter scenario, same diagram, only the numbers changed -- this scenario had also already recurred across QR4/QR5). A second draft invented a fresh rectangle+triangle AREA problem, but a real official item for this exact topic (gid736, also rectangle+triangle) was sitting unused in the library -- swapped to that instead of inventing, per the done/not-done rule.",
    diagram='<svg viewBox="0 0 110 130" width="110" height="130" role="img"><rect x="0" y="0" width="100" height="40" fill="none" stroke="currentColor" stroke-width="2"/><line x1="30" y1="40" x2="70" y2="40" stroke="currentColor" stroke-width="2" stroke-dasharray="4,3"/><line x1="30" y1="40" x2="50" y2="120" stroke="currentColor" stroke-width="2"/><line x1="70" y1="40" x2="50" y2="120" stroke="currentColor" stroke-width="2"/><text x="-9" y="22" font-size="10" text-anchor="middle" fill="currentColor">4 ft</text><text x="109" y="22" font-size="10" text-anchor="middle" fill="currentColor">4 ft</text><text x="50" y="35" font-size="10" text-anchor="middle" fill="currentColor">4 ft</text><text x="16" y="48" font-size="10" text-anchor="middle" fill="currentColor">3 ft</text><text x="84" y="48" font-size="10" text-anchor="middle" fill="currentColor">3 ft</text><text x="32" y="82" font-size="10" text-anchor="middle" fill="currentColor">8 ft</text><text x="68" y="82" font-size="10" text-anchor="middle" fill="currentColor">8 ft</text></svg>')

add(11, "Medium", "Percent Increase Decrease basic",
    "A gym membership fee is increased by 20%, and then the new fee is decreased by 20%. What is the overall percent change from the original fee?",
    {"A": "No change", "B": "4% decrease", "C": "4% increase", "D": "20% decrease"}, "B",
    "<b>Answer: B.</b> Let the original fee be 100. After a 20% increase: 100 &times; 1.2 = 120. After a 20% decrease: 120 &times; 0.8 = 96. That's a net change of 100 &rarr; 96, a 4% decrease. The two 20% changes do NOT cancel out, because the second 20% is taken from a larger (then smaller) base.",
    None, "Tier: Medium &middot; Topic: Percent Increase Decrease basic &middot; Diagram: no &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick. Fixed 2026-10-26: real model items (gid198/711) are plain text, no diagram.")

add(12, "Easy", "Finding Unit Price",
    "Pack A has 8 juice boxes for $4.00. Pack B has 12 juice boxes for $5.40. What is the unit price of Pack B, in dollars per juice box?",
    {"A": "$0.40", "B": "$0.45", "C": "$0.50", "D": "$0.54"}, "B",
    "<b>Answer: B.</b> Pack B: $5.40 &divide; 12 boxes = $0.45 per box. (Pack A is $4.00 &divide; 8 = $0.50 per box, so Pack B is actually the better deal, but the question only asks for Pack B's unit price.)",
    None, "Tier: Easy &middot; Topic: Finding Unit Price &middot; Diagram: no &middot; Wrong so far: 1/4 &middot; Times practised before: 3 (last: set 4) &middot; Fixed 2026-10-26: real model item (gid230) is plain text, no table -- folded the pack data into the question.")

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
    "Tier: Medium &middot; Topic: Word Problems with Ratios &middot; Diagram: no &middot; Wrong so far: 3/7 &middot; Times practised before: 8 (last: set 7) &middot; Fixed 2026-10-26: real model items (gid28/88) are plain text, no diagram.")

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
    None, "Tier: Easy &middot; Topic: Adding and Subtracting Integers &middot; Diagram: no &middot; Wrong so far: 0/9 &middot; Times practised before: 1 (last: set 6) &middot; Fixed 2026-10-26: no real example anywhere used a diagram for this topic; dropped the invented thermometer graphic.")

add(19, "Medium", "Estimation (sums, products, money, ranges)",
    "Nina tracked her weekly grocery spending for four weeks: $62.80, $47.15, $71.40, and $55.90. Which is the best estimate of her total spending?",
    {"A": "between $190 and $210", "B": "between $215 and $230", "C": "between $260 and $280", "D": "between $230 and $250"}, "D",
    "<b>Answer: D.</b> $62.80 + $47.15 + $71.40 + $55.90 = $237.25, which falls between $230 and $250. Don't compute the exact total when an estimate (rounded range) is asked for -- rounding each amount to the nearest $10 first (63+47+71+56 &asymp; 237) gets there faster.",
    "compute-both-sides",
    "Tier: Medium &middot; Topic: Estimation (sums, products, money, ranges) &middot; Diagram: no &middot; Wrong so far: 4/14 &middot; Times practised before: 7 (last: set 7) &middot; Note: biggest gap by count on official tests. Fixed 2026-10-26: real model item (gid774) lists the amounts in plain text, no table.")

add(20, "Easy", "Identifying Numbers, Standard Form Word Form",
    "What is the standard form for four hundred sixteen thousand, seventy-two?",
    {"A": "416,072", "B": "416,720", "C": "46,072", "D": "4,160,072"}, "A",
    "<b>Answer: A.</b> Four hundred sixteen thousand = 416,000. Seventy-two = 72. Together: 416,072.",
    None, "Tier: Easy &middot; Topic: Identifying Numbers, Standard Form Word Form &middot; Diagram: no &middot; Wrong so far: 0/5 &middot; Maintain priority (keep this skill fresh).")

add(21, "Medium", "Remaining Amount after Reducing by Fractions",
    "Omar had $240 in savings. He spent " + frac(1,3) + " of it on a bike helmet, then spent " + frac(1,4) + " of what remained on a lock. How much money does Omar have left?",
    {"A": "$160", "B": "$40", "C": "$80", "D": "$120"}, "D",
    f"<b>Answer: D.</b> Helmet: {frac(1,3)} of $240 = $80, leaving $160. Lock: {frac(1,4)} of $160 = $40, leaving $160 &minus; $40 = $120.",
    None, "Tier: Medium &middot; Topic: Remaining Amount after Reducing by Fractions &middot; Diagram: no &middot; Wrong so far: 3/7 &middot; Times practised before: 6 (last: set 7) &middot; Fixed 2026-10-26: real model item (gid849) is explicitly text-only, no figure.")

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
    "Tier: Medium &middot; Topic: No Remainder when Divided by a given Number &middot; Diagram: no &middot; Wrong so far: 4/11 &middot; Times practised before: 6 (last: set 7) &middot; Fixed 2026-10-26: real model item (gid58) is plain text, no diagram.")

add(25, "Medium", "Multi-step unit conversion (off-by-10, multi-step)",
    '<div>4 zips = 6 bons.</div><div>1 bon = 5 crons.</div>How many crons equal 10 zips?',
    {"A": "60", "B": "75", "C": "90", "D": "50"}, "B",
    "<b>Answer: B.</b> 4 zips = 6 bons, so 1 zip = 1.5 bons. 10 zips = 15 bons. Each bon = 5 crons, so 15 bons = 75 crons.",
    "exact-thing-asked",
    "Tier: Medium &middot; Topic: Multi-step unit conversion (off-by-10, multi-step) &middot; Diagram: no &middot; Wrong so far: 5/8 &middot; Times practised before: 11 (last: set 7) &middot; Fixed 2026-10-26: real model item (gid861) has no figure -- just the two given equations on their own lines above the question (matches this exact convention now instead of the invented arrow-chain graphic).")

add(26, "Medium", "Divisibility / number constraints (Serena/Who am I style)",
    "Felix picked a whole number greater than 60 but less than 75. The number is even and is divisible by 7. What is Felix's number?",
    {"A": "63", "B": "66", "C": "70", "D": "72"}, "C",
    "<b>Answer: C.</b> Multiples of 7 between 60 and 75: 63 and 70. 63 is odd, so it fails the 'even' condition. 70 is even and divisible by 7 -- it satisfies every condition. (66 and 72 are even and in range, but neither is divisible by 7.)",
    "check-every-condition / use-all-data",
    "Tier: Medium &middot; Topic: Divisibility / number constraints (Serena/Who am I style) &middot; Diagram: no &middot; Wrong so far: 4/19 &middot; Times practised before: 10 (last: set 6) &middot; Fixed 2026-10-26: real model item (gid130) has no diagram.")

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
    "Tier: Hard &middot; Topic: Equivalent Fractions Decimals and Percents &middot; Diagram: no &middot; Wrong so far: 4/24 &middot; Times practised before: 3 (last: set 7) &middot; Fixed 2026-10-26: real model items (gid45/50) are plain text, no diagram.")

add(29, "Medium", "Probability (simple, equally likely outcomes)",
    "A spinner is divided into 8 equal sections: 3 red, 2 blue, and 3 yellow. If the spinner is spun once, what is the probability it lands on blue?",
    {"A": frac(1,8), "B": frac(1,4), "C": frac(3,8), "D": frac(1,2)}, "B",
    f"<b>Answer: B.</b> 2 blue sections out of 8 total = {frac(2,8)} = {frac(1,4)}.",
    None, "Tier: Medium &middot; Topic: Probability (simple, equally likely outcomes) &middot; Diagram: no &middot; Wrong so far: 0/2 &middot; Times practised before: 2 (last: set 5)")

add(30, "Hard", "Cryptarithm / digit substitution",
    "P and Q are different digits from 1 through 9.<div>PQQ &minus; PQ = 570</div>What digit does P represent?",
    {"A": "3", "B": "4", "C": "9", "D": "6"}, "D",
    "<b>Answer: D.</b> PQQ = 100P + 11Q, and PQ = 10P + Q, so PQQ &minus; PQ = 90P + 10Q = 570, which means 9P + Q = 57. Testing valid digits: P=6 gives Q=3 (both valid, 1-9, distinct) -- this is the only solution that works. Checking the actual subtraction: 633 &minus; 63 = 570, and the tens column needs a borrow (3 &minus; 6), which is exactly the step she's shown she doesn't reliably reach for on her own.",
    "exact-thing-asked / no-bounding-strategy",
    "Tier: Hard &middot; Topic: Cryptarithm / digit substitution &middot; Diagram: no &middot; Wrong so far: 4/5 (80%) &middot; Swapped in 2026-10-26, replacing Finding Ratios given Probability -- this topic was confirmed wrong 4/5 on QR7 (10/25) and flagged by check_priority_staleness.py at the start of this build, but was left out of QR8's original plan because its priority was never actually escalated before planning. No real unused not_done SUBTRACTION cryptarithm exists in the library (the only unused real item, gid184, is an ADDITION cryptarithm testing carrying, not the confirmed borrow/regroup gap) -- this one is invented, same algebraic shape as QR7's real #4 (gid157, MNN-MM=745) but with different letters/subtrahend structure (PQQ-PQ, distinct letters throughout) and a fresh target, specifically requiring the same borrow step.")

add(31, "Hard", "Percent Word Problems",
    "A bookstore had 240 novels in stock. During a sale, 35% of the novels were sold. Of the novels that were NOT sold, " + frac(1,4) + " were paperbacks. How many of the unsold novels were paperbacks?",
    {"A": "39", "B": "84", "C": "60", "D": "21"}, "A",
    f"<b>Answer: A.</b> Sold: 35% of 240 = 84. Unsold: 240 &minus; 84 = 156. Paperbacks (unsold only): {frac(1,4)} of 156 = 39. (B=84 is the number SOLD, not the quantity asked for -- re-read which group the question is about before finalizing.)",
    "check-every-condition / exact-thing-asked",
    "Tier: Hard &middot; Topic: Percent Word Problems &middot; Diagram: no &middot; Wrong so far: 10/31 &middot; Times practised before: 7 (last: set 7) &middot; Fixed 2026-10-26: real Percent Word Problems items in the library are plain text, no diagram; dropped the decorative bar.")

add(32, "Medium", "Comparing Areas",
    "The floor of Room A is a square with area 196 ft&sup2;. The floor of Room B is a rectangle that is 10 ft by 22 ft. Which room has the larger floor area, and by how much?",
    {"A": "Room A, by 24 ft&sup2;", "B": "Room A, by 44 ft&sup2;", "C": "Room B, by 24 ft&sup2;", "D": "Room B, by 44 ft&sup2;"}, "C",
    "<b>Answer: C.</b> Room B's area = 10 &times; 22 = 220 ft&sup2;. Room A's area = 196 ft&sup2; (since 14 &times; 14 = 196). 220 &minus; 196 = 24 ft&sup2; -- Room B is larger by 24 ft&sup2;.",
    None, "Tier: Medium &middot; Topic: Comparing Areas &middot; Diagram: no &middot; Never tracked before (0 graded instances) &middot; Coverage-floor pick.")

add(33, "Hard", "Solving Problems with Geometric Formulas",
    "If the volume of a cylinder is 72&pi; in&sup3;, which is equivalent to the radius of the cylinder if the height is 8? (V = hr&sup2;&pi;, where V = volume, h = height, r = radius.)",
    {"A": "3", "B": "2", "C": "4", "D": "5"}, "A",
    "<b>Answer: A.</b> 72&pi; = 8 &times; r&sup2; &times; &pi;, so 72 = 8r&sup2;, r&sup2; = 9, r = 3.",
    None, "Tier: Hard &middot; Topic: Solving Problems with Geometric Formulas &middot; Diagram: no &middot; Wrong so far: 4/8 (50%) &middot; Real, unused not_done library item (global_id 751), used verbatim per the done/not-done rule. Swapped in 2026-10-26, replacing Fractional Parts Word Problems -- same root cause as #30's swap: confirmed wrong 4/8 (2 wrong on QR7 alone, 10/25) and flagged by check_priority_staleness.py at the start of this build, but left out of QR8's original plan because priority was never actually escalated before planning. QR7 used cone (gid791) and prism (gid797) items for this topic; this is a cylinder, for format variety.")

add(34, "Medium", "Total Shaded Area given Figure with Equal Divisions",
    "Each section of the triangle shown is the same size. The area of the shaded region is 24 in&sup2;. What is the area of the whole triangle?",
    {"A": "12 in&sup2;", "B": "20 in&sup2;", "C": "36 in&sup2;", "D": "48 in&sup2;"}, "C",
    "<b>Answer: C.</b> The triangle is split into 3 equal sections, and 2 of the 3 are shaded. If 2 equal sections = 24 in&sup2;, then 1 section = 12 in&sup2;, and the whole triangle (3 sections) = 36 in&sup2;.",
    "decimal-vs-nonnice-fraction",
    "Tier: Medium &middot; Topic: Total Shaded Area given Figure with Equal Divisions &middot; Diagram: yes &middot; Wrong so far: 1/6 &middot; Times practised before: 6 (last: set 7) &middot; Real, unused library item (global_id 1198) -- swapped in for an invented grid after a fuller not_done sweep turned up 15 unused real items for this exact topic.",
    diagram='<svg viewBox="0 0 120 100" width="120" height="100" role="img"><polygon points="60,10 10,90 60,63" fill="var(--accent-soft)" stroke="currentColor" stroke-width="1.5"/><polygon points="10,90 110,90 60,63" fill="var(--accent-soft)" stroke="currentColor" stroke-width="1.5"/><polygon points="110,90 60,10 60,63" fill="var(--surface)" stroke="currentColor" stroke-width="1.5"/></svg>')

add(35, "Medium", "Finding Area/Perimeter of Rectangle, given Length & Width",
    "The model represents the length and width of a rectangular patio.<br>What is the area, in meters&sup2;, of this patio? (A = l &times; w)",
    {"A": "13 m&sup2;", "B": "42 m&sup2;", "C": "26 m&sup2;", "D": "64 m&sup2;"}, "B",
    "<b>Answer: B.</b> Counting the tick marks: the top edge shows 7 unit squares (length = 7 m), the left edge shows 6 unit squares (width = 6 m). Area = 7 &times; 6 = 42 m&sup2;. (A=13 adds the two sides instead of multiplying. C=26 computes the PERIMETER, 2&times;(7+6), instead of the area. D=64 is an unrelated distractor.)",
    None, "Tier: Medium &middot; Topic: Finding Area/Perimeter of Rectangle, given Length &amp; Width &middot; Diagram: yes &middot; Wrong so far: 1/10 &middot; Times practised before: 2 (last: set 5) &middot; Real official item (global_id 163, ISEE Lower #4 Q4, DONE). Fixed 2026-10-26 (2nd pass): at the user's explicit request, the original real diagram is cropped directly from the source screenshot and embedded as-is, rather than hand-recreated as an SVG -- a hand-built recreation kept introducing subtle errors (first a fully-filled grid, this fixes that risk entirely by using the real image). Since the diagram itself is now the verbatim original, the numbers (7/6/42) are the real item's own numbers too, not fresh ones -- an explicit, deliberate exception to the usual done-item fresh-numbers rule for this one slot. Choices are the real item's own four values (13/26/42/64), just reordered so the correct one lands at the required letter B.",
    diagram=img_tag)

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
    None, "Tier: Hard &middot; Topic: No Remainder when Divided by a given Number &middot; Diagram: no &middot; Wrong so far: 4/11 &middot; Times practised before: 6 (last: set 7) &middot; Fixed 2026-10-26: real model item (gid58-family) is plain text, no diagram.")

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
