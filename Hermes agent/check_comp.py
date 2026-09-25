with open('dashboard.html','r',encoding='utf-8') as f:
    html=f.read()

s=html.find('<script>')
e=html.find('</script>')
js=html[s+8:e]

# Check the comp() function more carefully
comp_start = js.find('function comp(')
comp_end = js.find('function renderStats', comp_start)
comp_code = js[comp_start:comp_end] if comp_end > comp_start else js[comp_start:comp_start+600]

print('=== COMP FUNCTION FULL ===')
for line in comp_code.split('\n'):
    if line.strip():
        print(f'  {line.strip()[:140]}')

print()
print('=== KEY CHECKS ===')
print(f'comp has forEach with arrow: {"rows.forEach(r=>" in comp_code}')
print(f'comp accesses r[9] for carrier: {"r[9]" in comp_code}')
print(f'comp accesses r[5] for POD: {"r[5]" in comp_code}')
print(f'comp accesses r[3] for supplier: {"r[3]" in comp_code}')
print(f'comp accesses r[16] for remark: {"r[16]" in comp_code}')
print(f'comp accesses r[17] for rate: {"r[17]" in comp_code}')
print(f'comp accesses r[7] for 20ft: {"r[7]" in comp_code}')
print(f'comp accesses r[8] for 40ft: {"r[8]" in comp_code}')
print(f'comp accesses r[14] for TT: {"r[14]" in comp_code}')

# Check data arrays - are they properly formed?
or_start = js.find('const OR=[')
or_end = js.find('];', or_start) + 2
or_code = js[or_start:or_end]
print()
print(f'OR array: starts at {or_start}, ends at {or_end}, length={len(or_code)}')
print(f'OR first row sample: {or_code[or_code.find("[["):or_code.find("]],")+2][:120]}')

ts_start = js.find('const TS=[')
ts_end = js.find('];', ts_start) + 2
ts_code = js[ts_start:ts_end]
print(f'TS array: starts at {ts_start}, ends at {ts_end}, length={len(ts_code)}')
print(f'TS first row sample: {ts_code[ts_code.find("[[",1):ts_code.find("]],",1)+2][:120]}')

# Verify allD assignment
print()
print(f'allD assignment present: {"const allD={origin:OR,ts:TS}" in js or "allD={origin:OR" in js}')
alld_pos = js.find('allD={')
if alld_pos > 0:
    print(f'allD context: {js[alld_pos:alld_pos+60]}')
