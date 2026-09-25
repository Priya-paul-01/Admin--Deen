#!/usr/bin/env python3
"""Generate complete LCP dashboard HTML from data."""
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

# Build data arrays
or_parts = []
for r in origin:
    or_parts.append("[" + ",".join(e(v) for v in r) + "]")
or_str = "const OR=[" + ",".join(or_parts) + "];\n\n"

ts_parts = []
for r in ts:
    ts_parts.append("[" + ",".join(e(v) for v in r) + "]")
ts_str = "const TS=[" + ",".join(ts_parts) + "];\n"

data_js = or_str + ts_str
print(f"Data: OR={len(origin)} rows, TS={len(ts)} rows, {len(data_js)} chars")

# Write data to file
with open("E:/Samsudeen/Hermes agent/_data.js", "w") as f:
    f.write(data_js)

print("Done. _data.js written.")
