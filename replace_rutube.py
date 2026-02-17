#!/usr/bin/env python3
"""Скрипт для замены всех вложений rutube на единый URL."""

import os
import re
from pathlib import Path

# Целевой URL для замены
TARGET_URL = "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"

# Паттерн для поиска любых URL rutube embed
RUTUBE_PATTERN = re.compile(r"https://rutube\.ru/play/embed/[a-zA-Z0-9]+/?")


def process_file(filepath: Path, log_entries: list) -> bool:
    """Обрабатывает файл, заменяя URL rutube. Возвращает True, если были замены."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        log_entries.append(f"Ошибка чтения {filepath}: {e}")
        return False

    matches = RUTUBE_PATTERN.findall(content)
    if not matches:
        return False

    new_content = RUTUBE_PATTERN.sub(TARGET_URL, content)

    try:
        filepath.write_text(new_content, encoding="utf-8")
    except Exception as e:
        log_entries.append(f"Ошибка записи {filepath}: {e}")
        return False

    for match in matches:
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
    log_file = logs_dir / "rutube_replace_report.txt"

    log_entries = [
        "Отчет о замене URL RUTUBE",
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
        matches = RUTUBE_PATTERN.findall(md_file.read_text(encoding="utf-8"))
        if matches:
            total_replacements += len(matches)
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
