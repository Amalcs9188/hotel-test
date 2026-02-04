"""
Search for review data inside script tags
"""
import re
import json

def search_scripts():
    with open('problem_snippet.html', encoding='utf-8') as f:
        content = f.read()
    
    # Look for scripts
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    print(f"Total scripts: {len(scripts)}")
    
    # Pattern for something that looks like an array of reviews
    # Looking for reviewer_name, review_text, or similar
    for i, script in enumerate(scripts):
        if len(script) < 100: continue
        
        # Search for common keys
        if 'reviewText' in script or 'reviewerName' in script or 'review_body' in script or 'review_comment' in script:
            print(f"--- Script {i} (Length: {len(script)}) contains review keys ---")
            print(script[:500] + "...")
            
            # Try to extract the JSON if it's there
            try:
                # Look for { ... "reviews": [ ... ] ... }
                # This is very rough
                pass
            except:
                pass

if __name__ == "__main__":
    search_scripts()
