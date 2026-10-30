import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

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

def cylinder_net():
    return ('<svg viewBox="0 0 140 150" width="140" height="150" role="img">'
            '<ellipse cx="50" cy="20" rx="30" ry="12" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="20" y="30" width="60" height="90" fill="var(--surface)" stroke="currentColor" stroke-width="1.5"/>'
            '<ellipse cx="50" cy="130" rx="30" ry="12" fill="var(--surface-alt)" stroke="currentColor" stroke-width="1.5"/>'
            '</svg>')

def io_table_machine(rows):
    return table(["Input", "Output"], rows)

P = []
def add(n, tier, topic, q, choices, correct, key, habit_note, ref, diagram=None):
    key = key.replace('<<<ANSWERPREFIX>>>', f'<b>Answer: {correct}.</b> ')
    P.append(dict(n=n, tier=tier, topic=topic, q=q, choices=choices, correct=correct, key=key,
                   habit_note=habit_note, ref=ref, diagram=diagram, needs_diagram=diagram is not None))

add(1, "Hard", "Cryptarithm / digit substitution",
    "R and S are different digits from 1 through 9.<br>RSS<br>&minus; RS<br>650<br>What digit does S represent?",
    {"A": "2", "B": "5", "C": "7", "D": "9"}, "A",
    "<<<ANSWERPREFIX>>>RSS = 100R + 11S, and RS = 10R + S, so RSS &minus; RS = 90R + 10S = 650. Testing valid digits: R=7 gives S=2 (both valid, 1-9, distinct) -- this is the only combination that works. Check: 722 &minus; 72 = 650. (7 is the value of R, not S -- the exact-thing-asked trap.)",
    "exact-thing-asked / no-bounding-strategy",
    "Tier: Hard &middot; Topic: Cryptarithm / digit substitution &middot; Diagram: yes &middot; INVENTED -- both known real cryptarithm items in the library are already spent (global_id 157, used in QR7 #4; global_id 184, used in QR3 #34 with different letters/target digit -- confirmed via a direct grep of every published worksheet, not just used_real_gids.json, which was missing that QR3 usage). Same borrow/regroup algebraic shape as QR8 #30's PQQ&minus;PQ puzzle (fresh letters and target so it isn't a repeat of that one either), reinforcing the same digit-testing-with-a-bound method.",
    diagram='<div style="font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',\'Courier New\',monospace;letter-spacing:2px;max-width:140px;margin:0 auto;font-size:1.1em;"><div style="padding:2px 6px;line-height:1.5;text-align:right;">RSS</div><div style="padding:2px 6px;line-height:1.5;text-align:right;">&minus;RS</div><div style="padding:2px 6px;line-height:1.5;text-align:right;border-top:1.5px solid currentColor;margin-top:5px;padding-top:5px;">650</div></div>')

add(2, "Easy", "Algebraic Equations with Symbol Variables",
    "Marti wrote two equations: f &divide; g = 8, and 8 &times; 7 = f. What is the value of g?",
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
    "If &#9633; + &#9633; + &#9633; = 12, and &#9633; &times; &#9675; = 20 are both true, what is the value of &#9675; &minus; &#9633;?",
    {"A": "1", "B": "5", "C": "8", "D": "9"}, "A",
    "<<<ANSWERPREFIX>>>From the first equation, &#9633; + &#9633; + &#9633; = 12, so &#9633; = 4. Substitute into the second equation: 4 &times; &#9675; = 20, so &#9675; = 5. Then &#9675; &minus; &#9633; = 5 &minus; 4 = 1.",
    "no-solve-method-for-symbolic-equations",
    "Tier: Medium &middot; Topic: Algebra with Geometric Shapes &middot; Diagram: no &middot; Real, unused library item (global_id 123, ISEE Lower #3, answered correctly), used verbatim -- exact same 2-equation/2-symbol structure as QR8 #22 (&quot;she has no idea how to solve this&quot;), per the direct request to pull more real items of this exact shape. Solve-one-equation-first-then-substitute is the missing procedure to teach alongside this.")

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
    "A group of fraction bars is shown. Which list shows the fractions " + frac(2,3) + ", " + frac(3,4) + ", " + frac(3,6) + ", " + frac(2,5) + " in order from least to greatest?",
    {"A": frac(2,3)+", "+frac(3,4)+", "+frac(2,5)+", "+frac(3,6), "B": frac(2,5)+", "+frac(3,6)+", "+frac(2,3)+", "+frac(3,4),
     "C": frac(2,5)+", "+frac(2,3)+", "+frac(3,6)+", "+frac(3,4), "D": frac(3,4)+", "+frac(2,3)+", "+frac(3,6)+", "+frac(2,5)}, "B",
    f"<<<ANSWERPREFIX>>>Using the fraction-bar model: {frac(2,3)}&asymp;0.667, {frac(3,4)}=0.75, {frac(3,6)}=0.5, {frac(2,5)}=0.4. Least to greatest: {frac(2,5)}, {frac(3,6)}, {frac(2,3)}, {frac(3,4)}.",
    "key-word-watch (least-to-greatest direction)",
    "Tier: Medium &middot; Topic: Comparing &amp; Ordering Fractions &amp; Decimals &middot; Diagram: yes &middot; Real, unused library item (global_id 139, ISEE Lower #3) -- CONFIRMED WRONG on the real test. Her wrong pick (D) was the correct order B exactly reversed, suggesting she sized the fractions right but flipped the least-to-greatest direction -- worth a direct check-in on that specific slip.",
    diagram=fraction_bar_stack([3,4,5,6]))

add(7, "Easy", "Finding Unit Price",
    "If 6 apples cost $9, what is the cost of 8 apples at the same rate?",
    {"A": "$11", "B": "$12", "C": "$14", "D": "$16"}, "B",
    "<<<ANSWERPREFIX>>>Unit price: $9 &divide; 6 apples = $1.50 per apple. 8 apples &times; $1.50 = $12.",
    None,
    "Tier: Easy &middot; Topic: Finding Unit Price &middot; Diagram: no &middot; Real, unused library item (global_id 259) -- CONFIRMED WRONG (she circled $11, inconsistent with her own correct scratch work of $3 per 2 apples). Cross-topic real item: catalogued under &quot;unit price scaling&quot; rather than a literal &quot;Finding Unit Price&quot; tag (no item in the library carries that exact tag), but it is the identical find-the-per-unit-rate-then-scale mechanic.")

add(8, "Easy", "English Unit Conversions",
    "There are 12 inches in 1 foot. The length of one wall in Mr. Jones's classroom is 29 feet. What is the length of this wall in inches?",
    {"A": "242", "B": "248", "C": "338", "D": "348"}, "D",
    "<<<ANSWERPREFIX>>>29 feet &times; 12 inches per foot = 348 inches.",
    None,
    "Tier: Easy &middot; Topic: English Unit Conversions &middot; Diagram: no &middot; Real, unused library item (global_id 90, ISEE Lower #2), used verbatim, answered correctly. A clean single-step conversion -- deliberately NOT the 3-way mixed-unit comparison shape (that one was already used in QR8 #6).")

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

add(11, "Medium", "Numerical Patterns",
    "Frank shaded a number pattern on the chart shown. He missed shading one number in the pattern between 18 and 30. What number did Frank miss shading?",
    {"A": "21", "B": "22", "C": "23", "D": "24"}, "D",
    "<<<ANSWERPREFIX>>>The shaded numbers are every 6th number: 6, 12, 18, 30, 36 -- a multiples-of-6 pattern. Between 18 and 30, the next multiple of 6 should be 24, but it isn't shaded. Frank missed shading 24.",
    None,
    "Tier: Medium &middot; Topic: Numerical Patterns &middot; Diagram: yes &middot; Real, unused library item (global_id 125, ISEE Lower #3), used verbatim, answered correctly. A different presentation (spot the missing term in a shaded grid) than the usual extend-the-sequence format, for variety.",
    diagram=grid_shaded(10, 4, 1, {6,12,18,30,36}))

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
    "Which whole number is divisible by 6 without a remainder?",
    {"A": "200", "B": "376", "C": "732", "D": "916"}, "C",
    "<<<ANSWERPREFIX>>>A number is divisible by 6 if it's divisible by BOTH 2 and 3. 732 is even (divisible by 2), and its digit sum 7+3+2=12 is divisible by 3 -- so 732 is divisible by 6 (732 &divide; 6 = 122). None of the other choices pass both checks.",
    "no-remainder divisibility rule, combined 2-and-3 check for 6",
    "Tier: Hard &middot; Topic: No Remainder when Divided by a given Number &middot; Diagram: no &middot; Real, unused library item (global_id 174, ISEE Lower #4 Q15), used verbatim. Original pick for this slot (the &quot;Lillian and 7 other students&quot; word-problem item, ISEE Lower #1 Q29) was dropped once a grep of every published worksheet -- not just used_real_gids.json -- found it already in rotation twice over: verbatim in an earlier online-set and with fresh numbers in an earlier redo-set, both predating the current QR/MA pipeline.")

add(20, "Medium", "Finding Area/Perimeter of Rectangle, given Length & Width",
    "The width of a rectangle is Y meters. Which statement correctly compares the value of Y to the length of the rectangle, where Y = " + frac(1,4) + " &times; length?",
    {"A": "The value of Y is always " + frac(1,4) + " times the value of the length.",
     "B": "The value of Y is always " + frac(3,4) + " times the value of the length.",
     "C": "The value of Y is always 3 times the value of the length.",
     "D": "The value of Y is always 4 times the value of the length."}, "A",
    f"<<<ANSWERPREFIX>>>The equation directly states Y = {frac(1,4)} &times; length -- so Y is always {frac(1,4)} of the length. (B swaps in the COMPLEMENT, {frac(3,4)}, instead of the fraction actually given in the equation -- a complement-confusion trap, the same kind of mix-up as the 'decreased by 30%' language gap.)",
    "complement-confusion (mixing up a fraction/percent with its complement)",
    "Tier: Medium &middot; Topic: Finding Area/Perimeter of Rectangle, given Length &amp; Width &middot; Diagram: no &middot; Real, unused library item (global_id 103, ISEE Lower #2) -- CONFIRMED WRONG (she picked the 3/4-complement trap, B), reinforcing the same complement-confusion mechanism flagged in QR8 #14's diagnosis.")

add(21, "Medium", "Input Output Tables",
    "Brandon used a number machine. Each number he put in came out as a different number, according to one consistent rule. Some examples are shown in the table. Which statement describes the relationship between the number Brandon put into the machine and the number that came out of it?",
    {"A": "The output was 2 more than the input.", "B": "The output was 2 less than the input.",
     "C": "The output was 5 more than the input.", "D": "The output was 5 less than the input."}, "A",
    "<<<ANSWERPREFIX>>>Check each pair: 10&rarr;12, 15&rarr;17, 24&rarr;26, 41&rarr;43 -- every output is exactly 2 more than its input.",
    None,
    "Tier: Medium &middot; Topic: Input Output Tables &middot; Diagram: yes &middot; Real, unused library item (global_id 39, ISEE Lower #1), used verbatim, answered correctly.",
    diagram=io_table_machine([["10","12"],["15","17"],["24","26"],["41","43"]]))

add(22, "Medium", "Order of Operations and Equivalence",
    "Which expression is equal to (2 + 8) &times; 7?",
    {"A": "2 + 8 &times; 7", "B": "2 &times; 7 + 8", "C": "2 &times; 8 + 8 &times; 7", "D": "2 &times; 7 + 8 &times; 7"}, "D",
    "<<<ANSWERPREFIX>>>By the distributive property, a(b+c) = ab + ac, so (2+8)&times;7 = 2&times;7 + 8&times;7. (Check directly: (2+8)&times;7 = 10&times;7 = 70, and only this expression also equals 70.)",
    None,
    "Tier: Medium &middot; Topic: Order of Operations and Equivalence &middot; Diagram: no &middot; Real, unused library item (ISEE Lower #3 Q29), used verbatim, answered correctly -- a distributive-property-equivalence item, different shape than QR8 #8's plain simplify-both-groups version.")

add(23, "Easy", "Remainder when Divided by a given Number",
    "Which expression results in a remainder of 5?",
    {"A": "32 &divide; 6", "B": "33 &divide; 6", "C": "34 &divide; 6", "D": "35 &divide; 6"}, "D",
    "<<<ANSWERPREFIX>>>35 &divide; 6 = 5 remainder 5 (6&times;5=30, 35&minus;30=5). Check the others: 32&divide;6=5 r2, 33&divide;6=5 r3, 34&divide;6=5 r4 -- only D leaves remainder 5.",
    None,
    "Tier: Easy &middot; Topic: Remainder when Divided by a given Number &middot; Diagram: no &middot; Real, unused library item (MA library, not_done), used verbatim. Original pick for this slot (&quot;leaves a remainder of 2 when divided by both 5 and 8&quot;) was dropped once a grep of every published worksheet found it already used, verbatim, choices and all, in an earlier redo-set predating the current QR/MA pipeline -- used_real_gids.json had no record of it since that set is outside its tracked range.")

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
    "Which phrase is represented by the expression (46 &minus; 22) &divide; 2?",
    {"A": "22 less than the quotient of 46 and 2", "B": "46 more than the quotient of 22 and 2",
     "C": "half the difference of 46 and 22", "D": "twice the difference of 46 and 22"}, "C",
    "<<<ANSWERPREFIX>>>(46 &minus; 22) is &quot;the difference of 46 and 22.&quot; Dividing that difference by 2 is the same as taking HALF of it -- so &quot;half the difference of 46 and 22.&quot;",
    None,
    "Tier: Hard &middot; Topic: Translating Math Expressions &middot; Diagram: no &middot; Real, unused library item (global_id 106, ISEE Lower #2), used verbatim, answered correctly -- the reverse direction (expression &rarr; phrase) from the usual phrase &rarr; expression format, for variety.")

add(27, "Medium", "3D shape from its net (unfolding a solid)",
    "The net shown below will fold up into which shape?",
    {"A": "cylinder", "B": "cone", "C": "cube", "D": "sphere"}, "A",
    "<<<ANSWERPREFIX>>>A rectangle with a circle attached at each short end folds up so the circles become the two flat ends and the rectangle wraps around into the curved side -- that's a cylinder.",
    None,
    "Tier: Medium &middot; Topic: 3D shape from its net (unfolding a solid) &middot; Diagram: yes &middot; Real, unused library item (global_id 410), used verbatim, answered correctly. Never graded before on this exact topic (0 prior instances) -- first real data point.",
    diagram=cylinder_net())

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

add(30, "Hard", "Determining Averages/Points on Number Lines (merged)",
    "Use the number line shown. The hash marks are evenly spaced. What is the mean (average) of A and B?",
    {"A": "22", "B": "24", "C": "25", "D": "26"}, "A",
    "<<<ANSWERPREFIX>>>There are 9 equal intervals between 10 and 37, a total span of 27, so each interval = 27 &divide; 9 = 3. A is 2 intervals from 10 (A = 10 + 2&times;3 = 16); B is 6 intervals from 10 (B = 10 + 6&times;3 = 28). Mean of A and B = (16 + 28) &divide; 2 = 22.",
    None,
    "Tier: Hard &middot; Topic: Determining Averages/Points on Number Lines (merged) &middot; Diagram: yes &middot; Real, unused library item (global_id 194, ISEE Lower #4), used verbatim, answered correctly -- positions verified directly against the source screenshot (9 ticks from 10 to 37, A at tick 2, B at tick 6), not guessed from the text description alone.",
    diagram=numberline(9, [(2, "A"), (6, "B")], show_ends=(10, 37)))

assert len(P) == 30, len(P)
json.dump(P, open(os.path.join(HERE, 'ma3_problems.json'), 'w'), indent=1)
print("wrote ma3_problems.json,", len(P), "problems")
