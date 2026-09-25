#!/usr/bin/env python3
"""Generate complete LCP dashboard HTML."""
import json

with open("E:/Samsudeen/Hermes agent/_full_data.json") as f:
    data = json.load(f)

origin = data["origin"]
ts = data["ts"]

def e(v):
    if v == "" or v is None: return '""'
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except:
        return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'

or_str = "const OR=[" + ",".join("[" + ",".join(e(v) for v in r) + "]" for r in origin) + "];\n\n"
ts_str = "const TS=[" + ",".join("[" + ",".join(e(v) for v in r) + "]" for r in ts) + "];\n"

# Build complete HTML
html = f"""<!DOCTYPE html><html lang="en" data-theme="dark"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LCP Shipment Dashboard — 17.09.2026</title><style>
:root{{--bg:#0f1117;--panel:#1a1d27;--border:#2a2d3a;--text:#e4e6ed;--muted:#8b8fa3;--accent:#6c8cff;--green:#34d399;--yellow:#fbbf24;--red:#f87171;--blue:#60a5fa;--row-hov:rgba(108,140,255,.06)}}
[data-theme="light"]{{--bg:#f5f6f8;--panel:#fff;--border:#e2e4ea;--text:#1f2233;--muted:#6b7084;--row-hov:rgba(108,140,255,.08)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh;transition:background .2s,color .2s}}
.dash{{max-width:1600px;margin:0 auto;padding:24px;display:flex;flex-direction:column;gap:16px}}
.hdr{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
.hdr h1{{font-size:26px;font-weight:700;letter-spacing:-.5px}}
.hdr .date{{color:var(--muted);font-size:13px;margin-top:2px}}
.tb{{display:flex;justify-content:flex-end;gap:8px}}
.tb button{{background:var(--panel);border:1px solid var(--border);color:var(--text);padding:7px 12px;border-radius:7px;cursor:pointer;font-size:12px;display:flex;align-items:center;gap:5px;transition:all .15s}}
.tb button:hover{{border-color:var(--accent)}}
.sg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}}
.sc{{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px;position:relative;overflow:hidden;transition:transform .15s}}
.sc:hover{{transform:translateY(-2px)}}
.sc .lb{{font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}}
.sc .vl{{font-size:22px;font-weight:700;letter-spacing:-.5px}}
.sc .sb{{font-size:10px;color:var(--muted);margin-top:2px}}
.sc.ac{{border-left:3px solid var(--accent)}}.sc.gr{{border-left:3px solid var(--green)}}.sc.yl{{border-left:3px solid var(--yellow)}}.sc.rd{{border-left:3px solid var(--red)}}.sc.bl{{border-left:3px solid var(--blue)}}
.tabs{{display:flex;gap:3px;background:var(--panel);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin-bottom:3px}}
.tab{{padding:8px 14px;font-size:12px;font-weight:500;cursor:pointer;border:none;background:transparent;color:var(--muted);transition:all .15s;display:flex;align-items:center;gap:6px}}
.tab:hover{{color:var(--text)}}
.tab.act{{color:#fff;background:var(--accent)}}
.tab .ct{{background:rgba(255,255,255,.15);padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600}}
.tab.act .ct{{background:rgba(255,255,255,.3)}}
.sb{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
.sb input{{flex:1;min-width:160px;padding:8px 12px;border-radius:7px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:12px;outline:none;transition:border .15s}}
.sb input:focus{{border-color:var(--accent)}}
.sb select{{padding:8px 10px;border-radius:7px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:11px;outline:none;cursor:pointer;min-width:110px}}
.sb select:focus{{border-color:var(--accent)}}
.fa{{display:flex;gap:5px;align-items:center;margin-left:auto}}
.cr{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
@media(max-width:900px){{.cr{{grid-template-columns:1fr}}}}
.cc{{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px}}
.cc h3{{font-size:10px;font-weight:600;margin-bottom:8px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}}
.cc canvas{{display:block}}
.dw{{text-align:center}}
.dl{{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 10px;margin-top:5px}}
.dli{{display:flex;align-items:center;gap:2px;font-size:10px;color:var(--muted)}}
.dli .dt{{width:7px;height:7px;border-radius:2px}}
.ca{{margin-top:6px;display:flex;gap:4px;justify-content:flex-end}}
.ca select{{padding:3px 6px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);font-size:10px;cursor:pointer}}
.tw{{background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden;overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:11px;white-space:nowrap}}
thead th{{background:rgba(255,255,255,.04);padding:6px 7px;text-align:left;font-weight:600;font-size:9px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);border-bottom:1px solid var(--border);cursor:pointer;user-select:none;white-space:nowrap;position:relative;transition:color .15s}}
thead th:hover{{color:var(--text)}}
thead th.so{{color:var(--accent)}}
thead th.so::after{{content:' ▲';font-size:7px}}
thead th.so.de::after{{content:' ▼'}}
thead th .cv{{position:absolute;right:1px;top:50%;transform:translateY(-50%);font-size:11px;cursor:pointer;opacity:0;transition:opacity .15s;line-height:1;padding:1px}}
thead th:hover .cv{{opacity:.4}}
tbody td{{padding:5px 7px;border-bottom:1px solid rgba(42,45,58,.3);color:var(--text);cursor:pointer;transition:background .1s}}
tr{{cursor:pointer;transition:background .1s}}
tr:hover{{background:var(--row-hov)}}
tr.ur{{border-left:3px solid var(--red)}}
tr.de{{border-left:3px solid var(--yellow)}}
.fl{{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:3px}}
.fl.ur{{background:var(--red);box-shadow:0 0 3px rgba(248,113,113,.4);animation:pulse 1.5s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.bp{{display:inline-block;padding:1px 5px;border-radius:7px;font-size:9px;font-weight:600}}
.bp.cr{{background:rgba(108,140,255,.12);color:var(--accent)}}
.bp.rt{{background:rgba(52,211,153,.12);color:var(--green)}}
.eb{{padding:1px 5px;border-radius:7px;font-size:9px;font-weight:600}}
.eb.od{{background:rgba(248,113,113,.15);color:var(--red)}}
.eb.wa{{background:rgba(251,191,36,.15);color:var(--yellow)}}
.eb.ok{{background:rgba(52,211,153,.15);color:var(--green)}}
.eb.na{{background:rgba(139,143,163,.15);color:var(--muted)}}
.pg{{display:flex;justify-content:space-between;align-items:center;padding:7px 10px;border-top:1px solid var(--border);flex-wrap:wrap;gap:4px}}
.pg .info{{font-size:10px;color:var(--muted)}}
.pg .info strong{{color:var(--text)}}
.pb{{display:flex;gap:2px}}
.pb button{{padding:3px 7px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);cursor:pointer;font-size:10px;transition:all .15s}}
.pb button:hover{{border-color:var(--accent)}}
.pb button.act{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.pb button:disabled{{opacity:.35;cursor:not-allowed}}
.eb2{{padding:3px 7px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--text);cursor:pointer;font-size:10px;display:flex;align-items:center;gap:2px;transition:all .15s}}
.eb2:hover{{border-color:var(--green);color:var(--green)}}
.es{{text-align:center;padding:35px 20px;color:var(--muted)}}
.es p{{font-size:12px;margin-top:4px}}
.mo{{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;display:none;align-items:center;justify-content:center;padding:20px;animation:fadeIn .12s}}
.mo.sh{{display:flex}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
.md{{background:var(--panel);border:1px solid var(--border);border-radius:12px;max-width:480px;width:100%;max-height:80vh;overflow-y:auto;padding:16px;position:relative;animation:slideUp .15s}}
@keyframes slideUp{{from{{transform:translateY(15px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
.mc{{position:absolute;top:5px;right:5px;background:none;border:none;color:var(--muted);font-size:16px;cursor:pointer;padding:2px 4px;border-radius:3px;line-height:1}}
.mc:hover{{color:var(--text);background:rgba(255,255,255,.05)}}
.md h2{{font-size:14px;font-weight:700;margin-bottom:1px}}
.md .meta{{color:var(--muted);font-size:10px;margin-bottom:10px}}
.mf{{display:flex;gap:10px;padding:5px 0;border-bottom:1px solid var(--border)}}
.mf:last-child{{border-bottom:none}}
.mf .flb{{font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;min-width:90px;padding-top:1px}}
.mf .flv{{font-size:11px;color:var(--text);flex:1;word-break:break-word}}
.md .flv.cb{{background:rgba(108,140,255,.12);color:var(--accent);padding:1px 6px;border-radius:6px;font-size:10px;font-weight:600}}
.md .flv.uf{{color:var(--red);font-weight:600}}
.md .flv.rv{{color:var(--green);font-weight:600}}
.tt{{position:fixed;bottom:14px;right:14px;background:var(--green);color:#fff;padding:7px 12px;border-radius:6px;font-size:11px;font-weight:600;z-index:2000;opacity:0;transform:translateY(8px);transition:all .3s;pointer-events:none}}
.tt.sh{{opacity:1;transform:translateY(0)}}
.tp{{position:fixed;background:#222;color:#fff;padding:3px 6px;border-radius:3px;font-size:9px;pointer-events:none;display:none;z-index:999;max-width:200px;word-wrap:break-word}}
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
<script>
"""

# Add data
html += or_str + ts_str

# Add helpers
html += """
function esd(s){if(!s||s.trim()=="")
"""
html += """||isNaN(s))
"""
html += """?"""""
html += """""
"""
html += """
:var d=new Date(1899,11,30);d.setDate(d.getDate()+Math.round(Number(s)));var n=new Date();var diff=Math.round((d-n)/86400000);var l=d.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"});if(diff<0)l+=' <span style="color:var(--red);font-size:9px">('+Math.abs(diff)+'d late)</span>';else if(diff===0)l+=' <span style="color:var(--green);font-size:9px">(today)</span>';else if(diff<=3)l+=' <span style="color:var(--yellow);font-size:9px">('+diff+'d)</span>';return l}
function fd(d){if(!d||d==""||isNaN(d))
"""
html += """
return
"""
html += `"""` + """
";var n=Number(d);if(isNaN(n)||n<1)return String(d);var dt=new Date(1899,11,30);dt.setDate(dt.getDate()+Math.round(n));var n2=new Date();var diff=Math.round((dt-n2)/86400000);var l=dt.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"});if(diff<0)l+=' <span style="color:var(--red);font-size:9px">('+Math.abs(diff)+'d late)</span>';else if(diff===0)l+=' <span style="color:var(--green);font-size:9px">(today)</span>';else if(diff<=3)l+=' <span style="color:var(--yellow);font-size:9px">('+diff+'d)</span>';return l}
function fdd(d){if(!d||d==""||isNaN(d))
"""
html += `return"""` + `"""` + """
;var n=parseInt(d);if(isNaN(n)||n<1)return d+"d";return n+"d"}
function cv(l){var m={'HAPAG':'#6c8cff','MSC':'#34d399','CMA':'#fbbf24','MAERSK':'#f87171','COSCO':'#a78bfa','OOCL':'#f472b6','ONE':'#2dd4bf','HYUNDAI':'#fb923c'};return m[l]||'#60a5fa'}
function mtd(t){t=t.toLowerCase();if(t.includes("urgent"))return"urgent";if(t.includes("delay"))return"delayed";return""}
const CV=['#6c8cff','#34d399','#fbbf24','#f87171','#a78bfa','#f472b6','#2dd4bf','#fb923c','#60a5fa','#818cf8','#facc15','#4ade80','#c084fc','#38bdf8'];
var cs="origin",st="",cf_="",sf_="",pf_="",paPer=40,sortCol=-1,sortDir=1,_curPage=1,srdm="avg";
const OH=["Sl","SAP No","PtnrID","Supplier","POL","POD","Container No","20'","40'","Carrier","Vessel","POL ATD","Carrier ETA","Predictive ETA","Commit TT","Actual TT","Remark","Frt.Rate"];
const TH=["Sl","SAP No","PtnrID","Supplier","POL","POD","Container No","20'","40'","Carrier","T/S Vessel","POL ATD","Carrier ETA","Predictive ETA","Commit TT","Actual TT","Remark","Frt.Rate"];
const allH={origin:OH,ts:TH};const allD={origin:OR,ts:TS};
const HIDDEN={origin:new Set([6,7,8,14,15,16]),ts:new Set([6,7,8,14,15])};
try{if(localStorage.getItem("lcp_h")){const d=JSON.parse(localStorage.getItem("lcp_h"));for(const v of(d.origin||[]))HIDDEN.origin.add(v);for(const v of(d.ts||[]))HIDDEN.ts.add(v)}}catch(e){}
function saveH(){try{localStorage.setItem("lcp_h",JSON.stringify({origin:[...HIDDEN.origin],ts:[...HIDDEN.ts]}))}catch(e){}}
function comp(rows){const total=rows.length,car={},pod={},sup={};let urg=0,totR=0,rc=0,ttV=[],c20=0,c40=0;
rows.forEach(r=>{car[r[9]]=(car[r[9]]||0)+1;pod[r[5]]=(pod[r[5]]||0)+1;sup[r[3]]=(sup[r[3]]||0)+1;
if(r[16]&&r[16].toLowerCase().includes("urgent"))urg++;
const rt=parseFloat(r[17]);if(!isNaN(rt)){totR+=rt;rc++;}
const tt=parseInt(r[14]);if(!isNaN(tt))ttV.push(tt);
if(r[7]==="1")c20++;if(r[8]==="1")c40++;
});
return{total,car,pod,sup,urg,avgR:rc>0?totR/rc:0,uq:Object.keys(pod).length,avgT:ttV.length>0?ttV.reduce((a,b)=>a+b,0)/ttV.length:0,c20,c40};
}
"""

print(f"HTML so far: {len(html)} chars...")
with open("E:/Samsudeen/Hermes agent/_build_part1.txt","w") as f:
    f.write(html)
print("Wrote _build_part1.txt")
