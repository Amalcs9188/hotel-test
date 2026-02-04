"""
Parse PropertyReviewsRegionBlock
"""
from bs4 import BeautifulSoup

with open('problem_snippet.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

block = soup.find(attrs={"data-testid": "PropertyReviewsRegionBlock"})
if block:
    print("Found PropertyReviewsRegionBlock")
    # List all data-testid inside
    sub_testids = block.find_all(attrs={"data-testid": True})
    for el in sub_testids:
        print(f"Sub-testid: {el['data-testid']}, Text: {el.get_text(strip=True)[:50]}")
    
    # List all spans and divs with text
    all_text = block.find_all(['span', 'div', 'p'])
    print(f"Total text elements in block: {len(all_text)}")
    for el in all_text:
        txt = el.get_text(strip=True)
        if len(txt) > 20:
             print(f"TEXT: {txt[:100]}")
else:
    print("PropertyReviewsRegionBlock not found")
