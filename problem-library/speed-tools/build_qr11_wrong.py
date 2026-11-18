"""QR Set 11 wrong + not-reached problems (2026-11-17), parent request: a review page with NO answers showing until the
parent asks. Problems come from the exact published worksheet (grade_set.load_published_problems). Each card
has two buttons: "Her answer" and "Answer + explanation" (which also shows a question to ask her).
Writes worksheets/qr10-wrong.html."""
import os, sys, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from grade_set import load_published_problems

P = load_published_problems('qr', 11)
HER = {int(r['problem']): r['final_answer'] for r in
       csv.DictReader(open(os.path.expanduser('~/Documents/HannahISEEMath/reviews/speed-set-11-times-graded.csv')))}
ASK = {
 8: '2 cm stand for 15 km. How many km does 1 cm stand for?',
 14: 'How many 10s are in 20? How many in 1,000? So how many in 20 &times; 1,000?',
 15: 'You first picked C, then D. Which one did you mean? What is the regular price?',
 17: 'If the width is 6, what is the length? Is it a square?',
 23: 'How many jumps of 4 from the 1st number to the 2nd? To the 25th?',
 24: 'You had $0.70 first. What was the question asking for after that?',
 30: 'You found 84 minutes. What does 84 stand for? What did the question ask?',
 35: 'Write the number first. Which digit is in the ones place? The tens place? The hundreds place?',
}
WRONG = [8, 14, 15, 17, 23, 24, 30, 35]
NOTREACHED = []
for n in WRONG:
    assert HER[n] != P[n]['ans'], n

def choices(n):
    return '<div class="choices">' + ''.join(
        f'<button type="button" class="choice" data-l="{L}"><b>{L}</b>&nbsp; {html}</button>' for L, html in P[n]['choices']) + '</div>'

cards = ''
for i, n in enumerate(WRONG + NOTREACHED, 1):
    p = P[n]
    nr = n in NOTREACHED
    her_btn = '' if nr else '<button type="button" class="rev her">Show her answer</button>'
    her_box = '' if nr else f'<div class="herbox" hidden>Her answer on 11/17: <b>{HER[n]}</b></div>'
    ask = f'<div class="ask"><b>Ask her:</b> {ASK[n]}</div>' if ASK[n] else ''
    src = f'Set 11 #{n}' + (' &middot; not reached' if nr else '')
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
        f'<title>QR11 Missed Problems</title><style>{CSS}</style></head><body><div class="wrap">'
        f'<h1>QR Set 11 &mdash; Problems to Redo</h1><p class="lede">The {len(WRONG)} problems she missed on 11/17 (#30 and #35 were answered on paper), exactly as they were on the worksheet. '
        f'Nothing is shown until you press a button. No timer.</p>{cards}</div><script>{JS}</script></body></html>')
out = os.path.join(HERE, '..', '..', 'worksheets', 'qr11-wrong.html')
open(out, 'w').write(page)
print('wrote', out, len(WRONG), len(NOTREACHED))
