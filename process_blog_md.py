#!/usr/bin/env python3
"""
Script to update frontmatter in all markdown files in content/blog directory.
Replaces:
1. bg_image: "images/backgrounds/page-title.jpg" → bg_image: "images/backgrounds/blog-title.jpg"
2. image: "images/blog/post-placeholder.jpg" → image: ""
"""

import os
import glob

def update_frontmatter():
    # Get all markdown files in content/blog directory
    md_files = glob.glob("content/blog/**/*.md", recursive=True)

    print(f"Found {len(md_files)} markdown files to process...")

    old_bg = 'bg_image: "images/backgrounds/page-title.jpg"'
    new_bg = 'bg_image: "images/backgrounds/blog-title.jpg"'

    old_img = 'image: "images/blog/post-placeholder.jpg"'
    new_img = 'image: ""'

    updated_count = 0

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Track if changes were made
        changed = False

        # Replace bg_image
        if old_bg in content:
            content = content.replace(old_bg, new_bg)
            changed = True

        # Replace image
        if old_img in content:
            content = content.replace(old_img, new_img)
            changed = True

        # Write back only if changes were made
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            updated_count += 1

    print(f"\n✅ Successfully updated {updated_count} files!")

if __name__ == "__main__":
    update_frontmatter()
