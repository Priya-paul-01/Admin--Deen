import re, json

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.find('<script>')
e = html.find('</script>')
js = html[s+8:e]

# Extract OR and TS arrays as strings, then parse
def extract_array(js, name):
    pattern = f'const {name}='
    start = js.find(pattern) + len(pattern)
    end = js.find(']];', start)
    if end < 0:
        return None
    arr_str = js[start:end+2]  # include ]];
    # Wrap in brackets to make it a valid JS array literal
    # The array is [[row1],[row2],...] so just eval it
    return arr_str

or_str = extract_array(js, 'OR')
ts_str = extract_array(js, 'TS')

print(f'OR array string length: {len(or_str) if or_str else 0}')
print(f'TS array string length: {len(ts_str) if ts_str else 0}')

# Count rows by counting occurrences of '],' that separate rows
# In [[row1],[row2],...]], rows are separated by '],['
if or_str:
    or_row_count = or_str.count('],[')
    print(f'OR rows (by ], [ count): {or_row_count}')
    
if ts_str:
    ts_row_count = ts_str.count('],[')
    print(f'TS rows (by ], [ count): {ts_row_count}')

# Also count the number of '[' at positions that look like row starts
# Each row starts with '[' followed by a digit, emoji, or quote
if or_str:
    # Remove the outer [[ and trailing ]]
    inner = or_str[2:-2]
    # Split by '],[' to get individual rows
    rows = inner.split('],[')
    print(f'OR rows (by split): {len(rows)}')
    # Check first and last row
    if rows:
        print(f'First OR row preview: {rows[0][:80]}')
        print(f'Last OR row preview: {rows[-1][:80]}')

if ts_str:
    inner = ts_str[2:-2]
    rows = inner.split('],[')
    print(f'\nTS rows (by split): {len(rows)}')
    if rows:
        print(f'First TS row preview: {rows[0][:80]}')
        print(f'Last TS row preview: {rows[-1][:80]}')
