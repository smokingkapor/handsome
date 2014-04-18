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
        var $selector = $(this).parents('.selector');
        $selector.find('.option').removeClass('selected');
        $selector.parents('.item').find('.next').removeClass('hidden');
        $(this).addClass('selected');
        if ($selector.is('.auto-slide')) {
            $('.carousel').carousel('next');
        }
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
                    for (var key in result.profile) {
                        $('#sizes input[name=' + key + ']').val(result.profile[key]);
                    }
                    if (result.profile && result.profile.url) {
                        $('<img>').attr('height', 280).attr('src', result.profile.url).appendTo($('#files'));
                    }
                    $('.carousel').carousel('next');
                } else {
                    if (result.errors.length > 0) {
                        $('.form-error .alert', $form).text(result.errors[0]);
                        $('.form-error', $form).removeClass('hidden');
                    }
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
                $('<img>').attr('height', '280').attr('src', data.result.path + '?i=' + new Date().getTime()).appendTo($('#files'));
                $('#fullbody-shot').val(data.result.filename);
            }
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            if (progress == 100) {
                $('#progress').text('');
            } else {
                $('#progress').text(progress + '%');
            }
        }
    }).prop('disabled', !$.support.fileInput).parent().addClass($.support.fileInput ? undefined : 'disabled');

    // update image and description for size input
    $('.size-input').focus(function(){
        $('#sample img').attr('src', $(this).data('image'));
        $('#sample .description').text($(this).data('description'));
    });

    $('#finish-btn').click(function() {
        var $btn = $(this);
        $btn.button('loading');
        var url = $(this).data('url');
        var next = $(this).data('next');
        var style = $('#style .option.selected').data('value');
        var age_group = $('#age-group .option.selected').data('value');
        var height = $('#sizes input[name=height]').val();
        var weight = $('#sizes input[name=weight]').val();
        var waistline = $('#sizes input[name=waistline]').val();
        var hipline = $('#sizes input[name=hipline]').val();
        var chest = $('#sizes input[name=chest]').val();
        var foot = $('#sizes input[name=foot]').val();
        var filename = $('#fullbody-shot').val();
        var requirement = $('#personal-requirement').val();
        var price = $('#price .selector .option.selected').text();

        // cache requirement and price
        localStorage.requirement = requirement;
        localStorage.price = price;

        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: {
                style: style,
                age_group: age_group,
                height: height,
                weight: weight,
                waistline: waistline,
                chest: chest,
                hipline: hipline,
                foot: foot,
                filename: filename,
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            success: function(data) {
                $btn.button('reset');
                location.href = next;
            }
        });
    });

});
