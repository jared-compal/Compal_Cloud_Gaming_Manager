
$(window).on('scroll', function() {
    if ($(this).scrollTop() >= 30) {
        $('.navbar-items').addClass('hide');
        $('.navbar-img').addClass('hide');
        $('.sidebar-toggle>img').addClass('shrink');
        $('.sidebar').addClass('sidebar-shrink');
    } else {
        $('.navbar-items').removeClass('hide');
        $('.navbar-img').removeClass('hide');
        $('.sidebar-toggle>img').removeClass('shrink');
        $('.sidebar').removeClass('sidebar-shrink');
    }
});

// $('.card-container').on('click', function () {
//     console.log($(this).scrollLeft(50));
// });

