import json

with open("E:/Samsudeen/Hermes agent/_full_data.json") as f:
    data = json.load(f)

origin = data["origin"]
ts = data["ts"]

def esc(s):
    if s is None or str(s).strip() == "": return '""'
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'

def num_or_str(v):
    if v == "" or v is None:
        return '""'
    try:
        fv = float(v)
        return str(int(fv)) if fv == int(fv) else str(fv)
    except:
        return esc(v)

# Build ORIGIN JS array
or_parts = []
for r in origin:
    parts = [num_or_str(v) for v in r]
    or_parts.append("[" + ",".join(parts) + "]")
OR_JS = "const OR=[" + ",".join(or_parts) + "];\n\n"

# Build TS JS array
ts_parts = []
for r in ts:
    parts = [num_or_str(v) for v in r]
    ts_parts.append("[" + ",".join(parts) + "]")
TS_JS = "const TS=[" + ",".join(ts_parts) + "];\n"

print(f"ORIGIN: {len(origin)} rows, {len(OR_JS)} chars")
print(f"TS: {len(ts)} rows, {len(TS_JS)} chars")

with open("E:/Samsudeen/Hermes agent/_data_arrays.js", "w") as f:
    f.write(OR_JS + TS_JS)
print("Written _data_arrays.js")
