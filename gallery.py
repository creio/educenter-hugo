#!/usr/bin/env python3
"""
Script to fix gallery formatting in markdown files.
Converts inline galleries to multiline format with proper line breaks.
"""

import os
import re
import glob

def fix_galleries_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Регулярное выражение для поиска блоков галерей
    # Ищем: {{< gallery id="..." >}} ... {{< /gallery >}}
    pattern = r'({{<\s*gallery\s+id="[^"]+"\s*>}})(.*?)(\{\{<\s*/gallery\s*>}})'

    def replace_gallery(match):
        opening_tag = match.group(1).strip()
        content_block = match.group(2).strip()
        closing_tag = match.group(3).strip()

        # Разбиваем содержимое на отдельные строки по паттерну "путь,описание"
        # Каждая запись начинается с "/" (путь к изображению)
        items = []
        current = ""

        for part in content_block.split():
            if part.startswith('/') and current:
                # Новая запись начинается — сохраняем предыдущую
                items.append(current.strip())
                current = part
            else:
                current += " " + part if current else part

        if current:
            items.append(current.strip())

        # Формируем многострочный блок
        if items:
            new_block = f"{opening_tag}\n" + "\n".join(items) + f"\n{closing_tag}"
        else:
            new_block = f"{opening_tag}\n{closing_tag}"

        return new_block

    # Применяем замену ко всем галереям в файле
    new_content = re.sub(pattern, replace_gallery, content, flags=re.DOTALL)

    # Сохраняем результат только если были изменения
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_all_files():
    md_files = glob.glob("universities_md/*.md")
    print(f"Найдено {len(md_files)} файлов для обработки...\n")

    fixed_count = 0
    for file_path in md_files:
        filename = os.path.basename(file_path)
        if fix_galleries_in_file(file_path):
            print(f"✅ Исправлено: {filename}")
            fixed_count += 1
        else:
            print(f"⚪ Пропущено (без изменений): {filename}")

    print(f"\n🎉 Готово! Исправлено галерей в {fixed_count} файлах из {len(md_files)}.")

if __name__ == "__main__":
    process_all_files()
