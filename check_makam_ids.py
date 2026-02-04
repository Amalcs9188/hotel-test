"""
Check Makam testids
"""
import re

with open('makam_snippet.html', encoding='utf-8') as f:
    content = f.read()

test_ids = re.findall(r'data-testid="([^"]*review[^"]*)"', content)
print(f"Makam review test-ids: {sorted(list(set(test_ids)))}")
