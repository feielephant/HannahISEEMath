"""Merge topic_history.py output into the topic groups used by QR11 and write qr11_metrics.json.
Usage: python3 topic_history.py /tmp/hist.json && python3 group_metrics.py /tmp/hist.json"""
import json, re, sys, os
H = json.load(open(sys.argv[1]))
def n(t): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',(t or '').lower().replace('&',' and ').replace('2-d','2d'))).strip()
G={'EST':['Estimating Multiplication & Division'],'CUBE':['Comparing Volume of Cubes'],'STORY':['Matching Stories to Equations'],
'SHAPES':['Identifying Shapes'],'PROB':['Finding Ratios, given Probability','Probability of 1 Event, given a List of Items'],
'DIGIT':['Value of Digits'],'POLY':['Area and Perimeter of Complex Polygons','Perimeter'],'SYM':['Algebra with Shapes for Variables','Algebra with Geometric Shapes','Algebraic Equations with Symbol Variables'],
'NUMLINE':['Determining Averages between Points on Number Lines'],'AREAS':['Comparing Areas'],'NEXT':['Predicting the Next Shapes, given Progressive Pattern','Patterns in Data Tables and Lists'],
'EQUIV':['Equivalent Fractions, Decimals, and Percents','Determining Fraction/Percent of Shaded Area, given Figure'],'PICTO':['Interpreting Pictographs','Cryptarithm / digit substitution'],
'PAT':['Numerical Patterns'],'ORDER':['Comparing & Ordering Fractions & Decimals'],'RATIO':['Word Problems with Ratios'],'MMMR':['Finding MMMR, given Bar Graph/Data Table of Values','Finding MMMR given Bar Graph Data Table','Finding Median, given Sets of Numbers'],
'DATA':['Data Collection & Random Sampling'],'UNIT':['English Unit Conversions'],'DIV':['No Remainder when Divided by a given Number','No Remainder when Divided by two given Numbers'],'VENN':['Solving for Subsets in a Venn Diagram'],
'PCT':['Percent Increase & Decrease (basic)','Percent Increase Decrease basic'],'PCTWORD':['Percent Word Problems'],'DEC':['Converting to a Decimal'],'MSUNIT':['Multi-step unit conversion (off-by-10, multi-step)'],'SPLIT':['Split Line Segments'],'MULT':['Counting Multiples within a Range'],'NTH':['Nth Term, given Arithmetic Sequence, Progressive Pattern, etc.'],'REMFRAC':['Remaining Amount after Reducing by Fractions'],'NUMPROP':['Identifying Number Properties'],'TRI':['Area of Triangles'],'IO':['Input/Output Tables','Input Output Tables'],'UNITPRICE':['Finding Unit Price'],'GEOFORM':['Solving Problems with Geometric Formulas'],'WHO':['Whole Number "Who am I?"','Whole Number Who am I'],'SCALE':['Measurement Scaling'],'TOTALCOST':['Determining Total Cost'],'LINEQ':['Interpreting Linear Equations from Word Problems'],'OOO':['Order of Operations and Equivalence','Translating Math Expressions'],'AVGMIX':['Averaging Mixed Numbers'],'RECT':['Finding Area/Perimeter of Rectangle, given Length & Width']}
out = {}
for g, ts in G.items():
    ev = sorted(set(tuple(e) for t in ts if n(t) in H for e in H[n(t)]['events']))
    real = [e for e in ev if e[4] == 'realQR']; ma = [e for e in ev if e[4] == 'realMA']; lw = [e for e in ev if e[3]]
    r5 = ev[-5:]; s = [e for e in ev if e[0] >= '2026-10-25']
    out[g] = dict(real_mid=sum(1 for e in real if 13 <= e[2] <= 25), real_last=sum(1 for e in real if e[2] >= 26),
        real_wrong='%d/%d' % (sum(e[3] for e in real+ma), len(real)+len(ma)),
        last_done='%s %s' % (ev[-1][1], ev[-1][0][5:]), last_wrong=('%s %s' % (lw[-1][1], lw[-1][0][5:])) if lw else 'never',
        last5='%d/%d' % (sum(e[3] for e in r5), len(r5)), since1025='%d/%d' % (sum(e[3] for e in s), len(s)), total='%d/%d' % (len(lw), len(ev)))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qr11_metrics.json'), 'w'), indent=1)
print(len(out), 'groups')
