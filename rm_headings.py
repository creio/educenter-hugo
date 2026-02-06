#!/usr/bin/env python3
"""
Script to process all markdown files in the cities_md directory.
Removes '## ' and '### ' prefixes from headings and ensures exactly one blank line after frontmatter.
"""

import os
import glob
import re

def process_markdown_files():
    # Get all markdown files in cities_md directory
    md_files = glob.glob("cities_md/*.md")

    print(f"Found {len(md_files)} markdown files to process...")

    for file_path in md_files:
        print(f"Processing {file_path}...")

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        # Find the end of frontmatter (second '---' line)
        dash_count = 0
        frontmatter_end_idx = -1

        for i, line in enumerate(lines):
            if line.strip() == '---':
                dash_count += 1
                if dash_count == 2:
                    frontmatter_end_idx = i
                    break

        # Skip files without proper frontmatter
        if frontmatter_end_idx == -1:
            print(f"  ⚠️ Warning: Could not find end of frontmatter in {file_path}, skipping.")
            continue

        # Split into frontmatter and body
        frontmatter = lines[:frontmatter_end_idx + 1]  # Includes closing '---'
        body = lines[frontmatter_end_idx + 1:]

        # Remove '## ' and '### ' prefixes from body lines
        processed_body = []
        for line in body:
            # Remove exactly '## ' prefix (2 hashes + whitespace)
            if re.match(r'^##\s', line):
                processed_body.append(re.sub(r'^##\s*', '', line, count=1))
            # Remove exactly '### ' prefix (3 hashes + whitespace)
            elif re.match(r'^###\s', line):
                processed_body.append(re.sub(r'^###\s*', '', line, count=1))
            elif re.match(r'^####\s', line):
                processed_body.append(re.sub(r'^####\s*', '', line, count=1))
            else:
                processed_body.append(line)

        # Remove ALL leading blank lines from processed body
        while processed_body and processed_body[0].strip() == '':
            processed_body.pop(0)

        # Reconstruct with EXACTLY one blank line after frontmatter
        new_content = '\n'.join(frontmatter + [''] + processed_body)

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print(f"\n✅ Successfully processed {len(md_files)} files!")

if __name__ == "__main__":
    process_markdown_files()
