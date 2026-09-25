with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.find('<script>')
e = html.find('</script>')
js = html[s+8:e]

# Revert the scattered try/catch insertions that broke syntax
# Remove the broken try{ insertions (they lack matching catch)
# and remove the catch blocks that were added in wrong places

# 1. Revert rbc: remove try{ and the catch that was added
js = js.replace('try{if(sortedRd.length){const cvEl=document.getElementById("rbc")',
                'if(sortedRd.length){const cvEl=document.getElementById("rbc")', 1)

# 2. Revert ttbc
js = js.replace('try{if(sortedTt.length){const cvEl=document.getElementById("ttbc")',
                'if(sortedTt.length){const cvEl=document.getElementById("ttbc")', 1)

# 3. Revert sc
js = js.replace('try{if(sortedSup.length){const cvEl=document.getElementById("sc")',
                'if(sortedSup.length){const cvEl=document.getElementById("sc")', 1)

# 4. Revert esc
js = js.replace('try{const etaCt=document.getElementById("esc")',
                'const etaCt=document.getElementById("esc")', 1)

# 5. Revert donut
js = js.replace('try{donut("pc","pl",s.pod)}catch(e){console.error("donut pc:",e)}',
                'donut("pc","pl",s.pod)', 1)

# Clean up any orphaned catch blocks
# Pattern: '});}catch(e){...}' that's left stranded
import re
# Remove '}catch(e){console.error("rbc chart:",e)}' etc that are orphaned
for chart in ['rbc', 'ttbc', 'sc', 'esc']:
    js = re.sub(r'\}\}\)\}\;catch\(e\)\{console\.error\("' + chart + ' chart:",e\}\)', '});})', js)

# Also remove rc/tc try/catch (they might be OK but let's keep it simple)
js = js.replace('try{bar("rc",rBins,5,null)}catch(e){console.error("rc chart:",e)}',
                'bar("rc",rBins,5,null)', 1)
js = js.replace('try{bar("tc",tBins,5,null)}catch(e){console.error("tc chart:",e)}',
                'bar("tc",tBins,5,null)', 1)

html = html[:s+8] + js + html[e:]
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify syntax
with open('_v.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f'Written: {len(html)} chars')
print('Reverted all try/catch additions')
