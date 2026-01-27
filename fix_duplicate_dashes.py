#!/usr/bin/env python3
"""
Script to fix duplicate --- lines at the beginning of articles_md files
"""

import os
from pathlib import Path

def fix_duplicate_dashes(filepath):
    """Fix duplicate --- lines at the beginning of the file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Print first few lines for debugging
    print(f"Processing {filepath.name}, first 5 lines: {lines[:5]}")
    
    # Check if the file starts with the problematic pattern: standalone '---' followed by empty line, then actual front matter with '---'
    # This means lines[0] == '---', lines[1] == '', lines[2] == '---'
    if (len(lines) >= 3 and 
        lines[0] == '---' and 
        lines[1] == '' and 
        lines[2] == '---'):
        
        print(f"Found issue in {filepath.name}, fixing...")
        
        # Remove the first '---' and the empty line, keeping the third '---' as the start of actual front matter
        # So we remove lines[0] and lines[1], keeping lines[2] onwards
        corrected_lines = lines[2:]  # Remove the first two lines
        corrected_content = '\n'.join(corrected_lines)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        
        print(f"Fixed {filepath.name}")
    elif (len(lines) >= 2 and
          lines[0] == '---' and
          lines[1] == '' and
          'title:' in content):
        # Alternative pattern: standalone '---' followed by empty line, then actual front matter starts without '---'
        # This would mean the first '---' is spurious and should be removed
        print(f"Found alternative issue in {filepath.name}, fixing...")
        
        # Remove just the first '---' and the empty line
        corrected_lines = lines[2:]  # Remove the first two lines
        corrected_content = '\n'.join(corrected_lines)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        
        print(f"Fixed {filepath.name}")
    else:
        print(f"No issue found in {filepath.name}")


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
            fix_duplicate_dashes(filepath)
        except Exception as e:
            print(f"Error processing {filepath.name}: {str(e)}")
    
    print("Processing complete!")


if __name__ == "__main__":
    main()