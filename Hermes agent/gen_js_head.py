#!/usr/bin/env python3
"""Generate complete LCP dashboard HTML."""
import json

with open("E:/Samsudeen/Hermes agent/_full_data.json") as f:
    data = json.load(f)

origin = data["origin"]
ts = data["ts"]

def fmt(v):
    if v == "" or v is None: return '""'
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except:
        return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'

# Build JavaScript data arrays
js_parts = []
js_parts.append("// Data")
js_parts.append("const OR=[" + ",".join("[" + ",".join(fmt(v) for v in r) + "]" for r in origin) + "];")
js_parts.append("const TS=[" + ",".join("[" + ",".join(fmt(v) for v in r) + "]" for r in ts) + "];")
js_parts.append("const allH={origin:OH,ts:TH};const allD={origin:OR,ts:TS};")
js_parts.append("")
js_parts.append("// Helpers")
js_parts.append("""function esd(s){if(!s||s.trim()=="")return"";var d=new Date(1899,11,30);d.setDate(d.getDate()+Math.round(Number(s)));var n=new Date();var diff=Math.round((d-n)/86400000);var l=d.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"});if(diff<0)l+=' <span style="color:var(--red);font-size:9px">('+Math.abs(diff)+'d late)</span>';else if(diff===0)l+=' <span style="color:var(--green);font-size:9px">(today)</span>';else if(diff<=3)l+=' <span style="color:var(--yellow);font-size:9px">('+diff+'d)</span>';return l}""")
js_parts.append("""function fd(d){if(!d||d==""||isNaN(d))return"";var n=Number(d);if(isNaN(n)||n<1)return String(d);var dt=new Date(1899,11,30);dt.setDate(dt.getDate()+Math.round(n));var n2=new Date();var diff=Math.round((dt-n2)/86400000);var l=dt.toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric"});if(diff<0)l+=' <span style="color:var(--red);font-size:9px">('+Math.abs(diff)+'d late)</span>';else if(diff===0)l+=' <span style="color:var(--green);font-size:9px">(today)</span>';else if(diff<=3)l+=' <span style="color:var(--yellow);font-size:9px">('+diff+'d)</span>';return l}""")
js_parts.append("""function fdd(d){if(!d||d==""||isNaN(d))return"";var n=parseInt(d);if(isNaN(n)||n<1)return d+"d";return n+"d"}""")
js_parts.append("""function cv(l){var m={'HAPAG':'#6c8cff','MSC':'#34d399','CMA':'#fbbf24','MAERSK':'#f87171','COSCO':'#a78bfa','OOCL':'#f472b6','ONE':'#2dd4bf','HYUNDAI':'#fb923c'};return m[l]||'#60a5fa'}""")
js_parts.append("""function mtd(t){t=t.toLowerCase();if(t.includes("urgent"))return"urgent";if(t.includes("delay"))return"delayed";return""}""")
js_parts.append('const CV=["#6c8cff","#34d399","#fbbf24","#f87171","#a78bfa","#f472b6","#2dd4bf","#fb923c","#60a5fa","#818cf8","#facc15","#4ade80","#c084fc","#38bdf8"];')
js_parts.append("")
js_parts.append("// State")
js_parts.append('var cs="origin",st="",cf_="",sf_="",pf_="",paPer=40,sortCol=-1,sortDir=1,_curPage=1,srdm="avg";')
js_parts.append('const OH=["Sl","SAP No","PtnrID","Supplier","POL","POD","Container No","20\'","40\'","Carrier","Vessel","POL ATD","Carrier ETA","Predictive ETA","Commit TT","Actual TT","Remark","Frt.Rate"];')
js_parts.append('const TH=["Sl","SAP No","PtnrID","Supplier","POL","POD","Container No","20\'","40\'","Carrier","T/S Vessel","POL ATD","Carrier ETA","Predictive ETA","Commit TT","Actual TT","Remark","Frt.Rate"];')
js_parts.append("")
js_parts.append("// Persistence")
js_parts.append("const HIDDEN={origin:new Set([6,7,8,14,15,16]),ts:new Set([6,7,8,14,15])};")
js_parts.append("try{if(localStorage.getItem('lcp_h')){const d=JSON.parse(localStorage.getItem('lcp_h'));for(const v of(d.origin||[]))HIDDEN.origin.add(v);for(const v of(d.ts||[]))HIDDEN.ts.add(v)}}catch(e){}")
js_parts.append("function saveH(){try{localStorage.setItem('lcp_h',JSON.stringify({origin:[...HIDDEN.origin],ts:[...HIDDEN.ts]}))}catch(e){}}")
js_parts.append("")

with open("E:/Samsudeen/Hermes agent/_js_head.js", "w") as f:
    f.write("\n".join(js_parts))
print(f"JS head: {sum(len(p) for p in js_parts)} chars")
print("Written _js_head.js")
