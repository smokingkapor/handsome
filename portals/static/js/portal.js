$(document).ready(function(){
    $('.carousel').carousel({
        wrap: false,
        interval: false
    });

    $('.carousel .next').click(function(){
        $('.carousel').carousel('next');
    });

    $('.carousel .previous').click(function(){
        $('.carousel').carousel('prev');
    });

    $('.selector .option').click(function(){
        $(this).parents('.selector').find('.option').removeClass('selected');
        $(this).addClass('selected');
    });
});
