$(document).ready(function(){

    $('.carousel').carousel({
        wrap: false,
        interval: false
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

    // save user survey to localStorage
    $('#survey-finish-btn').click(function(){
        var survey = {
            style: {
                label: $('#style .option.selected').data('label'),
                value: $('#style .option.selected').data('value')
            },
            age: {
                label: $('#age .option.selected').data('label'),
                value: $('#age .option.selected').data('value')
            },
            price: {
                label: $('#price .option.selected').data('label'),
                value: $('#price .option.selected').data('value')
            },
            designer: {
                label: $('#designer .option.selected').data('label'),
                value: $('#designer .option.selected').data('value'),
                avatar: $('#designer .option.selected').data('avatar'),
                requirement: $('#designer textarea').val()
            }
        };
        localStorage.survey = JSON.stringify(survey);
        location.href = $(this).data('href');
    });
});
