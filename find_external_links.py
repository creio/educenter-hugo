#!/usr/bin/env python3
"""Скрипт для поиска всех внешних ссылок в MD файлах."""

import re
from pathlib import Path

# Паттерн для поиска markdown ссылок [text](url) и прямых URL
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
URL_PATTERN = re.compile(r'https?://[^\s<>"\')\]]+')


def is_external_url(url: str) -> bool:
    """Проверяет, является ли ссылка внешней."""
    return url.startswith('http://') or url.startswith('https://')


def process_file(filepath: Path) -> list:
    """Извлекает все внешние ссылки из файла."""
    external_links = []
    
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [(f"Ошибка чтения: {e}", None)]

    # Ищем markdown ссылки [text](url)
    for match in MD_LINK_PATTERN.finditer(content):
        text = match.group(1)
        url = match.group(2)
        if is_external_url(url):
            external_links.append((url, text))

    return external_links


def main():
    content_dir = Path(__file__).parent / "content"
    logs_dir = Path(__file__).parent / "logs"

    if not content_dir.exists():
        print(f"Директория {content_dir} не найдена")
        return

    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "external_links_report.txt"

    log_entries = [
        "Отчет о внешних ссылках в MD файлах",
        "=" * 60,
        "",
    ]

    total_files = 0
    files_with_links = 0
    all_links = set()
    links_by_file = {}

    for md_file in sorted(content_dir.rglob("*.md")):
        total_files += 1
        external_links = process_file(md_file)
        
        if external_links:
            files_with_links += 1
            rel_path = md_file.relative_to(content_dir)
            links_by_file[str(rel_path)] = external_links
            
            for url, text in external_links:
                all_links.add(url)

    # Формируем отчет по файлам
    log_entries.append("Ссылки по файлам:")
    log_entries.append("-" * 60)
    
    for filepath, links in sorted(links_by_file.items()):
        log_entries.append(f"\nФайл: {filepath}")
        for url, text in sorted(links, key=lambda x: x[0]):
            log_entries.append(f"  [{text}]({url})")
    
    # Сводка по всем уникальным ссылкам
    log_entries.append("")
    log_entries.append("=" * 60)
    log_entries.append("Все уникальные внешние ссылки:")
    log_entries.append("-" * 60)
    
    for url in sorted(all_links):
        # Находим все файлы, где встречается эта ссылка
        files_containing = [f for f, links in links_by_file.items() 
                          if any(u == url for u, _ in links)]
        log_entries.append(f"{url}")
        log_entries.append(f"  Встречается в: {', '.join(files_containing)}")

    log_entries.append("")
    log_entries.append("=" * 60)
    log_entries.append("ИТОГО:")
    log_entries.append(f"Всего файлов проверено: {total_files}")
    log_entries.append(f"Файлов с внешними ссылками: {files_with_links}")
    log_entries.append(f"Всего уникальных внешних ссылок: {len(all_links)}")

    log_file.write_text("\n".join(log_entries), encoding="utf-8")

    print(f"Готово! Проверено файлов: {total_files}")
    print(f"Найдено файлов с внешними ссылками: {files_with_links}")
    print(f"Всего уникальных внешних ссылок: {len(all_links)}")
    print(f"Отчет сохранен в: {log_file}")


if __name__ == "__main__":
    main()
