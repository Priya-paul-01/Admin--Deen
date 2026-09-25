with open('dashboard.html', 'rb') as f:
    data = f.read()

s = data.find(b'<script>')
e = data.find(b'</script>')
if s < 0 or e < 0:
    print('SCRIPT NOT FOUND')
    exit(1)

head = data[:s+8]
js = data[s+8:e]
tail = data[e:]

print(f'Script: {len(js)} bytes')

# Fix 1: remove extra } before getDisplayHeaders
pat1 = b'}\r\nfunction getDisplayHeaders'
if pat1 in js:
    js = js.replace(pat1, b'\r\nfunction getDisplayHeaders', 1)
    print('Fixed: extra } removed')
else:
    pat1b = b'}\nfunction getDisplayHeaders'
    if pat1b in js:
        js = js.replace(pat1b, b'\nfunction getDisplayHeaders', 1)
        print('Fixed: extra } removed ( LF )')

# Fix 2: lines.join("\r\n") -> lines.join("\\n") using byte replacement
bs_nl = bytes([92, 110])  # \ and n
idx = js.find(b'lines.join("')
if idx >= 0:
    oq = idx + len(b'lines.join("')
    cq = js.find(b'"', oq)
    inner = js[oq:cq]
    print(f'Join inner bytes: {inner} (hex: {inner.hex()})')
    if inner == b'\r\n' or inner == b'\n':
        js = js[:oq] + bs_nl + js[cq:]
        print(f'Fixed: replaced {inner} with backslash-n')
    elif inner == bs_nl:
        print('Already fixed')
    else:
        print(f'Unexpected: {inner}')

fixed = head + js + tail
with open('dashboard.html', 'wb') as f:
    f.write(fixed)
print(f'Written dashboard.html: {len(fixed)} bytes')

# Write JS to temp file for node check
with open('_verify.js', 'wb') as f:
    f.write(js)
print('Wrote _verify.js')
