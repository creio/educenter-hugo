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
    $('.venobox').venobox();
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

    if (!formIframe.src) {
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
