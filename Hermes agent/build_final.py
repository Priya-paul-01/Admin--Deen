#!/usr/bin/env python3
"""Complete LCP Dashboard Generator."""
import json

with open("E:/Samsudeen/Hermes agent/_full_data.json") as f:
    data = json.load(f)

ORIGIN = data["origin"]
TS = data["ts"]

def jv(v):
    if v == "" or v is None: return '""'
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except:
        s = str(v)
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

# --- Build JS data arrays ---
or_entries = ",".join("[" + ",".join(jv(c) for c in r) + "]" for r in ORIGIN)
ts_entries = ",".join("[" + ",".join(jv(c) for c in r) + "]" for r in TS)

DATA_JS = f"const OR=[{or_entries}];\nconst TS=[{ts_entries}];\n"

# --- Write the full HTML ---
html_parts = []

# HTML head + CSS
html_parts.append("""<!DOCTYPE html><html lang="en" data-theme="dark"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LCP Shipment Dashboard — 17.09.2026</title><style>
:root{--bg:#0f1117;--panel:#1a1d27;--border:#2a2d3a;--text:#e4e6ed;--muted:#8b8fa3;--accent:#6c8cff;--green:#34d399;--yellow:#fbbf24;--red:#f87171;--blue:#60a5fa;--row-hov:rgba(108,140,255,.06)}
[data-theme="light"]{--bg:#f5f6f8;--panel:#fff;--border:#e2e4ea;--text:#1f2233;--muted:#6b7084;--row-hov:rgba(108,140,255,.08)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh;transition:background .2s,color .2s}
.dash{max-width:1600px;margin:0 auto;padding:24px;display:flex;flex-direction:column;gap:16px}
.hdr{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
.hdr h1{font-size:26px;font-weight:700;letter-spacing:-.5px}
.hdr .date{color:var(--muted);font-size:13px;margin-top:2px}
.tb{display:flex;justify-content:flex-end;gap:8px}
.tb button{background:var(--panel);border:1px solid var(--border);color:var(--text);padding:7px 12px;border-radius:7px;cursor:pointer;font-size:12px;display:flex;align-items:center;gap:5px;transition:all .15s}
.tb button:hover{border-color:var(--accent)}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.sc{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px;position:relative;overflow:hidden;transition:transform .15s}
.sc:hover{transform:translateY(-2px)}
.sc .lb{font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}
.sc .vl{font-size:22px;font-weight:700;letter-spacing:-.5px}
.sc .sb{font-size:10px;color:var(--muted);margin-top:2px}
.sc.ac{border-left:3px solid var(--accent)} .sc.gr{border-left:3px solid var(--green)} .sc.yl{border-left:3px solid var(--yellow)} .sc.rd{border-left:3px solid var(--red)} .sc.bl{border-left:3px solid var(--blue)}
.tabs{display:flex;gap:3px;background:var(--panel);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin-bottom:3px}
.tab{padding:8px 14px;font-size:12px;font-weight:500;cursor:pointer;border:none;background:transparent;color:var(--muted);transition:all .15s;display:flex;align-items:center;gap:6px}
.tab:hover{color:var(--text)}
.tab.act{color:#fff;background:var(--accent)}
.tab .ct{background:rgba(255,255,255,.15);padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600}
.tab.act .ct{background:rgba(255,255,255,.3)}
.sb{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.sb input{flex:1;min-width:160px;padding:8px 12px;border-radius:7px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:12px;outline:none;transition:border .15s}
.sb input:focus{border-color:var(--accent)}
.sb select{padding:8px 10px;border-radius:7px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:11px;outline:none;cursor:pointer;min-width:110px}
.sb select:focus{border-color:var(--accent)}
.fa{display:flex;gap:5px;align-items:center;margin-left:auto}
.cr{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:900px){.cr{grid-template-columns:1fr}}
.cc{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px}
.cc h3{font-size:10px;font-weight:600;margin-bottom:8px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.cc canvas{display:block}
.dw{text-align:center}
.dl{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 10px;margin-top:5px}
.dli{display:flex;align-items:center;gap:2px;font-size:10px;color:var(--muted)}
.dli .dt{width:7px;height:7px;border-radius:2px}
.ca{margin-top:6px;display:flex;gap:4px;justify-content:flex-end}
.ca select{padding:3px 6px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:10px;cursor:pointer}
.tw{background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:11px;white-space:nowrap}
thead th{background:rgba(255,255,255,.04);padding:6px 7px;text-align:left;font-weight:600;font-size:9px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);border-bottom:1px solid var(--border);cursor:pointer;user-select:none;white-space:nowrap;position:relative;transition:color .15s}
thead th:hover{color:var(--text)}
thead th.so{color:var(--accent)}
thead th.so::after{content:' ▲';font-size:7px}
thead th.so.de::after{content:' ▼'}
thead th .cv{position:absolute;right:1px;top:50%;transform:translateY(-50%);font-size:11px;cursor:pointer;opacity:0;transition:opacity .15s;line-height:1;padding:1px}
thead th:hover .cv{opacity:.4}
tbody td{padding:5px 7px;border-bottom:1px solid rgba(42,45,58,.3);color:var(--text);cursor:pointer;transition:background .1s}
tr{cursor:pointer;transition:background .1s}
tr:hover{background:var(--row-hov)}
tr.ur{border-left:3px solid var(--red)}
tr.de{border-left:3px solid var(--yellow)}
.fl{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:3px}
.fl.ur{background:var(--red);box-shadow:0 0 3px rgba(248,113,113,.4);animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.bp{display:inline-block;padding:1px 5px;border-radius:7px;font-size:9px;font-weight:600}
.bp.cr{background:rgba(108,140,255,.12);color:var(--accent)}
.bp.rt{background:rgba(52,211,153,.12);color:var(--green)}
.eb{padding:1px 5px;border-radius:7px;font-size:9px;font-weight:600}
.eb.od{background:rgba(248,113,113,.15);color:var(--red)}
.eb.wa{background:rgba(251,191,36,.15);color:var(--yellow)}
.eb.ok{background:rgba(52,211,153,.15);color:var(--green)}
.eb.na{background:rgba(139,143,163,.15);color:var(--muted)}
.pg{display:flex;justify-content:space-between;align-items:center;padding:7px 10px;border-top:1px solid var(--border);flex-wrap:wrap;gap:4px}
.pg .info{font-size:10px;color:var(--muted)}
.pg .info strong{color:var(--text)}
.pb{display:flex;gap:2px}
.pb button{padding:3px 7px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);cursor:pointer;font-size:10px;transition:all .15s}
.pb button:hover{border-color:var(--accent)}
.pb button.act{background:var(--accent);color:#fff;border-color:var(--accent)}
.pb button:disabled{opacity:.35;cursor:not-allowed}
.eb2{padding:3px 7px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);cursor:pointer;font-size:10px;display:flex;align-items:center;gap:2px;transition:all .15s}
.eb2:hover{border-color:var(--green);color:var(--green)}
.es{text-align:center;padding:35px 20px;color:var(--muted)}
.es p{font-size:12px;margin-top:4px}
.mo{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;display:none;align-items:center;justify-content:center;padding:20px;animation:fadeIn .12s}
.mo.sh{display:flex}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.md{background:var(--panel);border:1px solid var(--border);border-radius:12px;max-width:480px;width:100%;max-height:80vh;overflow-y:auto;padding:16px;position:relative;animation:slideUp .15s}
@keyframes slideUp{from{transform:translateY(15px);opacity:0}to{transform:translateY(0);opacity:1}}
.mc{position:absolute;top:5px;right:5px;background:none;border:none;color:var(--muted);font-size:16px;cursor:pointer;padding:2px 4px;border-radius:3px;line-height:1}
.mc:hover{color:var(--text);background:rgba(255,255,255,.05)}
.md h2{font-size:14px;font-weight:700;margin-bottom:1px}
.md .meta{color:var(--muted);font-size:10px;margin-bottom:10px}
.mf{display:flex;gap:10px;padding:5px 0;border-bottom:1px solid var(--border)}
.mf:last-child{border-bottom:none}
.mf .flb{font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;min-width:90px;padding-top:1px}
.mf .flv{font-size:11px;color:var(--text);flex:1;word-break:break-word}
.md .flv.cb{background:rgba(108,140,255,.12);color:var(--accent);padding:1px 6px;border-radius:6px;font-size:10px;font-weight:600}
.md .flv.uf{color:var(--red);font-weight:600}
.md .flv.rv{color:var(--green);font-weight:600}
.tt{position:fixed;bottom:14px;right:14px;background:var(--green);color:#fff;padding:7px 12px;border-radius:6px;font-size:11px;font-weight:600;z-index:2000;opacity:0;transform:translateY(8px);transition:all .3s;pointer-events:none}
.tt.sh{opacity:1;transform:translateY(0)}
.tp{position:fixed;background:#222;color:#fff;padding:3px 6px;border-radius:3px;font-size:9px;pointer-events:none;display:none;z-index:999;max-width:200px;word-wrap:break-word}
</style></head><body>
<div class="dash">
<div class="hdr"><div><h1>📦 LCP Shipment Dashboard</h1><div class="date">Report: 17 September 2026 &nbsp;|&nbsp; <span id="rCnt"></span></div></div>
<div class="tb"><button id="themeBtn" title="Toggle theme"><span id="themeIcon">🌙</span><span id="themeLbl">Dark</span></button></div></div>
<div class="sg" id="sg"></div>
<div class="cr"><div class="cc"><h3>🚢 Top Carriers</h3><canvas id="cc1" height="170"></canvas></div>
<div class="cc"><h3>📍 Destination Ports</h3><div class="dw"><canvas id="pc" height="190"></canvas><div class="dl" id="pl"></div></div></div></div>
<div class="cr"><div class="cc"><h3>📊 Rate by Destination</h3><canvas id="rbc" height="170"></canvas><div class="ca"><select id="rdm"><option value="avg">Avg Rate</option><option value="max">Max Rate</option><option value="min">Min Rate</option><option value="count">Count</option></select></div></div>
<div class="cc"><h3>⏱️ Transit Time by Carrier</h3><canvas id="ttbc" height="170"></canvas></div></div>
<div class="cr"><div class="cc"><h3>🏭 Shipments by Supplier</h3><canvas id="sc" height="170"></canvas></div>
<div class="cc"><h3>💰 Rate Distribution</h3><canvas id="rc" height="170"></canvas></div></div>
<div class="cr"><div class="cc"><h3>⏱️ Transit Time Distribution</h3><canvas id="tc" height="170"></canvas></div>
<div class="cc"><h3>🚦 ETA Status</h3><canvas id="esc" height="170"></canvas></div></div>
<div class="tabs"><button class="tab act" data-sheet="origin">📋 Origin Port <span class="ct" id="oc"></span></button><button class="tab" data-sheet="ts">🚢 TS Ports <span class="ct" id="tc2"></span></button></div>
<div class="sb"><input id="si" placeholder="Search SAP No, supplier, POD, carrier, remark..."><select id="cf"></select><select id="sf"></select><select id="pf"></select>
<div class="fa"><button class="eb2" id="ecb">📥 CSV</button><button class="eb2" id="cfl" title="Clear">✕ Clear</button></div></div>
<div class="tw" id="tw"><table><thead id="th"></thead><tbody id="tb"></tbody></table><div class="pg" id="pg"></div></div>
<div class="es" id="es" style="display:none"><div style="font-size:36px;margin-bottom:5px">🔍</div><p>No matches</p></div>
</div>
<div class="mo" id="mo"><div class="md"><button class="mc" id="mc">✕</button><h2 id="mt">Details</h2><div class="meta" id="mm"></div><div id="mf"></div></div></div>
<div class="tt" id="tt"></div><div class="tp" id="tp"></div>
<script>""")

# --- JavaScript helpers ---
html_parts.append("""
function esd(s){if(!s||s.trim()=="")return"";var d=new Date(1899,11,30);d.setDate(d.getDate()+Math.round(Number(s)));var n=new Date();var diff=Math.round((d-n)/86400000);var l=d.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"});if(diff<0)l+=' <span style="color:var(--red);font-size:9px">('+Math.abs(diff)+'d late)</span>';else if(diff===0)l+=' <span style="color:var(--green);font-size:9px">(today)</span>';else if(diff<=3)l+=' <span style="color:var(--yellow);font-size:9px">('+diff+'d)</span>';return l}
function fd(d){if(!d||d==""||isNaN(d))return"";var n=Number(d);if(isNaN(n)||n<1)return String(d);var dt=new Date(1899,11,30);dt.setDate(dt.getDate()+Math.round(n));var n2=new Date();var diff=Math.round((dt-n2)/86400000);var l=dt.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"});if(diff<0)l+=' <span style="color:var(--red);font-size:9px">('+Math.abs(diff)+'d late)</span>';else if(diff===0)l+=' <span style="color:var(--green);font-size:9px">(today)</span>';else if(diff<=3)l+=' <span style="color:var(--yellow);font-size:9px">('+diff+'d)</span>';return l}
function fdd(d){if(!d||d==""||isNaN(d))return"";var n=parseInt(d);if(isNaN(n)||n<1)return d+"d";return n+"d"}
function cv(l){var m={"HAPAG":"#6c8cff","MSC":"#34d399","CMA":"#fbbf24","MAERSK":"#f87171","COSCO":"#a78bfa","OOCL":"#f472b6","ONE":"#2dd4bf","HYUNDAI":"#fb923c"};return m[l]||"#60a5fa"}
function mtd(t){t=t.toLowerCase();if(t.includes("urgent"))return"urgent";if(t.includes("delay"))return"delayed";return""}
const CV=["#6c8cff","#34d399","#fbbf24","#f87171","#a78bfa","#f472b6","#2dd4bf","#fb923c","#60a5fa","#818cf8","#facc15","#4ade80","#c084fc","#38bdf8"];
var cs="origin",st="",cf_="",sf_="",pf_="",paPer=40,sortCol=-1,sortDir=1,_curPage=1,srdm="avg";
const OH=["Sl","SAP No","PtnrID","Supplier","POL","POD","Container No","20'","40'","Carrier","Vessel","POL ATD","Carrier ETA","Predictive ETA","Commit TT","Actual TT","Remark","Frt.Rate"];
const TH=["Sl","SAP No","PtnrID","Supplier","POL","POD","Container No","20'","40'","Carrier","T/S Vessel","POL ATD","Carrier ETA","Predictive ETA","Commit TT","Actual TT","Remark","Frt.Rate"];
const allH={origin:OH,ts:TH};const allD={origin:OR,ts:TS};
const HIDDEN={origin:new Set([6,7,8,14,15,16]),ts:new Set([6,7,8,14,15])};
try{if(localStorage.getItem("lcp_h")){const d=JSON.parse(localStorage.getItem("lcp_h"));for(const v of(d.origin||[]))HIDDEN.origin.add(v);for(const v of(d.ts||[]))HIDDEN.ts.add(v)}}catch(e){}
function saveH(){try{localStorage.setItem("lcp_h",JSON.stringify({origin:[...HIDDEN.origin],ts:[...HIDDEN.ts]}))}catch(e){}}
""")

# --- Stats ---
html_parts.append("""
function comp(rows){const total=rows.length,car={},pod={},sup={};let urg=0,totR=0,rc=0,ttV=[],c20=0,c40=0;
rows.forEach(r=>{car[r[9]]=(car[r[9]]||0)+1;pod[r[5]]=(pod[r[5]]||0)+1;sup[r[3]]=(sup[r[3]]||0)+1;
if(r[16]&&r[16].toLowerCase().includes("urgent"))urg++;
const rt=parseFloat(r[17]);if(!isNaN(rt)){totR+=rt;rc++;}
const tt=parseInt(r[14]);if(!isNaN(tt))ttV.push(tt);
if(r[7]==="1")c20++;if(r[8]==="1")c40++;
});
return{total,car,pod,sup,urg,avgR:rc>0?totR/rc:0,uq:Object.keys(pod).length,avgT:ttV.length>0?ttV.reduce((a,b)=>a+b,0)/ttV.length:0,c20,c40};
}
function renderStats(){const d=allD[cs],s=comp(d);
const cards=[{lb:"Total Shipments",vl:s.total,cl:"ac",sb:s.c20+"x20' · "+s.c40+"x40'"},{lb:"Unique Ports",vl:s.uq,cl:"bl",sb:"destinations"},{lb:"Carriers",vl:Object.keys(s.car).length,cl:"gr",sb:"active"},{lb:"Avg Rate",vl:"$"+s.avgR.toFixed(0),cl:"yl",sb:"$"+Math.round(s.avgR*s.total)+" total"},{lb:"Avg Transit",vl:s.avgT.toFixed(1)+"d",cl:"ac",sb:"committed"},{lb:"Urgent",vl:s.urg,cl:s.urg>0?"rd":"gr",sb:s.urg>0?"needs attention":"clear"}];
document.getElementById("sg").innerHTML=cards.map(c=>'<div class="sc '+c.cl+'"><div class="lb">'+c.lb+'</div><div class="vl">'+c.vl+'</div><div class="sb">'+c.sb+'</div></div>').join("");
document.getElementById("rCnt").textContent=d.length+" shipments";
}
""")

# --- Charts ---
html_parts.append("""
function bar(cid,data,topN,mfn){const sorted=Object.entries(data).sort((a,b)=>b[1]-a[1]).slice(0,topN);if(!sorted.length)return;
const cv=document.getElementById(cid);const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28;const H=170;const D=window.devicePixelRatio||1;
cv.width=W*D;cv.height=H*D;cv.style.width=W+"px";cv.style.height=H+"px";ctx.scale(D,D);ctx.clearRect(0,0,W,H);
const P={t:6,r:10,b:32,l:32};const cW=W-P.l-P.r,cH=H-P.t-P.b;const mx=sorted[0][1]||1;
const bw=Math.min(50,cW/sorted.length*.55);const gap=cW/sorted.length;
ctx.strokeStyle="rgba(255,255,255,.04)";ctx.lineWidth=1;
for(let i=1;i<=4;i++){const y=P.t+cH-cH*i/4;ctx.beginPath();ctx.moveTo(P.l,y);ctx.lineTo(W-P.r,y);ctx.stroke();
ctx.fillStyle="rgba(139,143,163,.5)";ctx.font="9px Inter,sans-serif";ctx.textAlign="right";ctx.fillText(Math.round(mx*i/4),P.l-3,y+2);}
sorted.forEach(function(p,i){const lb=p[0],v=p[1];const x=P.l+i*gap+(gap-bw)/2;const h=(v/mx)*cH;const y=P.t+cH-h;
const col=mfn?mfn(lb):CV[i%CV.length];
ctx.fillStyle=col;ctx.globalAlpha=.8;ctx.beginPath();ctx.roundRect(x,y,bw,h,[3,3,0,0]);ctx.fill();ctx.globalAlpha=1;
ctx.fillStyle="#e4e6ed";ctx.font="bold 10px Inter,sans-serif";ctx.textAlign="center";ctx.fillText(v,x+bw/2,y-3);
ctx.fillStyle="#8b8fa3";ctx.font="9px Inter,sans-serif";ctx.fillText(lb.length>11?lb.slice(0,10)+"…":lb,x+bw/2,P.t+cH+13);});
}
function donut(cid,legId,data){const sorted=Object.entries(data).sort((a,b)=>b[1]-a[1]).slice(0,8);if(!sorted.length)return;
const cv=document.getElementById(cid);const ctx=cv.getContext("2d");const sz=180;const D=window.devicePixelRatio||1;
cv.width=sz*D;cv.height=sz*D;cv.style.width=sz+"px";cv.style.height=sz+"px";ctx.scale(D,D);ctx.clearRect(0,0,sz,sz);
const cx=sz/2,cy=sz/2,r=72,ir=48;const tot=sorted.reduce((s,p)=>s+p[1],0);
const pal=["#6c8cff","#34d399","#fbbf24","#f87171","#a78bfa","#f472b6","#2dd4bf","#fb923c"];let sa=-Math.PI/2;
sorted.forEach(function(p,i){const lb=p[0],v=p[1];const sl=(v/tot)*Math.PI*2;const ea=sa+sl;
ctx.beginPath();ctx.arc(cx,cy,r,sa,ea);ctx.arc(cx,cy,ir,ea,sa,true);ctx.closePath();
ctx.fillStyle=pal[i%pal.length];ctx.globalAlpha=.78;ctx.fill();ctx.globalAlpha=1;sa=ea;});
ctx.fillStyle="#e4e6ed";ctx.font="bold 18px Inter,sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
ctx.fillText(tot,cx,cy-4);ctx.fillStyle="#8b8fa3";ctx.font="9px Inter,sans-serif";ctx.fillText("shipments",cx,cy+12);
document.getElementById(legId).innerHTML=sorted.map(function(p,i){return'<div class="dli"><span class="dt" style="background:'+pal[i%pal.length]+'"></span>'+p[0]+' <span style="color:#e4e6ed;font-weight:600">'+p[1]+'</span></div>'}).join("");
}
function renderCharts(){const d=allD[cs],s=comp(d);
bar("cc1",s.car,8,function(l){return cv(l)});
donut("pc","pl",s.pod);

const rdMap={};d.forEach(function(r){const p=r[5]||"Unknown";if(!rdMap[p])rdMap[p]={sum:0,count:0,max:0,min:Infinity};
const rt=parseFloat(r[17]);if(!isNaN(rt)){rdMap[p].sum+=rt;rdMap[p].count++;rdMap[p].max=Math.max(rdMap[p].max,rt);if(rt<rdMap[p].min)rdMap[p].min=rt}});
const rdB={};for(const p in rdMap){const st=rdMap[p];
if(srdm==="avg")rdB[p]=st.count?st.sum/st.count:0;else if(srdm==="max")rdB[p]=st.max;else if(srdm==="min")rdB[p]=st.min;else rdB[p]=st.count}
const sortedRd=Object.entries(rdB).sort((a,b)=>b[1]-a[1]).slice(0,8);
if(sortedRd.length){const cv=document.getElementById("rbc");const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28;const H=170;const D=window.devicePixelRatio||1;
cv.width=W*D;cv.height=H*D;cv.style.width=W+"px";cv.style.height=H+"px";ctx.scale(D,D);ctx.clearRect(0,0,W,H);
const P={t:6,r:10,b:32,l:32};const cW=W-P.l-P.r,cH=H-P.t-P.b;const mx=sortedRd[0][1]||1;
const bw=Math.min(50,cW/sortedRd.length*.55);const gap=cW/sortedRd.length;
ctx.strokeStyle="rgba(255,255,255,.04)";ctx.lineWidth=1;
for(let i=1;i<=4;i++){const y=P.t+cH-cH*i/4;ctx.beginPath();ctx.moveTo(P.l,y);ctx.lineTo(W-P.r,y);ctx.stroke();
ctx.fillStyle="rgba(139,143,163,.5)";ctx.font="9px Inter,sans-serif";ctx.textAlign="right";ctx.fillText(Math.round(mx*i/4),P.l-3,y+2);}
sortedRd.forEach(function(p,i){const lb=p[0],v=p[1];const x=P.l+i*gap+(gap-bw)/2;const h=(v/mx)*cH;const y=P.t+cH-h;
ctx.fillStyle=CV[i%CV.length];ctx.globalAlpha=.8;ctx.beginPath();ctx.roundRect(x,y,bw,h,[3,3,0,0]);ctx.fill();ctx.globalAlpha=1;
ctx.fillStyle="#e4e6ed";ctx.font="bold 10px Inter,sans-serif";ctx.textAlign="center";ctx.fillText(v.toFixed(0),x+bw/2,y-3);
ctx.fillStyle="#8b8fa3";ctx.font="9px Inter,sans-serif";ctx.fillText(lb.length>11?lb.slice(0,10)+"…":lb,x+bw/2,P.t+cH+13);});
}

const ttMap={};d.forEach(function(r){const c=r[9];const tt=parseInt(r[14]);if(!isNaN(tt)){if(!ttMap[c])ttMap[c]={sum:0,count:0};ttMap[c].sum+=tt;ttMap[c].count++}});
const ttAvg={};for(const c in ttMap)ttAvg[c]=ttMap[c].sum/ttMap[c].count;
const sortedTt=Object.entries(ttAvg).sort((a,b)=>b[1]-a[1]);
if(sortedTt.length){const cv=document.getElementById("ttbc");const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28;const H=170;const D=window.devicePixelRatio||1;
cv.width=W*D;cv.height=H*D;cv.style.width=W+"px";cv.style.height=H+"px";ctx.scale(D,D);ctx.clearRect(0,0,W,H);
const P={t:6,r:10,b:32,l:32};const cW=W-P.l-P.r,cH=H-P.t-P.b;const mx=sortedTt[0][1]||1;
const bw=Math.min(50,cW/sortedTt.length*.55);const gap=cW/sortedTt.length;
ctx.strokeStyle="rgba(255,255,255,.04)";ctx.lineWidth=1;
for(let i=1;i<=4;i++){const y=P.t+cH-cH*i/4;ctx.beginPath();ctx.moveTo(P.l,y);ctx.lineTo(W-P.r,y);ctx.stroke();
ctx.fillStyle="rgba(139,143,163,.5)";ctx.font="9px Inter,sans-serif";ctx.textAlign="right";ctx.fillText(Math.round(mx*i/4),P.l-3,y+2);}
sortedTt.forEach(function(p,i){const lb=p[0],v=p[1];const x=P.l+i*gap+(gap-bw)/2;const h=(v/mx)*cH;const y=P.t+cH-h;
ctx.fillStyle=cv(lb);ctx.globalAlpha=.8;ctx.beginPath();ctx.roundRect(x,y,bw,h,[3,3,0,0]);ctx.fill();ctx.globalAlpha=1;
ctx.fillStyle="#e4e6ed";ctx.font="bold 10px Inter,sans-serif";ctx.textAlign="center";ctx.fillText(v.toFixed(1),x+bw/2,y-3);
ctx.fillStyle="#8b8fa3";ctx.font="9px Inter,sans-serif";ctx.fillText(lb.length>11?lb.slice(0,10)+"…":lb,x+bw/2,P.t+cH+13);});
}

const sortedSup=Object.entries(s.sup).sort((a,b)=>b[1]-a[1]).slice(0,8);
if(sortedSup.length){const cv=document.getElementById("sc");const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28;const H=170;const D=window.devicePixelRatio||1;
cv.width=W*D;cv.height=H*D;cv.style.width=W+"px";cv.style.height=H+"px";ctx.scale(D,D);ctx.clearRect(0,0,W,H);
const P={t:6,r:10,b:32,l:32};const cW=W-P.l-P.r,cH=H-P.t-P.b;const mx=sortedSup[0][1]||1;
const bw=Math.min(50,cW/sortedSup.length*.55);const gap=cW/sortedSup.length;
ctx.strokeStyle="rgba(255,255,255,.04)";ctx.lineWidth=1;
for(let i=1;i<=4;i++){const y=P.t+cH-cH*i/4;ctx.beginPath();ctx.moveTo(P.l,y);ctx.lineTo(W-P.r,y);ctx.stroke();
ctx.fillStyle="rgba(139,143,163,.5)";ctx.font="9px Inter,sans-serif";ctx.textAlign="right";ctx.fillText(Math.round(mx*i/4),P.l-3,y+2);}
sortedSup.forEach(function(p,i){const lb=p[0],v=p[1];const x=P.l+i*gap+(gap-bw)/2;const h=(v/mx)*cH;const y=P.t+cH-h;
ctx.fillStyle=CV[(i*3)%CV.length];ctx.globalAlpha=.8;ctx.beginPath();ctx.roundRect(x,y,bw,h,[3,3,0,0]);ctx.fill();ctx.globalAlpha=1;
ctx.fillStyle="#e4e6ed";ctx.font="bold 10px Inter,sans-serif";ctx.textAlign="center";ctx.fillText(v,x+bw/2,y-3);
ctx.fillStyle="#8b8fa3";ctx.font="9px Inter,sans-serif";ctx.fillText(lb.length>11?lb.slice(0,10)+"…":lb,x+bw/2,P.t+cH+13);});
}

const rates=d.map(function(r){return parseFloat(r[17])}).filter(function(v){return!isNaN(v)&&v>0});
const rBins={};if(rates.length){const mn=Math.min.apply(null,rates),mx=Math.max.apply(null,rates),rg=mx-mn||1,nb=5;
for(let i=0;i<nb;i++){const lo=mn+rg*i/nb;const hi=mn+rg*(i+1)/nb;rBins["$"+Math.round(lo)+"–"+Math.round(hi)]=0}
rates.forEach(function(v){const idx=Math.min(nb-1,Math.floor((v-mn)/rg*nb));const ks=Object.keys(rBins);rBins[ks[idx]]++})}
bar("rc",rBins,5,null);

const tts=d.map(function(r){return parseInt(r[14])}).filter(function(v){return!isNaN(v)&&v>0});
const tBins={};if(tts.length){const mn=Math.min.apply(null,tts),mx=Math.max.apply(null,tts),rg=mx-mn||1,nb=5;
for(let i=0;i<nb;i++){const lo=mn+rg*i/nb;const hi=Math.min(mx,mn+rg*(i+1)/nb);tBins[Math.round(lo)+"–"+Math.round(hi)+"d"]=0}
tts.forEach(function(v){const idx=Math.min(nb-1,Math.floor((v-mn)/rg*nb));const ks=Object.keys(tBins);tBins[ks[idx]]++})}
bar("tc",tBins,5,null);

const etaS={ok:0,warning:0,overdue:0,na:0};
d.forEach(function(r){const e=r[12];if(!e||e===""){etaS.na++;return}
const ed=esd(e);if(ed.includes("late"))etaS.overdue++;else if(ed.includes("(today)")||ed.includes("(1d)")||ed.includes("(2d)")||ed.includes("(3d)"))etaS.warning++;else etaS.ok++;
});
const etaCt=document.getElementById("esc");const ctx=etaCt.getContext("2d");const W=etaCt.parentElement.clientWidth-28;const H=170;const D=window.devicePixelRatio||1;
etaCt.width=W*D;etaCt.height=H*D;etaCt.style.width=W+"px";etaCt.style.height=H+"px";ctx.scale(D,D);ctx.clearRect(0,0,W,H);
const P={t:6,r:10,b:32,l:32};const cW=W-P.l-P.r,cH=H-P.t-P.b;
const items=[["On Track",etaS.ok,"#34d399"],["Soon",etaS.warning,"#fbbf24"],["Overdue",etaS.overdue,"#f87171"],["No ETA",etaS.na,"#8b8fa3"]];
const mx=Math.max.apply(null,items.map(function(i){return i[1]}),1);
const bw=Math.min(55,cW/items.length*.5);const gap=cW/items.length;
ctx.strokeStyle="rgba(255,255,255,.04)";ctx.lineWidth=1;
for(let i=1;i<=4;i++){const y=P.t+cH-cH*i/4;ctx.beginPath();ctx.moveTo(P.l,y);ctx.lineTo(W-P.r,y);ctx.stroke();
ctx.fillStyle="rgba(139,143,163,.5)";ctx.font="9px Inter,sans-serif";ctx.textAlign="right";ctx.fillText(Math.round(mx*i/4),P.l-3,y+2);}
items.forEach(function(p,i){const lb=p[0],v=p[1],col=p[2];const x=P.l+i*gap+(gap-bw)/2;const h=(v/mx)*cH;const y=P.t+cH-h;
ctx.fillStyle=col;ctx.globalAlpha=.8;ctx.beginPath();ctx.roundRect(x,y,bw,h,[3,3,0,0]);ctx.fill();ctx.globalAlpha=1;
ctx.fillStyle="#e4e6ed";ctx.font="bold 10px Inter,sans-serif";ctx.textAlign="center";ctx.fillText(v,x+bw/2,y-3);
ctx.fillStyle="#8b8fa3";ctx.font="9px Inter,sans-serif";ctx.fillText(lb,x+bw/2,P.t+cH+13);});
}
}
""")

# --- Table ---
html_parts.append("""
function getDisplayHeaders(){const h=cs==="origin"?OH:TH;return h.filter(function(_,i){return!HIDDEN[cs].has(i)});}
function getFilteredRows(){const d=allD[cs];let rows=d.filter(function(r){if(!st)return true;const q=st.toLowerCase();return r.some(function(c){return c!==undefined&&c!==null&&String(c).toLowerCase().includes(q)})});
if(cf_)rows=rows.filter(function(r){return r[9]===cf_});
if(sf_)rows=rows.filter(function(r){return r[3]===sf_});
if(pf_)rows=rows.filter(function(r){return r[5]===pf_});
if(sortCol>=0){rows.sort(function(a,b){var va=a[sortCol],vb=b[sortCol];
if(va===""||va===undefined)va="";if(vb===""||vb===undefined)vb="";
if(typeof va==="number"&&typeof vb==="number")return sortDir*(va-vb);
return sortDir*String(va).localeCompare(String(vb))});
}
return rows;
}
function renderTable(){const h=getDisplayHeaders();const rows=getFilteredRows();
const fHead=document.getElementById("th");const fBody=document.getElementById("tb");
const fEmpty=document.getElementById("es");const fWrap=document.getElementById("tw");const pg=document.getElementById("pg");
const total=rows.length;const totalPages=Math.max(1,Math.ceil(total/paPer));
const page=Math.min(Math.max(1,_curPage),totalPages);_curPage=page;
const start=(page-1)*paPer,end=Math.min(start+paPer,total);
const pageRows=rows.slice(start,end);
fHead.innerHTML='<tr>'+h.map(function(name){const oi=cs==="origin"?OR[0].indexOf(name):TH[0].indexOf(name);
return'<th data-col="'+oi+'" class="'+(sortCol===oi?(sortDir>0?"":"de"):"")+'">'+name+(HIDDEN[cs].has(oi)?"":"<span class=\"cv\" data-cv=\""+oi+"\" title=\"Hide\">👁</span>")+'</th>';
}).join("")+'</tr>';
if(rows.length===0){fBody.innerHTML="";fEmpty.style.display="block";fWrap.style.display="none";pg.style.display="none";
document.getElementById(cs==="origin"?"oc":"tc2").textContent="0";return;}
fEmpty.style.display="none";fWrap.style.display="block";pg.style.display="flex";
document.getElementById(cs==="origin"?"oc":"tc2").textContent=total;
fBody.innerHTML=pageRows.map(function(r,rowIdx){const isUrg=mtd(r[16])==="urgent";const isDelay=mtd(r[16])==="delayed";
const eta=r[12];const etaCls=(eta===''||eta===undefined)?"na":(eta.startsWith("46")&&parseInt(eta)>46305||esd(eta).includes("late"))?"od":
(esd(eta).includes("(today)")||esd(eta).includes("(1d)")||esd(eta).includes("(2d)")||esd(eta).includes("(3d)"))?"wa":"ok";
return'<tr class="'+(isUrg?"ur":"")+(isDelay?"de":"")+'" data-idx="'+Math.round(start+rowIdx)+'">'+h.map(function(name){const oi=cs==="origin"?OR[0].indexOf(name):TH[0].indexOf(name);const v=r[oi];
if(oi===9){return'<td><span class="bp cr" style="background:'+cv(v)+'22;color:'+cv(v)+'">'+v+'</span></td>'}
if(oi===17){return v?'<td><span class="bp rt">$'+v+'</span></td>':'<td></td>'}
if(oi===12){return'<td><span class="eb '+etaCls+'">'+(etaCls==="na"?"N/A":etaCls==="od"?"Overdue":etaCls==="wa"?"Soon":"On track")+'</span></td>'}
if(oi===11){return'<td>'+fd(v)+'</td>'}
if(oi===13){return'<td>'+fdd(v)+'</td>'}
if(oi===14||oi===15){return'<td>'+(v===''?'':(parseInt(v)).toFixed(0)+'d')+'</td>'}
if(oi===16&&v){return'<td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;color:#8b8fa3" title="'+v.replace(/"/g,'&quot;')+'">'+v+'</td>'}
return'<td>'+(v===''?'':' '+String(v))+'</td>';
}).join("")+'</tr>';
}).join("");
pg.innerHTML='<div class="info">Showing <strong>'+(start+1)+'</strong>–<strong>'+end+'</strong> of <strong>'+total+'</strong></div>'+
'<div style="display:flex;gap:6px;align-items:center">'+
'<button class="eb2" id="exportCsvBtn">📥 CSV</button>'+
'<div class="pb"><button data-pg="1" '+(page===1?'disabled':'')+'>«</button>'+
'<button data-pg="'+(page-1)+'" '+(page===1?'disabled':'')+'>‹</button>'+
'<button data-pg="'+(page+1)+'" '+(page===totalPages?'disabled':'')+'>›</button>'+
'<button data-pg="'+totalPages+'" '+(page===totalPages?'disabled':'')+'>»</button></div>'+
'<select id="pp" style="padding:3px 6px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:10px">'+
[5,10,20,40,50,100].map(function(n){return'<option value="'+n+'" '+(paPer===n?'selected':'')+'>'+n+'/page</option>'}).join("")+'</select></div>';
document.querySelectorAll(".pb button[data-pg]").forEach(function(b){b.addEventListener("click",function(){const p=parseInt(b.dataset.pg);if(p>=1&&p<=totalPages){_curPage=p;renderTable();}});});
document.getElementById("pp").addEventListener("change",function(e){paPer=parseInt(e.target.value);_curPage=1;renderTable();});
document.getElementById("exportCsvBtn").addEventListener("click",exportCSV);
}
""")

# --- Modal ---
html_parts.append("""
function showModal(r){const h=cs==="origin"?OH:TH;
document.getElementById("mt").textContent="Shipment #"+(cs==="origin"?"":"TS ")+r[0];
document.getElementById("mm").textContent="SAP: "+r[1]+" · "+r[3]+" · "+r[9]+" · "+(r[5]||"N/A");
const fields=[];
const eta=r[12];const etaDisp=eta?esd(eta):"N/A";
const pred=r[13];const predDisp=pred?fdd(pred):"N/A";
const comm=r[14];const commDisp=comm===''?'':' '+comm+'d';
const act=r[15];const actDisp=act===''?'':' '+act+'d';
const atd=r[11];const atdDisp=atd?fd(atd):"N/A";
fields.push(["SAP No",'<strong>'+r[1]+'</strong>']);
fields.push(["Partner ID",String(r[2])]);
fields.push(["Supplier",'<strong>'+r[3]+'</strong>']);
fields.push(["POL",r[4]]);
fields.push(["POD",'<strong>'+(r[5]||"N/A")+'</strong>']);
fields.push(["Container",r[6]||"N/A"]);
fields.push(["20'",r[7]==="1"?"Yes":"—"]);
fields.push(["40'",r[8]==="1"?"Yes":"—"]);
fields.push(["Carrier",'<span class="cb" style="background:'+cv(r[9])+'22;color:'+cv(r[9])+'">'+r[9]+'</span>']);
fields.push(["Vessel",r[10]||"N/A"]);
fields.push(["POL ATD",atdDisp]);
fields.push(["Carrier ETA",etaDisp]);
fields.push(["Pred. ETA",predDisp]);
fields.push(["Commit TT",commDisp]);
fields.push(["Actual TT",actDisp]);
const remark=r[16];const isUrg=mtd(remark)==="urgent";const isDl=mtd(remark)==="delayed";
fields.push(["Status",isUrg?'<span class="uf">🚩 URGENT</span>':isDl?'<span style="color:var(--yellow);font-weight:600">⚠️ Delay</span>':'✅ On track']);
fields.push(["Rate",r[17]?'<span class="rv">$'+r[17]+'</span>':'<span class="rv">N/A</span>']);
if(remark){fields.push(["Remark",'<span style="color:#8b8fa3">'+remark+'</span>'])}
document.getElementById("mf").innerHTML=fields.map(function(f){return'<div class="mf"><div class="flb">'+f[0]+'</div><div class="flv">'+f[1]+'</div></div>'}).join("");
document.getElementById("mo").classList.add("show");
}
document.getElementById("mc").addEventListener("click",function(){document.getElementById("mo").classList.remove("show");});
document.getElementById("mo").addEventListener("click",function(e){if(e.target===e.currentTarget)document.getElementById("mo").classList.remove("show");});
document.addEventListener("keydown",function(e){if(e.key==="Escape")document.getElementById("mo").classList.remove("show");});
document.getElementById("tb").addEventListener("click",function(e){const tr=e.target.closest("tr");if(!tr)return;const idx=parseInt(tr.dataset.idx);if(isNaN(idx))return;const rows=getFilteredRows();if(idx>=0&&idx<rows.length)showModal(rows[idx]);});
""")

# --- Filters ---
html_parts.append("""
function updateFilters(){const d=allD[cs];
const cars=[...new Set(d.map(function(r){return r[9]}).filter(Boolean))].sort();
const sups=[...new Set(d.map(function(r){return r[3]}).filter(Boolean))].sort();
const pods=[...new Set(d.map(function(r){return r[5]}).filter(Boolean))].sort();
const cf=document.getElementById("cf"),sf=document.getElementById("sf"),pf=document.getElementById("pf");
cf.innerHTML="<option value=\"\">All Carriers</option>"+cars.map(function(c){return'<option value="'+c+'" '+(cf_===c?"selected":"")+'>'+c+'</option>'}).join("");
sf.innerHTML="<option value=\"\">All Suppliers</option>"+sups.map(function(s){return'<option value="'+s+'" '+(sf_===s?"selected":"")+'>'+s+'</option>'}).join("");
pf.innerHTML="<option value=\"\">All PODs</option>"+pods.map(function(p){return'<option value="'+p+'" '+(pf_===p?"selected":"")+'>'+p+'</option>'}).join("");
}
document.getElementById("si").addEventListener("input",function(e){st=e.target.value;renderTable();});
document.getElementById("cf").addEventListener("change",function(e){cf_=e.target.value;renderTable();});
document.getElementById("sf").addEventListener("change",function(e){sf_=e.target.value;renderTable();});
document.getElementById("pf").addEventListener("change",function(e){pf_=e.target.value;renderTable();});
document.getElementById("cfl").addEventListener("click",function(){st="";cf_="";sf_="";pf_="";document.getElementById("si").value="";document.getElementById("cf").value="";document.getElementById("sf").value="";document.getElementById("pf").value="";renderTable();});
""")

# --- Column visibility + sort ---
html_parts.append("""
document.getElementById("th").addEventListener("click",function(e){const cvBtn=e.target.closest(".cv");if(cvBtn){e.stopPropagation();const col=parseInt(cvBtn.dataset.cv);HIDDEN[cs].add(col);saveH();renderTable();return;}
const th=e.target.closest("th");if(!th)return;const col=parseInt(th.dataset.col);
if(sortCol===col)sortDir=-sortDir;else{sortCol=col;sortDir=1}
renderTable();
});
""")

# --- CSV Export ---
html_parts.append("""
function exportCSV(){const d=allD[cs];const f=getFilteredRows();const h=cs==="origin"?OH:TH;
const visH=h.filter(function(_,i){return!HIDDEN[cs].has(i)});
const lines=[visH.map(function(c){return '"'+c+'"'}).join(",")];
f.forEach(function(r){const vals=[];h.forEach(function(_,i){const v=r[i];
if(typeof v==="number")vals.push(v);else vals.push('"'+String(v).replace(/"/g,'""')+"'");
});lines.push(vals.join(","));});
const csv=lines.join("\n");const blob=new Blob([csv],{type:"text/csv;charset=utf-8;"});
const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;
a.download="LCP_Shipments_"+(cs==="origin"?"Origin":"TS")+"_"+new Date().toISOString().slice(0,10)+".csv";a.click();URL.revokeObjectURL(url);
showToast("CSV exported");
}
function showToast(msg){const t=document.getElementById("tt");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},1800);}
""")

# --- Theme + Tabs + Init ---
html_parts.append("""
document.getElementById("themeBtn").addEventListener("click",function(){const d=document.documentElement;const c=d.getAttribute("data-theme");const n=c==="dark"?"light":"dark";
d.setAttribute("data-theme",n);document.getElementById("themeIcon").textContent=n==="dark"?"🌙":"☀️";document.getElementById("themeLbl").textContent=n==="dark"?"Dark":"Light";
try{localStorage.setItem("lcp_theme",n)}catch(e){}});
try{if(localStorage.getItem("lcp_theme")==="light"){document.documentElement.setAttribute("data-theme","light");document.getElementById("themeIcon").textContent="☀️";document.getElementById("themeLbl").textContent="Light"}}catch(e){}
document.querySelectorAll(".tab").forEach(function(t){t.addEventListener("click",function(){document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("act")});t.classList.add("act");cs=t.dataset.sheet;st="";cf_="";sf_="";pf_="";sortCol=-1;sortDir=1;_curPage=1;
document.getElementById("si").value="";document.getElementById("cf").value="";document.getElementById("sf").value="";document.getElementById("pf").value="";
updateFilters();renderStats();renderCharts();renderTable();});});
updateFilters();renderStats();renderCharts();renderTable();
window.addEventListener("resize",function(){renderCharts();});
const tpEl2=document.getElementById("tp");document.addEventListener("mousemove",function(e){const el=e.target.closest("td[title]");if(el&&el.title){tpEl2.style.display="block";tpEl2.style.left=(e.clientX+8)+"px";tpEl2.style.top=(e.clientY+8)+"px";tpEl2.textContent=el.title}else{tpEl2.style.display="none"}});
document.getElementById("rdm").addEventListener("change",function(e){srdm=e.target.value;renderCharts();});
</script></body></html>""")

# --- Combine everything ---
full_html = "".join(html_parts)

# Insert data before the helpers
final_html = full_html.replace('<script>\nfunction esd', '<script>\n' + DATA_JS + '\nfunction esd')

# Clean up extra newlines
while '\n\n\n' in final_html:
    final_html = final_html.replace('\n\n\n', '\n\n')

# Write output
with open("E:/Samsudeen/Hermes agent/dashboard.html", "w") as f:
    f.write(final_html)

print(f"\nDone! dashboard.html = {len(final_html)} chars")
print(f"  ORIGIN entries: {len(ORIGIN)}")
print(f"  TS entries: {len(TS)}")
