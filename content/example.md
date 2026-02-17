---
title: "Example"
h1: "Example page"
description : "Lorem ipsum dolor."
draft: false
# page title background image
bg_image: "images/backgrounds/page-title.jpg"
# image: "images/about/about-page.jpg"
iframe_video:
  - iframe_link: "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"
    iframe_title: "Видео-тур по Таньцзиньскому Университету"
  - iframe_link: "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"
    iframe_title: "Как выглядит китайский вуз?"
  - iframe_link: "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"
    iframe_title: "START GLOBAL, START WITH CHINA"
---

Каждую конструкцыю `shortcodes` нужно оборачивать в `{{...}}`

```bash
# это одиночный
/{/{< asd id="param" >/}/}

# это многострочный
/{/{< asd id="param" >/}/}
/images/cities/Guangzhou-Zhongshan-Memorial-Hall-1.jpg,Здание
/images/cities/akademiya.jpg
/{/{< /asd >/}/}

# убрать / просто без них блок кода ломается
```

## Галерея img

Code

```go
< gallery id="city1" >
/images/cities/Guangzhou-Zhongshan-Memorial-Hall-1.jpg,Здание
/images/cities/akademiya.jpg
< /gallery >
```

result

{{< gallery id="city1" >}}
/images/cities/Guangzhou-Zhongshan-Memorial-Hall-1.jpg,Здание
/images/cities/akademiya.jpg
{{< /gallery >}}

## Video

В данном случае `poster` не обязательный параметр.

```bash
< video src="https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/" poster="/images/cities/akademiya.jpg" >
```

result

{{< video src="https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/" poster="/images/cities/akademiya.jpg" >}}

## Video gallery

```bash
< video-gallery id="demo" >
https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/,Demo
https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/
< /video-gallery >
```

{{< video-gallery id="demo" >}}
https://www.youtube.com/embed/iLBrDXHnk6g,Demo
https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/
{{< /video-gallery >}}


## Yandex map

```bash
< yandexmap lat="55.781813" lon="49.131818" zoom="16" width="100%" height="400px" >

# параметры ниже работают, если в настройках указан api key
width="100%" height="300px"
```

result

{{< yandexmap lat="55.781813" lon="49.131818" zoom="18" width="100%" height="300px" >}}

## Frontmatter

Вводная часть yaml в md файлах. В некоторых разделах можно использовать, доп конструкции.

### Video gallery

Вот пример на текущей стр. Выводится под контентом

```bash
iframe_video:
  - iframe_link: "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"
    iframe_title: "Видео-тур по Таньцзиньскому Университету"
  - iframe_link: "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"
    iframe_title: "Как выглядит китайский вуз?"
  - iframe_link: "https://rutube.ru/play/embed/2972c71905d5bc5cb873e653b98f31c3/"
    iframe_title: "START GLOBAL, START WITH CHINA"
```

result
