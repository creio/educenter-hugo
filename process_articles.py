#!/usr/bin/env python3
"""
Script to update articles_md files with appropriate categories and tags based on content,
and improve text uniqueness.
"""

import os
import re
from pathlib import Path
import random

def get_category_and_tags(content):
    """Determine appropriate category and tags based on content."""
    content_lower = content.lower()
    
    # Define keywords for each category
    education_keywords = [
        'образование', 'обучение', 'вуз', 'университет', 'студент', 'школа', 'учеба', 
        'поступление', 'грант', 'ccn', 'ifp', 'китайский язык', 'языковые курсы',
        'бакалавриат', 'магистратура', 'докторантура', 'олимпиада', 'конкурс'
    ]
    
    culture_keywords = [
        'культура', 'традиции', 'обычаи', 'традиция', 'обычай', 'жизнь', 'быт',
        'традиции китая', 'китайцы', 'жизнь в китае', 'адаптация', 'китайская культура'
    ]
    
    travel_keywords = [
        'путешествие', 'путешествия', 'поездка', 'поездки', 'таивань', 'китай',
        'туризм', 'визит', 'путешественник', 'страна', 'город', 'регион'
    ]
    
    technology_keywords = [
        'технологии', 'технология', 'инновации', 'инновация', '5g', 'телефон',
        'интернет', 'приложение', 'смартфон', 'телематика', 'телемедицина'
    ]
    
    # Count keywords for each category
    edu_count = sum(content_lower.count(keyword) for keyword in education_keywords)
    cult_count = sum(content_lower.count(keyword) for keyword in culture_keywords)
    trav_count = sum(content_lower.count(keyword) for keyword in travel_keywords)
    tech_count = sum(content_lower.count(keyword) for keyword in technology_keywords)
    
    # Determine primary category based on keyword counts
    category_counts = [
        ('Образование', edu_count),
        ('Культура', cult_count),
        ('Путешествия', trav_count),
        ('Технологии', tech_count)
    ]
    
    # Sort by count to get the most relevant category
    primary_category = max(category_counts, key=lambda x: x[1])[0]
    
    # If no strong match, default to Образование
    if max(category_counts, key=lambda x: x[1])[1] == 0:
        primary_category = 'Образование'
    
    # Define tags based on content
    tags = []
    
    # Common tags
    if 'китай' in content_lower or 'китае' in content_lower or 'китайский' in content_lower:
        tags.append('Китай')
        
    if 'грант' in content_lower or 'гранты' in content_lower:
        tags.append('Гранты')
        
    if 'язык' in content_lower and 'китайск' in content_lower:
        if 'Китай' not in tags:
            tags.append('Китай')
        tags.append('Китайский язык')
        
    if 'ccn' in content_lower or 'china campus network' in content_lower:
        tags.append('CCN')
        
    if 'студент' in content_lower or 'студенты' in content_lower:
        tags.append('Студенты')
        
    if 'университет' in content_lower or 'вуз' in content_lower:
        tags.append('Университеты')
        
    if 'традици' in content_lower:
        tags.append('Традиции')
        
    if 'обычаи' in content_lower:
        tags.append('Обычаи')
        
    if 'путешеств' in content_lower:
        tags.append('Путешествия')
        
    if 'таивань' in content_lower or 'тайвань' in content_lower:
        tags.append('Тайвань')
        
    if 'технологи' in content_lower:
        tags.append('Технологии')
        
    if 'конкурс' in content_lower or 'олимпиад' in content_lower:
        tags.append('Конкурсы')
        
    if 'обучение' in content_lower:
        tags.append('Образование')
        
    # Limit to max 2 tags
    if len(tags) > 2:
        tags = tags[:2]
    elif len(tags) == 0:
        # Default tag if no specific tags found
        tags = ['Образование']
    
    return primary_category, tags

def improve_text_uniqueness(content):
    """Make minor changes to improve text uniqueness while preserving meaning."""
    # Add some variations to common phrases
    variations = {
        r'\bобразование в китае\b': ['обучение в Поднебесной', 'высшее образование в КНР', 'система образования в Китае'],
        r'\bкитайский язык\b': ['язык китайской народности', 'мандаринский диалект', 'китайская речь'],
        r'\bкитайские университеты\b': ['вузы Китайской Республики', 'китайские вузы', 'университеты Поднебесной'],
        r'\bиностранные студенты\b': ['студенты из других стран', 'иностранцы-студенты', 'зарубежные учащиеся'],
        r'\bпоступить в китай\b': ['получить место в китайском вузе', 'вступить в китайский университет', 'зачислиться в китайский вуз'],
        r'\bкитайская культура\b': ['культурные особенности Китая', 'традиции Поднебесной', 'культурное наследие Китая'],
        r'\bкитайские традиции\b': ['традиции Поднебесной', 'национальные обычаи Китая', 'культурные традиции КНР'],
        r'\bобучение в китае\b': ['учеба в Поднебесной', 'процесс обучения в КНР', 'студенчество в Китае'],
        r'\bкитайские вузы\b': ['университеты Китая', 'китайские высшие учебные заведения', 'вузы Поднебесной'],
        r'\bв китае\b': ['в Поднебесной', 'в КНР', 'в Китайской Республике']
    }
    
    modified_content = content
    
    for pattern, options in variations.items():
        if re.search(pattern, modified_content, re.IGNORECASE):
            replacement = random.choice(options)
            modified_content = re.sub(pattern, replacement, modified_content, flags=re.IGNORECASE)
    
    # Add some unique phrases to make content more distinctive
    if '!' in modified_content:
        # Add a unique phrase occasionally
        if random.random() > 0.7:  # 30% chance
            unique_phrases = [
                'Интересный факт: ',
                'Важно знать: ',
                'Примечательно, что: ',
                'Заметим: '
            ]
            phrase = random.choice(unique_phrases)
            # Insert at a random position
            sentences = modified_content.split('. ')
            if len(sentences) > 3:
                insert_pos = random.randint(1, min(len(sentences)-1, 3))
                sentences[insert_pos] = phrase + sentences[insert_pos]
                modified_content = '. '.join(sentences)
    
    return modified_content

def process_article_file(filepath):
    """Process a single article file to add categories and tags."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if front matter already exists
    if content.startswith('---'):
        # Split front matter and content
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            body = parts[2]
            
            # Check if categories or tags already exist
            has_categories = 'categories:' in front_matter
            has_tags = 'tags:' in front_matter
            
            if has_categories and has_tags:
                print(f"Skipping {filepath.name} - already has categories and tags")
                return
                
            # Get content for categorization (combine front matter and body)
            full_content_for_analysis = front_matter + body
        else:
            # If malformed, treat entire content as body
            body = content
            front_matter = ""
            full_content_for_analysis = content
    else:
        # No front matter, treat all as body
        body = content
        front_matter = ""
        full_content_for_analysis = content
    
    # Determine category and tags based on content
    category, tags = get_category_and_tags(full_content_for_analysis)
    
    # Improve text uniqueness
    unique_body = improve_text_uniqueness(body)
    
    # Create new front matter with categories and tags
    if front_matter:
        # Add categories and tags to existing front matter
        fm_lines = front_matter.strip().split('\n')
        
        # Check if categories and tags already exist
        categories_exists = any(line.strip().startswith('categories:') for line in fm_lines)
        tags_exists = any(line.strip().startswith('tags:') for line in fm_lines)
        
        if not categories_exists:
            # Find position to insert categories (before tags if tags exist)
            insert_pos = len(fm_lines)
            for i, line in enumerate(fm_lines):
                if line.strip().startswith('tags:'):
                    insert_pos = i
                    break
            fm_lines.insert(insert_pos, f'categories: ["{category}"]')
        
        if not tags_exists:
            # Find position to insert tags (at end or after categories)
            fm_lines.append(f'tags: {tags}')
        
        new_front_matter = '\n'.join(fm_lines)
    else:
        # Create new front matter
        new_front_matter = f"""title: "New Title"
h1: "New H1"
date: {os.popen('date -Iseconds').read().strip()}
draft: false
bg_image: "images/backgrounds/page-title.jpg"
description: "Description of the article"
image: "images/blog/post-placeholder.jpg"
categories: ["{category}"]
tags: {tags}"""
    
    # Combine everything
    new_content = f"---\n{new_front_matter}\n---\n{unique_body}"
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {filepath.name} with category: '{category}' and tags: {tags}")

def main():
    articles_dir = Path('/media/files/work/educenter-hugo/articles_md')
    
    if not articles_dir.exists():
        print(f"Directory {articles_dir} does not exist!")
        return
    
    # Process all markdown files in articles_md
    md_files = list(articles_dir.glob('*.md'))
    
    print(f"Processing {len(md_files)} files...")
    
    for filepath in md_files:
        try:
            process_article_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath.name}: {str(e)}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()