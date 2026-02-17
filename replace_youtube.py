#!/usr/bin/env python3
"""Скрипт для замены всех вложений youtube на единый URL."""

import os
import re
from pathlib import Path

# Целевой URL для замены
TARGET_URL = "https://www.youtube.com/embed/zB53Gf6COV8"

# Паттерны для поиска разных форматов YouTube URL
YOUTUBE_PATTERNS = [
    re.compile(r"https://www\.youtube\.com/embed/[a-zA-Z0-9_-]+"),
    re.compile(r"https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]+"),
    re.compile(r"https://youtu\.be/[a-zA-Z0-9_-]+"),
]


def process_file(filepath: Path, log_entries: list) -> bool:
    """Обрабатывает файл, заменяя URL youtube. Возвращает True, если были замены."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        log_entries.append(f"Ошибка чтения {filepath}: {e}")
        return False

    total_matches = []
    for pattern in YOUTUBE_PATTERNS:
        matches = pattern.findall(content)
        total_matches.extend(matches)

    if not total_matches:
        return False

    new_content = content
    for pattern in YOUTUBE_PATTERNS:
        new_content = pattern.sub(TARGET_URL, new_content)

    try:
        filepath.write_text(new_content, encoding="utf-8")
    except Exception as e:
        log_entries.append(f"Ошибка записи {filepath}: {e}")
        return False

    for match in total_matches:
        log_entries.append(f"Файл: {filepath}")
        log_entries.append(f"  Заменено: {match} → {TARGET_URL}")
    log_entries.append("")

    return True


def main():
    content_dir = Path(__file__).parent / "content"
    logs_dir = Path(__file__).parent / "logs"

    if not content_dir.exists():
        print(f"Директория {content_dir} не найдена")
        return

    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "youtube_replace_report.txt"

    log_entries = [
        "Отчет о замене URL YOUTUBE",
        "=" * 50,
        f"Целевой URL: {TARGET_URL}",
        "=" * 50,
        "",
    ]

    total_files = 0
    replaced_files = 0
    total_replacements = 0

    for md_file in content_dir.rglob("*.md"):
        total_files += 1
        matches_count = 0
        for pattern in YOUTUBE_PATTERNS:
            try:
                matches_count += len(pattern.findall(md_file.read_text(encoding="utf-8")))
            except:
                pass
        if matches_count > 0:
            total_replacements += matches_count
            if process_file(md_file, log_entries):
                replaced_files += 1

    log_entries.extend([
        "=" * 50,
        "ИТОГО:",
        f"Всего файлов проверено: {total_files}",
        f"Файлов с заменами: {replaced_files}",
        f"Всего заменено вхождений: {total_replacements}",
    ])

    log_file.write_text("\n".join(log_entries), encoding="utf-8")

    print(f"Готово! Проверено файлов: {total_files}")
    print(f"Заменено вхождений: {total_replacements} в {replaced_files} файлах")
    print(f"Отчет сохранен в: {log_file}")


if __name__ == "__main__":
    main()
