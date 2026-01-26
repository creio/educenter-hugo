#!/usr/bin/env python3

import requests
import markdownify
import os

BASE_URL = "https://chinacampus.ru"
API_URL = f"{BASE_URL}/wp-json/wp/v2/posts"
OUTPUT_DIR = "articles_md"

os.makedirs(OUTPUT_DIR, exist_ok=True)

page = 1
while True:
    print(f"Fetching page {page}...")
    response = requests.get(API_URL, params={"per_page": 10, "page": page})
    if response.status_code != 200:
        print("No more pages or error:", response.status_code)
        break

    posts = response.json()
    if not posts:
        print("No more posts.")
        break

    for post in posts:
        title = post["title"]["rendered"]
        content = post["content"]["rendered"]
        slug = post["slug"]
        url = post["link"]
        post_date = post["date"]  # формат уже подходит для YAML

        # Экранируем кавычки для корректного YAML
        safe_title = title.replace('"', '\\"')

        front_matter = f"""---
title: "{safe_title}"
h1: "{safe_title}"
date: {post_date}
draft: false
bg_image: "images/backgrounds/page-title.jpg"
description: "Статья с сайта ChinaCampus: {safe_title}"
image: "images/blog/post-placeholder.jpg"
---"""

        md_content = f"{front_matter}\n\n{markdownify.markdownify(content, heading_style='ATX')}"

        # Очищаем slug от недопустимых символов (опционально)
        filename = f"{OUTPUT_DIR}/{slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md_content)

    page += 1  # ← обязательно!

print("Готово!")
