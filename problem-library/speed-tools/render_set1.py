import json, html
items=json.load(open('/tmp/gen/set1/set1_items.json'))
CSS='''
:root{--bg:#EEF2F0;--surface:#FFFFFF;--surface-alt:#E7EDEA;--ink:#1E2A28;--ink-muted:#57655F;--border:#D6DFDA;--accent:#1C7A69;--accent-ink:#0F5648;--accent-soft:#E1F2EC;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12181A;--surface:#1B2224;--surface-alt:#212A2C;--ink:#E8EFEC;--ink-muted:#9FB0AA;--border:#2C3739;--accent:#4FC4AC;--accent-ink:#8FE0CC;--accent-soft:rgba(79,196,172,0.14);color-scheme:dark;}}
:root[data-theme="dark"]{--bg:#12181A;--surface:#1B2224;--surface-alt:#212A2C;--ink:#E8EFEC;--ink-muted:#9FB0AA;--border:#2C3739;--accent:#4FC4AC;--accent-ink:#8FE0CC;--accent-soft:rgba(79,196,172,0.14);color-scheme:dark;}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Public Sans",system-ui,sans-serif;line-height:1.45;}
.wrap{max-width:900px;margin:0 auto;padding:32px 18px 64px;}
h1{font-family:Georgia,serif;font-size:1.9rem;margin:0 0 6px;}
.lede{color:var(--ink-muted);margin:0 0 20px;}
.timer{display:inline-block;border:1px solid var(--border);border-radius:8px;padding:8px 14px;background:var(--surface);font-weight:600;margin-bottom:22px;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 18px;margin:0 0 14px;}
.num{font-family:Georgia,serif;font-style:italic;color:var(--ink-muted);margin-bottom:4px;}
.q{margin:0 0 10px;}
.diag{margin:8px 0 12px;color:var(--ink);}
.choices{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;}
.choices span{padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);}
table.data{border-collapse:collapse;font-size:0.9rem;}
table.data th,table.data td{border:1px solid var(--border);padding:4px 10px;text-align:left;}
.key{border-left:3px solid var(--accent);padding:6px 10px;margin-top:8px;color:var(--ink-muted);font-size:0.92rem;}
.ref{font-size:0.8rem;color:var(--ink-muted);margin-top:4px;}
button.choice{font:inherit;text-align:left;cursor:pointer;color:var(--ink);padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);}
button.choice:hover{border-color:var(--ink-muted);}
button.choice.selected{background:var(--accent-soft);border-color:var(--accent);font-weight:600;}
.ptime{font-size:0.85rem;color:var(--accent-ink);font-weight:600;}
.card,.q,.diag,.choices{-webkit-user-select:none;user-select:none;}
.sticky-top{position:sticky;top:0;z-index:5;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--border);}
.progress{font-weight:600;color:var(--accent-ink);}
@media (max-width:520px){.choices{grid-template-columns:1fr;}}
'''
def card(it, key):
    diag = f'<div class="diag">{it["diag"]}</div>' if it.get('diag') else ''
    if key:
        ch = ''.join(f'<span><b>{L}</b>&nbsp; {html.escape(c)}</span>' for L,c in zip('ABCD', it['ch']))
    else:
        ch = ''.join(f'<button type="button" class="choice" data-qid="{it["n"]}" data-letter="{L}"><b>{L}</b>&nbsp; {html.escape(c)}</button>' for L,c in zip('ABCD', it['ch']))
    body = f'<div class="card"><div class="num">{it["n"]}. <span class="ptime" id="pt{it["n"]}"></span></div><div class="q">{html.escape(it["q"])}</div>{diag}<div class="choices">{ch}</div>'
    if key:
        r=it['ref']
        body += f'<div class="key"><b>Answer: {it["ans"]}.</b> {html.escape(it["why"])}</div>'
        body += f'<div class="ref">Tier: {it["tier"]} · Topic: {html.escape(it["topic"])} · Diagram: {"yes" if it["needs_diag"] else "no"} · Times practised before: {r["times_practised_before"]} · Wrong so far: {r["wrong_so_far"]}/{r["graded_so_far"]}</div>'
    return body + '</div>'
ws = ['<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Speed Set 1</title><style>'+CSS+'</style></head><body><div class="wrap">',
      '<h1>Speed Practice — Set 1</h1><p class="lede">Quantitative Reasoning · 38 problems · 35 minutes · choose one answer (A–D) for each.</p>',
      '<div class="sticky-top"><div class="timer">Time left: <span id="clock">35:00</span> <button type="button" class="choice" id="go">Start</button> <button type="button" class="choice" id="rst">Reset</button></div><div class="progress">Answered: <span id="count">0</span> / 38</div></div>', '<div id="timing" style="display:none"><h2>Timing</h2><p>Total: <span id="total">0:00</span> · Answered: <span id="answered">0</span> / 38</p><table class="data"><tr><th>#</th><th>Time (s)</th><th>Answer</th></tr><tbody id="rows"></tbody></table><p><button type="button" class="choice" id="dl">Download times (CSV)</button> <button type="button" class="choice" id="clr">Clear all answers</button></p></div>']
ws += [card(it, False) for it in items]
ws.append('<script>(function(){var K="speed-set-1-v1",T="speed-set-1-times";var st={},ev=[];try{st=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}try{ev=JSON.parse(localStorage.getItem(T)||"[]")}catch(e){}function sv(){try{localStorage.setItem(K,JSON.stringify(st));localStorage.setItem(T,JSON.stringify(ev))}catch(e){}}function upd(){var n=Object.keys(st).filter(function(k){return !!st[k]}).length;document.getElementById("count").textContent=n;}function fmt(s){s=Math.max(0,Math.round(s));return Math.floor(s/60)+":"+("0"+(s%60)).slice(-2);}function firsts(){var seen={},out=[];for(var i=0;i<ev.length;i++){var e=ev[i];if(e.letter&&!seen[e.q]){seen[e.q]=1;out.push({q:e.q,letter:e.letter,sec:(i===0?0:(e.t-ev[i-1].t)/1000),t:e.t});}}return out;}function summary(){var f=firsts();var box=document.getElementById("timing");box.style.display="block";if(!f.length){document.getElementById("rows").innerHTML="";document.getElementById("answered").textContent=0;document.getElementById("total").textContent="0:00";return;}var rows=f.map(function(r){return "<tr><td>"+r.q+"</td><td>"+Math.round(r.sec)+"</td><td>"+r.letter+"</td></tr>";}).join("");document.getElementById("rows").innerHTML=rows;document.getElementById("answered").textContent=f.length;var total=ev.length?(ev[ev.length-1].t-ev[0].t)/1000:0;document.getElementById("total").textContent=fmt(total);}function paint(){document.querySelectorAll("button.choice").forEach(function(b){b.classList.toggle("selected", st[b.dataset.qid]===b.dataset.letter);});document.querySelectorAll(".ptime").forEach(function(x){x.textContent="";});firsts().forEach(function(r){var el=document.getElementById("pt"+r.q);if(el)el.textContent="· "+Math.round(r.sec)+" s";});upd();summary();}document.addEventListener("click",function(e){if(e.target.id==="clr"){if(confirm("Clear all answers and times?")){st={};ev=[];sv();paint();}return;}var b=e.target.closest("button.choice");if(b&&b.dataset.qid){var same=st[b.dataset.qid]===b.dataset.letter;st[b.dataset.qid]=same?null:b.dataset.letter;ev.push({q:b.dataset.qid,letter:same?null:b.dataset.letter,t:Date.now()});sv();paint();return;}if(e.target.id==="dl"){var f=firsts();var csv="problem,seconds,answer\\n"+f.map(function(r){return r.q+","+Math.round(r.sec)+","+r.letter}).join("\\n");var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));a.download="speed-set-1-times.csv";document.body.appendChild(a);a.click();a.remove();}});["copy","cut","contextmenu","selectstart","dragstart"].forEach(function(ev2){document.addEventListener(ev2,function(e){if(e.target.id!=="dl")e.preventDefault();});});paint();})();</script>')
ws.append('<script>(function(){var K="speed-set-1-clock";var TOTAL=2100;var st={rem:TOTAL,run:false,last:0};try{var x=JSON.parse(localStorage.getItem(K)||"null");if(x)st=x;}catch(e){}function sv(){try{localStorage.setItem(K,JSON.stringify(st));}catch(e){}}function show(){var r=Math.max(0,Math.round(st.rem));var m=Math.floor(r/60),s=r%60;document.getElementById("clock").textContent=m+":"+("0"+s).slice(-2);document.getElementById("go").textContent=st.run?"Running":"Start";document.getElementById("go").disabled=st.run;}function tick(){if(st.run){var now=Date.now();st.rem=Math.max(0,st.rem-(now-st.last)/1000);st.last=now;if(st.rem<=0){st.run=false;}sv();}show();}document.getElementById("go").addEventListener("click",function(){if(!st.run&&st.rem>0){st.run=true;st.last=Date.now();sv();show();}});document.getElementById("rst").addEventListener("click",function(){if(confirm("Reset the clock to 35:00?")){st={rem:TOTAL,run:false,last:0};sv();show();}});show();setInterval(tick,500);})();</script>')
ws.append('</div></body></html>')
open('/tmp/gen/set1/set1_worksheet.html','w').write(''.join(ws))
kh = ['<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Speed Set 1 — Key</title><style>'+CSS+'</style></head><body><div class="wrap">',
      '<h1>Speed Practice — Set 1 · Answer Key</h1><p class="lede">For parent use. Tier, topic, and reference show how each problem connects to Hannah\'s gaps and past practice.</p>']
kh += [card(it, True) for it in items]
kh.append('</div></body></html>')
open('/tmp/gen/set1/set1_key.html','w').write(''.join(kh))
print('rendered')
