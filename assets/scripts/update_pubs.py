#!/usr/bin/env python3
from scholarly import scholarly
from datetime import datetime

def main():
    author_name = "Alistair Plum"
    search = scholarly.search_author(author_name)
    try:
        author_dict = next(search)
    except StopIteration:
        return
    author_filled = scholarly.fill(author_dict)
    
    pubs = []
    for p in author_filled.get('publications', []):
        p_filled = scholarly.fill(p)
        bib = p_filled.get('bib', {})
        raw_year = bib.get('year') or bib.get('pub_year') or ''
        try:
            year_int = int(raw_year)
        except ValueError:
            year_int = 0  # fallback if not an integer
        title = bib.get('title', '')
        authors = bib.get('author', '').replace(' and ', ', ')
        name = f"{title}. {raw_year}. {authors}"
        url = bib.get('eprint_url') or p_filled.get('pub_url') or ''
        pubs.append({'name': name, 'year': str(year_int), 'sort_year': year_int, 'url': url})
    
    current_year = str(datetime.now().year)
    featured, index = [], []
    for pub in pubs:
        entry = {
            'name': pub['name'],
            'url': pub['url'],
            'sort_year': pub['sort_year']  # keep for sorting
        }
        if pub['year'] == current_year:
            featured.append({'name': pub['name'], 'url': pub['url']})
        index.append(entry)
    
    # Sort the index by 'sort_year' descending
    index.sort(key=lambda x: x['sort_year'], reverse=True)
    
    with open('../../_data/publications.yml', 'w', encoding='utf-8') as f:
        f.write("featured:\n")
        for p in featured:
            t = p['name'].replace("'", "\\'")
            u = p['url'].replace("'", "\\'")
            f.write(rf"- {{name: '{t}', url: '{u}'}}" + "\n")
        
        f.write("index:\n")
        for p in index:
            t = p['name'].replace("'", "\\'")
            u = p['url'].replace("'", "\\'")
            f.write(rf"- {{name: '{t}', url: '{u}'}}" + "\n")

if __name__ == "__main__":
    main()
