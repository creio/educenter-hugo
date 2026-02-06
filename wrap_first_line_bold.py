#!/usr/bin/env python3
"""
Script to process all markdown files in the cities_md directory.
Wraps the first line after frontmatter in ** ** (bold).
"""

import os
import glob

def process_markdown_files():
    # Get all markdown files in cities_md directory
    md_files = glob.glob("cities_md/*.md")
    
    print(f"Found {len(md_files)} markdown files to process...")
    
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
        
        # If we found the end of frontmatter, process the next line
        if frontmatter_end_idx != -1 and frontmatter_end_idx + 1 < len(lines):
            # Get the line after frontmatter
            line_after_frontmatter = lines[frontmatter_end_idx + 1]
            
            # Skip empty lines after frontmatter
            idx = frontmatter_end_idx + 1
            while idx < len(lines) and lines[idx].strip() == '':
                idx += 1
            
            if idx < len(lines):
                # Wrap the first non-empty line after frontmatter in bold
                original_line = lines[idx]
                if not (original_line.startswith('**') and original_line.endswith('**')):
                    lines[idx] = f"**{original_line.strip()}**"
                
                # Join the lines back together
                updated_content = '\n'.join(lines)
                
                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"  - Updated line: '{original_line}' -> '**{original_line.strip()}**'")
            else:
                print(f"  - No content found after frontmatter")
        else:
            print(f"  - Could not find proper frontmatter in file")
    
    print(f"\nSuccessfully processed {len(md_files)} files!")

if __name__ == "__main__":
    process_markdown_files()