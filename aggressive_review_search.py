"""
Aggressive review search
"""
from bs4 import BeautifulSoup
import re

with open('problem_snippet.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("Searching for ANY review-like content...")

# Look for elements that have a rating (number) and some text
potential_cards = soup.find_all(['div', 'li'], class_=True)
for card in potential_cards:
    cls_str = " ".join(card['class'])
    if len(card.get_text(strip=True)) > 50:
        # Check if it has a score badge
        score_badge = card.find(class_=re.compile(r'score|badge|rating', re.I))
        if score_badge and score_badge.get_text(strip=True).replace('.','').isdigit():
            # Check if it has a name-like element
            print(f"Candidate Card - Class: {cls_str}")
            print(f"Content: {card.get_text(strip=True)[:150]}...")
            print("-" * 20)
            
# Look for data-testid values that might be reviews
for el in soup.find_all(attrs={"data-testid": True}):
    tid = el['data-testid']
    if 'review' in tid.lower():
        print(f"Found testid with review: {tid}")
        print(f"Content: {el.get_text(strip=True)[:100]}...")
