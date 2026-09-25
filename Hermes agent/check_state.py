import re

with open('dashboard.html','r',encoding='utf-8') as f:
    html=f.read()
s=html.find('<script>')
e=html.find('</script>')
js=html[s+8:e]

# Quick checks
print('Script tags:', re.findall(r'</?script>', html))
print()

or_rows = js.count('],[')
print('OR+TS rows (], [ count):', or_rows)
print('const OR=[ in js:', 'const OR=[' in js)
print('const TS=[ in js:', 'const TS=[' in js)
print()

for fn in ['renderStats', 'renderCharts', 'renderTable', 'comp', 'bar', 'donut', 'esd', 'fd']:
    print(fn + ': ' + str('function ' + fn + '(' in js))
print()

print('Extra } removed: ' + str(js.count('\n}\nfunction getDisplayHeaders') > 0))
print('lines.join fixed: ' + str('lines.join("\\n")' in js))
print('cvEl shadowing fixed: ' + str('const cvEl=document.getElementById("ttbc")' in js))
print('try/catch added: ' + str('catch(e){console.error' in js))
print()

print('HTML size:', len(html), 'bytes, JS size:', len(js), 'bytes')
