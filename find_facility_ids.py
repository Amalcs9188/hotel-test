"""
Find data-testid attributes related to facilities
"""
import re

with open('problem_snippet.html', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'data-testid="([^"]*)"', content)
related = [m for m in matches if any(x in m.lower() for x in ['facility', 'amenity', 'property-section'])]
print(sorted(list(set(related))))
