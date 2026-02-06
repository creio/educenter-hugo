#!/usr/bin/env python3
"""
Script to process all markdown files in the cities_md directory.
Adds logical heading structures (h2 and h3) to organize content.
"""

import os
import glob
import re

def process_markdown_files():
    # Get all markdown files in cities_md directory
    md_files = glob.glob("cities_md/*.md")
    
    print(f"Found {len(md_files)} markdown files to process...")
    
    # Define patterns for section headers that should become h2
    h2_patterns = [
        r'Что посмотреть\?',
        r'Еда.*',
        r'Куда сходить\?',
        r'Про индустрии и компании'
    ]
    
    # Compile regex patterns
    h2_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in h2_patterns]
    
    # Define patterns for subsections that should become h3
    h3_patterns = [
        r'Достопримечательности города',
        r'Что поесть',
        r'Развлечения и музеи',
        r'Компании и возможности'
    ]
    
    h3_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in h3_patterns]
    
    for file_path in md_files:
        print(f"Processing {file_path}...")
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into lines
        lines = content.split('\n')
        
        # Find the end of frontmatter (first line after the second '---')
        frontmatter_end_idx = -1
        dash_count = 0
        
        for i, line in enumerate(lines):
            if line.strip() == '---':
                dash_count += 1
                if dash_count == 2:
                    frontmatter_end_idx = i
                    break
        
        # Process the content after frontmatter
        if frontmatter_end_idx != -1:
            # Look for section headers and add appropriate markdown headings
            new_lines = lines[:frontmatter_end_idx + 1]  # Include the closing '---' of frontmatter
            
            i = frontmatter_end_idx + 1
            while i < len(lines):
                line = lines[i]
                
                # Check if this line is a section header that needs to become an h2
                is_h2 = False
                is_h3 = False
                
                # Check for h2 patterns
                for regex in h2_regexes:
                    if regex.match(line.strip()):
                        new_lines.append(f"## {line.strip()}")
                        is_h2 = True
                        break
                
                # If not an h2, check for h3 patterns (typically bold text that matches h3 patterns)
                if not is_h2:
                    clean_line = line.strip().strip('* ')
                    for regex in h3_regexes:
                        if regex.match(clean_line):
                            new_lines.append(f"### {clean_line}")
                            is_h3 = True
                            break
                
                # If it's neither h2 nor h3, just add the line as is
                if not is_h2 and not is_h3:
                    new_lines.append(line)
                
                i += 1
            
            # Join the lines back together
            updated_content = '\n'.join(new_lines)
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
    print(f"\nSuccessfully processed {len(md_files)} files!")

if __name__ == "__main__":
    process_markdown_files()
