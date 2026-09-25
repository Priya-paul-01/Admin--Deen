with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.find('<script>')
e = html.find('</script>')
js = html[s+8:e]

# Add try/catch around each chart block that could fail independently
# We'll wrap each "if(sortedXXX.length){...}" block in try/catch

# 1. rbc chart block
rbc_old = 'if(sortedRd.length){const cvEl=document.getElementById("rbc")'
rbc_new = 'try{if(sortedRd.length){const cvEl=document.getElementById("rbc")'
js = js.replace(rbc_old, rbc_new, 1)

# Find the closing of rbc block: after its forEach, it ends with });}}
# The rbc block ends right before "const sortedSup=" or "const rates="
rbc_end_marker = 'const sortedSup=Object.entries(s.sup)'
if rbc_end_marker in js:
    rbc_end = js.find(rbc_end_marker)
    # Go back to find the closing }))});
    # Pattern before sortedSup: });}\n\n\nconst sortedSup
    # Find the last });}\ before sortedSup
    before = js[:rbc_end]
    last_close = before.rfind('});}')
    if last_close > 0:
        # Insert }catch after the }));}
        js = js[:last_close+4] + '}catch(e){console.error("rbc chart:",e)}' + js[last_close+4:]
        print('Added rbc try/catch')
    
# 2. ttbc chart block
ttbc_old = 'if(sortedTt.length){const cvEl=document.getElementById("ttbc")'
ttbc_new = 'try{if(sortedTt.length){const cvEl=document.getElementById("ttbc")'
js = js.replace(ttbc_old, ttbc_new, 1)

ttbc_end_marker = 'const sortedSup=Object.entries(s.sup)'
# Actually ttbc comes BEFORE sc, and sc comes after ttbc
# Let me use sc start as ttbc end marker
sc_start_marker = 'const sortedSup=Object.entries(s.sup)'
sc_start = js.find(sc_start_marker)
before_sc = js[:sc_start]
last_ttbc_close = before_sc.rfind('});}')
if last_ttbc_close > 0:
    js = js[:last_ttbc_close+4] + '}catch(e){console.error("ttbc chart:",e)}' + js[last_ttbc_close+4:]
    print('Added ttbc try/catch')

# 3. sc chart block  
sc_old = 'if(sortedSup.length){const cvEl=document.getElementById("sc")'
sc_new = 'try{if(sortedSup.length){const cvEl=document.getElementById("sc")'
js = js.replace(sc_old, sc_new, 1)

# sc ends before "const rates=d.map"
rates_marker = 'const rates=d.map(function(r)'
rates_start = js.find(rates_marker)
before_rates = js[:rates_start]
last_sc_close = before_rates.rfind('});}')
if last_sc_close > 0:
    js = js[:last_sc_close+4] + '}catch(e){console.error("sc chart:",e)}' + js[last_sc_close+4:]
    print('Added sc try/catch')

# 4. rc chart (inline bar call) - wrap the bar call  
rc_old = 'bar("rc",rBins,5,null);'
rc_new = 'try{bar("rc",rBins,5,null)}catch(e){console.error("rc chart:",e)}'
js = js.replace(rc_old, rc_new, 1)
print('Added rc try/catch')

# 5. tc chart (inline bar call)  
tc_old = 'bar("tc",tBins,5,null);'
tc_new = 'try{bar("tc",tBins,5,null)}catch(e){console.error("tc chart:",e)}'
js = js.replace(tc_old, tc_new, 1)
print('Added tc try/catch')

# 6. esc chart (eta status)  
esc_old = 'const etaCt=document.getElementById("esc")'
esc_new = 'try{const etaCt=document.getElementById("esc")'
js = js.replace(esc_old, esc_new, 1)

# esc ends before "function getDisplayHeaders"
gdh_marker = 'function getDisplayHeaders()'
gdh_start = js.find(gdh_marker)
before_gdh = js[:gdh_start]
last_esc_close = before_gdh.rfind('});}')
if last_esc_close > 0:
    js = js[:last_esc_close+4] + '}catch(e){console.error("esc chart:",e)}' + js[last_esc_close+4:]
    print('Added esc try/catch')

# Write back
html = html[:s+8] + js + html[e:]
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\nWritten: {len(html)} chars')
