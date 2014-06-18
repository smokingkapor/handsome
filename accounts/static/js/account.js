$(document).ready(function(){
    // update image and description for size input
    $('.size-input').focus(function(){
        $('#sample img').attr('src', $(this).data('image'));
        $('#sample .description').text($(this).data('description'));
    });

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
        $.ajax({
            url: $(this).data('url'),
            data: {phone: phone},
            success: function() {
                $('#send-password-btn').attr('disabled', 'disabled').data('seconds', 60);
                send_pwd_timer();
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
