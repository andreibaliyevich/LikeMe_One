$('.dropdown-toggle').click(function() {
    if ($(this).hasClass('active')) {
        $(this).removeClass('active').parent().find('.dropdown-menu').slideUp(200);
        return
    }
    $(this).addClass('active').parent().find('.dropdown-menu').slideDown(200);
});


$('.subnav-body-slider').slick({
    slidesToShow: 6,
    slidesToScroll: 1,
    arrows:false,
    dots:true,
    autoplay: true,
    responsive: [
        {
            breakpoint: 1400,
            settings: {
                slidesToShow: 5,
            }
        },
        {
            breakpoint: 1000,
            settings: {
                slidesToShow: 4,
            }
        },
        {
            breakpoint: 990,
            settings: {
                slidesToShow: 3,
            }
        },
        {
            breakpoint: 780,
            settings: {
                slidesToShow: 2,
            }
        },
        {
            breakpoint: 550,
            settings: {
                slidesToShow: 1,
            }
        }
    ]
});


$('.nav-wrap-burger').click(function() {
    if ($(this).hasClass('active')) {
        $('body').css({"margin-left":"0","position":"relative","width":"auto"});
        $('nav').css({"margin-left":"0"});
        $('.nav-wrap-middle').css({"left":"-250px"});
        $(this).removeClass('active');
        return
    }
    $(this).addClass('active');
    $('body').css({"margin-left":"250px","position":"absolute","width":"100vw"});
    $('nav').css({"margin-left":"250px"});
    $('.nav-wrap-middle').css({"left":"0","display":"block"});
})
