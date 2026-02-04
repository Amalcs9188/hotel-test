"""
Script to find any review-like data in the snippet
"""
from bs4 import BeautifulSoup
import re

with open('problem_snippet.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("Searching for reviews...")

# 1. Any element with "review" in id or class
review_elements = soup.find_all(class_=re.compile(r'review', re.I))
print(f"Found {len(review_elements)} elements with 'review' in class")

# 2. Look for text that looks like a score (e.g. 7.5, 8.2) inside those elements
for el in review_elements[:20]:
    txt = el.get_text(strip=True)[:50]
    if txt:
        print(f"  Class: {el['class']}, Text: {txt}")

# 3. Look for "Staff", "Cleanliness", etc.
categories = ["Staff", "Cleanliness", "Location", "Facilities", "Comfort", "Value for money"]
for cat in categories:
    el = soup.find(text=re.compile(cat))
    if el:
        print(f"Found category {cat} in element: {el.parent.get_text(strip=True)}")

# 4. Search for the actual review comments if they exist
# Usually they are in a <p> or <span> inside a review block
potential_comments = soup.find_all(['p', 'span', 'div'], text=re.compile(r'.{20,}'))
print(f"Found {len(potential_comments)} elements with more than 20 chars")
for i, el in enumerate(potential_comments):
    txt = el.get_text(strip=True)
    if "Staff" in txt or "Good" in txt or "Bad" in txt:
        if len(txt) > 50:
            print(f"Potential Review: {txt[:100]}...")
    if i > 500: break
