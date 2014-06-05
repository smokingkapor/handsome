$(document).ready(function(){
    // update image and description for size input
    $('.size-input').focus(function(){
        $('#sample img').attr('src', $(this).data('image'));
        $('#sample .description').text($(this).data('description'));
    });
});
