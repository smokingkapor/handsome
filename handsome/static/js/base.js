$(document).ready(function(){

    // enable popover
    $('.popover-btn').popover();

    $('a.confirm').click(function(){
        if(confirm($(this).data('confirm'))) {
            location.href = $(this).data('url');
        }
    });
    $('.carousel').carousel();

    $('.right_bar').click(function() {
        $(this).hide();
        $('#kefu').show();
    });
    $('#kefu .close').click(function() {
        $('.right_bar').show();
        $('#kefu').hide();
    });
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
