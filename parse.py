#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import markdownify
import os
import re
import time
import datetime
import urllib.parse

# Настройки
BASE_URL = "https://chinacampus.ru"
API_PAGES = f"{BASE_URL}/wp-json/wp/v2/pages"
UNI_DIR = "universities_md"
IMG_DIR = "assets/images/universities"

os.makedirs(UNI_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

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

# Фильтруем только университеты
uni_pages = [p for p in all_pages if "/universitety/" in p["link"]]
print(f"✅ Найдено {len(uni_pages)} университетов.")

for item in uni_pages:
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

    # --- Meta title & description ---
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

    # --- h1 ---
    h1_text = ""
    h1_elems = soup.select("h1")
    if h1_elems:
        h1_text = h1_elems[0].get_text().strip()
        for h1 in h1_elems:
            h1.decompose()
    safe_h1 = h1_text.replace('"', '\\"')

    # --- Определяем bg_image и image из .main_section ---
    bg_image_url = ""
    main_section = soup.select_one(".main_section")
    if main_section and main_section.get("style"):
        style = main_section["style"]
        match = re.search(r'background-image:\s*url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', style, re.IGNORECASE)
        if match:
            bg_image_url = match.group(1).strip()
            if bg_image_url.startswith("//"):
                bg_image_url = "https:" + bg_image_url
            elif bg_image_url.startswith("/"):
                bg_image_url = BASE_URL.rstrip() + bg_image_url

    # Скачиваем фоновое изображение, если есть
    bg_local_path = "images/backgrounds/page-title.jpg"  # fallback
    if bg_image_url:
        try:
            parsed = urllib.parse.urlparse(bg_image_url)
            filename = os.path.basename(parsed.path)
            if not filename or "." not in filename:
                filename = f"bg_{abs(hash(bg_image_url)) % 1000000}.jpg"

            local_file = f"{IMG_DIR}/{filename}"
            full_local_path = os.path.join(os.getcwd(), local_file)

            if not os.path.exists(full_local_path):
                img_data = requests.get(bg_image_url, timeout=10).content
                with open(full_local_path, "wb") as f:
                    f.write(img_data)

            bg_local_path = f"/images/universities/{filename}"
        except Exception as e:
            print(f"  ⚠️ Не удалось скачать фон: {e}")

    # --- Извлекаем видео-блоки (.vsl_big_link + .vsl_big_name) ---
    iframe_videos = []
    # 1. Обработка .vsl_big
    for big in soup.select(".vsl_big"):
        link_elem = big.select_one(".vsl_big_link")
        name_elem = big.select_one(".vsl_big_name")
        img_span = big.select_one("span[style*='background-image']")

        link = link_elem.get("href", "").strip() if link_elem else ""
        title = name_elem.get_text().strip() if name_elem else ""
        img_url = ""
        if img_span and img_span.get("style"):
            match = re.search(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', img_span["style"])
            if match:
                img_url = match.group(1).strip()

        if link:
            iframe_videos.append({
                "link": link,
                "title": title,
                "img_url": img_url
            })

    # 2. Обработка .vsl_side
    for side in soup.select(".vsl_side"):
        for item in side.select(".vsl_side_item"):
            link_elem = item.select_one(".vsl_side_item_link")
            name_elem = item.select_one(".vsl_side_item_name")
            img_span = item.select_one("span[style*='background-image']")

            link = link_elem.get("href", "").strip() if link_elem else ""
            title = name_elem.get_text().strip() if name_elem else ""
            img_url = ""
            if img_span and img_span.get("style"):
                match = re.search(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', img_span["style"])
                if match:
                    img_url = match.group(1).strip()

            if link:
                iframe_videos.append({
                    "link": link,
                    "title": title,
                    "img_url": img_url
                })

    # Скачиваем превью-изображения для видео
    video_entries = []
    for vid in iframe_videos:
        local_img = ""  # fallback — пустая строка
        img_url = vid["img_url"]

        if img_url:
            try:
                # Нормализуем URL
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url.startswith("/"):
                    img_url = BASE_URL.rstrip() + img_url

                parsed = urllib.parse.urlparse(img_url)
                filename = os.path.basename(parsed.path)
                if not filename or "." not in filename:
                    filename = f"video_{abs(hash(img_url)) % 1000000}.jpg"

                local_path = f"{IMG_DIR}/{filename}"
                full_local_path = os.path.join(os.getcwd(), local_path)

                if not os.path.exists(full_local_path):
                    img_data = requests.get(img_url, timeout=10).content
                    with open(full_local_path, "wb") as f:
                        f.write(img_data)

                local_img = f"/images/universities/{filename}"
            except Exception as e:
                print(f"  ⚠️ Не удалось скачать превью видео: {e}")

        video_entries.append({
            "iframe_link": vid["link"],
            "iframe_title": vid["title"],
            "iframe_img": local_img
        })

    # Генерация YAML для видео
    iframe_yaml = ""
    if video_entries:
        iframe_yaml = "iframe_video:\n"
        for entry in video_entries:
            link = entry["iframe_link"].replace('"', '\\"')
            title = entry["iframe_title"].replace('"', '\\"')
            img = entry["iframe_img"].replace('"', '\\"') if entry["iframe_img"] else ""
            iframe_yaml += f'  - iframe_link: "{link}"\n'
            iframe_yaml += f'    iframe_title: "{title}"\n'
            iframe_yaml += f'    iframe_img: "{img}"\n'

    # --- Front matter ---
    front_matter = f"""---
title: "{safe_title}"
h1: "{safe_h1}"
description: "{safe_desc}"
date: {datetime.datetime.now().isoformat()}
draft: false
bg_image: "{bg_local_path}"
image: "{bg_local_path}"
{iframe_yaml}---
---
"""

    # --- Контентная область ---
    main_content = soup.select_one(".inner_page") or soup

    # Удаляем мусор
    for el in main_content.select("""
        .cookie-notice, .header_new, .ms_uni_logo, .mobile_sp_tr,
        link, .top_line, .logo_block, .bread_crumbs, .card_links,
        footer, nav, script, noscript, style, .rbi_img, .gl_item_img,
        .video_section,
        .zakon152, .btns_container, .overlay--modal-page, .application_btn,
        .burger-menu-piece, .popup-youtube, .side_menu_mobile, .custom_section,
        .sticky_sidebar_menu, .univer_side_menu, .simple_read_more, .side_menu,
        .purple_btn, .plh_head_wrap, .specs-filter-block, .st_show_all
    """):
        el.decompose()

    # --- Собираем все URL изображений ---
    image_urls = set()

    # <img src>
    for img in main_content.select("img[src]"):
        src = img.get("src").strip()
        if src and src.startswith(("http", "//")):
            image_urls.add(src)

    # background-image
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

    # data-thumb
    for el in main_content.select("[data-thumb]"):
        thumb = el.get("data-thumb").strip()
        if thumb and thumb.startswith(("http", "//")):
            image_urls.add(thumb)

    # --- Скачиваем изображения ---
    url_to_local = {}
    for img_url in image_urls:
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

            local_path = f"{IMG_DIR}/{filename}"
            full_local_path = os.path.join(os.getcwd(), local_path)

            if not os.path.exists(full_local_path):
                img_data = requests.get(img_url, timeout=10).content
                with open(full_local_path, "wb") as f:
                    f.write(img_data)

            new_url = f"/images/universities/{filename}"
            url_to_local[orig_url] = new_url

        except Exception as e:
            print(f"  ⚠️ Не удалось скачать {img_url}: {e}")

    # --- Заменяем фоновые блоки на <img> ---
    for li in main_content.select("li.yo_slide, .ftl_item, .ifp_center_item, .esh_img, .teacher_thumb"):
        thumb = li.get("data-thumb") or ""
        style = li.get("style", "")
        bg_url = ""

        if thumb:
            bg_url = thumb
        elif "background-image" in style:
            match = re.search(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', style)
            if match:
                bg_url = match.group(1).strip()

        if not bg_url:
            continue

        norm_url = bg_url
        if bg_url.startswith("//"):
            norm_url = "https:" + bg_url
        elif bg_url.startswith("/"):
            norm_url = BASE_URL + bg_url

        local_src = url_to_local.get(norm_url)
        if not local_src:
            continue

        alt_text = "Изображение"
        desc_elem = li.select_one(".yo_slide_desc, .tbi_block_title")
        if desc_elem:
            alt_text = desc_elem.get_text().strip()

        new_img = soup.new_tag("img", src=local_src, alt=alt_text, **{"class": "img-fluid"})
        li.clear()
        li.append(new_img)

    # --- Заменяем остальные URL ---
    html_str = str(main_content)
    for orig, local in url_to_local.items():
        escaped = re.escape(orig)
        html_str = re.sub(escaped, local, html_str)

    main_content = BeautifulSoup(html_str, "html.parser")

    # --- Конвертируем в Markdown ---
    md_body = markdownify.markdownify(str(main_content), heading_style="ATX")
    md_body = re.sub(r'\n{3,}', '\n\n', md_body).strip()

    # --- Сохраняем ---
    full_md = front_matter + "\n" + md_body
    filename = f"{UNI_DIR}/{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_md)

    time.sleep(0.5)

print(f"\n🎉 Готово! Все университеты сохранены в папку '{UNI_DIR}'")
