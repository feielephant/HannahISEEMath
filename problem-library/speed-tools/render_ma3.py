import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'worksheets')
P = json.load(open(os.path.join(HERE, 'ma3_problems.json')))
N = len(P)
SLUG = 'ma-set-3'

HEAD_STYLE = ':root{--bg:#EEF2F0;--surface:#FFFFFF;--surface-alt:#E7EDEA;--ink:#1E2A28;--ink-muted:#57655F;--border:#D6DFDA;--accent:#1C7A69;--accent-ink:#0F5648;--accent-soft:#E1F2EC;}@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12181A;--surface:#1B2224;--surface-alt:#212A2C;--ink:#E8EFEC;--ink-muted:#9FB0AA;--border:#2C3739;--accent:#4FC4AC;--accent-ink:#8FE0CC;--accent-soft:rgba(79,196,172,0.14);color-scheme:dark;}}:root[data-theme="dark"]{--bg:#12181A;--surface:#1B2224;--surface-alt:#212A2C;--ink:#E8EFEC;--ink-muted:#9FB0AA;--border:#2C3739;--accent:#4FC4AC;--accent-ink:#8FE0CC;--accent-soft:rgba(79,196,172,0.14);color-scheme:dark;}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Public Sans",system-ui,sans-serif;line-height:1.45;}.wrap{max-width:900px;margin:0 auto;padding:32px 18px 64px;}h1{font-family:Georgia,serif;font-size:1.9rem;margin:0 0 6px;}.lede{color:var(--ink-muted);margin:0 0 20px;}.timer{display:inline-block;border:1px solid var(--border);border-radius:8px;padding:8px 14px;background:var(--surface);font-weight:600;margin-bottom:22px;}.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 18px;margin:0 0 14px;}.num{font-family:Georgia,serif;font-style:italic;color:var(--ink-muted);margin-bottom:4px;}.q{margin:0 0 10px;}.diag{margin:8px 0 12px;color:var(--ink);}.choices{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;}.choices > span{padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);}table.data{border-collapse:collapse;font-size:0.9rem;}table.data th,table.data td{border:1px solid var(--border);padding:4px 10px;text-align:left;}.key{border-left:3px solid var(--accent);padding:6px 10px;margin-top:8px;color:var(--ink-muted);font-size:0.92rem;}.ref{font-size:0.8rem;color:var(--ink-muted);margin-top:4px;}button.choice{font:inherit;text-align:left;cursor:pointer;color:var(--ink);padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);}button.choice:hover{border-color:var(--ink-muted);}button.choice.selected{background:var(--accent-soft);border-color:var(--accent);font-weight:600;}.ptime{font-size:0.85rem;color:var(--accent-ink);font-weight:600;}.card,.q,.diag,.choices{-webkit-user-select:none;user-select:none;}.sticky-top{position:sticky;top:0;z-index:5;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--border);}.progress{font-weight:600;color:var(--accent-ink);}@media (max-width:520px){.choices{grid-template-columns:1fr;}}.logwrap{max-height:320px;overflow:auto;margin-bottom:12px}button.choice:disabled{opacity:0.5;cursor:not-allowed;}.frac{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1;font-size:0.82em;margin:0 1px;}.frac .n{border-bottom:2px solid currentColor;padding:0 3px 2px;}.frac .d{padding:2px 3px 0;}.pictograph{margin:8px 0;}.pictorow{display:flex;align-items:center;gap:8px;margin:3px 0;}.piclabel{min-width:60px;font-weight:600;}.picicons{letter-spacing:3px;font-size:1.25em;color:var(--accent-ink);}.picicons .half{display:inline-block;width:0.52em;overflow:hidden;vertical-align:top;}.pictokey{font-size:0.82em;color:var(--ink-muted);margin-top:6px;}.testbar{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;flex-wrap:wrap;}.navgrid{display:flex;flex-wrap:wrap;gap:4px;flex:1;min-width:0;}.navbtn{width:30px;height:30px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);color:var(--ink);font:inherit;font-size:0.78rem;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;}.navbtn.answered{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-ink);font-weight:600;}.navbtn.current{outline:2px solid var(--accent);outline-offset:1px;font-weight:700;}.timerbox{display:flex;flex-direction:column;align-items:flex-end;gap:6px;flex-shrink:0;}.navcontrols{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;}.bignav{font:inherit;padding:10px 16px;border:1px solid var(--border);border-radius:8px;background:var(--surface-alt);color:var(--ink);cursor:pointer;font-weight:600;}.bignav:disabled{opacity:0.4;cursor:not-allowed;}.timingtoggle{font-size:0.8rem;color:var(--ink-muted);background:none;border:none;text-decoration:underline;cursor:pointer;padding:4px 0;}'

def head(title):
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>'
            f'<style>{HEAD_STYLE}</style></head>')

def choices_html_live(n, choices):
    out = '<div class="choices">'
    for L in ["A","B","C","D"]:
        out += f'<button type="button" class="choice" data-qid="{n}" data-letter="{L}"><b>{L}</b>&nbsp; {choices[L]}</button>'
    out += '</div>'
    return out

def choices_html_key(choices):
    out = '<div class="choices">'
    for L in ["A","B","C","D"]:
        out += f'<span><b>{L}</b>&nbsp; {choices[L]}</span>'
    out += '</div>'
    return out

# ---- live worksheet ----
cards = []
for p in P:
    n = p["n"]
    diag = f'<div class="diag">{p["diagram"]}</div>' if p.get("diagram") else ''
    cards.append(f'<div class="card" data-n="{n}"><div class="num">{n}. <span class="ptime" id="pt{n}"></span></div>'
                 f'<div class="q">{p["q"]}</div>{diag}{choices_html_live(n, p["choices"])}</div>')

live = head("Math Achievement Set 3") + '<style>.card{display:none;}.card.active{display:block;}</style><body><div class="wrap">'
live += f'<h1>Math Achievement Practice — Set 3</h1><p class="lede">Mathematics Achievement · {N} problems · 30 minutes · choose one answer (A–D) for each.</p>'
live += f'<div class="sticky-top"><div class="testbar"><div class="navgrid" id="navgrid"></div><div class="timerbox"><div class="timer">Time left: <span id="clock">30:00</span></div><button type="button" class="bignav" id="go">Start</button><button type="button" class="bignav" id="end" disabled>Submit</button></div></div><div class="navcontrols"><button type="button" class="bignav" id="prev">← Back</button><span class="progress">Answered: <span id="count">0</span> / {N}</span><button type="button" class="bignav" id="next">Next →</button></div><p><button type="button" class="timingtoggle" id="toggletiming">Show timing details (parent)</button></p></div>'
live += f'<div id="timing" style="display:none"><p>Total: <span id="total">0:00</span> · Answered: <span id="answered">0</span> / {N}</p><table class="data"><tr><th>#</th><th>Time (s)</th><th>First answer</th><th>Final answer</th></tr><tbody id="rows"></tbody></table><p><button type="button" class="bignav" id="dl">Download times (CSV)</button> <button type="button" class="bignav" id="dl2">Download click log (CSV)</button> <button type="button" class="bignav" id="clr">Clear all answers</button></p></div>'
live += ''.join(cards)
live += '</div>'

SCRIPT = ('''<script>(function(){
var N=%d,K="%s-v1",T="%s-times",IDX="%s-idx";
var st={},clicks=[],visits=[],idx=1;
try{st=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
try{var saved=JSON.parse(localStorage.getItem(T)||"{}");clicks=saved.clicks||[];visits=saved.visits||[];}catch(e){}
try{idx=parseInt(localStorage.getItem(IDX)||"1",10)||1}catch(e){}
function sv(){try{localStorage.setItem(K,JSON.stringify(st));localStorage.setItem(T,JSON.stringify({clicks:clicks,visits:visits}));localStorage.setItem(IDX,String(idx));}catch(e){}}
function fmt(s){s=Math.max(0,Math.round(s));return Math.floor(s/60)+":"+("0"+(s%%60)).slice(-2);}

var visitStart=null, visitN=null;
function clockRunning(){ return window.__clockRunning===true; }
function closeVisit(now){
  if(visitN!==null && visitStart!==null && now>visitStart){ visits.push({n:visitN,start:visitStart,end:now}); }
  visitStart=null; visitN=null;
}
function openVisit(now){ if(clockRunning()){ visitStart=now; visitN=idx; } }
function secondsFor(n){
  var tot=0;
  visits.forEach(function(v){ if(v.n===n) tot += (v.end-v.start)/1000; });
  if(visitN===n && visitStart!==null) tot += (Date.now()-visitStart)/1000;
  return tot;
}
function answeredCount(){ return Object.keys(st).filter(function(k){return !!st[k];}).length; }
function firstFinalFor(n){
  var cs = clicks.filter(function(c){return c.q===String(n);});
  if(!cs.length) return {first:null, final:null};
  return {first: cs[0].letter, final: st[n]||null};
}

function render(){
  document.querySelectorAll(".card").forEach(function(c){
    c.classList.toggle("active", parseInt(c.dataset.n,10)===idx);
  });
  document.querySelectorAll("button.choice[data-qid]").forEach(function(b){
    b.classList.toggle("selected", st[b.dataset.qid]===b.dataset.letter);
  });
  var grid=document.getElementById("navgrid");
  grid.innerHTML="";
  for(var i=1;i<=N;i++){
    var b=document.createElement("button");
    b.type="button"; b.className="navbtn"+(st[i]?" answered":"")+(i===idx?" current":"");
    b.textContent=i;
    (function(n){ b.addEventListener("click",function(){ goTo(n); }); })(i);
    grid.appendChild(b);
  }
  document.getElementById("count").textContent=answeredCount();
  document.getElementById("prev").disabled = idx<=1;
  document.getElementById("next").disabled = idx>=N;
  renderSummary();
}
function goTo(n){
  if(n<1||n>N) return;
  if(n===idx){ render(); return; }
  var now=Date.now();
  closeVisit(now);
  idx=n;
  openVisit(now);
  sv(); render();
}
document.getElementById("prev").addEventListener("click",function(){ goTo(idx-1); });
document.getElementById("next").addEventListener("click",function(){ goTo(idx+1); });
document.addEventListener("keydown",function(e){
  if(e.key==="ArrowLeft"){ e.preventDefault(); goTo(idx-1); }
  else if(e.key==="ArrowRight"){ e.preventDefault(); goTo(idx+1); }
});
document.addEventListener("click",function(e){
  if(e.target.id==="clr"){
    if(confirm("Clear all answers, times, and the timer?")){
      st={}; clicks=[]; visits=[]; visitStart=null; visitN=null;
      sv(); if(window.__clockReset) window.__clockReset();
      render();
    }
    return;
  }
  var b=e.target.closest("button.choice");
  if(b && b.dataset.qid){
    var same = st[b.dataset.qid]===b.dataset.letter;
    var letter = same ? null : b.dataset.letter;
    st[b.dataset.qid] = letter;
    clicks.push({q:b.dataset.qid, letter:letter, t:Date.now()});
    sv(); render();
    return;
  }
  if(e.target.id==="dl"){
    var rows=["problem,seconds,first_answer,final_answer"];
    for(var i=1;i<=N;i++){
      var ff=firstFinalFor(i);
      if(ff.first===null) continue;
      rows.push(i+","+Math.round(secondsFor(i))+","+ff.first+","+(ff.final||""));
    }
    save("%s-times.csv", rows.join("\\n"));
    return;
  }
  if(e.target.id==="dl2"){
    var t0 = clicks.length?clicks[0].t:Date.now();
    var prevByQ={};
    var rows2=["seq,problem,elapsed_s,clock,action,letter,previous"];
    clicks.forEach(function(c,i){
      var prev = prevByQ[c.q]!==undefined ? prevByQ[c.q] : null;
      var kind = c.letter===null ? "cleared" : (prev===null ? "chose" : "changed");
      rows2.push((i+1)+","+c.q+","+((c.t-t0)/1000).toFixed(1)+","+new Date(c.t).toLocaleTimeString()+","+kind+","+(c.letter||"")+","+(prev||""));
      prevByQ[c.q]=c.letter;
    });
    save("%s-click-log.csv", rows2.join("\\n"));
    return;
  }
});
["copy","cut","contextmenu","selectstart","dragstart"].forEach(function(ev2){
  document.addEventListener(ev2,function(e){ if(e.target.id!=="dl"&&e.target.id!=="dl2") e.preventDefault(); });
});
function save(name,csv){
  var a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));
  a.download=name; document.body.appendChild(a); a.click(); a.remove();
}
function renderSummary(){
  var box=document.getElementById("timing");
  if(!box) return;
  var answered=[];
  for(var i=1;i<=N;i++){ var ff=firstFinalFor(i); if(ff.first!==null) answered.push({n:i,ff:ff,sec:secondsFor(i)}); }
  if(!answered.length){ document.getElementById("rows").innerHTML=""; document.getElementById("answered").textContent=0; document.getElementById("total").textContent="0:00"; return; }
  document.getElementById("rows").innerHTML = answered.map(function(r){
    return "<tr><td>"+r.n+"</td><td>"+Math.round(r.sec)+"</td><td>"+r.ff.first+"</td><td>"+(r.ff.final||"")+"</td></tr>";
  }).join("");
  document.getElementById("answered").textContent = answered.length;
  var totalSec = visits.reduce(function(a,v){return a+(v.end-v.start)/1000;},0) + (visitStart!==null?(Date.now()-visitStart)/1000:0);
  document.getElementById("total").textContent = fmt(totalSec);
}

// ---- timer ----
var CK="%s-clock", TOTAL=1800;
var cst={rem:TOTAL,run:false,last:0};
try{var x=JSON.parse(localStorage.getItem(CK)||"null"); if(x) cst=x;}catch(e){}
function csv2(){try{localStorage.setItem(CK,JSON.stringify(cst));}catch(e){}}
function lock(){ var L=!cst.run; document.querySelectorAll("button.choice[data-qid]").forEach(function(b){b.disabled=L;}); }
function show(){
  window.__clockRunning = cst.run;
  var r=Math.max(0,Math.round(cst.rem)); var m=Math.floor(r/60), s=r%%60;
  var status = cst.rem<=0 ? " — time\\u2019s up" : (cst.submitted ? " — submitted" : (cst.run?"":" — press Start to unlock"));
  document.getElementById("clock").textContent=m+":"+("0"+s).slice(-2)+status;
  document.getElementById("go").textContent=cst.run?"Running":"Start";
  document.getElementById("go").disabled=cst.run||cst.submitted;
  if(endBtn) endBtn.disabled=!cst.run;
  lock();
}
function tick(){
  if(cst.run){
    var now=Date.now();
    cst.rem=Math.max(0,cst.rem-(now-cst.last)/1000);
    cst.last=now;
    if(cst.rem<=0){ cst.run=false; closeVisit(now); sv(); }
    csv2();
  }
  show(); renderSummary();
}
document.getElementById("go").addEventListener("click",function(){
  if(!cst.run && cst.rem>0 && !cst.submitted){
    cst.run=true; cst.last=Date.now(); csv2(); show();
    openVisit(Date.now()); sv(); render();
  }
});
var endBtn=document.getElementById("end");
if(endBtn){
  endBtn.addEventListener("click",function(){
    if(!cst.run) return;
    if(confirm("Submit now and stop the timer? You can still look back at your answers, but the clock won\\'t run again.")){
      var now=Date.now();
      cst.run=false; cst.submitted=true; closeVisit(now); csv2(); show();
      sv(); render();
    }
  });
}
window.__clockReset=function(){ cst={rem:TOTAL,run:false,last:0,submitted:false}; csv2(); show(); };

show();
if(clockRunning() && visitN===null){ openVisit(Date.now()); sv(); }
render();
setInterval(tick,500);
})();
</script><script>document.getElementById("toggletiming").addEventListener("click",function(){var b=document.getElementById("timing");var showing=b.style.display!=="none";b.style.display=showing?"none":"block";this.textContent=showing?"Show timing details (parent)":"Hide timing details";});</script></body></html>'''
          % (N, SLUG, SLUG, SLUG, SLUG, SLUG, SLUG))

live += SCRIPT
open(os.path.join(WS, f'{SLUG}.html'), 'w').write(live)

# ---- answer key ----
cards_k = []
for p in P:
    n = p["n"]
    diag = f'<div class="diag">{p["diagram"]}</div>' if p.get("diagram") else ''
    ref = p["ref"]
    cards_k.append(f'<div class="card"><div class="num">{n}. </div>'
                    f'<div class="q">{p["q"]}</div>{diag}{choices_html_key(p["choices"])}'
                    f'<div class="key">{p["key"]}</div><div class="ref">{ref}</div></div>')

key = head("Math Achievement Set 3 Answer Key") + '<body><div class="wrap">'
key += f'<h1>Math Achievement Practice — Set 3 · Answer Key</h1><p class="lede">For parent use. Tier, topic, and reference show how each problem connects to Hannah\'s gaps and past practice.</p>'
key += ''.join(cards_k)
key += '</div></body></html>'
open(os.path.join(WS, f'{SLUG}-answer-key.html'), 'w').write(key)

print(f"wrote {SLUG}.html and {SLUG}-answer-key.html")
