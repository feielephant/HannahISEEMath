import json, random, html
random.seed(101)
# (question, correct, [d1,d2,d3], tier, topic, diagram_html_or_None, why)
P = [
("What number comes next in the pattern 3, 6, 9, 12, ___?", "15", ["13","14","18"], "Easy", "patterns: add 3", None, "Each term increases by 3: 12 + 3 = 15."),
("Which number is divisible by 8?", "56", ["36","44","62"], "Easy", "divisibility by 8", None, "56 ÷ 8 = 7. 36, 44, and 62 leave remainders."),
("Which number is divisible by 9?", "63", ["52","74","85"], "Easy", "divisibility by 9 (digit sum)", None, "6 + 3 = 9, so 63 is divisible by 9."),
("Which number leaves a remainder of 3 when divided by 5?", "13", ["15","20","22"], "Medium", "remainders", None, "13 = 2 × 5 + 3. 15 and 20 leave 0; 22 leaves 2."),
("A machine changes numbers by one rule. Input 4 gives output 13, and input 6 gives output 19. What is the output for input 10?", "31", ["29","34","25"], "Medium", "function machine rule (output = 3 × input + 1)", "<table class='data'><tr><th>Input</th><th>Output</th></tr><tr><td>4</td><td>13</td></tr><tr><td>6</td><td>19</td></tr><tr><td>10</td><td>?</td></tr></table>", "Rule: output = 3 × input + 1. 3 × 10 + 1 = 31."),
("In the pattern 2, 3, 5, 9, 17, ___, what is the next number?", "33", ["25","27","31"], "Medium", "difference pattern (differences 1, 2, 4, 8, ...)", None, "Differences double: 1, 2, 4, 8, 16. 17 + 16 = 33."),
("What is the next number in the pattern 1, 3, 9, 27, ___?", "81", ["54","36","63"], "Medium", "geometric pattern (× 3)", None, "Each term is 3 times the one before: 27 × 3 = 81."),
("What is 2.9 + 1.7?", "4.6", ["3.6","4.5","5.6"], "Easy", "adding decimals", None, "2.9 + 1.7 = 4.6."),
("What is 6.5 + 1.25?", "7.75", ["7.25","7.70","7.30"], "Hard", "adding decimals with different place values", None, "Write 6.50 + 1.25 = 7.75. Trap: 7.70 or 7.25 come from lining up digits wrong."),
("Which fraction is greater than 0.6?", "5/8", ["1/2","3/5","2/5"], "Hard", "comparing fraction to decimal", None, "5/8 = 0.625, which is greater than 0.6. 3/5 = 0.6 exactly."),
("Which fraction is less than 0.4?", "1/3", ["1/2","3/5","5/12"], "Hard", "comparing fraction to decimal", None, "1/3 ≈ 0.33, less than 0.4. 5/12 ≈ 0.42, which is greater."),
("What is the median of 4, 9, 2, 7, 5?", "5", ["4","7","6"], "Medium", "median", None, "Order: 2, 4, 5, 7, 9. The middle value is 5."),
("What is the range of 12, 3, 8, and 20?", "17", ["12","20","8"], "Medium", "range", None, "Range = largest − smallest = 20 − 3 = 17."),
("Which number is divisible by both 4 and 6?", "36", ["28","30","42"], "Medium", "divisibility by 4 and 6", None, "36 ÷ 4 = 9 and 36 ÷ 6 = 6. 28 fails 6, 30 fails 4, and 42 fails 4."),
("Which statement is always true?", "Every square is a rectangle.", ["Every rectangle is a square.","Every triangle has 4 sides.","A quadrilateral has 3 sides."], "Medium", "always-true statement about shapes", None, "A square has 4 right angles and opposite sides equal, so it is a rectangle. The reverse is not always true."),
("Which expression is equivalent to 16 × (13 + 19)?", "16 × 13 + 16 × 19", ["16 × 13 + 19","16 + 13 × 19","16 × 13 × 19"], "Hard", "distributive property", None, "Multiply 16 by each part of the sum."),
("A square has a perimeter of 24 cm. What is its area?", "36 sq cm", ["24 sq cm","12 sq cm","48 sq cm"], "Medium", "square area from perimeter", None, "Side = 24 ÷ 4 = 6. Area = 6 × 6 = 36."),
("Lois has 12 pencils. She loses one third of them. How many pencils does she have left?", "8", ["4","9","12"], "Medium", "fraction of a quantity", None, "One third of 12 is 4. 12 − 4 = 8."),
("A bag has 3 red cards and 5 blue cards. What is the probability of picking a blue card?", "5/8", ["3/8","3/5","5/3"], "Easy", "probability of one event", None, "5 blue out of 8 total = 5/8."),
("It is 3:00 PM in New York. Los Angeles is 3 hours behind New York. What time is it in Los Angeles?", "12:00 PM", ["6:00 PM","3:00 PM","9:00 AM"], "Medium", "time zones", None, "3:00 PM − 3 hours = 12:00 PM."),
("Which number is a multiple of both 3 and 7?", "21", ["14","24","28"], "Easy", "multiples", None, "21 = 3 × 7. 14 is not a multiple of 3, 24 is not a multiple of 7, and 28 is not a multiple of 3."),
("About how much is 49 × 21?", "about 1,000", ["about 500","about 2,000","about 100"], "Medium", "estimating a product", None, "Round to 50 × 20 = 1,000."),
("The table shows tickets sold: Friday 14, Saturday 22, Sunday 19. How many tickets were sold in all?", "55", ["45","51","59"], "Easy", "table total", "<table class='data'><tr><th>Day</th><th>Tickets</th></tr><tr><td>Friday</td><td>14</td></tr><tr><td>Saturday</td><td>22</td></tr><tr><td>Sunday</td><td>19</td></tr></table>", "14 + 22 + 19 = 55."),
("Which number leaves a remainder of 2 when divided by both 5 and 8?", "42", ["32","37","52"], "Hard", "remainders with two divisors", None, "42 = 8 × 5 + 2 and 42 = 5 × 8 + 2. Check each candidate against both divisors."),
("What is the value of the digit 7 in 3.472?", "7 hundredths", ["7 tenths","7 thousandths","7 tens"], "Medium", "decimal place value", None, "3.472: 4 is tenths, 7 is hundredths, 2 is thousandths."),
("Which list orders 1/2, 1/4, and 3/4 from least to greatest?", "1/4, 1/2, 3/4", ["3/4, 1/2, 1/4","1/2, 1/4, 3/4","1/4, 3/4, 1/2"], "Medium", "ordering fractions", None, "1/4 = 0.25, 1/2 = 0.5, 3/4 = 0.75."),
("What is the next number in the pattern 2, 4, 8, 16, ___?", "32", ["24","20","18"], "Easy", "patterns: doubling", None, "Each term doubles: 16 × 2 = 32."),
("Which statement is true?", "2 is even.", ["9 is prime.","15 is prime.","1 is prime."], "Medium", "true/false statements about numbers", None, "2 is even. 9 and 15 are divisible by 3; 1 is not prime."),
("What is the average of 4, 8, and 6?", "6", ["5","7","8"], "Medium", "average (mean)", None, "(4 + 8 + 6) ÷ 3 = 6."),
("A pattern of dots: each figure has 2 more dots than the one before. Figure 1 has 3 dots. How many dots does Figure 5 have?", "11", ["10","13","15"], "Hard", "figure pattern (linear)", None, "Figure n has 3 + 2(n − 1) dots. Figure 5: 3 + 8 = 11."),
]
assert len(P)==30
letters=['A']*8+['B']*8+['C']*7+['D']*7
for _ in range(1000):
    random.shuffle(letters)
    if not any(letters[i]==letters[i+1]==letters[i+2] for i in range(28)): break
items=[]
for i,(q,cor,dis,tier,topic,diag,why) in enumerate(P):
    L=letters[i]; idx='ABCD'.index(L)
    ch=list(dis); ch.insert(idx, cor)
    items.append(dict(n=i+1,q=q,ch=ch,ans=L,tier=tier,topic=topic,diag=diag,why=why,needs_diag=bool(diag),ref={"times_practised_before":0,"wrong_so_far":None}))
json.dump(items,open('ma1_items.json','w'),indent=1)
from collections import Counter
print(Counter(letters), 'diagrams:', sum(1 for x in items if x['diag']), 'tiers:', Counter(x['tier'] for x in items))
