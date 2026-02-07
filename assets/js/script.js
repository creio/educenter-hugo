(function ($) {
  'use strict';

  // Preloader js    
  $(window).on('load', function () {
    $('.preloader').fadeOut(100);
  });

  // Sticky Menu
  $(window).scroll(function () {
    var height = $('.top-header').innerHeight();
    if ($('header').offset().top > 10) {
      $('.top-header').addClass('hide');
      $('.navigation').addClass('nav-bg');
      $('.navigation').css('margin-top','-'+height+'px');
    } else {
      $('.top-header').removeClass('hide');
      $('.navigation').removeClass('nav-bg');
      $('.navigation').css('margin-top','-'+0+'px');
    }
  });

  

  // Background-images
  $('[data-background]').each(function () {
    $(this).css({
      'background-image': 'url(' + $(this).data('background') + ')'
    });
  });

  //Hero Slider
  $('.hero-slider').slick({
    autoplay: true,
    autoplaySpeed: 7500,
    pauseOnFocus: false,
    pauseOnHover: false,
    infinite: true,
    arrows: true,
    fade: true,
    prevArrow: '<button type=\'button\' class=\'prevArrow\'><i class=\'ti-angle-left\'></i></button>',
    nextArrow: '<button type=\'button\' class=\'nextArrow\'><i class=\'ti-angle-right\'></i></button>',
    dots: true
  });
  $('.hero-slider').slickAnimation();


  // venobox popup
  $(document).ready(function () {
    $('.venobox').venobox({
      autoplay: true,
    });
  });

  // filter
  $(document).ready(function () {
    var containerEl = document.querySelector('.filtr-container');
    var filterizd;
    if (containerEl) {
      filterizd = $('.filtr-container').filterizr({});
    }
    //Active changer
    $('.filter-controls li').on('click', function () {
      $('.filter-controls li').removeClass('active');
      $(this).addClass('active');
    });
  });

  //  Count Up
  function counter() {
    var oTop;
    if ($('.count').length !== 0) {
      oTop = $('.count').offset().top - window.innerHeight;
    }
    if ($(window).scrollTop() > oTop) {
      $('.count').each(function () {
        var $this = $(this),
          countTo = $this.attr('data-count');
        $({
          countNum: $this.text()
        }).animate({
          countNum: countTo
        }, {
          duration: 1000,
          easing: 'swing',
          step: function () {
            $this.text(Math.floor(this.countNum));
          },
          complete: function () {
            $this.text(this.countNum);
          }
        });
      });
    }
  }
  $(window).on('scroll', function () {
    counter();
  });

  // Animation
  $(document).ready(function () {
    $('.has-animation').each(function (index) {
      $(this).delay($(this).data('delay')).queue(function () {
        $(this).addClass('animate-in');
      });
    });
  });
})(jQuery);


document.addEventListener('DOMContentLoaded', function() {

// фиксирование таблицы и добавление скролла
document.querySelectorAll('.content table').forEach(table => {
  const wrapper = document.createElement('div');
  wrapper.className = 'table-wrapper';
  table.parentNode.insertBefore(wrapper, table);
  wrapper.appendChild(table);
});

// Инициализация всех галерей на странице
document.querySelectorAll('.gallery-wrapper').forEach(function(wrapper) {
  const $wrapper = $(wrapper);
  const $single = $wrapper.find('.slider-single');
  const $nav = $wrapper.find('.slider-nav');
  // Основной слайдер
  $single.slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    fade: true,
    infinite: true,
    speed: 400,
    prevArrow: '<button type=\'button\' class=\'prevArrow\'><i class=\'ti-angle-left\'></i></button>',
    nextArrow: '<button type=\'button\' class=\'nextArrow\'><i class=\'ti-angle-right\'></i></button>',
  });
  // Навигационный слайдер
  $nav.on('init', function(event, slick) {
    $nav.find('.slick-slide.slick-current').addClass('is-active');
  })
  .slick({
    slidesToShow: 5,
    slidesToScroll: 5,
    dots: false,
    focusOnSelect: false,
    infinite: true,
    variableWidth: true,
    prevArrow: '<button type=\'button\' class=\'prevArrow\'><i class=\'ti-angle-left\'></i></button>',
    nextArrow: '<button type=\'button\' class=\'nextArrow\'><i class=\'ti-angle-right\'></i></button>',
    responsive: [{
      breakpoint: 1200,
      settings: {
        slidesToShow: 4,
        slidesToScroll: 4,
      }
    },{
      breakpoint: 768,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
      }
    }, {
      breakpoint: 480,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
      }
    }]
  });
  // Синхронизация
  $single.on('afterChange', function(event, slick, currentSlide) {
    $nav.slick('slickGoTo', currentSlide);
    $nav.find('.slick-slide.is-active').removeClass('is-active');
    $nav.find('.slick-slide[data-slick-index="' + currentSlide + '"]').addClass('is-active');
  });
  $nav.on('click', '.slick-slide', function(event) {
    event.preventDefault();
    const goToSingleSlide = $(this).data('slick-index');
    $single.slick('slickGoTo', goToSingleSlide);
  });
});

new VenoBox({
  selector: ".venobox-gal",
  numeration: true,
  infinigall: true
});


$(window).on('load', function() {
  document.querySelectorAll('.gallery-wrap').forEach(function(wrapper) {
    const $wrapper = $(wrapper);
    const $gallery = $wrapper.find('.video-gallery');
    const $nav = $wrapper.find('.gallery-nav');
    const $slides = $gallery.find('.slide');
    const slideCount = $slides.length;
    // Если ≤1 слайда — скрываем навигацию и выходим
    if (slideCount <= 1) {
      $nav.hide();
      $gallery.show(); // показываем, даже если один слайд
      return;
    }
    // Инициализируем Slick
    $gallery.slick({
      dots: false,
      arrows: false,
      infinite: true,
      slidesToShow: 1,
      adaptiveHeight: true,
      speed: 500,
      fade: true,
      cssEase: 'linear',
      lazyLoad: 'ondemand'
    });
    $gallery.show();
    // === Работаем ТОЛЬКО с элементами внутри $wrapper ===
    const $dots = $nav.find('.dots');
    const $prevBtn = $nav.find('.nav-btn.prev');
    const $nextBtn = $nav.find('.nav-btn.next');
    // Отрисовка точек
    function renderDots() {
      $dots.empty();
      for (let i = 0; i < slideCount; i++) {
        const dot = $('<span class="dot" data-index="' + i + '">');
        if (i === 0) dot.addClass('active');
        $dots.append(dot);
      }
    }

    function updateDots(currentIndex) {
      $dots.find('.dot').removeClass('active');
      $dots.find('.dot[data-index="' + currentIndex + '"]').addClass('active');
    }
    renderDots();
    // Привязка событий к ЭТОЙ галерее
    $prevBtn.on('click', () => $gallery.slick('slickPrev'));
    $nextBtn.on('click', () => $gallery.slick('slickNext'));
    $dots.on('click', '.dot', function() {
      const idx = $(this).data('index');
      $gallery.slick('slickGoTo', idx);
    });
    $gallery.on('afterChange', function(event, slick, currentSlide) {
      updateDots(currentSlide);
    });
  });
});


// popup form
const openFormBtns = document.querySelectorAll('.openFormBtn');
const formPopup = document.getElementById('formPopup');
const formIframe = document.getElementById('formIframe');
const closeBtn = formPopup.querySelector('.close');

// Функция для блокировки скролла страницы
function disableBodyScroll() {
  // Сохраняем текущую ширину скролла (для компенсации)
  const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
  document.body.style.overflow = 'hidden';
  document.body.style.paddingRight = `${scrollbarWidth}px`;
}

// Функция для разблокировки скролла
function enableBodyScroll() {
  document.body.style.overflow = '';
  document.body.style.paddingRight = '';
}

// Навешиваем обработчик на КАЖДУЮ кнопку
openFormBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault(); // на случай, если это <a href="#">

    formPopup.classList.add('show');
    disableBodyScroll();

    if (formIframe && !formIframe.src) {
      formIframe.src = formIframe.dataset.src;
    }

    // Загружаем iframe с задержкой
    /*setTimeout(() => {
      if (!formIframe.src) {
        formIframe.src = formIframe.dataset.src;
      }
    }, 700);*/
  });
});

// Закрытие попапа
function closePopup() {
  formPopup.classList.remove('show');
  enableBodyScroll(); // Возвращаем скролл
}
closeBtn.addEventListener('click', closePopup);
// По клику вне попапа
formPopup.addEventListener('click', (e) => {
  if (e.target === formPopup) {
    closePopup();
  }
});
// По нажатию Esc
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && formPopup.classList.contains('show')) {
    closePopup();
  }
});


// forms
// const form = document.getElementById('sendForm');
const forms = document.querySelectorAll('.sendFormWrap form');

forms.forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());
    const action = e.currentTarget.dataset.action;
    // console.log(action);

    // === Сброс ошибок ТОЛЬКО в этой форме ===
    form.querySelectorAll('.is-invalid').forEach(el => {
      el.classList.remove('is-invalid');
    });

    const errorBlock = form.querySelector('.form-error'); // ← локальный блок ошибок
    if (errorBlock) errorBlock.style.display = 'none';

    // === Валидация полей в ЭТОЙ форме ===
    let isValid = true;

    const name = form.querySelector('[name="name"]');
    if (!name?.value.trim()) {
      name?.classList.add('is-invalid');
      isValid = false;
    }

    const email = form.querySelector('[name="email"]');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email?.value.trim() || !emailRegex.test(email.value)) {
      email?.classList.add('is-invalid');
      isValid = false;
    }

    const phone = form.querySelector('[name="phone"]');
    const phoneDigits = phone?.value.replace(/\D/g, '') || '';
    if (phoneDigits.length < 10) {
      phone?.classList.add('is-invalid');
      isValid = false;
    }

    const consent = form.querySelector('[name="consent"]');
    if (!consent?.checked) {
      consent?.classList.add('is-invalid');
      isValid = false;
    }

    // Проверка всех обязательных полей
    form.querySelectorAll('[required]').forEach(field => {
      let isEmpty = false;
      if (field.type === 'checkbox') {
        isEmpty = !field.checked;
      } else if (field.tagName === 'SELECT') {
        isEmpty = field.value === '';
      } else {
        // input, textarea
        isEmpty = !field.value.trim();
      }
      if (isEmpty) {
        field.classList.add('is-invalid');
      }
    });

    // === Если есть ошибки ===
    if (!isValid) {
      if (errorBlock) errorBlock.style.display = 'block';
      return;
    }

    // === Отправка ===
    try {
      const res = await fetch(action, { // ← используем action из формы
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        const successBlock = form.querySelector('.form-success');
        // console.log(successBlock);
        if (successBlock) {
          successBlock.style.display = 'block';
          setTimeout(() => {
            successBlock.style.display = 'none';
            form.reset();
            // Сброс стилей после reset
            form.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
              el.classList.remove('is-valid', 'is-invalid');
            });
          }, 3000);
        }
      } else {
        alert('Ошибка отправки');
      }
    } catch (err) {
      alert('Ошибка сети');
    }
  });

  // === Динамическая валидация ===
  form.querySelectorAll('input, select, textarea').forEach(el => {
    const event = el.tagName === 'SELECT' ? 'change' : 'input';
    el.addEventListener(event, () => validateField(el));
  });

  form.querySelectorAll('input[type="checkbox"]').forEach(el => {
    el.addEventListener('change', () => validateField(el));
  });
});

// === Универсальная валидация ===
function validateField(field) {
  let isValid = false;

  if (field.type === 'checkbox') {
    isValid = field.hasAttribute('required') ? field.checked : true;
    if (field.checked) {
      field.value = 'Y';
      field.classList.add('is-valid');
    } else if (!field.checked) {
      field.value = '';
      field.classList.remove('is-valid');
    }
  } else if (field.tagName === 'SELECT') {
    isValid = field.value !== '';
  } else {
    // Для input/textarea
    if (field.hasAttribute('required')) {
      if (field.type === 'email') {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        isValid = re.test(field.value);
      } else {
        isValid = field.value.trim() !== '';
      }
      // field.classList.add('is-invalid');
    } else {
      isValid = true; // не обязательное поле — всегда валидно
    }
  }

  // field.classList.toggle('is-valid', isValid);
  field.classList.toggle('is-invalid', !isValid);
}


const oldArticles = document.querySelector('.old_articles');
const tocSticky = document.querySelector('.toc-sticky');

if (!oldArticles || !tocSticky) return;

// Получаем нижнюю координату блока .old_articles
const getOldArticlesBottom = () => {
  const rect = oldArticles.getBoundingClientRect();
  return rect.top + window.scrollY + rect.height;
};

let oldArticlesBottom = getOldArticlesBottom();

function handleScroll() {
  // Нижняя граница .old_articles в документе (абсолютная координата)
  const oldArticlesRect = oldArticles.getBoundingClientRect();
  const oldArticlesBottom = oldArticlesRect.top + window.scrollY + oldArticlesRect.height;

  if (window.scrollY >= oldArticlesBottom) {
    // Пользователь проскроллил ниже конца .old_articles → делаем sticky
    tocSticky.style.position = 'sticky';
    tocSticky.style.top = '100px';
  } else {
    // Ещё не доскроллили до конца → обычное поведение
    tocSticky.style.position = 'relative';
    tocSticky.style.top = '0';
  }
}

// Обновляем позицию при изменении размера окна (на случай адаптивности)
window.addEventListener('resize', () => {
  oldArticlesBottom = getOldArticlesBottom();
  handleScroll();
});

window.addEventListener('scroll', handleScroll);
handleScroll(); // Проверяем сразу при загрузке


}); // end DOMContentLoaded
