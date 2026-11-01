"""Practice Test 5 (ISEE Lower, Test Innovators result 5053390, taken 2026-11-01) retake.
Her 9 wrong problems, verbatim: same wording, same choice order, same diagrams cropped from
the source screenshots. Deliberately NOT fresh numbers (parent request: redo with no teaching
to see where she is actually missing). Run with the crop folder as argv[1]."""
import base64, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]

def img(name, alt, width):
    b = base64.b64encode(open(os.path.join(D, name + '.png'), 'rb').read()).decode()
    return (f'<img src="data:image/png;base64,{b}" alt="{alt}" '
            f'style="width:{width}px;max-width:100%;display:block;background:#fff;border-radius:4px;padding:4px;" />')

def after(t):
    return f'<div class="q" style="margin-top:12px">{t}</div>'

def src(section, num, letter_her, letter_ok, pct, her_sec, avg_sec, diff, topic):
    return (f'Original: {section} #{num} &middot; Her answer on 11/1: {letter_her} &middot; Correct: {letter_ok} '
            f'({pct} of test takers) &middot; Her time: {her_sec}s (avg {avg_sec}s) &middot; {diff} &middot; {topic}')

def tile(L, alt):
    return img(f'qr29_{L}', alt, 74)

def scale(L, alt, width):
    return img(f'qr34_{L}', alt, width)

P = [
 dict(n=1, tier='Hard', topic='Shape Construction & Symmetry in 2-D Figures',
  q='The design, when completed has one line of symmetry.',
  diagram=img('qr29_fig', 'Design of five square tiles with a missing bottom-left tile', 260) + after('Which tile, without rotating, correctly completes the design?'),
  choices=dict(A=tile('A', 'Tile A'), B=tile('B', 'Tile B'), C=tile('C', 'Tile C'), D=tile('D', 'Tile D')), correct='D',
  key='<b>Answer: D.</b> The design has a horizontal line of symmetry, so the missing tile is the mirror image of the top-left tile.',
  ref=src('QR', 29, 'B', 'D', '70.5%', 23, 45, 'Hard', 'Shape Construction & Symmetry in 2-D Figures')),
 dict(n=2, tier='Hard', topic='Perimeter',
  q='Ben builds picture frames. The first rectangular frame he builds has a perimeter of 20 centimeters (cm). The length of one of the sides is shown.',
  diagram=img('qr33_fig', 'Rectangle with bottom side 7 and right side marked with a question mark', 300) + after('If the unknown side length of the next frame he builds is doubled, by what amount will he increase the unknown side length of the next frame?'),
  choices=dict(A='2', B='3', C='4', D='6'), correct='B',
  key='<b>Answer: B.</b> 2 &times; (length + width) = 20, so length + width = 10 and the unknown side is 10 &minus; 7 = 3. Doubled, it is 6, an increase of 6 &minus; 3 = 3. (6 is the doubled value, not the increase.)',
  ref=src('QR', 33, 'C', 'B', '66.1%', 145, 49, 'Hard', 'Perimeter')),
 dict(n=3, tier='Hard', topic='Interpreting Pictographs (balance scales)',
  q='The scales shown are balanced.',
  diagram=img('qr34_fig', 'Two balanced scales: C S S equals C T, and S S T equals C C', 560) + after('Which set of figures would create a balanced scale?'),
  choices=dict(A=scale('A', 'C equals T T', 130), B=scale('B', 'T equals C C', 130), C=scale('C', 'T equals C', 90), D=scale('D', 'T equals S', 100)), correct='C',
  key='<b>Answer: C.</b> Left scale: take C off both sides, so S S = T. Right scale: replace S S with T, so T T = C C. Therefore T = C.',
  ref=src('QR', 34, 'B', 'C', '63.1%', 24, 57, 'Hard', 'Interpreting Pictographs')),
 dict(n=4, tier='Hard', topic='Comparing Volume of Cubes',
  q='The thousands cube shown has a volume of 1,000 cubic inches.',
  diagram=img('qr38_fig', 'Thousands cube made of small unit cubes', 220) + after('Exactly 30 of these thousands cubes are used to make a new three-dimensional figure. Which expression represents the volume of the new figure in cubic inches?'),
  choices=dict(A='3 &times; 10', B='3 &times; 10 &times; 10 &times; 10', C='3 &times; 10 &times; 10 &times; 10 &times; 10', D='3 &times; 10 &times; 10 &times; 10 &times; 10 &times; 10'), correct='C',
  key='<b>Answer: C.</b> 1,000 = 10 &times; 10 &times; 10 and 30 = 3 &times; 10, so 30 &times; 1,000 = 3 &times; 10 &times; 10 &times; 10 &times; 10 = 30,000.',
  ref=src('QR', 38, 'A', 'C', '39.6%', 66, 41, 'Hard', 'Comparing Volume of Cubes')),
 dict(n=5, tier='Easy', topic='Comparing/Adding/Subtracting Bar Graph/Data Table Values',
  q='This table shows the number of books that three friends read last year.',
  diagram=img('ma6_tbl', 'Books Read table by month for Jacob, Megan, and Patrick', 640) + after('How many more books did Megan read than Jacob last August?'),
  choices=dict(A='1', B='2', C='3', D='4'), correct='B',
  key='<b>Answer: B.</b> August: Megan 6, Jacob 4, and 6 &minus; 4 = 2.',
  ref=src('MA', 6, 'A', 'B', '92.0%', 18, 27, 'Easy', 'Comparing/Adding/Subtracting Bar Graph/Data Table Values')),
 dict(n=6, tier='Medium', topic='Finding MMMR, given Bar Graph/Data Table of Values',
  q='The table shows four test scores of four students.',
  diagram=img('ma17_tbl', 'Test Scores table for Betty, Francis, Pualani, and WeiMing', 520) + after('What is the mode of this set of data?'),
  choices=dict(A='71', B='87', C='93', D='95'), correct='C',
  key='<b>Answer: C.</b> 93 appears 3 times (Francis, Pualani, WeiMing), more than any other score. 83 and 95 each appear twice.',
  ref=src('MA', 17, 'D', 'C', '82.9%', 57, 75, 'Medium', 'Finding MMMR, given Bar Graph/Data Table of Values')),
 dict(n=7, tier='Hard', topic='Identifying Shapes',
  q='Which figure best describes a quadrilateral with all its sides equal?', diagram='',
  choices=dict(A='parallelogram', B='rectangle', C='rhombus', D='trapezoid'), correct='C',
  key='<b>Answer: C.</b> A rhombus is a quadrilateral whose sides are all equal.',
  ref=src('MA', 28, 'A', 'C', '62.0%', 18, 20, 'Hard', 'Identifying Shapes')),
 dict(n=8, tier='Hard', topic='Counting Multiples within a Range',
  q='How many numbers between 65 and 85 are divisible by 3?', diagram='',
  choices=dict(A='4', B='5', C='6', D='7'), correct='D',
  key='<b>Answer: D.</b> 66, 69, 72, 75, 78, 81, 84 is 7 numbers.',
  ref=src('MA', 29, 'C', 'D', '63.7%', 134, 59, 'Hard', 'Counting Multiples within a Range')),
 dict(n=9, tier='Hard', topic='Data Collection & Random Sampling',
  q='The table shows some of the characteristics and data gathered by a scientist about a particular type of bug.',
  diagram=img('ma30_tbl', 'Bug Data table: length, mass, number of antennae, number of legs', 360) + after('Which question is NOT a valid statistical question based on the data in the table?'),
  choices=dict(A='How long was each bug?', B='What mass did each bug have?', C='How many legs did each bug have?', D='What was the ratio of mass to length for each bug?'), correct='C',
  key='<b>Answer: C.</b> A statistical question expects variability in the data. Every bug has 6 legs, so the answer never varies. (73.2% of test takers picked D, the same choice she made.)',
  ref=src('MA', 30, 'D', 'C', '18.8%', 282, 43, 'Hard', 'Data Collection & Random Sampling')),
]
json.dump(P, open(os.path.join(HERE, 'pt5_retake_problems.json'), 'w'), ensure_ascii=False, indent=1)
print(len(P), 'problems')
