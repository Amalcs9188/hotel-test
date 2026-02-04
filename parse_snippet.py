"""
Parse the problematic snippet to investigate scraper logic
"""
from bs4 import BeautifulSoup
import json

def parse_snippet():
    with open('problem_snippet.html', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    results = {
        'amenities': [],
        'reviews': []
    }
    
    # Check amenities
    # Current selectors: [data-testid="facility-group"], .hp-facility-block, .facilitiesChecklistSection
    amenity_groups = soup.select('[data-testid="facility-group"], [data-testid="facility-group-container"], .hp-facility-block, .facilitiesChecklistSection')
    print(f"Found {len(amenity_groups)} amenity groups")
    
    for group in amenity_groups:
        title_el = group.select_one('[data-testid="facility-group-title"], .bui-title__text, h3')
        category = title_el.get_text(strip=True) if title_el else "General"
        
        items = group.select('li, [data-testid="facility-item"], .bui-list__item')
        for item in items:
            name = item.get_text(strip=True)
            if name:
                results['amenities'].append({'category': category, 'name': name})
    
    # Check reviews
    # Current selectors: [data-testid="review-card"], .review_item
    review_cards = soup.select('[data-testid="review-card"], [data-testid="review-item"], .review_item, .c-review-block')
    print(f"Found {len(review_cards)} review cards")
    
    for i, card in enumerate(review_cards):
        if i >= 10: break
        
        reviewer_el = card.select_one('.bui-avatar-block__title, .review_item_reviewer_name, .bui-avatar-block__title')
        reviewer = reviewer_el.get_text(strip=True) if reviewer_el else "Anonymous"
        
        score_el = card.select_one('.bui-review-score__badge, .review-score-badge, .bui-review-score__badge')
        score = score_el.get_text(strip=True) if score_el else "0"
        
        comment_el = card.select_one('.c-review__body, .review_item_header_content, .c-review-block__title')
        comment = comment_el.get_text(strip=True) if comment_el else ""
        
        results['reviews'].append({
            'reviewer': reviewer,
            'score': score,
            'comment': comment
        })

    # If NO reviews found, try finding ANY review-like structure
    if not results['reviews']:
        print("Looking for alternative review structures...")
        # Search for any text that looks like a review
        potential_reviews = soup.select('.review_list_new_item_block, .review_item, .hp-social-review-item')
        print(f"Found {len(potential_reviews)} potential reviews via alternative classes")
        for i, card in enumerate(potential_reviews):
             results['reviews'].append({'raw': card.get_text(strip=True)[:100]})

    return results

if __name__ == "__main__":
    res = parse_snippet()
    print(json.dumps(res, indent=2))
