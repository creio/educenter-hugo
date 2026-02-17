#!/bin/bash

# Директории
IMAGES_DIR="/media/files/work/educenter-hugo/assets/images/blog"
CONTENT_DIR="/media/files/work/educenter-hugo/content/blog"
LOGS_DIR="/media/files/work/educenter-hugo/logs"
LOG_FILE="$LOGS_DIR/unused_blog_images.txt"

# Создаем директорию logs если не существует
mkdir -p "$LOGS_DIR"

# Получаем список всех файлов в assets/images/blog
echo "Получение списка всех изображений..."
mapfile -t all_images < <(find "$IMAGES_DIR" -type f -printf "%f\n" | sort)

# Получаем список используемых изображений из MD файлов
echo "Поиск используемых изображений в content/blog..."
used_images=$(grep -rhoE '/?images/blog/[^"'\''[:space:]]*\.[a-zA-Z0-9_%-]+' "$CONTENT_DIR" --include="*.md" 2>/dev/null | \
              sed -E 's|.*[/]?images/blog/||; s|^[[:space:]]+||; s|[[:space:]]+$||' | \
              sort -u)

# echo "$used_images"
# exit

# Считаем статистику
total_images=${#all_images[@]}
used_count=0
unused_count=0
deleted_count=0

# Временный файл для неиспользуемых изображений
unused_list=$(mktemp)

echo "Анализ изображений..."
echo "Всего изображений в assets/images/blog: $total_images"

# Проверяем каждое изображение
for img in "${all_images[@]}"; do
    # Исправление: добавлено '--' перед "$img"
    if echo "$used_images" | grep -qxF -- "$img"; then
        ((used_count++))
    else
        echo "$img" >> "$unused_list"
        ((unused_count++))
    fi
done

echo "Используется: $used_count"
echo "Не используется: $unused_count"

# echo "$used_images" | grep -qxF -- 'adult-1846436_1280%20q%20'
# cat "$unused_list" | grep "adul"
# grep -rhoE '/?images/blog/[^"'\''[:space:]]*\.[a-zA-Z0-9_%-]+' "$CONTENT_DIR" --include="*.md" | sed -E 's|.*[/]?images/blog/||; s|^[[:space:]]+||; s|[[:space:]]+$||' | grep "adul"
# exit

# Создаем отчет
{
    echo "========================================"
    echo "Отчет о неиспользуемых изображениях"
    echo "Дата: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "========================================"
    echo ""
    echo "Статистика:"
    echo "-----------"
    echo "Всего изображений в assets/images/blog: $total_images"
    echo "Используется в content/blog: $used_count"
    echo "Не используется: $unused_count"
    echo ""
    echo "========================================"
    echo "Неиспользуемые изображения ($unused_count):"
    echo "========================================"
    cat "$unused_list"
    echo ""
    echo "========================================"
    echo "Удаленные файлы:"
    echo "========================================"
} > "$LOG_FILE"

# Удаляем неиспользуемые изображения
echo ""
echo "Удаление неиспользуемых изображений..."
while IFS= read -r img; do
    if [ -f "$IMAGES_DIR/$img" ]; then
        rm "$IMAGES_DIR/$img"
        # echo "Удалено: $img" >> "$LOG_FILE"
        ((deleted_count++))
    fi
done < "$unused_list"

# Добавляем итоговую статистику
{
    echo ""
    echo "========================================"
    echo "Итог:"
    echo "========================================"
    echo "Удалено файлов: $deleted_count"
    echo "Осталось файлов: $((total_images - deleted_count))"
    echo ""
    echo "Отчет сохранен в: $LOG_FILE"
} >> "$LOG_FILE"

# Очищаем временный файл
rm "$unused_list"

echo ""
echo "Готово!"
echo "Удалено неиспользуемых изображений: $deleted_count"
echo "Отчет сохранен в: $LOG_FILE"
