$(function () {
    // 为了隐藏滚动条
    $('.home').width(innerWidth)

     new Swiper('#topSwiper', {
         paginationClickable: true,
         centeredSlides: true,
        slidesPerView: 1,
        spaceBetween: 30,
        autoplay: 2500,
         loop: true,
        pagination: '.swiper-pagination',
    });


     new Swiper('#mustbuySwiper', {
        slidesPerView: 3,
        spaceBetween: 10,
        loop: true
    })
})