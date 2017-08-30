$(document).ready(function () {

    $('.btn-vertical-slider').on('click', function () {
        
        if ($(this).attr('data-slide') == 'next') {
            $('#myCarousel').carousel('next');
        }
        if ($(this).attr('data-slide') == 'prev') {
            $('#myCarousel').carousel('prev')
        }
        if ($(this).attr('data-slide') == 'next') {
            $('.myCarousel1').carousel('next');
        }
        if ($(this).attr('data-slide') == 'prev') {
            $('.myCarousel1').carousel('prev')
        }
    });
});
