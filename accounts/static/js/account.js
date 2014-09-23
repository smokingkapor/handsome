$(document).ready(function(){
    // enable submit button if the agreement is checked
    $('#agreement-btn').on('click change', function(){
        if ($(this).is(':checked')) {
            $('#submit-btn').removeAttr('disabled');
        } else {
            $('#submit-btn').attr('disabled', 'disabled');
        }
    });

    // send temporary password
    $('#send-password-btn').click(function(){
        var phone = $('#id_phone').val();
        if (!/^1[3-8]\d{9}$/.test(phone)) {
            alert('手机号码格式不正确');
            return;
        }
        $('#send-password-btn').attr('disabled', 'disabled').data('seconds', 60);
        $.ajax({
            url: $(this).data('url'),
            data: {phone: phone},
            success: function() {
                send_pwd_timer();
            }
        });
    });

    // selector in survey more
    $('#update-profile .line .selector li,#update-profile .line .image-selector li').click(function(){
        $(this).siblings('li').removeClass('selected');
        $(this).addClass('selected');
        $(this).parents('.line').removeClass('required');
    });

    // validate height and weight when changed
    $('#height,#weight').on('change blur focus', function(){
        var height = parseFloat($('#height').val());
        var weight = parseFloat($('#weight').val());
        if (height && weight) {
            $(this).parents('.line').removeClass('required');
            $('#height').val(height);
            $('#weight').val(weight);
        } else {
            if ((!height && $('#height').val()) || (!weight && $('#weight').val()))
            $(this).parents('.line').addClass('required');
        }
    });

    // validate fields
    function validate_fields() {
        $('#update-profile .line').removeClass('required');
        var $first_error_selector = undefined;

        var height = parseFloat($('#height').val());
        var weight = parseFloat($('#weight').val());
        if (!height || !weight) {
            $first_error_selector = $('#height').parents('.line').addClass('required');
            $('#height').val(height?height:'');
            $('#weight').val(weight?weight:'');
        }

        $('#update-profile .line .selector').each(function(){
            if ($(this).find('li.selected').size() == 0) {
                if (!$first_error_selector) $first_error_selector = $(this);
                $(this).parents('.line').addClass('required');
            }
        });

        if ($first_error_selector) {
            $('html, body').animate({scrollTop: $first_error_selector.offset().top-50}, 500);
            return false;
        }
        return true;
    }

    // submit more survey data
    $('#update-profile-btn').click(function(){
        var $btn = $(this);
        if (!validate_fields())
            return;
        $btn.button('loading');
        var data = {
            age_group: $('#age li.selected').data('value'),
            clothing_size: $('#clothing_size li.selected').data('value'),
            color: $('#color li.selected').data('value'),
            height: $('#height').val(),
            pants_size: $('#pants_size li.selected').data('value'),
            pants_style: $('#pants_style li.selected').data('value'),
            shoe_size: $('#shoe_size li.selected').data('value'),
            weight: $('#weight').val(),
            csrfmiddlewaretoken: get_cookie('csrftoken')
        };
        $.ajax({
            url: $btn.data('url'),
            type: 'post',
            dataType: 'json',
            data: data,
            success: function(data) {
                $btn.button('reset');
                if (data.success) {
                    location.href = data.next;
                }
            }
        });
    });
});

function send_pwd_timer() {
    var seconds = $('#send-password-btn').data('seconds');
    if (seconds > 0) {
        seconds -= 1;
        $('#send-password-btn').data('seconds', seconds).text(seconds + '秒');
        setTimeout('send_pwd_timer()', 1000);
    } else {
        $('#send-password-btn').removeAttr('disabled').text('重新发送密码');
    }
}
