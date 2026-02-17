#!/usr/bin/env python3
"""
Скрипт для рандомизации дат во фронтметтере MD файлов.
Даты устанавливаются случайным образом от середины 2025 до текущего дня.
"""

import os
import re
import random
from datetime import datetime, timedelta

CONTENT_DIR = "content"
START_DATE = datetime(2025, 1, 1, 0, 0, 0)
END_DATE = datetime(2026, 1, 30, 23, 59, 59)


def get_random_date():
    """Генерирует случайную дату от середины 2025 до текущего дня."""
    now = datetime.now()
    # Если END_DATE в прошлом, используем диапазон от START_DATE до END_DATE
    if END_DATE < now:
        total_seconds = int((END_DATE - START_DATE).total_seconds())
        random_seconds = random.randint(0, total_seconds)
        return START_DATE + timedelta(seconds=random_seconds)
    else:
        total_seconds = int((now - START_DATE).total_seconds())
        random_seconds = random.randint(0, total_seconds)
        return START_DATE + timedelta(seconds=random_seconds)


def format_date(dt):
    """Форматирует дату в формате Hugo (YYYY-MM-DDTHH:MM:SS)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def process_file(filepath):
    """Обрабатывает один MD файл, заменяя дату во фронтметтере."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Паттерн для поиска date: во фронтметтере
    pattern = r"(^---\n(?:.*?\n)*?)date:\s*\S+(\n)"
    
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        print(f"⚠️  Не найдено date: {filepath}")
        return False

    random_date = format_date(get_random_date())
    new_content = content[: match.start()] + match.group(1) + f"date: {random_date}" + match.group(2) + content[match.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ {filepath}")
    return True


def main():
    processed = 0
    errors = 0

    for root, _, files in os.walk(CONTENT_DIR):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                try:
                    if process_file(filepath):
                        processed += 1
                    else:
                        errors += 1
                except Exception as e:
                    print(f"✗ Ошибка {filepath}: {e}")
                    errors += 1

    print(f"\nГотово! Обработано: {processed}, ошибок: {errors}")


if __name__ == "__main__":
    main()
