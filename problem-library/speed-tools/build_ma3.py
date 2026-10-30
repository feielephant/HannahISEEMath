import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def img_from_b64(name, alt):
    b64 = open(os.path.join(HERE, f'{name}_b64.txt')).read().strip()
    return f'<img src="data:image/png;base64,{b64}" alt="{alt}" style="max-width:260px;display:block;" />'

def frac(n, d):
    return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data"><tr>{th}</tr>{trs}</table>'

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

def fraction_bar_stack(denoms):
    # one full-width bar per denominator, divided into that many equal cells
    w, bh, gap = 220, 20, 8
    out = []
    y = 0
    for d in denoms:
        cw = w / d
        out.append(f'<g transform="translate(0,{y})">')
        out.append(f'<rect x="0" y="0" width="{w}" height="{bh}" fill="none" stroke="currentColor" stroke-width="1.5"/>')
        for i in range(1, d):
            out.append(f'<line x1="{i*cw}" y1="0" x2="{i*cw}" y2="{bh}" stroke="currentColor" stroke-width="1" opacity="0.6"/>')
        out.append(f'<text x="{w+8}" y="{bh-5}" font-size="11" fill="currentColor">1/{d} each</text>')
        out.append('</g>')
        y += bh + gap
    return f'<svg viewBox="0 0 300 {y}" width="300" height="{y}" role="img">' + ''.join(out) + '</svg>'

def grid_shaded(cols, rows, start, shaded):
    cw, ch = 26, 24
    cells = []
    n = start
    for r in range(rows):
        for c in range(cols):
            fill = 'var(--accent-soft)' if n in shaded else 'var(--surface)'
            cells.append(f'<rect x="{c*cw}" y="{r*ch}" width="{cw}" height="{ch}" fill="{fill}" stroke="currentColor" stroke-width="1"/>')
            cells.append(f'<text x="{c*cw+cw/2}" y="{r*ch+ch/2+4}" font-size="10" text-anchor="middle" fill="currentColor">{n}</text>')
            n += 1
    w, h = cols*cw, rows*ch
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">' + ''.join(cells) + '</svg>'

def two_cubes(sideA, sideB):
    sA, sB = sideA*9, sideB*9
    def cube(s, label, x0):
        d = s * 0.35
        return (f'<g transform="translate({x0},{0})">'
                f'<polygon points="{d},0 {s+d},0 {s},{d} {0},{d}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
                f'<polygon points="{s},{d} {s+d},0 {s+d},{s} {s},{s+d}" fill="var(--accent-soft)" stroke="currentColor" stroke-width="1.5"/>'
                f'<rect x="0" y="{d}" width="{s}" height="{s}" fill="var(--surface)" stroke="currentColor" stroke-width="1.5"/>'
                f'<text x="{s/2}" y="{s+d+16}" font-size="12" text-anchor="middle" fill="currentColor">{label} (side {sideA if label=="A" else sideB})</text>'
                '</g>')
    maxh = max(sA, sB) * 1.35 + 20
    return (f'<svg viewBox="0 0 {sA+sB+80} {maxh}" width="{sA+sB+80}" height="{maxh}" role="img">'
            + cube(sA, 'A', 0) + cube(sB, 'B', sA + 50) + '</svg>')

def pyramid_net():
    # central square base with a triangle attached outward on each of its 4
    # sides -- the classic star/pinwheel net for a square pyramid.
    sq = (40, 40, 100, 100)  # x0,y0,x1,y1
    x0, y0, x1, y1 = sq
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    tris = [
        f'<polygon points="{x0},{y0} {x1},{y0} {cx},10" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>',   # top
        f'<polygon points="{x0},{y1} {x1},{y1} {cx},170" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>',  # bottom
        f'<polygon points="{x0},{y0} {x0},{y1} 10,{cy}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>',   # left
        f'<polygon points="{x1},{y0} {x1},{y1} 170,{cy}" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>',  # right
    ]
    return (f'<svg viewBox="0 0 180 180" width="180" height="180" role="img">'
            + ''.join(tris)
            + f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="var(--surface)" stroke="currentColor" stroke-width="1.5"/>'
            + '</svg>')

def cylinder_net():
    return ('<svg viewBox="0 0 140 150" width="140" height="150" role="img">'
            '<ellipse cx="50" cy="20" rx="30" ry="12" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="20" y="30" width="60" height="90" fill="var(--surface)" stroke="currentColor" stroke-width="1.5"/>'
            '<ellipse cx="50" cy="130" rx="30" ry="12" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            '</svg>')

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

def io_table_machine(rows):
    return table(["Input", "Output"], rows)

P = []
def add(n, tier, topic, q, choices, correct, key, habit_note, ref, diagram=None):
    key = key.replace('<<<ANSWERPREFIX>>>', f'<b>Answer: {correct}.</b> ')
    P.append(dict(n=n, tier=tier, topic=topic, q=q, choices=choices, correct=correct, key=key,
                   habit_note=habit_note, ref=ref, diagram=diagram, needs_diagram=diagram is not None))

add(1, "Hard", "Cryptarithm / digit substitution",
    "R and S are different digits from 1 through 9. What digit does S represent?",
    {"A": "6", "B": "8", "C": "3", "D": "9"}, "B",
    "<<<ANSWERPREFIX>>>RSS = 100R + 11S, and RS = 10R + S, so RSS &minus; RS = 90R + 10S = 260. Testing valid digits: R=2 gives S=8 (both valid, 1-9, distinct) -- this is the only combination that works. Check: 288 &minus; 28 = 260, and every column subtracts cleanly with NO borrowing needed (8&minus;2=6 in the tens place).",
    "exact-thing-asked / no-bounding-strategy",
    "Tier: Hard &middot; Topic: Cryptarithm / digit substitution &middot; Diagram: yes &middot; INVENTED -- both known real cryptarithm items in the library are already spent (global_id 157, used in QR7 #4; global_id 184, used in QR3 #34 with different letters/target digit -- confirmed via a direct grep of every published worksheet, not just used_real_gids.json, which was missing that QR3 usage). Same RSS&minus;RS algebraic shape as QR8 #30's PQQ&minus;PQ puzzle, but target 260 (not 650) is chosen so NO borrow/regroup step is needed -- at the user's request, replacing the earlier borrow-requiring version of this same slot, to isolate the digit-testing/bounding method on its own rather than combine it with the borrow mechanic.",
    diagram='<div style="font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',\'Courier New\',monospace;letter-spacing:2px;max-width:140px;margin:0 auto;font-size:1.1em;"><div style="padding:2px 6px;line-height:1.5;text-align:right;">RSS</div><div style="padding:2px 6px;line-height:1.5;text-align:right;">&minus;RS</div><div style="padding:2px 6px;line-height:1.5;text-align:right;border-top:1.5px solid currentColor;margin-top:5px;padding-top:5px;">260</div></div>')

add(2, "Easy", "Algebraic Equations with Symbol Variables",
    "Marti wrote two equations.<br>f &divide; g = 8<br>8 &times; 7 = f<br>What is the value of g?",
    {"A": "6", "B": "7", "C": "8", "D": "9"}, "B",
    "<<<ANSWERPREFIX>>>From the second equation, f = 8 &times; 7 = 56. Substitute into the first equation: 56 &divide; g = 8, so g = 56 &divide; 8 = 7.",
    None,
    "Tier: Easy &middot; Topic: Algebraic Equations with Symbol Variables &middot; Diagram: no &middot; Real official item (MA library, done/seen on ISEE Lower #2 Q7, answered correctly), used verbatim -- a simpler, 2-step chained-equation warmup for the same symbolic-equation skill family as #4's Algebra with Geometric Shapes.")

add(3, "Medium", "Evaluating Percents of Numbers",
    "A grocery store originally sells a pear for $3.70. The price of a pear decreased by 16%. What is the cost of a pear now, rounded to the nearest cent?",
    {"A": "$3.01", "B": "$3.11", "C": "$3.21", "D": "$3.31"}, "B",
    "<<<ANSWERPREFIX>>>16% of $3.70 = 0.16 &times; 3.70 = $0.592. New price: $3.70 &minus; $0.592 = $3.108, which rounds to $3.11.",
    None,
    "Tier: Medium &middot; Topic: Evaluating Percents of Numbers &middot; Diagram: no &middot; Real, unused library item (global_id 1108), used verbatim -- same &quot;price decreased by X%&quot; language/structure as QR8 #14 (the confirmed language gap), fresh numbers, never shown to her before.")

add(4, "Medium", "Algebra with Geometric Shapes",
    "Two equations are shown.<br>&#9633; + &#9633; + &#9671; = 23<br>&#9633; + &#9671; + &#9671; = 19<br>What is the value of &#9671;?",
    {"A": "5", "B": "9", "C": "14", "D": "4"}, "A",
    "<<<ANSWERPREFIX>>>Let &#9633;=x and &#9671;=y. 2x+y=23 and x+2y=19. Double the first equation: 4x+2y=46. Subtract the second equation: 3x=27, so x=9. Then y=23&minus;2(9)=5. (9 is the value of &#9633;, not &#9671; -- the exact-thing-asked trap. 14 is x+y, and 4 is x&minus;y -- neither is what's asked.)",
    "no-solve-method-for-symbolic-equations",
    "Tier: Medium &middot; Topic: Algebra with Geometric Shapes &middot; Diagram: no &middot; INVENTED, swapped 2026-10-30 after a difficulty-check comparison against the real historical error (QR8 #22: 2&#9651;+&#9675;=19, &#9651;+2&#9675;=17) found the earlier pick (gid123) too easy -- gid123's two equations each have only ONE unknown term that can be isolated directly (&#9633;+&#9633;+&#9633;=12 solves &#9633; alone), so it never required the elimination technique. None of the 5 real library items for this topic (gid75/121/123/177/195) are true simultaneous systems where BOTH unknowns appear in BOTH equations -- all were checked and are either single-unknown-per-equation or expression-building tasks. This is a fresh invented pair, same 2&#9633;+&#9671;=N / &#9633;+2&#9671;=M shape and elimination method as QR8 #22, different symbols (&#9633;/&#9671; instead of &#9651;/&#9675;) and numbers.")

add(5, "Medium", "Comparing Areas",
    "The floor of Room A is in the shape of a square and has an area of 121 feet&sup2;. The floor of Room B is in the shape of a rectangle and has a length of 7 feet and width of 15 feet. Which statement correctly compares the floors in the two rooms?",
    {"A": "The area of the floor in Room A is the same as the area of the floor in Room B.",
     "B": "The area of the floor in Room A is less than the area of the floor in Room B.",
     "C": "The perimeter of the floor in Room A is less than the perimeter of the floor in Room B.",
     "D": "The perimeter of the floor in Room A is equal to the perimeter of the floor in Room B."}, "D",
    "<<<ANSWERPREFIX>>>Room A is a square with area 121 ft&sup2;, so its side length is 11 ft and its perimeter is 4 &times; 11 = 44 ft. Room B's area is 7 &times; 15 = 105 ft&sup2; (not equal to 121, so the two area-comparison choices are both false). Room B's perimeter is 2(7+15) = 44 ft -- the SAME as Room A's perimeter, even though the areas are different. You have to compute both area AND perimeter for both rooms before you can tell which comparison is true.",
    "compute-both-sides",
    "Tier: Medium &middot; Topic: Comparing Areas &middot; Diagram: no &middot; Real item (global_id 117, ISEE Lower #2) -- CONFIRMED WRONG on the real test (she picked C). All 3 real library items for this topic (gid107/117/188) have already been shown to her at least once (redo-set-5/6, predating the current QR/MA pipeline) -- this is gid117's scenario again, but with a 3rd, never-before-used pair of numbers (121/7/15, not the original 144/9/15 or redo-set-6's 100/6/14) so the specific values are still fresh even though the setup is familiar. Same compute-both-sides trap as QR8 #32's invented Room A/B version.")

add(6, "Medium", "Comparing & Ordering Fractions & Decimals",
    "This list of numbers is in order from least to greatest. A fraction is missing in the list.<br>" + frac(1,4) + ", 0.3, ___, " + frac(2,3) + "<br>Which fraction goes in the blank?",
    {"A": frac(1,5), "B": frac(1,2), "C": frac(5,6), "D": frac(3,4)}, "B",
    f"<<<ANSWERPREFIX>>>Use process of elimination. {frac(1,5)} is less than {frac(1,4)}, so it can't go after 0.3 in the list. {frac(1,2)} is between 0.3 and {frac(2,3)} (0.5 is between 0.3 and about 0.667), so it fits. {frac(5,6)} and {frac(3,4)} are both greater than {frac(2,3)}, so they can't go before it.",
    None,
    "Tier: Medium &middot; Topic: Comparing &amp; Ordering Fractions &amp; Decimals &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #3 Q18), used verbatim, answered correctly. Swapped 2026-10-30 from gid139 -- gid139's real presentation came with a fraction-bar diagram (extra scaffolding the real historical error, gid674, didn't have) and friendlier denominators (3,4,5,6 vs. 1/7,1/8,1/9-style ones). This item preserves the same multi-item ordering complexity (the confirmed order-3-plus gap) but mixes a DECIMAL into the list and asks her to find a missing value by elimination rather than just sort 4 given ones, with no diagram.")

add(7, "Easy", "Finding Unit Price",
    "If 6 apples cost $9, what is the cost of 8 apples at the same rate?",
    {"A": "$11", "B": "$12", "C": "$14", "D": "$16"}, "B",
    "<<<ANSWERPREFIX>>>Unit price: $9 &divide; 6 apples = $1.50 per apple. 8 apples &times; $1.50 = $12.",
    None,
    "Tier: Easy &middot; Topic: Finding Unit Price &middot; Diagram: no &middot; Real, unused library item (global_id 259) -- CONFIRMED WRONG (she circled $11, inconsistent with her own correct scratch work of $3 per 2 apples). Cross-topic real item: catalogued under &quot;unit price scaling&quot; rather than a literal &quot;Finding Unit Price&quot; tag (no item in the library carries that exact tag), but it is the identical find-the-per-unit-rate-then-scale mechanic.")

add(8, "Hard", "English Unit Conversions",
    "Jeff is practicing his long jumps for the track team. His first jump measured 3 yards, 1 foot, 2 inches. His second jump measured 2 yards, 3 feet, 3 inches. His final jump measured 3 yards, 15 inches. Which statement about these jumps is true? (1 yard = 3 feet; 1 foot = 12 inches)",
    {"A": "Jeff jumped further in his first jump than in his second.", "B": "Jeff jumped further in his second jump than in his first.",
     "C": "Jeff jumped the same distance in his first and final jumps.", "D": "Jeff jumped the same distance in his second and final jumps."}, "A",
    "<<<ANSWERPREFIX>>>Simplify each jump first. Jump 1: 3 yd, 1 ft, 2 in (already simplified). Jump 2: 3 ft = 1 yd, so this is 3 yd, 3 in. Jump 3: 12 in = 1 ft, so this is 3 yd, 1 ft, 3 in. Ordering: Jump 2 (3 yd, 3 in) &lt; Jump 1 (3 yd, 1 ft, 2 in) &lt; Jump 3 (3 yd, 1 ft, 3 in). So Jeff jumped further in his first jump than in his second.",
    None,
    "Tier: Hard &middot; Topic: English Unit Conversions &middot; Diagram: no &middot; Real, unused library item (global_id 144, ISEE Lower #3), used verbatim, answered correctly. Swapped in 2026-10-30, replacing the earlier single-step version (gid90) -- a difficulty-check comparison against the real historical error (QR8 #6, a 3-way mixed-unit comparison) found gid90 much easier. This item is the same 3-way mixed-unit comparison shape, but a different cover story (long jumps, not ribbons) and different numbers than QR8 #6's own version, so it isn't a repeat.")

add(9, "Hard", "Percent Word Problems",
    "A parking lot is " + frac(3,5) + " full. Of the cars in the parking lot, 20% of them are blue. If the parking lot has 100 total parking spots, how many blue cars are in the parking lot?",
    {"A": "12", "B": "18", "C": "20", "D": "60"}, "A",
    f"<<<ANSWERPREFIX>>>Cars in the lot: {frac(3,5)} of 100 = 60. Blue cars: 20% of 60 = 0.2 &times; 60 = 12. (20 is 20% of the full 100 spots, not 20% of the 60 actual cars -- using the wrong base.)",
    "exact-thing-asked / which-base",
    "Tier: Hard &middot; Topic: Percent Word Problems &middot; Diagram: no &middot; Real, unused library item (global_id 710), used verbatim, answered correctly -- a genuine 2-step fraction-then-percent problem (fraction of a whole, then percent of THAT amount, not the original total).")

add(10, "Hard", "Converting to a Decimal",
    "Which decimal is equivalent to " + frac(17,20) + "?",
    {"A": "0.17", "B": "0.68", "C": "0.8", "D": "0.85"}, "D",
    f"<<<ANSWERPREFIX>>>{frac(17,20)} &times; {frac(5,5)} = {frac(85,100)} = 0.85. (Or: 17 &divide; 20 = 0.85 by long division.)",
    None,
    "Tier: Hard &middot; Topic: Converting to a Decimal &middot; Diagram: no &middot; Real, unused library item (global_id 647), used verbatim, answered correctly.")

add(11, "Hard", "Numerical Patterns",
    "Use the number pattern to answer the question.<br>2&nbsp; 3&nbsp; 5&nbsp; 9&nbsp; 17&nbsp; ___<br>What is the next number in the pattern?",
    {"A": "21", "B": "27", "C": "30", "D": "33"}, "D",
    "<<<ANSWERPREFIX>>>Find the differences between consecutive numbers: 3&minus;2=1, 5&minus;3=2, 9&minus;5=4, 17&minus;9=8. The differences themselves are DOUBLING each time (1, 2, 4, 8), so the next difference is 16. 17 + 16 = 33.",
    None,
    "Tier: Hard &middot; Topic: Numerical Patterns &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #1 Q21), used verbatim -- CONFIRMED WRONG on the real test (she picked 27). Swapped in 2026-10-30, replacing gid125's simpler missing-multiple-of-6 grid -- a difficulty-check comparison against the real historical error (QR8 #5, a growing-difference pattern) found gid125 much easier and over-scaffolded with a diagram. This item is an even harder growing-difference pattern (differences DOUBLE, not just increase by a constant), with no diagram, matching the real confirmed gap directly.")

add(12, "Medium", "Multi-step unit conversion (off-by-10, multi-step)",
    "4,000 milliliters is equal to how many kiloliters?",
    {"A": "0.004 kiloliters", "B": "0.04 kiloliters", "C": "40,000 kiloliters", "D": "4,000,000 kiloliters"}, "A",
    "<<<ANSWERPREFIX>>>1 kiloliter = 1,000,000 milliliters (1 kL = 1,000 L, and 1 L = 1,000 mL). So 4,000 mL &divide; 1,000,000 = 0.004 kL. This is a two-step metric jump (mL &rarr; L &rarr; kL), which is exactly where a factor-of-10 slip creeps in.",
    "off-by-10 (metric prefix jump)",
    "Tier: Medium &middot; Topic: Multi-step unit conversion (off-by-10, multi-step) &middot; Diagram: no &middot; Real, unused library item (global_id 203) -- CONFIRMED WRONG, and confirmed off by exactly a factor of 10 (she circled 0.04 instead of 0.004) -- a direct, real hit on this exact named gap.")

add(13, "Hard", "Solving Problems with Geometric Formulas",
    "If the volume of a rectangular prism is 72 in&sup3;, which equation can be used to determine the height of the prism if the length is 6? (V = lwh, where V = volume, l = length, w = width, and h = height.)",
    {"A": frac(12,'w'), "B": frac(12,'h'), "C": frac(72,'(6h)'), "D": "72w"}, "A",
    "<<<ANSWERPREFIX>>>V = lwh, so 72 = 6 &times; w &times; h, which means w &times; h = 12. Solving for h: h = 12/w.",
    None,
    "Tier: Hard &middot; Topic: Solving Problems with Geometric Formulas &middot; Diagram: no &middot; Real, unused library item (global_id 748), used verbatim -- same rearrange-the-volume-formula skill as QR8 #1, different given variable (length instead of height) so it's not a repeat.")

add(14, "Medium", "Classification of Numbers, given a Set",
    "Two numbers are greater than 1. One is a prime number and the other is an odd number. What will always describe the product of the two numbers?",
    {"A": "odd number", "B": "even number", "C": "prime number", "D": "composite number"}, "D",
    "<<<ANSWERPREFIX>>>A prime number has exactly two factors (1 and itself). Multiplying it by another number greater than 1 always creates a number with MORE than two factors -- which makes it composite, no matter which prime or odd number you pick. Example: prime 2 &times; odd 5 = 10 (composite). Example: prime 5 &times; odd 7 = 35 (odd AND composite) -- the only thing true in both examples is &quot;composite.&quot;",
    "always-true reasoning (test with 2 examples, keep only what matches both)",
    "Tier: Medium &middot; Topic: Classification of Numbers, given a Set &middot; Diagram: no &middot; Real official item (ISEE Lower #2 Q29), used verbatim -- the user's own pick, direct from Screenshot 2026-10-06 at 10.37.09 AM.png. CONFIRMED WRONG on the real test (she picked A, odd number) -- a genuine &quot;always true&quot; logic gap, replacing Vertices Forming Right Angles Quadrilaterals (only 2 graded instances, both correct, weak evidence either way).")

add(15, "Medium", "Word Problems with Ratios",
    "Justin had some coins in a bag. He counted 38 coins that were silver and 27 coins that were copper. What fraction of the coins that Justin had were silver?",
    {"A": frac(27,38), "B": frac(38,27), "C": frac(27,65), "D": frac(38,65)}, "D",
    f"<<<ANSWERPREFIX>>>The part is the silver coins (38); the whole is ALL the coins (38 + 27 = 65). Fraction silver = {frac(38,65)}. (Using 27 as the denominator or numerator instead of the 65 total gives a part-to-part ratio instead of part-to-whole.)",
    "part-to-whole vs part-to-part",
    "Tier: Medium &middot; Topic: Word Problems with Ratios &middot; Diagram: no &middot; Real, unused library item (global_id 140, ISEE Lower #3), used verbatim, answered correctly.")

add(16, "Easy", "Nth Term, Arithmetic Sequence (merged)",
    "Use the pattern to help answer the question: 1+3=2&sup2;, 1+3+5=3&sup2;, 1+3+5+7=4&sup2;. What is the solution to 1+3+5+7+9+11+13+15?",
    {"A": "5&sup2;", "B": "8&sup2;", "C": "12&sup2;", "D": "13&sup2;"}, "B",
    "<<<ANSWERPREFIX>>>Each time you add one more odd number, the base number on the right goes up by 1. Continuing: 1+3+5+7+9=5&sup2;, +11=6&sup2;, +13=7&sup2;, +15=8&sup2;. So the full sum 1+3+5+7+9+11+13+15 = 8&sup2;.",
    None,
    "Tier: Easy &middot; Topic: Nth Term, Arithmetic Sequence (merged) &middot; Diagram: no &middot; Real, unused library item (global_id 16, &quot;What to Expect&quot; set), used verbatim, answered correctly -- a different pattern-recognition flavor (sum of consecutive odds = perfect square) than the usual find-a-missing-term format, for variety within this merged topic.")

add(17, "Hard", "Measurement Scaling",
    "Two cubes are shown. Cube A has sides of length 2 units and Cube B has sides of length 4 units. How many Cube A's can fit inside of Cube B?",
    {"A": "4", "B": "8", "C": "12", "D": "16"}, "B",
    "<<<ANSWERPREFIX>>>Volume of Cube A = 2&times;2&times;2 = 8 cubic units. Volume of Cube B = 4&times;4&times;4 = 64 cubic units. 64 &divide; 8 = 8 Cube A's fit inside Cube B. (Doubling the side length multiplies the VOLUME by 2&sup3;=8, not by 2 -- a very common trap, which is why 4 is also offered as a choice.)",
    "linear-vs-volume scaling",
    "Tier: Hard &middot; Topic: Measurement Scaling &middot; Diagram: yes &middot; Real, unused library item (global_id 66, ISEE Lower #1), used verbatim, answered correctly.",
    diagram=two_cubes(2, 4))

add(18, "Hard", "Counting Multiples within a Range",
    "How many numbers between 67 and 85 are divisible by 4?",
    {"A": "2", "B": "3", "C": "5", "D": "7"}, "C",
    "<<<ANSWERPREFIX>>>Multiples of 4 between 67 and 85: 68, 72, 76, 80, 84 -- that's 5 numbers.",
    "check-every-condition / use-all-data",
    "Tier: Hard &middot; Topic: Counting Multiples within a Range &middot; Diagram: no &middot; Real, unused library item (global_id 725), used verbatim -- source screenshot had no visible answer marker, so the correct letter (C) was independently verified by direct computation.")

add(19, "Hard", "No Remainder when Divided by a given Number",
    "Which whole number is divisible by 7?",
    {"A": "202", "B": "204", "C": "217", "D": "219"}, "C",
    "<<<ANSWERPREFIX>>>217 &divide; 7 = 31, a whole number. 202 &divide; 7 &asymp; 28.9, 204 &divide; 7 &asymp; 29.1, 219 &divide; 7 &asymp; 31.3 -- none are whole numbers. Like 31, 7 has no quick digit-sum shortcut, so this has to be checked by actual division.",
    "no-bounding-strategy",
    "Tier: Hard &middot; Topic: No Remainder when Divided by a given Number &middot; Diagram: no &middot; Real, unused library item (global_id 893), used verbatim. Swapped in 2026-10-30, replacing gid174's divisible-by-6 version -- a difficulty-check comparison against the real historical error (QR8 #37, divisor 31, &quot;no easy digit-sum shortcut&quot;) found gid174 easier, since 6 has quick divisibility rules (even + digit-sum-by-3). Divisor 7 restores that same no-shortcut property without reusing 31 itself (gid892, already used in QR8 #37).")

add(20, "Hard", "Finding Area/Perimeter of Rectangle, given Length & Width",
    "The perimeter of a square is 24 centimeters. If a rectangle with a width of 3 centimeters has the same area as the square, what is the length of the rectangle in centimeters?",
    {"A": "6", "B": "8", "C": "9", "D": "12"}, "D",
    "<<<ANSWERPREFIX>>>If the square's perimeter is 24 cm, its side length is 24 &divide; 4 = 6 cm. Its area is 6 &times; 6 = 36 cm&sup2;. For the rectangle to have the same area (36 cm&sup2;) with a width of 3 cm, its length must be 36 &divide; 3 = 12 cm.",
    "multi-step geometric formula chaining",
    "Tier: Hard &middot; Topic: Finding Area/Perimeter of Rectangle, given Length &amp; Width &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #1 Q30) -- CONFIRMED WRONG on the real test (she picked B, 8). Swapped in 2026-10-30, replacing gid103's Y=1/4&times;length item -- a difficulty-check comparison found gid103 didn't actually require computing an area or perimeter at all, despite the topic tag. This one genuinely chains perimeter&rarr;side&rarr;area&rarr;length, matching QR8 #9's real historical mechanic (and is harder than it, requiring 3 steps instead of 2).")

add(21, "Medium", "Input Output Tables",
    "The number machine performs the same operation on each input number to create an output number, as shown in the table. What input gives an output of 12?",
    {"A": "21", "B": "23", "C": "25", "D": "27"}, "B",
    "<<<ANSWERPREFIX>>>Use the given pairs to find the rule: 19&rarr;10, 13&rarr;7, 9&rarr;5, 5&rarr;3, 3&rarr;2 -- each output is (input+1)&divide;2. Working backward from an output of 12: 12 = (input+1)&divide;2, so input+1 = 24, and input = 23.",
    None,
    "Tier: Medium &middot; Topic: Input Output Tables &middot; Diagram: yes &middot; Real, unused library item (global_id 492), used verbatim, answered correctly. Swapped in 2026-10-30, replacing the ISEE Lower #2 Q6 version (find a missing OUTPUT) -- this one asks for the INPUT given an output, the reverse direction, which requires inverting the rule rather than just applying it forward. The two confirmed-wrong real items found for this topic (ISEE Lower #1 Q5, and gid609's non-linear rule) are both already used multiple times in pre-pipeline redo-sets.",
    diagram=io_table_machine([["19","10"],["13","7"],["9","5"],["5","3"],["3","2"]]))

add(22, "Medium", "Order of Operations and Equivalence",
    "Which expression is equal to (2 + 8) &times; 7?",
    {"A": "2 + 8 &times; 7", "B": "2 &times; 7 + 8", "C": "2 &times; 8 + 8 &times; 7", "D": "2 &times; 7 + 8 &times; 7"}, "D",
    "<<<ANSWERPREFIX>>>By the distributive property, a(b+c) = ab + ac, so (2+8)&times;7 = 2&times;7 + 8&times;7. (Check directly: (2+8)&times;7 = 10&times;7 = 70, and only this expression also equals 70.)",
    None,
    "Tier: Medium &middot; Topic: Order of Operations and Equivalence &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #3 Q29), used verbatim, answered correctly -- a distributive-property-equivalence item, different shape than QR8 #8's plain simplify-both-groups version.")

add(23, "Medium", "Remainder when Divided by a given Number",
    "When 183 is divided by a number, the remainder is 3. Which of the following could be the number?",
    {"A": "3", "B": "7", "C": "8", "D": "9"}, "D",
    "<<<ANSWERPREFIX>>>If the remainder is 3, the divisor must evenly divide 183&minus;3=180, and the divisor must be GREATER than the remainder (3). 180&divide;9=20 exactly, and 9&gt;3, so 9 works. 180&divide;7 and 180&divide;8 don't come out even, and the divisor can't be equal to the remainder itself (3) -- a remainder of 3 is only possible when dividing by something bigger than 3.",
    "no-bounding-strategy",
    "Tier: Medium &middot; Topic: Remainder when Divided by a given Number &middot; Diagram: no &middot; Real, unused library item (global_id 505), used verbatim, answered correctly. Swapped 2026-10-30 (2nd pass) from the plain &quot;which expression leaves remainder 5&quot; version -- this reverses the task (given the dividend AND remainder, find a possible DIVISOR), a genuine inverse-reasoning upgrade. Still doesn't replicate QR6 #33's full money/chart complexity (confirmed: no word-problem-framed remainder item, and no &quot;opposite face&quot; item for #27, exist anywhere in the library after a full-text search) -- but this is meaningfully harder than the version it replaces.")

add(24, "Medium", "Numerical Patterns",
    "The 2nd number in a pattern is 19, the 3rd number is 31, and the 4th number is 43. What is the 1st number in the pattern?",
    {"A": "7", "B": "12", "C": "55", "D": "31"}, "A",
    "<<<ANSWERPREFIX>>>The common difference is 12 (31&minus;19=12, 43&minus;31=12). Working backward: 1st number = 19 &minus; 12 = 7. (12 is the DIFFERENCE, not the 1st term -- the same off-by-one-direction trap as QR7 #35. 55 extends the pattern FORWARD instead of backward, which isn't what's asked.)",
    "working-backward-to-an-earlier-term",
    "Tier: Medium &middot; Topic: Numerical Patterns &middot; Diagram: no &middot; INVENTED, replacing Area and Perimeter of Complex Polygons at the user's request -- same algebraic shape as the real item behind QR7 #35 and QR8 #7 (global_id 44, ISEE Lower #1 Q6: &quot;2nd=11, 3rd=19, 4th=27, find the 1st&quot;), with fresh numbers and a fresh difference (12 instead of 8/9) since gid44 itself has already been used twice. This &quot;anchor from a later term, count backward&quot; framing is the one technique that's worked for her on this trap so far (see QR8 skill-gap notes).")

add(25, "Medium", "Remaining Amount after Reducing by Fractions",
    "Lois had 4 pencils and 6 pens. She lost " + frac(1,2) + " of her pencils and " + frac(1,3) + " of her pens. How many pencils and pens does she have remaining, combined?",
    {"A": "3", "B": "5", "C": "6", "D": "9"}, "C",
    f"<<<ANSWERPREFIX>>>Pencils remaining: lost {frac(1,2)} of 4 = 2, so 4 &minus; 2 = 2 left. Pens remaining: lost {frac(1,3)} of 6 = 2, so 6 &minus; 2 = 4 left. Combined: 2 + 4 = 6.",
    None,
    "Tier: Medium &middot; Topic: Remaining Amount after Reducing by Fractions &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #1 Q25) -- CONFIRMED WRONG on the real test (she picked B, 5) -- two different fractions applied to two different starting amounts in one problem, more demanding than a single-fraction version.")

add(26, "Hard", "Translating Math Expressions",
    "Which expression represents &quot;9 times n decreased by 16&quot;?",
    {"A": "9n &minus; 16", "B": "16 &minus; 9n", "C": "9(n &minus; 16)", "D": "n(16 &minus; 9)"}, "A",
    "<<<ANSWERPREFIX>>>&quot;9 times n&quot; is 9n. &quot;Decreased by 16&quot; means subtract 16 AFTER that -- so 9n &minus; 16, not 16 &minus; 9n (which would be &quot;16 decreased by 9n,&quot; the terms in the wrong order).",
    "key-word-watch (order of subtraction)",
    "Tier: Hard &middot; Topic: Translating Math Expressions &middot; Diagram: no &middot; Real, unused library item (global_id 55, ISEE Lower #1), used verbatim, answered correctly. Swapped in 2026-10-30, replacing gid106's expression&rarr;phrase version -- a difficulty-check comparison against the real historical error (QR5 #28, build a 2-unknown equation from a word problem) found gid106 was the easier direction (describe an already-given expression). This one is phrase&rarr;expression, the harder direction that's actually closer to what building an equation from words requires.")

add(27, "Hard", "3D shape from its net (unfolding a solid)",
    "A cube has three colored circles drawn on it (shown below). Which diagram could be folded to make this cube, if the colored circles are on the outside of the cube and cannot be seen from the other side?",
    {"A": img_from_b64('gid151_choice_A', 'Net choice A: diamond net with yellow circle center, blue circle lower-left, orange circle to the right'),
     "B": img_from_b64('gid151_choice_B', 'Net choice B: diamond net with orange circle upper, yellow circle center, blue circle lower-left'),
     "C": img_from_b64('gid151_choice_C', 'Net choice C: diamond net with blue circle left, orange circle center, yellow circle far right'),
     "D": img_from_b64('gid151_choice_D', 'Net choice D: diamond net with yellow circle upper-left, blue circle below it, orange circle center-right')}, "A",
    "<<<ANSWERPREFIX>>>On the cube, going around from the yellow (top) face: blue (front) is adjacent to yellow, and orange (right) is adjacent to both. The correct net keeps that same adjacency when unfolded -- look for the diagram where yellow sits in the middle with blue directly to its lower-left and orange directly to its right, the same relative arrangement as on the cube. The other three diagrams swap or shift the circles into positions that don't fold back into the cube shown.",
    "spatial-reasoning (tracking face adjacency through a fold)",
    "Tier: Hard &middot; Topic: 3D shape from its net (unfolding a solid) &middot; Diagram: yes &middot; Real item (global_id 151, ISEE Lower #3 Q32), answered correctly -- only 60.5% of test-takers got this right, genuinely harder than the topic's other real items (simple name-the-shape questions). Swapped in 2026-10-30 (3rd pass) at the user's request, replacing gid516's pyramid-net version. The real question's answer choices are themselves 4 different net diagrams (not text), and the net is drawn as a skewed diamond/rhombus strip rather than this project's usual plain-square net style -- hand-recreating that risked a subtle transcription error (the exact bug class flagged in feedback_diagram_authenticity.md), so the cube reference and all 4 choice diagrams are cropped directly from the source screenshot and embedded verbatim, the same fix already used for QR8 #35's rectangle diagram.",
    diagram=img_from_b64('gid151_cube', 'A cube with a yellow circle on top, a blue circle on the front face, and an orange circle on the right face'))

add(28, "Medium", "Estimating Multiplication & Division",
    "Alika is buying 23 shirts that cost $18.99 each. Which expression can be used to find the best estimate of how much it will cost Alika to buy the shirts?",
    {"A": "20 + 20", "B": "30 + 20", "C": "20 &times; 20", "D": "30 &times; 20"}, "C",
    "<<<ANSWERPREFIX>>>Round each number to the nearest ten: 23 rounds to 20, and $18.99 rounds to $20. Since this is a total COST for many items, you multiply (not add): 20 &times; 20.",
    None,
    "Tier: Medium &middot; Topic: Estimating Multiplication &amp; Division &middot; Diagram: no &middot; Real, unused library item (global_id 85, ISEE Lower #2), used verbatim, answered correctly.")

add(29, "Medium", "Dividing Equally From a Total",
    "Manny has a total of 228 eggs. Using these eggs, he will fill empty egg cartons that each hold 12 eggs. What is the greatest number of egg cartons that Manny can fill completely?",
    {"A": "18", "B": "19", "C": "240", "D": "2,736"}, "B",
    "<<<ANSWERPREFIX>>>228 &divide; 12 = 19 full cartons exactly.",
    None,
    "Tier: Medium &middot; Topic: Dividing Equally From a Total &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #3 Q14), used verbatim, answered correctly.")

add(30, "Hard", "Minimum Distance on Coordinate Plane / Grid",
    "Katrina is walking from point X to point Z. If she can only move left, right, up, and down (not diagonally), what is the shortest distance she can travel to get from point X to point Z?",
    {"A": "7 grid units", "B": "10 grid units", "C": "14 grid units", "D": "16 grid units"}, "C",
    "<<<ANSWERPREFIX>>>Moving only along grid lines (taxicab distance), the shortest path is the horizontal distance plus the vertical distance: from X(3, &minus;4) to Z(&minus;3, 4), that's |3&minus;(&minus;3)| + |4&minus;(&minus;4)| = 6 + 8 = 14 grid units. (Point Y isn't part of this question -- it's just another labeled point on the same grid.)",
    "use-all-data (ignoring an irrelevant labeled point) / exact-thing-asked",
    "Tier: Hard &middot; Topic: Minimum Distance on Coordinate Plane / Grid &middot; Diagram: yes &middot; Real, unused library item (global_id 406, Elevate Prep &quot;Coordinate Geometry Practice Set 2&quot;), used verbatim, answered correctly. New topic 2026-10-30, replacing Determining Averages/Points on Number Lines at the user's request -- that topic is the one most recently confirmed solid (5 straight correct after the tag-fragmentation merge earlier this session), so the safest slot to free up for new, never-tracked content. Picked over the simpler gid394 (2 points only, no distractor) for the extra &quot;which 2 of the 3 labeled points actually matter&quot; layer. Point positions verified directly against the source photo (IMG_20260823_093839.jpg) rather than the transcription alone -- the real page has handwritten pencil marks scribbled across the grid, so the diagram here is a clean redraw with the same coordinates, not a crop.",
    diagram=coordplane(-5, 5, -5, 5, [(3, -4, "X"), (-3, 4, "Z"), (4, 2, "Y")]))

assert len(P) == 30, len(P)
json.dump(P, open(os.path.join(HERE, 'ma3_problems.json'), 'w'), indent=1)
print("wrote ma3_problems.json,", len(P), "problems")
