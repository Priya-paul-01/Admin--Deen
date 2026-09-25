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
    if v == "" or v is None: return '""'
    try:
        fv = float(v)
        return str(int(fv)) if fv == int(fv) else str(fv)
    except: return esc(v)

OR_JS = "const OR=[" + ",".join("[" + ",".join(num_or_str(v) for v in r) + "]" for r in origin) + "];\n\n"
TS_JS = "const TS=[" + ",".join("[" + ",".join(num_or_str(v) for v in r) + "]" for r in ts) + "];\n"

print(f"OR: {len(origin)} rows, {len(OR_JS)} chars")
print(f"TS: {len(ts)} rows, {len(TS_JS)} chars")

# Write ONLY the data arrays (small)
with open("E:/Samsudeen/Hermes agent/_data.js", "w") as f:
    f.write(OR_JS + TS_JS)
print("Written _data.js")
