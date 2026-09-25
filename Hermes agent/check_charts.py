with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.find('<script>')
e = html.find('</script>')
js = html[s+8:e]

# Find and check the donut function
donut_start = js.find('function donut(')
donut_end = js.find('function renderCharts')
if donut_start >= 0 and donut_end > donut_start:
    donut_code = js[donut_start:donut_end]
    print('=== DONUT FUNCTION ===')
    print(f'Length: {len(donut_code)} chars')
    print()
    for line in donut_code.split('\n'):
        if line.strip():
            print(f'  {line.strip()[:120]}')
else:
    print('Donut function not found!')

print()
print('=== KEY CHECKS ===')
print(f'donut has early return for empty: {"if(!sorted.length)return" in donut_code}')
print(f'donut references legId: {"getElementById(legId)" in donut_code}')
print(f'donut uses pal[i%pal.length]: {"pal[i%pal.length]" in donut_code}')

# Check the esc chart
eta_start = js.find('const etaS={')
eta_end = js.find('function getDisplayHeaders')
if eta_start >= 0:
    eta_code = js[eta_start:eta_end]
    print()
    print('=== ESC CHART ISSUE ===')
    # The esc chart uses 'const cv=document.getElementById("esc")' which shadows cv()
    if 'const cv=document.getElementById("esc")' in eta_code:
        print('ISSUE: esc chart has cv=document shadow (same bug as before!)')
    if 'const cvEl=document.getElementById("esc")' in eta_code:
        print('OK: esc chart uses cvEl')
    # Check for cv() calls in esc
    if 'cv(' in eta_code.replace('cvEl.', ''):
        print('WARNING: potential cv() call in esc')
    # Print esc chart canvas setup
    for line in eta_code.split('\n'):
        if 'cv=' in line or 'ctx=' in line or 'width=' in line or 'getContext' in line:
            print(f'  {line.strip()[:120]}')
