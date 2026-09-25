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

def make_array(rows):
    parts = []
    for r in rows:
        parts.append("[" + ",".join(fmt(v) for v in r) + "]")
    return "const X=[" + ",".join(parts) + "];\n"

or_js = make_array(origin).replace("const X", "const OR")
ts_js = make_array(ts).replace("const X", "const TS")
data_js = or_js + "\n" + ts_js

# Write data
with open("E:/Samsudeen/Hermes agent/_data.js", "w") as f:
    f.write(data_js)

print(f"Data: {len(origin)} origin + {len(ts)} ts rows, {len(data_js)} chars")

# Now generate the full HTML from template files
template = "E:/Samsudeen/Hermes agent/_dashboard_template.html"
output = "E:/Samsudeen/Hermes agent/dashboard.html"

# Read template
with open(template) as f:
    template_content = f.read()

# Replace placeholder
html = template_content.replace("/*DATA*/", data_js)

# Write output
with open(output, "w") as f:
    f.write(html)

print(f"Output: {len(html)} chars -> {output}")
