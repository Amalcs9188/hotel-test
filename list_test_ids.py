"""
List all data-testid values from the file
"""
import re

with open('problem_snippet.html', encoding='utf-8') as f:
    content = f.read()

test_ids = re.findall(r'data-testid="([^"]+)"', content)
unique_ids = sorted(list(set(test_ids)))

with open('test_ids.txt', 'w') as f:
    for tid in unique_ids:
        f.write(tid + '\n')

print(f"Found {len(unique_ids)} unique test-ids. Saved to test_ids.txt")
