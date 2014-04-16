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
        $(this).parents('.carousel-caption').find('.next').removeClass('hidden');
        $('.carousel').carousel('next');
    });

    // login or register
    $('#register-btn, #login-btn').click(function(){
        var $btn = $(this);
        var $form = $btn.parents('form');
        $('.form-error', $form).addClass('hidden');
        $btn.button('loading');
        $.ajax({
            url: $form.attr('action'),
            type: 'post',
            dataType: 'json',
            data: {
                username: $('input[name=username]', $form).val(),
                password: $('input[name=password]', $form).val(),
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            success: function(result) {
                $btn.button('reset');
                if (result.success) {
                    $('.carousel').carousel('next');
                } else {
                    $('.form-error .alert', $form).text(result.errors[0]);
                    $('.form-error', $form).removeClass('hidden');
                }
            }
        });
    });

    // ajax upload full body shot
    $('#fileupload').fileupload({
        url: $(this).data('url'),
        dataType: 'json',
        done: function (e, data) {
            if (data.result.success) {
                $('#files').empty();
                $('<img>').attr('width', '500').attr('src', data.result.path + '?i=' + new Date().getTime()).appendTo($('#files'));
            }
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css('width', progress + '%');
        }
    }).prop('disabled', !$.support.fileInput).parent().addClass($.support.fileInput ? undefined : 'disabled');

});
