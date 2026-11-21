"""MA Set 6 missed + timed-out problems (2026-11-20), same redo format as qr11-wrong: no answers showing until the
parent presses a button. Problems come from the exact published worksheet (grade_set.load_published_problems).
Writes worksheets/ma6-wrong.html."""
import os, sys, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from grade_set import load_published_problems

P = load_published_problems('ma', 6)
ROWS = {int(r['problem']): r for r in
        csv.DictReader(open(os.path.expanduser('~/Documents/HannahISEEMath/reviews/ma-set-6-times-graded.csv')))}
HER = {n: r['final_answer'] for n, r in ROWS.items()}
ASK = {
 3: 'The price went up to $80. What is 30% of $80? So what does "decreased by 30%" take away?',
 8: 'You found 15 plants. 15 out of how many? How do you write 15 out of 25 as a decimal?',
 12: 'Read the question again. Which comes first in the list, the greatest or the least?',
 14: 'How did you get 196? Which part is the top box and which is the bottom box? What are each box\'s three sides?',
 15: 'How many cards does Max have now? Then how many did he have before Ella gave him &#9675;?',
 16: 'You found 56. What does 56 stand for? What did the question ask?',
 17: 'Find the smallest number in BOTH rows. Which day is it?',
 18: 'How many minutes is 1 hour? So how many minutes is 1 1/6 hours?',
 19: 'If the blank is 15, what gap takes you from 15 to 35? Does it fit the gaps 1, 2, 4?',
 20: 'About how much is 47 &divide; 6? Is it closer to 5 or to 8? Then times about 100?',
 21: 'If purple is 2/5 of the bag, what fraction are the other 18 marbles?',
 27: 'Is 12 a multiple of both 4 and 6? Is 12 a multiple of 24? So which numbers count?',
 29: 'How did you get 10? The perimeter goes around all 4 sides. What are length + width together?',
}
WRONG = [3, 8, 12, 14, 15, 16, 17, 18, 19, 20, 21, 27, 29]
NOTREACHED = [30]   # random pick as time ran out, not redone
for n in WRONG:
    assert HER[n] != P[n]['ans'], n
REDO = [n for n in WRONG if ROWS[n]['seconds'] == '']
assert REDO == [20, 21, 27, 29], REDO

def choices(n):
    return '<div class="choices">' + ''.join(
        f'<button type="button" class="choice" data-l="{L}"><b>{L}</b>&nbsp; {html}</button>' for L, html in P[n]['choices']) + '</div>'

cards = ''
for i, n in enumerate(WRONG + NOTREACHED, 1):
    p = P[n]
    nr = n in NOTREACHED
    her_btn = '<button type="button" class="rev her">Show her answer</button>'
    her_box = f'<div class="herbox" hidden>Her answer on 11/20: <b>{HER[n]}</b>' + (' (redone after the timer; her timed pick was random; no time recorded)' if n in REDO else '') + (' (random pick as time ran out, right by chance; not redone)' if nr else '') + '</div>'
    ask = f'<div class="ask"><b>Ask her:</b> {ASK[n]}</div>' if ASK.get(n) else ''
    src = f'MA6 #{n}' + (' &middot; redone after the timer' if n in REDO else '') + (' &middot; random pick, not redone' if nr else '')
    cards += (f'<section class="card" data-ans="{p["ans"]}" data-her="{HER.get(n, "")}">'
              f'<div class="num">{i}. &nbsp;<span class="src">{src}</span></div>'
              f'<div class="q">{p["q"]}</div>' + (f'<div class="diag">{p["diag"]}</div>' if p['diag'] else '') + choices(n) +
              f'<div class="btns">{her_btn}<button type="button" class="rev key">Show answer + explanation</button></div>'
              f'{her_box}<div class="keybox" hidden><b>Answer: {p["ans"]}.</b> {p["why"]}{ask}</div></section>')

CSS = ''':root{--bg:#EEF2F0;--surface:#FFFFFF;--surface-alt:#E7EDEA;--ink:#1E2A28;--muted:#57655F;--border:#D6DFDA;--accent:#1C7A69;--accent-soft:#E1F2EC;--right:#2E7D4F;--right-soft:#E3F3E8;--wrong:#B5452E;--wrong-soft:#FBE7E1;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12181A;--surface:#1B2224;--surface-alt:#212A2C;--ink:#E8EFEC;--muted:#9FB0AA;--border:#2C3739;--accent:#4FC4AC;--accent-soft:rgba(79,196,172,0.14);--right:#6FD39A;--right-soft:rgba(111,211,154,0.14);--wrong:#E58A74;--wrong-soft:rgba(229,138,116,0.14);color-scheme:dark;}}
:root[data-theme="dark"]{--bg:#12181A;--surface:#1B2224;--surface-alt:#212A2C;--ink:#E8EFEC;--muted:#9FB0AA;--border:#2C3739;--accent:#4FC4AC;--accent-soft:rgba(79,196,172,0.14);--right:#6FD39A;--right-soft:rgba(111,211,154,0.14);--wrong:#E58A74;--wrong-soft:rgba(229,138,116,0.14);color-scheme:dark;}
body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,sans-serif;line-height:1.45;}
.wrap{max-width:900px;margin:0 auto;padding:28px 16px 64px;}h1{font-family:Georgia,serif;font-size:1.8rem;margin:0 0 6px;}
.lede{color:var(--muted);margin:0 0 18px;}.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 18px;margin:0 0 14px;}
.num{font-family:Georgia,serif;font-style:italic;color:var(--muted);margin-bottom:4px;}.src{font-size:0.8rem;}.q{margin:0 0 10px;}.diag{margin:8px 0 12px;}
.choices{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;}@media (max-width:520px){.choices{grid-template-columns:1fr;}}
button.choice{font:inherit;text-align:left;cursor:pointer;color:var(--ink);padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);}
button.choice.sel{border-color:var(--accent);background:var(--accent-soft);font-weight:600;}
button.choice.right{border-color:var(--right);background:var(--right-soft);}button.choice.her{border-color:var(--wrong);background:var(--wrong-soft);}
.btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;}.rev{font:inherit;font-size:0.85rem;padding:6px 12px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);cursor:pointer;}
.herbox,.keybox{margin-top:10px;border-left:3px solid var(--accent);padding:6px 10px;color:var(--muted);font-size:0.93rem;}.herbox{border-color:var(--wrong);}.ask{margin-top:6px;color:var(--ink);}
table.data{border-collapse:collapse;font-size:0.9rem;}table.data th,table.data td{border:1px solid var(--border);padding:4px 10px;text-align:left;}
.frac{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1;font-size:0.82em;margin:0 1px;}.frac .n{border-bottom:2px solid currentColor;padding:0 3px 2px;}.frac .d{padding:2px 3px 0;}
svg{max-width:100%;height:auto;}'''
JS = '''document.querySelectorAll('.card').forEach(function(c){
 c.querySelectorAll('.choice').forEach(function(b){b.addEventListener('click',function(){c.querySelectorAll('.choice').forEach(function(x){x.classList.remove('sel')});b.classList.add('sel');});});
 function tog(btn,box,on,off,mark){btn.addEventListener('click',function(){var show=box.hidden;box.hidden=!show;btn.textContent=show?off:on;mark(show);});}
 if(c.querySelector('.rev.her'))tog(c.querySelector('.rev.her'),c.querySelector('.herbox'),'Show her answer','Hide her answer',function(s){c.querySelector('.choice[data-l="'+c.dataset.her+'"]').classList.toggle('her',s);});
 tog(c.querySelector('.rev.key'),c.querySelector('.keybox'),'Show answer + explanation','Hide answer',function(s){c.querySelector('.choice[data-l="'+c.dataset.ans+'"]').classList.toggle('right',s);});
});'''
page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>MA6 Problems to Redo</title><style>{CSS}</style></head><body><div class="wrap">'
        f'<h1>MA Set 6 &mdash; Problems to Redo</h1><p class="lede">The {len(WRONG)} problems she missed on 11/20 ({len(REDO)} of them in her redo of #20&ndash;29 after the timer), then #30, a random pick she has not redone, exactly as they were on the worksheet. '
        f'Nothing is shown until you press a button. No timer.</p>{cards}</div><script>{JS}</script></body></html>')
out = os.path.join(HERE, '..', '..', 'worksheets', 'ma6-wrong.html')
open(out, 'w').write(page)
print('wrote', out, len(WRONG), len(NOTREACHED))
