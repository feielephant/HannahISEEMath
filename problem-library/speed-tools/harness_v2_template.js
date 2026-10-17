(function(){
var N=__N__,K="__SLUG__-v1",T="__SLUG__-times",IDX="__SLUG__-idx";
var st={},clicks=[],visits=[],idx=1;
try{st=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
try{var saved=JSON.parse(localStorage.getItem(T)||"{}");clicks=saved.clicks||[];visits=saved.visits||[];}catch(e){}
try{idx=parseInt(localStorage.getItem(IDX)||"1",10)||1}catch(e){}
function sv(){try{localStorage.setItem(K,JSON.stringify(st));localStorage.setItem(T,JSON.stringify({clicks:clicks,visits:visits}));localStorage.setItem(IDX,String(idx));}catch(e){}}
function fmt(s){s=Math.max(0,Math.round(s));return Math.floor(s/60)+":"+("0"+(s%60)).slice(-2);}

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
    save("__SLUG__-times.csv", rows.join("\n"));
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
    save("__SLUG__-click-log.csv", rows2.join("\n"));
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
var CK="__SLUG__-clock", TOTAL=__TOTAL_SECONDS__;
var cst={rem:TOTAL,run:false,last:0};
try{var x=JSON.parse(localStorage.getItem(CK)||"null"); if(x) cst=x;}catch(e){}
function csv2(){try{localStorage.setItem(CK,JSON.stringify(cst));}catch(e){}}
function lock(){ var L=!cst.run; document.querySelectorAll("button.choice[data-qid]").forEach(function(b){b.disabled=L;}); }
function show(){
  window.__clockRunning = cst.run;
  var r=Math.max(0,Math.round(cst.rem)); var m=Math.floor(r/60), s=r%60;
  var status = cst.rem<=0 ? " — time’s up" : (cst.submitted ? " — submitted" : (cst.run?"":" — press Start to unlock"));
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
    if(confirm("Submit now and stop the timer? You can still look back at your answers, but the clock won't run again.")){
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
