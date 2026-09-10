import re
import sys

def audit_html_js():
    with open('templates/index.html', encoding='utf-8') as f:
        html_content = f.read()

    with open('static/js/app.js', encoding='utf-8') as f:
        js_content = f.read()

    # 1. Check HTML IDs vs getElementById in JS
    html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html_content))
    onclick_handlers = set(re.findall(r'onclick=["\']([a-zA-Z0-9_]+)\(', html_content))

    print(f"[HTML] Total IDs in index.html: {len(html_ids)}")
    print(f"[HTML] Total onclick functions called: {len(onclick_handlers)}")

    js_get_ids = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_content))
    print(f"[JS] Total getElementById calls: {len(js_get_ids)}")

    missing_ids = [gid for gid in js_get_ids if gid not in html_ids]
    print(f"\n[CHECK 1] getElementById targets missing from index.html: {len(missing_ids)}")
    for m in missing_ids:
        print(f"  - Missing element ID: '{m}'")

    # 2. Check onclick handlers vs functions in JS
    js_functions = set(re.findall(r'(?:function\s+([a-zA-Z0-9_]+)\s*\(|const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\()', js_content))
    flat_js_functions = {fn for tuple_fn in js_functions for fn in tuple_fn if fn}
    # Add native window functions
    builtins = {'window', 'alert', 'print'}
    missing_handlers = [h for h in onclick_handlers if h not in flat_js_functions and h not in builtins]
    print(f"\n[CHECK 2] Onclick functions called in HTML but missing in JS: {len(missing_handlers)}")
    for h in missing_handlers:
        print(f"  - Missing function: '{h}'")

    # 3. Check JS Syntax by running node or python regex checks
    print("\n[CHECK 3] JS Syntax check...")
    brackets_diff = js_content.count('{') - js_content.count('}')
    parens_diff = js_content.count('(') - js_content.count(')')
    print(f"  - Curly brackets balance: {brackets_diff} (0 is balanced)")
    print(f"  - Parentheses balance: {parens_diff} (0 is balanced)")

if __name__ == '__main__':
    audit_html_js()
