#!/usr/bin/env python3
"""Extract data from an .xlsx file using only stdlib (zipfile + xml)."""
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import OrderedDict

def col_to_idx(col_str):
    """Convert column letters (ABC...) to 0-based index."""
    result = 0
    for ch in col_str:
        result = result * 26 + (ord(ch) - ord('A') + 1)
    return result - 1

def parse_cell_ref(ref):
    """Parse 'A1' -> (col_idx, row_idx)."""
    import re
    m = re.match(r'^([A-Z]+)(\d+)$', ref)
    if not m:
        return None, None
    col = col_to_idx(m.group(1))
    row = int(m.group(2)) - 1  # 0-based
    return col, row

def read_shared_strings(zf):
    """Read shared strings from xl/sharedStrings.xml."""
    try:
        with zf.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
        ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        strings = []
        for si in tree.findall('.//s:si', ns):
            # concatenate all text nodes
            texts = []
            for t in si.findall('.//s:t', ns):
                if t.text:
                    texts.append(t.text)
            strings.append(''.join(texts))
        return strings
    except KeyError:
        return []

def read_sheet(zf, sheet_path, shared_strings):
    """Read a sheet XML and return a list of rows (list of dicts)."""
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    with zf.open(sheet_path) as f:
        tree = ET.parse(f)
    
    rows = []
    sheet_data = tree.find(f'{{{ns}}}sheetData')
    if sheet_data is None:
        return rows
    
    for row_elem in sheet_data.findall(f'{{{ns}}}row'):
        row_idx = int(row_elem.get('r'))
        cells = {}
        for cell_elem in row_elem.findall(f'{{{ns}}}c'):
            ref = cell_elem.get('r')
            col_idx, _ = parse_cell_ref(ref) if ref else (None, None)
            t = cell_elem.get('t', '')  # type
            v_elem = cell_elem.find(f'{{{ns}}}v')
            is_elem = cell_elem.find(f'{{{ns}}}is')
            
            value = None
            if t == 's' and v_elem is not None:
                # shared string
                idx = int(v_elem.text)
                value = shared_strings[idx] if idx < len(shared_strings) else None
            elif t == 'inlineStr' and is_elem is not None:
                texts = []
                for t_elem in is_elem.findall(f'.//{{{ns}}}t'):
                    if t_elem.text:
                        texts.append(t_elem.text)
                value = ''.join(texts)
            elif v_elem is not None:
                value = v_elem.text
            elif t == 'b':
                value = bool(cell_elem.get('v', '0') == '1')
            
            if col_idx is not None and value is not None:
                cells[col_idx] = value
        
        if cells:
            rows.append({'row': row_idx, 'cells': cells})
    
    return rows

def get_sheet_paths(zf):
    """Get all sheet paths from the workbook."""
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    with zf.open('xl/workbook.xml') as f:
        tree = ET.parse(f)
    
    sheets = []
    for sheet_elem in tree.findall(f'.//{{{ns}}}sheet'):
        name = sheet_elem.get('name')
        rid = sheet_elem.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        sheets.append((name, rid))
    
    # Read relationships
    with zf.open('xl/_rels/workbook.xml.rels') as f:
        rels_tree = ET.parse(f)
    rels_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    rel_map = {}
    for rel in rels_tree.findall(f'{{{rels_ns}}}Relationship'):
        rel_map[rel.get('Id')] = rel.get('Target')
    
    result = []
    for name, rid in sheets:
        target = rel_map.get(rid, '')
        result.append((name, f'xl/{target}' if not target.startswith('/') else f'xl{target[1:]}'))
    
    return result

def main():
    path = sys.argv[1]
    with zipfile.ZipFile(path, 'r') as zf:
        shared = read_shared_strings(zf)
        sheet_paths = get_sheet_paths(zf)
        
        for sheet_name, sheet_path in sheet_paths:
            print(f"=== Sheet: {sheet_name} ===")
            rows = read_sheet(zf, sheet_path, shared)
            for row in rows:
                max_col = max(row['cells'].keys()) if row['cells'] else -1
                values = []
                for i in range(max_col + 1):
                    values.append(str(row['cells'].get(i, '')))
                print('\t'.join(values))

if __name__ == '__main__':
    main()
