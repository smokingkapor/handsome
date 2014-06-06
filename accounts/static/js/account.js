$(document).ready(function(){
    // update image and description for size input
    $('.size-input').focus(function(){
        $('#sample img').attr('src', $(this).data('image'));
        $('#sample .description').text($(this).data('description'));
    });

    // enable submit button if the agreement is checked
    $('#agreement-btn').on('click change', function(){
        if ($(this).is(':checked')) {
            $(this).parents('form').find('input:submit').removeClass('disabled');
        } else {
            $(this).parents('form').find('input:submit').addClass('disabled');
        }
    });
});
