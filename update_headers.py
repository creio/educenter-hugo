#!/usr/bin/env python3
"""
Скрипт для автоматического обновления заголовков в файлах markdown
в директории cities_md
"""

import os
import re
from datetime import datetime

def update_markdown_headers(file_path):
    """Обновляет заголовки в указанном markdown-файле"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Обновляем дату
    today = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "000"
    content = re.sub(r'date: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+', 
                     f'date: {today}', content)
    
    # Заменяем заголовки
    replacements = [
        (r'^## О городе$', '## Общая информация', re.MULTILINE),
        (r'^## Что посмотреть\?\s*$', '## Достопримечательности', re.MULTILINE),
        (r'^Достопримечательности города\s*$', '### Исторические памятники', re.MULTILINE),
        (r'^## Еда\s*$', '## Гастрономия', re.MULTILINE),
        (r'^Что поесть\s*$', '### Традиционные блюда', re.MULTILINE),
        (r'^## Куда сходить\?\s*$', '## Развлечения', re.MULTILINE),
        (r'^Развлечения и музеи\s*$', '### Культурные и развлекательные объекты', re.MULTILINE),
        (r'^## Про индустрии и компании\s*$', '## Экономика и карьерные возможности', re.MULTILINE),
        (r'^Компании и возможности\s*$', '### Основные отрасли', re.MULTILINE),
        
        # Добавляем раздел "История и современность" если его нет
        (r'(## Общая информация.*?)!.*?\n(## Достопримечательности)', 
         r'\1\n\n## История и современность\n\n### Историческое развитие\n\nИстория города насчитывает многие века, в течение которых он пережил множество изменений и трансформаций. Город прошел путь от небольшого поселения до одного из ведущих мегаполисов страны.\n\n### Современный облик\n\nСовременный облик города представляет собой уникальное сочетание традиций и инноваций. Город активно развивается, сохраняя при этом свою культурную идентичность.\n\n\\2', 
         re.DOTALL),
    ]
    
    for old_header, new_header, flags in replacements:
        content = re.sub(old_header, new_header, content, flags=flags)
    
    # Сохраняем изменения
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Обновлен файл: {file_path}")

def main():
    directory = "/media/files/work/educenter-hugo/cities_md"
    
    # Список файлов для обработки (исключая уже обработанные)
    processed_files = {"chanchun.md", "shanhaj.md", "pekin.md"}
    
    for filename in os.listdir(directory):
        if filename.endswith(".md") and filename not in processed_files:
            file_path = os.path.join(directory, filename)
            update_markdown_headers(file_path)

if __name__ == "__main__":
    main()