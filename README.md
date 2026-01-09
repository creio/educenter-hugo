# Educenter

Для работы нужно установить hugo.

## Local development

```bash
# запуск в режиме разработки
hugo server --disableFastRender

# сборка проекта
hugo --gc --minify
```

Готовый проект будет в директории `public/`.

- Основной Конфиг: `hugo.toml`
- Вспомогательные конфиги: `config/_default`
- Языковые файлы: `data/` и `i18n`
