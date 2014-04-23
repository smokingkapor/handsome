$(document).ready(function(){
    // ajax upload full body shot
    $('#fileupload').fileupload({
        url: $(this).data('url'),
        dataType: 'json',
        disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
        maxFileSize: 5000000,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        done: function (e, data) {
            if (data.result.success) {
                $('<img height="280">').data('filename', data.result.filename).attr('src', data.result.path).appendTo($('#photos'));
                update_photos_field();
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

    // update hidden photos field
    function update_photos_field() {
        var photos = [];
        $('#photos img').each(function(){
            photos.push($(this).data('filename'));
        });
        $('#design-photos').val(photos.join(';'));
    }

    // create design
    $('#create-design-btn').click(function(){
        var $btn = $(this);
        $btn.button('loading');
        $.ajax({
            url: $btn.data('url'),
            type: 'post',
            dataType: 'json',
            data: {
                comment: $('#comment').val(),
                photos: $('#design-photos').val(),
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            success: function(data) {
                $btn.button('reset');
                if (data.success) {
                    location.href = data.next;
                }
            }
        });
    });
});
