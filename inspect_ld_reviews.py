"""
Inspect JSON-LD reviews
"""
import json
import re

with open('problem_snippet.html', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'application/ld\+json[^>]*>(.*?)</script>', content, re.DOTALL)
for m in matches:
    try:
        data = json.loads(m)
        if 'review' in data:
            reviews = data['review']
            print(f"Found {len(reviews)} reviews in JSON-LD")
            for i, r in enumerate(reviews[:3]):
                print(f"Review {i}:")
                for k, v in r.items():
                    print(f"  {k}: {v}")
    except:
        pass
