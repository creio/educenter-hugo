#!/usr/bin/env python3
import os
import re

# Путь к папке с Markdown-файлами
folder = "content/universities"

# Компилируем регулярное выражение для заголовка "## Документы"
doc_header_pattern = re.compile(r"^##\s+Документы\s*$")

for filename in os.listdir(folder):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    skip = False

    for line in lines:
        # Если встречаем "## Документы" — включаем пропуск
        if doc_header_pattern.match(line.strip()):
            skip = True
            continue

        # Если встречаем новый заголовок уровня 2 — выключаем пропуск
        if skip and line.startswith("## ") and not line.startswith("###"):
            skip = False

        # Сохраняем строку, только если не в режиме пропуска
        if not skip:
            new_lines.append(line)

    # Записываем обратно (только если что-то изменилось)
    if len(new_lines) != len(lines):
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Обработан: {filename}")
