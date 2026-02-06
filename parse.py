#!/usr/bin/env python3
"""
Script to parse CCN programs page and all nested pages from chinacampus.ru via WP REST API.
"""

import requests
from bs4 import BeautifulSoup
import markdownify
import os
import re
import datetime
import urllib.parse
from pathlib import Path

# Настройки
BASE_URL = "https://chinacampus.ru"
API_PAGES = f"{BASE_URL}/wp-json/wp/v2/pages"
OUTPUT_DIR = "content/programs"
IMG_DIR = "assets/images/programs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Глобальный словарь для отслеживания использованных имен файлов
used_filenames = {}

def get_unique_filename(base_path, filename):
    """Генерирует уникальное имя файла, добавляя суффикс при конфликте"""
    file_path = Path(base_path) / filename
    name, ext = os.path.splitext(filename)

    if not file_path.exists():
        used_filenames[filename] = filename
        return filename

    if filename in used_filenames:
        return used_filenames[filename]

    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_path = Path(base_path) / new_filename
        if not new_path.exists():
            used_filenames[filename] = new_filename
            return new_filename
        counter += 1

def download_image(img_url, img_dir, base_url):
    """Скачивает изображение только если его ещё нет, возвращает локальный путь"""
    try:
        orig_url = img_url

        # Нормализуем URL
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        elif img_url.startswith("/"):
            img_url = base_url.rstrip() + img_url

        # Извлекаем имя файла из URL
        parsed = urllib.parse.urlparse(img_url)
        filename = os.path.basename(parsed.path)

        if not filename or "." not in filename:
            filename = f"img_{abs(hash(img_url)) % 1000000}.jpg"

        # Получаем уникальное имя (с учётом конфликтов)
        unique_filename = get_unique_filename(img_dir, filename)
        local_path = f"{img_dir}/{unique_filename}"
        full_local_path = os.path.join(os.getcwd(), local_path)

        # Проверяем, существует ли файл
        if os.path.exists(full_local_path):
            # Файл уже есть — пропускаем скачивание
            print(f"  ℹ️  Пропущено (уже существует): {unique_filename}")
            return f"/images/programs/{unique_filename}", orig_url

        # Скачиваем только если файла нет
        print(f"  ⬇️  Скачивание: {unique_filename}")
        img_data = requests.get(img_url, timeout=10).content
        with open(full_local_path, "wb") as f:
            f.write(img_data)

        return f"/images/programs/{unique_filename}", orig_url

    except Exception as e:
        print(f"  ⚠️ Не удалось скачать {img_url}: {e}")
        return None, orig_url

def process_page(page_data, is_main=False):
    """Обрабатывает одну страницу и возвращает её контент"""

    page_id = page_data.get("id")
    page_title = page_data.get("title", {}).get("rendered", "")
    page_slug = page_data.get("slug", f"page-{page_id}")
    page_link = page_data.get("link", "")

    print(f"\n📄 Обработка: {page_title}")
    print(f"   URL: {page_link}")
    print(f"   Slug: {page_slug}")

    # Получаем полную страницу для извлечения изображений
    try:
        r = requests.get(page_link, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"  ❌ Ошибка загрузки {page_link}: {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # --- Meta title & description ---
    meta_title = page_title.strip()
    meta_desc = ""

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

    # --- Featured image (фоновое изображение из .main_section) ---
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

    bg_local_path = "images/backgrounds/page-title.jpg"
    if bg_image_url:
        local_path, _ = download_image(bg_image_url, IMG_DIR, BASE_URL)
        if local_path:
            bg_local_path = local_path

    # --- Основной контент ---
    main_content = soup.select_one(".inner_page") or soup

    # Удаляем ВСЕ заголовки h1 из контента
    for h1 in main_content.select("h1"):
        h1.decompose()

    # Удаляем нежелательные элементы
    for el in main_content.select("""
        .cookie-notice, .header_new, .ms_uni_logo, .mobile_sp_tr,
        link, .top_line, .logo_block, .bread_crumbs, .card_links,
        footer, nav, script, noscript, style, .rbi_img, .gl_item_img,
        .video_section, .zakon152, .btns_container, .overlay--modal-page,
        .application_btn, .burger-menu-piece, .popup-youtube, .side_menu_mobile,
        .custom_section, .sticky_sidebar_menu, .univer_side_menu,
        .simple_read_more, .side_menu, .purple_btn, .plh_head_wrap,
        .specs-filter-block, .st_show_all, .wp-block-template-part,
        .header, .footer, .comments, .author-box, .share-buttons,
        .related-posts, .post-navigation
    """):
        el.decompose()

    # --- Собираем все изображения ---
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

    print(f"  📷 Найдено {len(image_urls)} изображений")

    # --- Скачиваем изображения ---
    url_to_local = {}
    for img_url in image_urls:
        local_path, orig_url = download_image(img_url, IMG_DIR, BASE_URL)
        if local_path:
            url_to_local[orig_url] = local_path

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

    # --- Заменяем все остальные ссылки на изображения ---
    html_str = str(main_content)
    for orig, local in url_to_local.items():
        escaped = re.escape(orig)
        html_str = re.sub(escaped, local, html_str)

    main_content = BeautifulSoup(html_str, "html.parser")

    # --- Конвертируем в Markdown ---
    md_body = markdownify.markdownify(str(main_content), heading_style="ATX")
    md_body = re.sub(r'\n{3,}', '\n\n', md_body).strip()

    # --- Удаляем # заголовки из начала контента ---
    md_lines = md_body.split('\n')
    cleaned_lines = []

    for line in md_lines:
        # Пропускаем строки, начинающиеся с # (заголовки)
        if line.strip().startswith('#'):
            continue
        cleaned_lines.append(line)

    md_body = '\n'.join(cleaned_lines).strip()

    # --- Front matter ---
    front_matter = f"""---
title: "{safe_title}"
h1: "{safe_h1}"
description: "{safe_desc}"
date: {datetime.datetime.now().isoformat()}
draft: false
bg_image: "{bg_local_path}"
image: "{bg_local_path}"
type: "programs"
---
"""

    return {
        "slug": page_slug,
        "front_matter": front_matter,
        "content": md_body,
        "is_main": is_main
    }

# --- Основной код ---
print("🔍 Получение данных через WP REST API...")
print(f"   API: {API_PAGES}?slug=programmy-ccn")

# Получаем основную страницу
try:
    resp = requests.get(f"{API_PAGES}?slug=programmy-ccn", timeout=10)
    resp.raise_for_status()
    main_page_data = resp.json()[0]
except Exception as e:
    print(f"❌ Ошибка получения основной страницы: {e}")
    exit(1)

print(f"\n✅ Основная страница найдена: {main_page_data.get('title', {}).get('rendered', '')}")

# Получаем все дочерние страницы
main_page_id = main_page_data.get("id")
print(f"\n🔍 Поиск дочерних страниц (parent={main_page_id})...")

try:
    resp = requests.get(f"{API_PAGES}?parent={main_page_id}&per_page=100", timeout=10)
    resp.raise_for_status()
    child_pages = resp.json()
    print(f"✅ Найдено {len(child_pages)} дочерних страниц")
except Exception as e:
    print(f"⚠️ Ошибка получения дочерних страниц: {e}")
    child_pages = []

# Обрабатываем основную страницу
main_result = process_page(main_page_data, is_main=True)

if main_result:
    # Сохраняем основную страницу
    full_md = main_result["front_matter"] + "\n" + main_result["content"]
    output_file = f"{OUTPUT_DIR}/_index.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_md)

    print(f"\n✅ Основная страница сохранена: {output_file}")

# Обрабатываем дочерние страницы
for i, child_page in enumerate(child_pages, 1):
    result = process_page(child_page)

    if result:
        full_md = result["front_matter"] + "\n" + result["content"]
        output_file = f"{OUTPUT_DIR}/{result['slug']}.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_md)

        print(f"✅ Дочерняя страница #{i} сохранена: {output_file}")

    # Небольшая пауза между запросами
    if i < len(child_pages):
        import time
        time.sleep(0.3)

print(f"\n{'='*60}")
print(f"📊 ИТОГОВАЯ СТАТИСТИКА")
print(f"{'='*60}")
print(f"✅ Основная страница: 1")
print(f"✅ Дочерние страницы: {len(child_pages)}")
print(f"✅ Всего обработано: {len(child_pages) + 1}")
print(f"📁 Изображения сохранены в: {IMG_DIR}")
print(f"📁 Страницы сохранены в: {OUTPUT_DIR}")
print(f"{'='*60}")
print(f"\n🎉 Готово!")
