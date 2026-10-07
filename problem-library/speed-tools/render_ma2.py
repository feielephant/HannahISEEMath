import json, html
S = '/private/tmp/claude-501/-Users-kxieztt-Documents-HannahISEEMath/5e000592-8898-4fa3-a99a-7f35349cf51d/scratchpad/'
REPO = '/Users/kxieztt/Documents/HannahISEEMath-repo/'
items = json.load(open(S + 'ma2_items.json'))

W1 = open(REPO + 'worksheets/ma-set-1.html').read()
K1 = open(REPO + 'worksheets/ma-set-1-answer-key.html').read()

def fix(s):
    return (s.replace('Set 1', 'Set 2').replace('ma-set-1', 'ma-set-2'))

ws_head = fix(W1[:W1.index('<div class="card">')])
ws_tail = fix(W1[W1.index('<script>'):])
k_head = fix(K1[:K1.index('<div class="card">')])

def card(it, key):
    diag = f'<div class="diag">{it["diag"]}</div>' if it.get('diag') else ''
    if key:
        ch = ''.join(f'<span><b>{L}</b>&nbsp; {html.escape(c)}</span>' for L, c in zip('ABCD', it['ch']))
    else:
        ch = ''.join(f'<button type="button" class="choice" data-qid="{it["n"]}" data-letter="{L}"><b>{L}</b>&nbsp; {html.escape(c)}</button>' for L, c in zip('ABCD', it['ch']))
    body = f'<div class="card"><div class="num">{it["n"]}. <span class="ptime" id="pt{it["n"]}"></span></div><div class="q">{html.escape(it["q"])}</div>{diag}<div class="choices">{ch}</div>'
    if key:
        r = it['ref']
        body += f'<div class="key"><b>Answer: {it["ans"]}.</b> {html.escape(it["why"])}</div>'
        body += f'<div class="ref">Tier: {it["tier"]} · Topic: {html.escape(it["topic"])} · Diagram: {"yes" if it["needs_diag"] else "no"} · Times practised before: {r["times_practised_before"]} · Wrong so far: {r["wrong_so_far"]}/{r["graded_so_far"]}</div>'
    return body + '</div>'

ws = ws_head + ''.join(card(it, False) for it in items) + ws_tail
key_html = k_head + ''.join(card(it, True) for it in items) + '</div></body></html>'
open(REPO + 'worksheets/ma-set-2.html', 'w').write(ws)
open(REPO + 'worksheets/ma-set-2-answer-key.html', 'w').write(key_html)
print('written')
