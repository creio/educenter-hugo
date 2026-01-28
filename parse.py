#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import markdownify
import os
import re
import time
import datetime
import urllib.parse

# Папка для изображений (Hugo assets/)
IMG_DIR = "assets/images/cities"
os.makedirs(IMG_DIR, exist_ok=True)

# ИСПРАВЛЕНО: убраны пробелы!
BASE_URL = "https://chinacampus.ru"
API_PAGES = f"{BASE_URL}/wp-json/wp/v2/pages"
OUTPUT_DIR = "cities_md"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🔍 Загружаем список всех страниц...")
all_pages = []
page = 1
while True:
    try:
        resp = requests.get(API_PAGES, params={"per_page": 100, "page": page}, timeout=10)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        all_pages.extend(data)
        page += 1
    except Exception as e:
        print(f"Ошибка API: {e}")
        break

city_pages = [p for p in all_pages if "/city/" in p["link"]]
print(f"✅ Найдено {len(city_pages)} целевых страниц.")

for item in city_pages:
    url = item["link"].strip()
    slug = item["slug"]

    print(f"📄 Обработка: {url}")

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"  ❌ Ошибка загрузки {url}: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")

    # --- 1. Meta title & description ---
    meta_title = ""
    meta_desc = ""

    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        meta_title = og_title["content"].strip()
    else:
        title_tag = soup.find("title")
        if title_tag:
            meta_title = title_tag.get_text().strip()

    og_desc = soup.find("meta", property="og:description")
    if og_desc and og_desc.get("content"):
        meta_desc = og_desc["content"].strip()
    else:
        desc_tag = soup.find("meta", attrs={"name": "description"})
        if desc_tag and desc_tag.get("content"):
            meta_desc = desc_tag["content"].strip()

    safe_title = meta_title.replace('"', '\\"')
    safe_desc = meta_desc.replace('"', '\\"').replace("\n", " ")

    # --- 2. h1 ---
    h1_text = ""
    h1_elems = soup.select("h1")
    if h1_elems:
        h1_text = h1_elems[0].get_text().strip()
        for h1 in h1_elems:
            h1.decompose()
    safe_h1 = h1_text.replace('"', '\\"')

    # --- 3. Front matter ---
    front_matter = f"""---
title: "{safe_title}"
h1: "{safe_h1}"
description: "{safe_desc}"
date: {datetime.datetime.now().isoformat()}
draft: false
bg_image: "images/backgrounds/page-title.jpg"
#image: "images/blog/post-placeholder.jpg"
---
"""

    # --- 4. Берём только контентную область ---
    main_content = soup.select_one(".inner_page")
    if not main_content:
        main_content = soup

    # Удаляем мусор
    for el in main_content.select("""
        .cookie-notice,
        .header_new,
        .ms_uni_logo,
        .mobile_sp_tr,
        link,
        .top_line,
        .logo_block,
        .bread_crumbs,
        footer,
        nav,
        script,
        noscript,
        style,
        .zakon152,
        .overlay--modal-page,
        .application_btn,
        .burger-menu-piece,
        .popup-youtube,
        .side_menu_mobile,
        .sticky_sidebar_menu
    """):
        el.decompose()

    # --- 5. Собираем ВСЕ URL изображений (без дублей) ---
    image_urls = set()

    # <img src="...">
    for img in main_content.select("img[src]"):
        src = img.get("src").strip()
        if src and src.startswith(("http", "//")):
            image_urls.add(src)

    # style="background-image: url(...)"
    for el in main_content.find_all(style=True):
        style = el.get("style")
        if "background-image" in style:
            match = re.search(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', style)
            if match:
                url = match.group(1).strip()
                if url.startswith("//"):
                    url = "https:" + url
                elif url.startswith("/"):
                    url = BASE_URL + url
                image_urls.add(url)

    # data-thumb="..."
    for el in main_content.select("[data-thumb]"):
        thumb = el.get("data-thumb").strip()
        if thumb and thumb.startswith(("http", "//")):
            image_urls.add(thumb)

    # --- 6. Скачиваем изображения (без дублей на диске) ---
    url_to_local = {}
    seen_filenames = set()

    for img_url in sorted(image_urls):  # сортировка для стабильности
        try:
            orig_url = img_url
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif img_url.startswith("/"):
                img_url = BASE_URL + img_url

            parsed = urllib.parse.urlparse(img_url)
            filename = os.path.basename(parsed.path)
            if not filename or "." not in filename:
                filename = f"img_{abs(hash(img_url)) % 1000000}.jpg"

            # Уникальное имя файла, если дубль
            counter = 1
            base_name, ext = os.path.splitext(filename)
            unique_filename = filename
            while unique_filename in seen_filenames:
                unique_filename = f"{base_name}_{counter}{ext}"
                counter += 1
            seen_filenames.add(unique_filename)

            local_path = f"{IMG_DIR}/{unique_filename}"
            full_local_path = os.path.join(os.getcwd(), local_path)

            if not os.path.exists(full_local_path):
                img_data = requests.get(img_url, timeout=10).content
                with open(full_local_path, "wb") as f:
                    f.write(img_data)

            new_url = f"/images/cities/{unique_filename}"
            url_to_local[orig_url] = new_url

        except Exception as e:
            print(f"  ⚠️ Не удалось скачать {img_url}: {e}")

    # --- 7. ЗАМЕНА фоновых блоков на <img> ---
    processed_imgs = set()

    # .yo_slide
    for li in main_content.select("li.yo_slide"):
        thumb = li.get("data-thumb", "").strip()
        if not thumb or thumb in processed_imgs:
            continue
        processed_imgs.add(thumb)

        norm_thumb = thumb
        if thumb.startswith("//"):
            norm_thumb = "https:" + thumb
        elif thumb.startswith("/"):
            norm_thumb = BASE_URL + thumb

        local_src = url_to_local.get(norm_thumb)
        if not local_src:
            continue

        desc_elem = li.select_one(".yo_slide_desc")
        alt_text = desc_elem.get_text().strip() if desc_elem else ""

        new_img = soup.new_tag("img", src=local_src, alt=alt_text)
        li.clear()
        li.append(new_img)

    # .ftl_item, .esh_img и др.
    for selector in [".ftl_item", ".ifp_center_item", ".esh_img", ".teacher_thumb"]:
        for el in main_content.select(selector):
            style = el.get("style", "")
            match = re.search(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', style)
            if not match:
                continue
            bg_url = match.group(1).strip()
            if bg_url in processed_imgs:
                continue
            processed_imgs.add(bg_url)

            norm_url = bg_url
            if bg_url.startswith("//"):
                norm_url = "https:" + bg_url
            elif bg_url.startswith("/"):
                norm_url = BASE_URL + bg_url

            local_src = url_to_local.get(norm_url)
            if not local_src:
                continue

            alt_text = "Изображение"
            new_img = soup.new_tag("img", src=local_src, alt=alt_text)
            parent = el.parent
            if parent and parent.name == "a":
                el.replace_with(new_img)
            else:
                el.replace_with(new_img)

    # --- 8. Удаляем пустые списки вокруг изображений ---
    for ul in main_content.select("ul"):
        imgs = ul.select("img")
        non_empty = ul.find_all(string=True, recursive=False)
        non_empty = [s.strip() for s in non_empty if s.strip()]
        if len(imgs) > 0 and len(non_empty) == 0:
            # Список содержит только изображения → заменяем на них
            parent = ul.parent
            idx = parent.index(ul)
            for img in reversed(imgs):
                parent.insert(idx, img)
            ul.decompose()

    # --- 9. Заменяем остальные URL (на случай пропущенных) ---
    html_str = str(main_content)
    for orig, local in url_to_local.items():
        escaped = re.escape(orig)
        html_str = re.sub(escaped, local, html_str)

    main_content = BeautifulSoup(html_str, "html.parser")

    # --- 10. Конвертируем в Markdown ---
    md_body = markdownify.markdownify(str(main_content), heading_style="ATX")
    md_body = re.sub(r'\n{3,}', '\n\n', md_body).strip()

    # --- 11. Сохраняем ---
    full_md = front_matter + "\n" + md_body
    filename = f"{OUTPUT_DIR}/{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_md)

    time.sleep(0.5)

print(f"\n🎉 Готово! Все страницы сохранены в папку '{OUTPUT_DIR}'")
