with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.find('<script>')
e = html.find('</script>')
js = html[s+8:e]

lines = js.split('\n')

# Find line indices (not char positions) for renderCharts and getDisplayHeaders
rc_line = None
gd_line = None
for i, line in enumerate(lines):
    if 'function renderCharts()' in line:
        rc_line = i
        print(f'renderCharts at line {i+1}: {line.strip()[:80]}')
    if 'function getDisplayHeaders()' in line:
        gd_line = i

if rc_line is None:
    print('ERROR: renderCharts not found')
    exit(1)
if gd_line is None:
    print('ERROR: getDisplayHeaders not found')
    exit(1)

print(f'getDisplayHeaders at line {gd_line+1}')

# Find the closing } of renderCharts: the last standalone } between rc_line+1 and gd_line
close_line = None
for i in range(rc_line + 1, gd_line):
    if lines[i].strip() == '}':
        close_line = i

if close_line:
    print(f'Found closing }} at line {close_line+1}')
    catch_line = "  }catch(e){console.error('renderCharts error:',e)}"
    lines.insert(close_line, catch_line)
    print(f'Inserted catch block at line {close_line+1}')
else:
    print('ERROR: could not find closing } for renderCharts')
    # Show context
    for i in range(max(0,rc_line), min(len(lines), gd_line+2)):
        print(f'  L{i+1}: {lines[i].rstrip()[:100]}')

new_js = '\n'.join(lines)
html = html[:s+8] + new_js + html[e:]
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Written: {len(html)} chars')
