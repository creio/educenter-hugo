#!/usr/bin/env python3
"""Скрипт для поиска всех ссылок на картинки в MD файлах."""

import re
from pathlib import Path

# Паттерн для изображений markdown: ![alt](url)
IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

# Паттерн для shortcode gallery: пути между {{< gallery >}} и {{< /gallery >}}
GALLERY_PATTERN = re.compile(r'{{<\s*gallery[^>]*>}}(.*?){{<\s*/gallery\s*>}}', re.DOTALL)

# Паттерн для путей в gallery (просто строки с путями)
GALLERY_PATH_PATTERN = re.compile(r'^\s*(/images/\S+|images/\S+)\s*$', re.MULTILINE)

# Паттерн для bg_image и image во фронтметтере
FRONTMATTER_IMAGE_PATTERN = re.compile(r'(?:bg_image|image)\s*:\s*["\']?([^"\'\n]+)["\']?')


def process_file(filepath: Path) -> set:
    """Извлекает все ссылки на изображения из файла."""
    images = set()

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return images

    # 1. Ищем изображения ![alt](url) в основном контенте
    for match in IMAGE_PATTERN.finditer(content):
        url = match.group(2)
        images.add(url)

    # 2. Ищем shortcode gallery и извлекаем пути
    for match in GALLERY_PATTERN.finditer(content):
        gallery_content = match.group(1)
        for path_match in GALLERY_PATH_PATTERN.finditer(gallery_content):
            url = path_match.group(1)
            if not url.startswith('/'):
                url = '/' + url
            images.add(url)

    # 3. Ищем изображения во фронтметтере (bg_image, image)
    for match in FRONTMATTER_IMAGE_PATTERN.finditer(content):
        url = match.group(1).strip()
        if url and not url.startswith('/'):
            url = '/' + url
        if url:
            images.add(url)

    return images


def main():
    content_dir = Path(__file__).parent / "content"
    logs_dir = Path(__file__).parent / "logs"

    if not content_dir.exists():
        print(f"Директория {content_dir} не найдена")
        return

    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "images_report.txt"

    all_images = set()
    total_files = 0

    for md_file in sorted(content_dir.rglob("*.md")):
        total_files += 1
        images = process_file(md_file)
        all_images.update(images)

    # Записываем просто список уникальных путей (отсортированный)
    log_file.write_text(
        "\n".join(sorted(all_images)),
        encoding="utf-8"
    )

    print(f"Готово! Проверено файлов: {total_files}")
    print(f"Найдено уникальных изображений: {len(all_images)}")
    print(f"Отчет сохранен в: {log_file}")


if __name__ == "__main__":
    main()
