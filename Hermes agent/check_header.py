with open('dashboard.html','r',encoding='utf-8') as f:
    html=f.read()

s=html.find('<script>')
e=html.find('</script>')
js=html[s+8:e]

# Check renderStats function
rs_start=js.find('function renderStats()')
rs_end=js.find('function bar(', rs_start)
if rs_start>=0:
    rs_code=js[rs_start:rs_end] if rs_end>rs_start else js[rs_start:rs_start+500]
    print('=== RENDER STATS FUNCTION ===')
    print(f'Length: {len(rs_code)} chars')
    print()
    for line in rs_code.split(chr(10)):
        if line.strip():
            print(f'  {line.strip()[:130]}')
else:
    print('renderStats not found!')

print()
# Check which elements are populated
print('=== ELEMENTS CHECK ===')
checks = [
    ('sg', 'stats cards container'),
    ('rCnt', 'report count'),
    ('oc', 'origin count badge'),
    ('tc2', 'TS count badge'),
    ('cf', 'carrier filter'),
    ('sf', 'supplier filter'),
    ('pf', 'POD filter'),
    ('si', 'search input'),
]
for el_id, desc in checks:
    pattern = f'document.getElementById("{el_id}")'
    if pattern in js:
        # Find the line
        for line_num, line in enumerate(js.split(chr(10)),1):
            if pattern in line:
                print(f'  {el_id} ({desc}): L{line_num} - {line.strip()[:100]}')
                break
    else:
        print(f'  {el_id} ({desc}): NOT FOUND in JS')
