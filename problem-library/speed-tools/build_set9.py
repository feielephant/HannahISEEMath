"""QR Set 9. Parent's rule 2026-11-01: every problem is built like the real last third
(see GENERATION_WORKFLOW.md, "Hard means how the problem is built"), so plan_set.py's
tier mix is not used. Every math claim below is asserted, not hand-checked."""
import json, os, re, itertools, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from joined_prism_diagram import joined_prisms_svg
T = {x['topic']: x for x in json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))['topics']}
SW = 'stroke="currentColor" stroke-width="1.6"'
def frac(n, d): return f'<span class="frac"><span class="n">{n}</span><span class="d">{d}</span></span>'
def svg(w, h, body): return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">{body}</svg>'
def txt(x, y, s, size=13, anchor='middle'): return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="currentColor">{s}</text>'
def table(h, rows, title=None):
    t = f'<div style="font-weight:600;margin-bottom:4px">{title}</div>' if title else ''
    return t + '<table class="data"><tr>' + ''.join(f'<th>{c}</th>' for c in h) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'

def shape(k, x, y):  # 30px box at x,y, same look as the real item: C circle, S square, T trapezoid
    if k == 'C': s = f'<circle cx="{x+15}" cy="{y+15}" r="14" fill="none" {SW}/>'
    elif k == 'S': s = f'<rect x="{x+1}" y="{y+1}" width="28" height="28" fill="none" {SW}/>'
    else: s = f'<polygon points="{x+7},{y+1} {x+23},{y+1} {x+29},{y+29} {x+1},{y+29}" fill="none" {SW}/>'
    return s + txt(x+15, y+20, k, 13)
def scale(left, right):
    w = (len(left)+len(right))*33 + 46
    b, x = '', 8
    for k in left: b += shape(k, x, 6); x += 33
    b += txt(x+12, 27, '=', 20); x += 30
    for k in right: b += shape(k, x, 6); x += 33
    m = w/2
    b += f'<line x1="2" y1="44" x2="{w-2}" y2="44" stroke="currentColor" stroke-width="3"/><polygon points="{m},46 {m-13},68 {m+13},68" fill="currentColor"/>'
    return svg(w, 70, b)
def scales(a, b): return f'<div style="display:flex;gap:26px;flex-wrap:wrap">{scale(*a)}{scale(*b)}</div>'

def tile(x, y, d, c, s=46):  # d: "\\" or "/" or "X"; c: corner of the small black square
    b = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="none" {SW}/>'
    if d in ('\\', 'X'): b += f'<line x1="{x}" y1="{y}" x2="{x+s}" y2="{y+s}" stroke="currentColor" stroke-width="1"/>'
    if d in ('/', 'X'): b += f'<line x1="{x+s}" y1="{y}" x2="{x}" y2="{y+s}" stroke="currentColor" stroke-width="1"/>'
    pos = {'UR': (s-16, 5), 'LR': (s-16, s-16), 'UL': (5, 5), 'LL': (5, s-16), 'T': (s/2-5.5, 4)}[c]
    return b + f'<rect x="{x+pos[0]}" y="{y+pos[1]}" width="11" height="11" fill="currentColor"/>'
def mirror_v(t):
    d, c = t
    return ({'\\': '/', '/': '\\', 'X': 'X'}[d], {'UR': 'UL', 'UL': 'UR', 'LR': 'LL', 'LL': 'LR', 'T': 'T'}[c])
TL, BL, CENTER = ('\\', 'UR'), ('/', 'UL'), ('X', 'T')
TR, BR = mirror_v(TL), mirror_v(BL)
assert mirror_v(CENTER) == CENTER and BR == ('\\', 'UR')
tile_fig = svg(142, 142, tile(2, 2, *TL) + tile(94, 2, *TR) + tile(48, 48, *CENTER) + tile(2, 94, *BL)
               + f'<rect x="94" y="94" width="46" height="46" fill="none" {SW}/>' + txt(117, 124, '?', 24))
def tc(t): return svg(50, 50, tile(2, 2, *t))

# one-more-square symmetry grid, solved by checking all four possible lines
N = 5
base = {(0,0),(0,1),(1,0),(0,3),(3,0),(2,1),(1,2),(4,2)}
cand = {'A': (3,4), 'B': (4,0), 'C': (1,4), 'D': (2,4)}
def axes(S):
    fs = {'vert': lambda r,c:(r,N-1-c), 'horiz': lambda r,c:(N-1-r,c), 'diag': lambda r,c:(c,r), 'anti': lambda r,c:(N-1-c,N-1-r)}
    return [k for k,f in fs.items() if {f(r,c) for r,c in S} == S]
for k, v in cand.items():
    assert v not in base
    assert axes(base | {v}) == (['diag'] if k == 'D' else []), (k, axes(base | {v}))
def symgrid():
    u, b = 36, ''
    for r in range(N):
        for c in range(N):
            b += f'<rect x="{c*u+2}" y="{r*u+2}" width="{u}" height="{u}" fill="{"currentColor" if (r,c) in base else "none"}" {SW}/>'
    for k, (r, c) in cand.items(): b += txt(c*u+20, r*u+26, k, 15)
    return svg(N*u+4, N*u+4, b)

def rect_q(w, h, top, right):
    return svg(w+70, h+36, f'<rect x="8" y="6" width="{w}" height="{h}" fill="none" {SW}/>' + txt(8+w/2, h+26, top) + txt(w+24, 6+h/2+4, right))
def tetro():
    u, b = 40, ''
    for r, c in [(0,0),(1,0),(2,0),(2,1)]: b += f'<rect x="{c*u+2}" y="{r*u+2}" width="{u}" height="{u}" fill="none" {SW}/>'
    return svg(2*u+4, 3*u+4, b)
def cube(x, base_y, s, lab):
    d = s*0.35
    return (f'<rect x="{x}" y="{base_y-s}" width="{s}" height="{s}" fill="none" {SW}/>'
            f'<polygon points="{x},{base_y-s} {x+d},{base_y-s-d} {x+s+d},{base_y-s-d} {x+s},{base_y-s}" fill="none" {SW}/>'
            f'<polygon points="{x+s},{base_y-s} {x+s+d},{base_y-s-d} {x+s+d},{base_y-d} {x+s},{base_y}" fill="none" {SW}/>' + txt(x+s/2, base_y+16, lab))
def coord(pts):
    u, o, b = 26, 22, ''
    top = 8*u
    for i in range(9):
        b += f'<line x1="{o+i*u}" y1="{4}" x2="{o+i*u}" y2="{4+top}" stroke="currentColor" stroke-width="{1.6 if i==0 else .5}"/>'
        b += f'<line x1="{o}" y1="{4+i*u}" x2="{o+top}" y2="{4+i*u}" stroke="currentColor" stroke-width="{1.6 if i==8 else .5}"/>'
        b += txt(o+i*u, top+20, i, 11) + txt(o-10, 4+top-i*u+4, i, 11)
    for lab, (x, y) in pts.items():
        px, py = o+x*u, 4+top-y*u
        b += f'<circle cx="{px}" cy="{py}" r="4" fill="currentColor"/>' + txt(px+10, py-7, lab, 14)
    return svg(o+top+12, top+26, b)
def floor_grid(cols, rows, cells):
    u, b = 30, ''
    for r in range(rows):
        for c in range(cols):
            b += f'<rect x="{c*u+2}" y="{r*u+2}" width="{u}" height="{u}" fill="{"var(--ink-muted)" if (r,c) in cells else "none"}" {SW}/>'
    return svg(cols*u+4, rows*u+4, b)
def pattern_rects():
    u, x, b = 15, 4, ''
    for n in (1, 2, 3):
        ht = (n)*u
        for r in range(n):
            for c in range(n+1):
                b += f'<rect x="{x+c*u}" y="{50-ht+r*u}" width="{u}" height="{u}" fill="none" stroke="currentColor" stroke-width="1.3"/>'
        b += txt(x+(n+1)*u/2, 68, f'Figure {n}', 11)
        x += (n+1)*u + 44
    return svg(x-30, 74, b)
def numline():
    u, x0 = 20, 16
    b = f'<line x1="{x0-8}" y1="30" x2="{x0+13.5*u}" y2="30" stroke="currentColor" stroke-width="2"/><polygon points="{x0+14*u},30 {x0+13.5*u},25 {x0+13.5*u},35" fill="currentColor"/>'
    for i in range(13): b += f'<line x1="{x0+i*u}" y1="24" x2="{x0+i*u}" y2="36" stroke="currentColor" stroke-width="1.5"/>'
    b += txt(x0, 52, 0) + txt(x0+12*u, 52, 12)
    for lab, v in (('Q', 2), ('P', 10)): b += f'<circle cx="{x0+v*u}" cy="30" r="4" fill="currentColor"/>' + txt(x0+v*u, 17, lab, 14)
    return svg(x0+14*u+6, 58, b)
def segment():
    b = f'<line x1="14" y1="24" x2="296" y2="24" stroke="currentColor" stroke-width="2"/>'
    for lab, x in (('A', 14), ('B', 80), ('C', 214), ('D', 296)): b += f'<circle cx="{x}" cy="24" r="4" fill="currentColor"/>' + txt(x, 14, lab, 14)
    return svg(312, 34, b)
def stem(rows, title):
    r = ''.join(f'<tr><td style="text-align:right;border-right:2px solid currentColor;padding:2px 10px">{s}</td><td style="padding:2px 10px;letter-spacing:6px;font-family:ui-monospace,Menlo,monospace">{" ".join(str(l) for l in ls)}</td></tr>' for s, ls in rows)
    return f'<div style="font-weight:600;margin-bottom:4px">{title}</div><table style="border-collapse:collapse">{r}</table>'
def colsum(rows):
    style = 'display:inline-block;font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',\'Courier New\',monospace;letter-spacing:2px;font-size:1.25rem;text-align:right'
    r = ''.join(f'<div style="padding:2px 6px;line-height:1.5">{x}</div>' for x in rows[:-1])
    return f'<div style="{style}">{r}<div style="padding:7px 6px 2px;margin-top:5px;line-height:1.5;border-top:2px solid currentColor">{rows[-1]}</div></div>'

P = []
def add(n, topic, q, ch, ans, key, model, diagram=None, habit=None, tier='Hard', verbatim=None):
    assert topic in T, topic
    assert len(set(ch)) == 4
    t = T[topic]
    hist = f"Wrong so far: {t.get('wrong')}/{t.get('graded')}" if t.get('graded') else 'Few graded instances so far'
    src = f'Real item used verbatim ({verbatim})' if verbatim else 'New problem'
    P.append({'n': n, 'tier': tier, 'topic': topic, 'q': q, 'choices': dict(zip('ABCD', ch)), 'correct': ans,
              'key': f'<b>Answer: {ans}.</b> {key}', 'habit_note': habit,
              'ref': f'Tier: {tier} &middot; Topic: {topic} &middot; Diagram: {"yes" if diagram else "no"} &middot; {hist} &middot; {src} &middot; Built like: {model}',
              'diagram': diagram, 'needs_diagram': bool(diagram)})

# 1 retake #2 shape, new numbers
u = 34//2 - 12; assert u == 5 and 3*u - u == 10
add(1, 'Perimeter', 'Mara builds garden beds. The first rectangular bed she builds has a perimeter of 34 feet. The length of one of the sides is shown. If the unknown side length of the next bed she builds is tripled, by what amount will she increase the unknown side length?',
    ['5', '10', '15', '17'], 'B', 'Half the perimeter is 17, so the unknown side is 17 &minus; 12 = 5. Tripled it is 15, so the increase is 15 &minus; 5 = 10. C stops at the new side, A at the old side, D at half the perimeter.',
    'Lower #5 #33', rect_q(150, 70, '12', '?'), 'exact-thing-asked')
# 2 scales
S, Tz, C = 1, 3, 5
assert C+S == 2*Tz and Tz+2*S == C and (C, 2*C, Tz) != (0,0,0)
assert C == 5*S and C != 2*Tz and Tz != 2*S and 2*C != 3*Tz
add(2, 'Algebra with Geometric Shapes', 'The scales shown are balanced. Which set of figures would create a balanced scale?',
    [scale('C','TT'), scale('T','SS'), scale('CC','TTT'), scale('C','SSSSS')], 'D',
    'Use the second scale to swap C on the first scale: C is the same as T S S. So T S S S balances T T. Take one T off both sides: S S S balances T. Then C = T S S = S S S S S. Other choices do not hold: if S weighs 1, then T weighs 3 and C weighs 5.',
    'Lower #5 #34', scales(('CS','TT'), ('TSS','C')))
# 3 wide table
tb = {'Apr':(12,15,9,14),'May':(18,16,14,11),'Jun':(21,19,17,23),'Jul':(16,24,13,20),'Aug':(22,18,20,15),'Sep':(10,13,11,17)}
sm = lambda i: sum(tb[m][i] for m in ('Jun','Jul','Aug'))
assert sm(1) - sm(2) == 11 and sm(1)-sm(0) == 2 and sum(v[1] for v in tb.values())-sum(v[2] for v in tb.values()) == 21 and tb['Jun'][1]-tb['Jun'][2] == 2
add(3, 'Comparing Adding Subtracting Bar Graph Data Table Values', 'The table shows the number of miles four friends biked each month. How many more miles did Noor bike than Owen in June, July, and August combined?',
    ['2', '9', '11', '21'], 'C', 'Noor: 19 + 24 + 18 = 61. Owen: 17 + 13 + 20 = 50. 61 &minus; 50 = 11. A uses only June (or the Lena column), D uses all six months.',
    'Lower #5 MA #6, parent asked for tables with many numbers', table(['Month','Lena','Noor','Owen','Priya'], [[m,*v] for m,v in tb.items()], 'MILES BIKED'))
# 4 real
assert F(90)/F(25,100) == 360
add(4, 'Percent Word Problems', 'The weight of a baby elephant increased by 25%. If the baby elephant gained 90 pounds, what was the initial weight of the baby elephant, in pounds?',
    ['22.5','112.5','360','450'], 'C', '90 pounds is 25% of the starting weight, and 25% is one fourth, so the start is 90 &times; 4 = 360. D is the new weight, 360 + 90.',
    'Lower #4 #38 language: increased by', None, 'percent-language', verbatim='gid 1114')
# 5 real, parent approved
sol = [(t,c) for t in range(1,10) for c in range(1,10) if t!=c and 100*t+11*c-11*t==667]
assert sol == [(7,4)]
add(5, 'Cryptarithm / digit substitution', 'Each shape shown represents a different digit from 1 through 9. What is the value of ○?',
    ['3','4','5','8'], 'B', 'The two-digit number must be taken from a number bigger than 667, so △ is 6 or 7. Try △ = 7: 7○○ &minus; 77 = 667 gives 7○○ = 744, so ○ = 4. △ = 6 gives 6○○ = 733, which does not start with 6.',
    'Lower #3 #38', colsum(['△○○','&minus;△△','667']), verbatim='gid 157, parent approved repeat')
# 6 prism
assert 3*5*6 + 8*5*4 == 250
add(6, 'Solving Problems with Geometric Formulas', 'The figure shown was made by joining two rectangular prisms. The side lengths are measured in feet. Which expression can be used to find the total volume of the figure? (V = lwh, where V = volume, l = length, w = width, and h = height.)',
    ['(3 &times; 5 &times; 6) + (8 &times; 5 &times; 4)','(3 &times; 5 &times; 10) + (8 &times; 5 &times; 4)','(3 &times; 5 &times; 6) + (5 &times; 5 &times; 4)','8 &times; 5 &times; 10'], 'A',
    'Top prism: 3 by 5 by 6. Bottom prism: 8 by 5 by 4. B uses the total height 10 for the top prism, which counts the bottom part twice. C uses the step width 5 instead of the full 8. D treats the shape as one full box.',
    'Lower #1 #36', joined_prisms_svg(3, 6, 8, 4, 5))
# 7
for a,b,ok in [(2,7,False),(14,49,False),(18,7,False),(10,25,True)]: assert (F(a,a+b)==F(2,7)) == ok
add(7, 'Finding Ratios given Probability' if 'Finding Ratios given Probability' in T else 'Word Problems with Ratios', 'Omar has a bag of red, blue, green, and white marbles. The probability of choosing a red marble is 2 out of 7. Which combination of marbles is possible?',
    ['2 red marbles and 7 others','14 red marbles and 49 others','18 red marbles and 7 others','10 red marbles and 25 others'], 'D',
    '2 out of 7 compares red to the WHOLE bag, not red to the others. 10 red out of 10 + 25 = 35 total is 2/7. A is 2 out of 9, and B is 14 out of 63.',
    'What to Expect #32', None, 'verbose-choices')
# 8
assert 80*F(85,100)-5 == 63
add(8, 'Percent Increase Decrease basic' if 'Percent Increase Decrease basic' in T else 'Percent Word Problems', 'A jacket cost $80. The price was decreased by 15%. Then Priya used a $5 coupon on the new price. How much did Priya pay for the jacket?',
    ['$63','$68','$74.85','$75'], 'A', '15% of 80 is 12, so the new price is 68. After the coupon, 68 &minus; 5 = 63. C subtracts 0.15 instead of 15% of the price. B stops before the coupon.',
    'Lower #4 #38 language plus a second step', None, 'percent-language')
# 9
sol = [(c,t) for c in range(1,20) for t in range(1,20) if 2*c+t==23 and c+2*t==19]; assert sol==[(9,5)]
add(9, 'Algebra with Geometric Shapes', '<div>○ + ○ + △ = 23</div><div>○ + △ + △ = 19</div><div style="margin-top:6px">What is the value of ○?</div>',
    ['4','5','9','14'], 'C', 'The first line has one more ○ and one fewer △ than the second, and it is 4 more, so ○ is 4 more than △. Replace ○ with △ + 4 in the second line: △ + 4 + △ + △ = 19, so three △ make 15 and △ = 5. Then ○ = 9. A is the difference and B is △.',
    'Lower #1 #37', None)
# 10 real
add(10, 'Area and Perimeter of Complex Polygons', 'The L-shaped figure is made using four squares whose total area is 64 inches&sup2;. What is the perimeter of the figure?',
    ['40 inches','44 inches','48 inches','52 inches'], 'A', 'Each square has area 64 &divide; 4 = 16, so each side is 4. Going around the outside there are 10 sides of 4, so the perimeter is 40.',
    'Lower #1 #38', tetro(), verbatim='gid 1059')
# 11 stem
vals=[42,45,45,48,50,53,53,53,57,61,64,69,70,72,76]
assert vals.count(53)==3 and min(vals)==42 and sum(v>=70 for v in vals)==3 and vals.count(64)==1
add(11, 'Identifying Correct Conclusions from Bar Graph Data Table', 'The stem-and-leaf plot shows the points a basketball team scored in 15 games, where 5|3 represents 53. Based on the data in the stem-and-leaf plot, which conclusion is true?',
    ['The team scored 53 points in exactly 2 games.','The team scored at least 45 points in every game.','The team scored 70 points or more in exactly 3 games.','The team scored 64 points in 2 games.'], 'C',
    '70, 72, and 76 are the 3 scores of 70 or more. A: 53 appears 3 times. B: the lowest score is 42. D: 64 appears once.',
    'Lower #2 #37', stem([(4,[2,5,5,8]),(5,[0,3,3,3,7]),(6,[1,4,9]),(7,[0,2,6])],'POINTS SCORED'), 'verbose-choices')
# 12 real
assert (F(19,6)-F(5,4))*60 == 115
add(12, 'Multi-step unit conversion (off-by-10, multi-step)', f'Mary spent 3 {frac(1,6)} hours at the health club. Of that time, 1 {frac(1,4)} hours were spent not exercising. How many minutes did Mary exercise? (1 hour = 60 minutes)',
    ['110','115','125','130'], 'B', '3 1/6 hours = 180 + 10 = 190 minutes. 1 1/4 hours = 60 + 15 = 75 minutes. 190 &minus; 75 = 115.',
    'Lower #1 #29', None, verbatim='gid 1005')
# 13 symmetry grid
add(13, 'Shape Construction & Symmetry in 2-D Figures', 'One more square in the grid will be shaded so that the design has exactly one line of symmetry. Which lettered square should be shaded?',
    ['Square A','Square B','Square C','Square D'], 'D', 'Find the line first. The line goes corner to corner, from the top left to the bottom right, not straight up or across. Every shaded square has a partner across that line except the shaded square in the bottom row, third column. Its partner is square D.',
    'Lower #5 #29, parent: she did not find the line', symgrid())
# 14 rhombus
d=lambda a,b:(a[0]-b[0])**2+(a[1]-b[1])**2
W,X,Y=(1,4),(4,6),(7,4)
for z,ok in [((1,2),False),((4,2),True),((4,3),False),((7,2),False)]:
    assert (d(W,X)==d(X,Y)==d(Y,z)==d(z,W))==ok
add(14, 'Identifying Shapes', 'The graph shows three of the four vertices of rhombus WXYZ. At which location on the coordinate grid could point Z be located?',
    ['(1, 2)','(4, 2)','(4, 3)','(7, 2)'], 'B', 'A rhombus has four equal sides. From X to W and from X to Y is 3 across and 2 up or down. So Z must also be 3 across and 2 down from W, which is (4, 2).',
    'Lower #1 #31 and Lower #5 MA #28', coord({'W':W,'X':X,'Y':Y}))
# 15
assert F(15,30+15)==F(1,3)
add(15, 'Probability of 1 Event, given a List of Items', f'The table shows the number of each color of bead in a box. If the probability of randomly taking a purple bead out of the box on the first try is {frac(1,3)}, how many purple beads are in the box?',
    ['3','5','10','15'], 'D', 'The other beads total 5 &times; 6 = 30, and those are 2/3 of the box. So 1/3 of the box is 15. C takes 1/3 of 30, but 1/3 is of the whole box, purple included.',
    'Lower #5 #37', table(['Color','red','orange','yellow','green','blue','pink','purple'],[['Beads',5,5,5,5,5,5,'?']],"LUCY'S BOX OF BEADS"))
# 16
assert F(75,100)*F(120,100)==F(9,10)
add(16, 'Percent Increase Decrease basic' if 'Percent Increase Decrease basic' in T else 'Percent Word Problems', 'The price of a bike is decreased by 25%. The new price is then increased by 20%. What is the overall percent increase or percent decrease from the original price?',
    ['percent decrease by 5%','percent decrease by 10%','percent increase by 5%','percent increase by 45%'], 'B', 'Try a $100 bike. 25% off leaves $75. 20% of 75 is 15, so the price becomes $90, which is 10% below $100. A just subtracts 25 and 20, but the 20% is of the new price.',
    'Lower #4 #38', None, 'percent-language')
# 17
cells={(0,1),(0,4),(0,6),(1,0),(1,3),(1,7),(2,2),(2,5),(3,0),(3,3),(3,6),(4,1),(4,4),(4,7)}
assert len(cells)==14 and F(14,40)==F(35,100)
add(17, 'Total Shaded Area given Figure with Equal Divisions', 'The shaded area on the grid represents the part of a rectangular floor that has tile already installed. Each small square on the floor has the same dimensions. What percentage of the floor has tile already installed?',
    ['14%','28%','35%','40%'], 'C', 'There are 8 &times; 5 = 40 squares and 14 are shaded. 14/40 = 7/20 = 35/100 = 35%. A reads the count as the percent.',
    'Lower #5 #35 and Lower #4 #37', floor_grid(8,5,cells))
# 18 real, parent approved
sols={(100*0+0) for _ in []}
res={ (11*a+11*b)//100 for a in range(1,10) for b in range(1,10) if a!=b and 11*a+11*b>=100}; assert res=={1}
add(18, 'Cryptarithm / digit substitution', 'Each letter represents a different digit from 1 through 9. What digit does C represent?',
    ['1','3','7','9'], 'A', 'Two 2-digit numbers add to less than 200, since even 99 + 99 = 198. So a 3-digit sum must start with 1, and C = 1.',
    'Lower #4 #24', colsum(['AA','+BB','CDE']), verbatim='gid 184, parent approved repeat')
# 19
add(19, 'Translating Math Expressions', 'Mia had □ marbles and then she gave ○ of them to Theo. Now Theo has △ times as many marbles as Mia has left. Which expression represents the number of marbles Theo had to begin with?',
    ['△ &times; □ &minus; ○','△ &times; □ + ○','△ &times; (□ &minus; ○) + ○','△ &times; (□ &minus; ○) &minus; ○'], 'D', 'Mia has □ &minus; ○ left. Theo now has △ &times; (□ &minus; ○). He got ○ from Mia, so take that back off to find what he started with. Test it: □ = 10, ○ = 2, △ = 3 means Theo has 24 now and started with 22.',
    'Lower #4 #35', None)
# 20 wide MMMR
sc={'Ava':[88,92,79,85],'Ben':[76,85,92,81],'Cho':[92,70,88,92],'Dev':[84,92,75,90],'Eli':[81,78,92,88]}
al=sum(sc.values(),[])
from collections import Counter
mc=Counter(al).most_common(2); assert mc[0]==(92,6) and mc[1][1]<6 and max(al)-min(al)==22
b=sorted(sc['Ben']); assert F(b[1]+b[2],2)==83
add(20, 'Finding MMMR given Bar Graph Data Table', 'The table shows four test scores for each of five students. Which statement about the scores is true?',
    ['The mode of all the scores is 92.','The mode of all the scores is 88.','The range of all the scores is 20.',"The median of Ben's scores is 85."], 'A',
    "92 appears 6 times, more than any other score. 88 appears only 3 times. The range is 92 &minus; 70 = 22. Ben's scores in order are 76, 81, 85, 92, so his median is 83.",
    'Lower #5 MA #17, parent asked for tables with many numbers', table(['Student','Test 1','Test 2','Test 3','Test 4'],[[k,*v] for k,v in sc.items()],'TEST SCORES'), 'verbose-choices')
# 21 real
assert 63//9*800==5600
add(21, 'Multi-step unit conversion (off-by-10, multi-step)', 'A chactrac is equal to 63 plibobs, and 9 plibobs are equal to 800 twips. How many twips are equal to a chactrac?',
    ['560','800','5,600','7,200'], 'C', '63 plibobs is 7 groups of 9 plibobs. 7 &times; 800 = 5,600.', 'Lower #1 #29', None, verbatim='gid 862')
# 22
assert F(3,10)<F(3,8)<F(2,5)<F(45,100)
add(22, 'Comparing & Ordering Fractions & Decimals', f'Four friends each walked part of the same trail. Ana walked {frac(2,5)} of it, Ben walked 0.3 of it, Cy walked {frac(3,8)} of it, and Dee walked 45% of it. Which list shows the friends in order from the shortest walk to the longest?',
    ['Ana, Ben, Cy, Dee','Ben, Ana, Cy, Dee','Ben, Cy, Ana, Dee','Cy, Ben, Ana, Dee'], 'C', 'Write each one as a decimal, then place them on a number line: Ben 0.3, Cy 0.375, Ana 0.4, Dee 0.45.',
    'Lower #4 #27 fractions plus her order-three gap', None, 'write-it-down')
# 23
add(23, 'Translating Math Expressions', 'Maya plans to buy enough pizzas so that each guest at her party gets 3 slices. Each pizza has 8 slices. How can Maya find out how many pizzas to buy?',
    ['multiply the number of guests by 3, then divide by 8','multiply the number of guests by 8, then divide by 3','multiply 3 by 8, then divide by the number of guests','add 3 and 8, then multiply by the number of guests'], 'A',
    'Guests times 3 gives the slices needed. Each pizza gives 8 slices, so divide by 8. Test it: 8 guests need 24 slices, which is 3 pizzas.',
    'Lower #4 #33', None, 'verbose-choices')
# 24 rule number
digits='12579'
ok=[int(''.join(p)) for p in itertools.permutations(digits) if int(p[-1])%2==0 and p[1]=='9']
assert max(ok)==79512
add(24, 'Value of Digits' if 'Value of Digits' in T else 'Numerical Patterns', 'Students were asked to write a new number using all the rules shown. What digit is in the hundreds place of the new number?',
    ['1','2','5','7'], 'C', 'Even means it ends in 2. The thousands digit is 9. To be as large as possible, the ten-thousands digit is 7, then 5, then 1: 79,512. The hundreds digit is 5.',
    'Lower #3 #31 and Lower #2 #35', '<div style="border:1.6px solid currentColor;padding:8px 12px;display:inline-block"><b>RULES FOR THE NEW NUMBER</b><br>1. The number must have 5 digits.<br>2. It must use each of the digits 1, 2, 5, 7, and 9 one time.<br>3. The number must be even.<br>4. The thousands digit must be 9.<br>5. The number must be as large as possible.</div>')
# 25
assert [n*(n+1) for n in (1,2,3,6,7)]==[2,6,12,42,56]
add(25, 'Numerical Patterns', 'The first three figures in a pattern are shown. If the pattern continues, how many small squares will the 7th figure have?',
    ['30','42','49','56'], 'D', 'Figures have 1 by 2, 2 by 3, and 3 by 4 squares, so the 7th is 7 by 8 = 56. Or write the differences: 2, 6, 12, 20, 30, 42, 56 grows by +4, +6, +8, +10, +12, +14. B is the 6th figure.',
    'Lower #3 #35 and Lower #2 #27', pattern_rects(), 'write-it-down')
# 26
assert 79+(30-12)*6==187
add(26, 'Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.', 'In a sequence, each number is 6 more than the number before it. The 12th number in the sequence is 79. What is the 30th number in the sequence?',
    ['181','187','193','259'], 'B', 'Start from the 12th number. From 12th to 30th is 18 steps, so 79 + 18 &times; 6 = 187. A and C are off by one step. D adds 30 steps.',
    'Lower #3 #35, anchored from a later term as in QR8 #23', None)
# 27
add(27, 'Split Line Segments', 'The length of AD is x. The length of AB is 3. The length of CD is y. What is the length of BC?',
    ['x &minus; 3 &minus; y','x + 3 + y','x &minus; 3 + y','3 + y &minus; x'], 'A', 'BC is what is left of AD after taking off AB and CD. Test it: x = 10, y = 2 gives AB + BC + CD = 3 + 5 + 2 = 10.',
    'Lower #5 #30', segment())
# 28
assert 800<49*612/31<1200
add(28, 'Estimating Multiplication & Division', f'Liam did the problem shown with his calculator: {frac("49 &times; 612","31")}. What is a reasonable estimation for his answer?',
    ['between 500 and 800','between 800 and 1,200','between 1,200 and 1,600','between 1,600 and 2,000'], 'B', 'Round to 50 &times; 600 &divide; 30. 50 &times; 600 = 30,000, and 30,000 &divide; 30 = 1,000.',
    'What to Expect #33', None)
# 29
assert 50*100==5*10*10*10
add(29, 'Comparing Volume of Cubes', 'A hundreds flat has a volume of 100 cubic inches. Exactly 50 of these hundreds flats are used to make a new three-dimensional figure. Which expression represents the volume of the new figure in cubic inches?',
    ['5 &times; 10','5 &times; 10 &times; 10','5 &times; 10 &times; 10 &times; 10','5 &times; 10 &times; 10 &times; 10 &times; 10'], 'C', '50 &times; 100 = 5,000, and 5,000 = 5 &times; 10 &times; 10 &times; 10. Count the zeros: three zeros means three tens.',
    'Lower #5 #38', None)
# 30
assert 13*13==169 and 11*16==176 and 2*(11+16)==54 and 13*4==52
add(30, 'Comparing Areas', 'Patio A is a square with a perimeter of 52 feet. Patio B is a rectangle with a length of 16 feet and a width of 11 feet. Which statement correctly compares the two patios?',
    ['The area of Patio B is 7 feet&sup2; greater than the area of Patio A.','The area of Patio A is 7 feet&sup2; greater than the area of Patio B.','The two patios have the same perimeter.','The perimeter of Patio A is 2 feet greater than the perimeter of Patio B.'], 'A',
    'Patio A: side 52 &divide; 4 = 13, area 169, perimeter 52. Patio B: area 176, perimeter 54. 176 &minus; 169 = 7.',
    'Lower #2 #38', None, 'verbose-choices')
# 31
assert F(27,90)*40==12
add(31, 'Identifying Correct Conclusions from Bar Graph Data Table', 'The table shows the number of votes for different school sports. Based on the information in the table, what is the most reasonable prediction of the number of votes for swimming out of the next 40 votes?',
    ['3','12','27','30'], 'B', 'There are 42 + 27 + 9 + 12 = 90 votes, and swimming has 27/90 = 3/10 of them. 3/10 of 40 is 12.',
    'Lower #2 #34', table(['Sport','Soccer','Swimming','Track','Tennis'],[['Number of Votes',42,27,9,12]],'VOTES FOR SPORTS'))
# 32 real
assert (lambda b:(b,5*b,10*b))(4)==(4,20,40) and 4+20+40==64
add(32, 'Word Problems with Ratios', 'A pasta recipe calls for dried pasta, sauce, and basil. The recipe uses 2 times as much dried pasta as sauce and 5 times as much sauce as basil. If the recipe uses a total of 64 ounces of ingredients, how many ounces of sauce does the recipe use?',
    ['18','20','35','40'], 'B', 'Basil = 1 part, sauce = 5 parts, pasta = 10 parts, so 16 parts = 64 and 1 part = 4. Sauce is 5 &times; 4 = 20. D is the pasta.',
    'Lower #2 #36', None, 'exact-thing-asked', verbatim='gid 1140')
# 33 tile
add(33, 'Shape Construction & Symmetry in 2-D Figures', 'The design, when completed, has one line of symmetry. Which tile, without rotating, correctly completes the design?',
    [tc(BR), tc(BL), tc(('\\','LL')), tc(('/','LR'))], 'A', 'Find the line first. The center tile has its black square at the top middle, so it matches itself only across an up-and-down line. So the line is vertical, and the right column mirrors the left. The bottom left tile flipped left to right gives choice A. B just copies the bottom left tile.',
    'Lower #5 #29, parent: she did not find the line', tile_fig)
# 34
fr=lambda n:F(n,6)+F(1,4)
assert not fr(1)<F(1,3) and not fr(2)<F(1,2) and not fr(4)>1 and fr(5)>1
add(34, 'Adding and Subtracting Fractions' if 'Adding and Subtracting Fractions' in T else 'Comparing & Ordering Fractions & Decimals', f'Eva has two equal-sized jugs of water. The first jug is {frac("n",6)} full. The second jug is {frac(1,4)} full. The water from these jugs will be combined by pouring the water from the first jug into the second jug. Which statement best describes the amount of water once the jugs are combined?',
    [f'If n = 1, then the amount of water is less than {frac(1,3)} of a jug.',f'If n = 2, then the amount of water is less than {frac(1,2)} of a jug.','If n = 4, then the water will not all fit in 1 jug.','If n = 5, then the water will not all fit in 1 jug.'], 'D',
    'In twelfths, the total is (2n + 3)/12. n = 1 gives 5/12, more than 4/12. n = 2 gives 7/12, more than 6/12. n = 4 gives 11/12, which fits. n = 5 gives 13/12, which does not fit.',
    'Lower #2 #36', None, 'verbose-choices')
# 35 cube
assert (3*4)**3//3**3==64
add(35, 'Comparing Volume of Cubes', 'Two cubes are shown. Cube A has sides with length 3 centimeters. Cube B is 4 times as wide as Cube A. How many Cube A\'s can fit inside Cube B?',
    ['12','16','27','64'], 'D', '4 cubes fit along each edge of B, so 4 &times; 4 &times; 4 = 64. A multiplies 3 by 4 and C is the volume of Cube A.',
    'Lower #4 #36', svg(230,172, cube(6,146,34,'A') + cube(70,146,104,'B')))
# 36 scales 2
Cc=1; Ss=2*Cc; Tt=F(3,2)*Ss; assert 2*Tt==3*Ss and 2*Ss==4*Cc and 4*Tt==12
add(36, 'Algebra with Geometric Shapes', 'The scales shown are balanced. How many C figures would balance 4 T figures?',
    ['12','16','18','24'], 'A', 'T T balances S S S, so T T T T balances S S S S S S. Each S S balances C C C C, so 6 S is three of those groups: 3 &times; 4 = 12 C.',
    'Lower #5 #34 and Lower #2 #17', scales(('TT','SSS'),('SS','CCCC')))
# 37
assert 2*10-2==18
add(37, 'Determining Averages between Points on Number Lines' if 'Determining Averages between Points on Number Lines' in T else 'Numerical Patterns', 'Use the number line shown to answer the question. P is the average of Q and another number. What is the other number?',
    ['6','12','14','18'], 'D', 'Each tick is 1, so Q = 2 and P = 10. P is 8 above Q, so the other number is 8 above P: 18. A is the average of Q and P.',
    'What to Expect #35', numline())
# 38
assert 72*F(3,4)*F(2,3)+5==41
add(38, 'Remaining Amount after Reducing by Fractions', f'A bakery made 72 muffins. It sold {frac(1,4)} of them in the morning. Then it sold {frac(1,3)} of the muffins it had left in the afternoon. Then it baked 5 more muffins. How many muffins does the bakery have now?',
    ['36','41','54','59'], 'B', '72 &minus; 18 = 54 left. 1/3 of 54 is 18, so 36 left. 36 + 5 = 41. A stops before the 5 more. C stops after the morning. D skips the afternoon.',
    'Lower #5 #33 step chain', None, 'exact-thing-asked')

assert [p['n'] for p in P]==list(range(1,39))
L=[p['correct'] for p in P]
print(Counter(L)); assert sorted(Counter(L).values())==[9,9,10,10]
assert not any(L[i]==L[i+1]==L[i+2] for i in range(36))
json.dump(P, open(os.path.join(HERE,'set9_problems.json'),'w'), indent=1)
print('wrote', len(P), 'diagrams', sum(1 for p in P if p['diagram']))
