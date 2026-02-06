#!/usr/bin/env python3
import re
import os

def process_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        # Ищем начало списка изображений
        if re.match(r'^\* !\[[^\]]*\]\([^)]+\)\s*$', lines[i]):
            # Собираем последовательные элементы списка изображений
            gallery_items = []
            j = i
            while j < len(lines) and re.match(r'^(\* !\[[^\]]*\]\([^)]+\)\s*|^\s*$)', lines[j]):
                # Пропускаем пустые строки внутри блока
                if lines[j].strip() and re.match(r'^\* !\[[^\]]*\]\([^)]+\)\s*$', lines[j]):
                    match = re.match(r'^\* !\[([^\]]*)\]\(([^)]+)\)\s*$', lines[j])
                    if match:
                        alt, path = match.groups()
                        gallery_items.append(f'{path},{alt}')
                j += 1

            # Формируем галерею, если найдено >= 2 изображения
            if len(gallery_items) >= 2:
                filename = os.path.splitext(os.path.basename(file_path))[0]
                gallery_id = f'{filename}-gallery-{i}'

                gallery_block = [
                    f'{{{{< gallery id="{gallery_id}" >}}}}\n'
                ]
                gallery_block.extend([f'{item}\n' for item in gallery_items])
                gallery_block.append('{{< /gallery >}}\n\n')

                new_lines.extend(gallery_block)
                i = j  # Пропускаем обработанные строки
                continue

        # Обычная строка — добавляем как есть
        new_lines.append(lines[i])
        i += 1

    # Записываем изменения
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Обрабатываем все файлы в директории cities_md
if __name__ == "__main__":
    processed = 0
    for filename in os.listdir('cities_md'):
        if filename.endswith('.md'):
            file_path = os.path.join('cities_md', filename)
            process_md_file(file_path)
            print(f'✅ Обработан файл: {filename}')
            processed += 1

    print(f'\n🎉 Обработано файлов: {processed}')
