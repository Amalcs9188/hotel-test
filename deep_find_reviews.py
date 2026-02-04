"""
Deep dive into snippet to find reviews
"""
from bs4 import BeautifulSoup
import re

def find_reviews():
    with open('problem_snippet.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    print("--- Searching for Review Indicators ---")
    
    # Check for review-related IDs or classes
    indicators = soup.find_all(attrs={"class": re.compile(r'review', re.I)})
    print(f"Elements with 'review' in class: {len(indicators)}")
    
    # Check for specific data-testids again
    test_ids = soup.find_all(attrs={"data-testid": re.compile(r'review', re.I)})
    print(f"Elements with 'review' in data-testid: {len(test_ids)}")
    for el in test_ids[:10]:
        print(f"  ID: {el.get('data-testid')}, Tag: {el.name}, Text: {el.get_text(strip=True)[:50]}")

    # Look for "Read all reviews" link
    read_all = soup.find('a', text=re.compile(r'Read all reviews', re.I))
    if read_all:
        print(f"Found 'Read all reviews' link: {read_all.get('href')}")

    # Look for ANY block that looks like a review (Score + Text + Name)
    # Usually reviews have a score badge (e.g. 7.5) and a username
    print("\n--- Searching for (Score + Text) patterns ---")
    potential_text = soup.find_all(['span', 'p', 'div'], text=re.compile(r'.{30,}'))
    for el in potential_text:
        txt = el.get_text(strip=True)
        if len(txt) > 50 and len(txt) < 500:
            # Check if there is a badge nearby
            parent = el.parent
            if parent:
                badge = parent.find(class_=re.compile(r'score|badge', re.I))
                if badge:
                    print(f"Potential Review Found!\nText: {txt[:100]}...\nBadge nearby: {badge.get_text(strip=True)}")
                    print(f"Parent Class: {parent.get('class')}")

    # Check for invisible blocks
    hidden = soup.find_all(style=re.compile(r'display:\s*none', re.I))
    review_hidden = [h for h in hidden if 'review' in str(h).lower()]
    print(f"\nHidden review elements: {len(review_hidden)}")

if __name__ == "__main__":
    find_reviews()
