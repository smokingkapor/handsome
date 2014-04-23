$(document).ready(function(){

    // Toggle the input type between password and text
    $('.eye_conversion').click(function(){
        var $password_input = $('#' + $(this).data('input-id'));
        if ($password_input.attr('type') == 'password') {
            $password_input.attr('type', 'text');
            $(this).removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
        } else {
            $password_input.attr('type', 'password');
            $(this).removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
        }
    });

    // enable popover
    $('.popover-btn').popover();
});

function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
