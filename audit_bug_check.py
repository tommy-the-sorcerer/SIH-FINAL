"""
Audit script entrypoint (forwards to scripts/audit_bug_check.py)
"""
from scripts.audit_bug_check import audit_html_js

if __name__ == '__main__':
    audit_html_js()
