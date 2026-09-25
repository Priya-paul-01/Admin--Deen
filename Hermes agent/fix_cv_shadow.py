with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.find('<script>')
e = html.find('</script>')
js = html[s+8:e]

# Fix 3 inline chart blocks that shadow the global cv() function with local canvas variable 'cv'
# Pattern: each block has "const cv=document.getElementById(\"XXX\")" where XXX is rbc/ttbc/sc
# Then later uses "ctx.fillStyle=cv(...)" or "ctx.fillStyle=CV[i%CV.length]" depending on chart

replacements = [
    # rbc chart: uses CV[i%CV.length] for color
    ('const cv=document.getElementById("rbc");const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28',
     'const cvEl=document.getElementById("rbc");const ctx=cvEl.getContext("2d");const W=cvEl.parentElement.clientWidth-28'),
    # ttbc chart: uses cv(lb) for color
    ('const cv=document.getElementById("ttbc");const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28',
     'const cvEl=document.getElementById("ttbc");const ctx=cvEl.getContext("2d");const W=cvEl.parentElement.clientWidth-28'),
    # sc chart: uses CV[(i*3)%CV.length] for color
    ('const cv=document.getElementById("sc");const ctx=cv.getContext("2d");const W=cv.parentElement.clientWidth-28',
     'const cvEl=document.getElementById("sc");const ctx=cvEl.getContext("2d");const W=cvEl.parentElement.clientWidth-28'),
]

for old, new in replacements:
    count = js.count(old)
    if count > 0:
        js = js.replace(old, new)
        print(f'Replaced {count}x: {old[:50]}...')
    else:
        print(f'NOT FOUND: {old[:50]}...')

# Also fix the remaining references in those blocks: cv.getContext -> cvEl.getContext, cv.width -> cvEl.width etc
# Actually the replace above only covers the first occurrence. Need to fix all cv. references in each block.
# Let's do targeted fixes for each block.

# For rbc block: replace "cv.width" "cv.height" "cv.style" with cvEl equivalents
# But only within the rbc section. Since we already replaced the declaration, we need to
# replace subsequent cv. references. But the variable name 'cv' is also used by the global function.
# The safest approach: replace all "cv." that appear AFTER "const cvEl=document.getElementById("rbc")"
# up to the next function or chart block.

# Simpler: just replace the remaining cv. references in each block individually
# rbc uses CV[i%CV.length] for fillStyle so cv() isn't called there - just need cv. -> cvEl.
# ttbc calls cv(lb) for fillStyle - this MUST stay as cv(lb) since cv() is the global color function
# sc uses CV[(i*3)%CV.length] for fillStyle so cv() isn't called there either.

# So for rbc and sc: replace cv.width/cv.height/cv.style/cv.parentElement with cvEl equivalents
# For ttbc: same replacements, BUT keep cv(lb) as-is

# Let's find each block and fix

# Block 1: rbc - find start after "const cvEl=document.getElementById(\"rbc\")" replace to end of its forEach
rbc_start = js.find('const cvEl=document.getElementById("rbc")')
if rbc_start > 0:
    # Find the closing })) of the forEach that follows
    # Pattern: ctx.fillText(v.toFixed(0)...});}
    rbc_end = js.find('}));}', rbc_start)
    if rbc_end < 0:
        rbc_end = js.find('});}', rbc_start + 100)
    if rbc_end > 0:
        rbc_block = js[rbc_start:rbc_end+4]
        # Replace cv. with cvEl. in this block, but NOT cv( (global function call)
        # Actually rbc doesn't call cv() so we can safely replace all cv.
        rbc_fixed = rbc_block.replace('cv.', 'cvEl.')
        js = js[:rbc_start] + rbc_fixed + js[rbc_end+4:]
        print(f'Fixed rbc block ({len(rbc_block)} chars)')
    else:
        print('WARNING: could not find rbc block end')

# Block 2: ttbc - same but keep cv(lb) calls
ttbc_start = js.find('const cvEl=document.getElementById("ttbc")')
if ttbc_start > 0:
    ttbc_end = js.find('}));}', ttbc_start)
    if ttbc_end < 0:
        ttbc_end = js.find('});}', ttbc_start + 100)
    if ttbc_end > 0:
        ttbc_block = js[ttbc_start:ttbc_end+4]
        # Replace cv. with cvEl. but NOT cv(lb) (the global color function call)
        # cv(lb) pattern: cv immediately followed by (
        # We need to replace 'cv.' but not 'cv('
        fixed = ''
        i = 0
        while i < len(ttbc_block):
            if ttbc_block[i:i+3] == 'cv.' and (i == 0 or ttbc_block[i-1] != '('):
                fixed += 'cvEl.'
                i += 3
            else:
                fixed += ttbc_block[i]
                i += 1
        js = js[:ttbc_start] + fixed + js[ttbc_end+4:]
        print(f'Fixed ttbc block ({len(ttbc_block)} chars)')
    else:
        print('WARNING: could not find ttbc block end')

# Block 3: sc - same as rbc (no cv() calls)
sc_start = js.find('const cvEl=document.getElementById("sc")')
if sc_start > 0:
    sc_end = js.find('}));}', sc_start)
    if sc_end < 0:
        sc_end = js.find('});}', sc_start + 100)
    if sc_end > 0:
        sc_block = js[sc_start:sc_end+4]
        sc_fixed = sc_block.replace('cv.', 'cvEl.')
        js = js[:sc_start] + sc_fixed + js[sc_end+4:]
        print(f'Fixed sc block ({len(sc_block)} chars)')
    else:
        print('WARNING: could not find sc block end')

# Write back
html = html[:s+8] + js + html[e:]
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\nWritten: {len(html)} chars')
