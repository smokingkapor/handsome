$(document).ready(function(){

    $('.carousel').carousel({
        wrap: false,
        interval: false
    });

    $('.carousel .previous').click(function(){
        $('.carousel').carousel('prev');
    });

    $('#survey #steps .style').addClass('active');
    $('.carousel').on('slid.bs.carousel', function(){
        // highlight step
        var active_item = $('#survey .item.active').prop('id');
        $('#survey #steps .active').removeClass('active');
        $('#survey #steps .' + active_item).addClass('active');
    });

    $('.selector .option .select-btn').click(function(){
        var $selector = $(this).parents('.selector');
        var $option = $(this).parents('.option');
        $selector.find('.option').removeClass('selected');
        $selector.parents('.item').find('.next').removeClass('hidden');
        $option.addClass('selected');
        if ($selector.is('.auto-slide')) {
            $('.carousel').carousel('next');
        } else if ($selector.is('.last-slide')) {
            save_survey();
            location.href = $selector.data('url');
        }
    });

    // price slider tooltip
    if ($('#price-slider').size() > 0){
        $('#price-slider').slider({
            range: 'min',
            value: 600,
            min: 300,
            max: 2000,
            slide: function(event, ui) {
                $("#price-val").text(ui.value + '元');
            }
        });
    }

    // init style and designer in survey more
    function init_survey_more() {
        if (!$('#survey-more').length)  return;
        try {
            var survey = JSON.parse(localStorage.survey || '{}');
        } catch(err){
            var survey = {};
        }
        $('#style_again li').removeClass('selected').each(function(){
            if (survey.style && $(this).data('value') == survey.style.value) {
                $(this).addClass('selected');
                return false;
            }
        });
        $('#designer_again li').removeClass('selected').each(function(){
            if (survey.designer && $(this).data('value') == survey.designer.value) {
                $(this).addClass('selected');
                return false;
            }
        });
        if (location.href.indexOf('mode=edit') != -1) {
            $('#situation li').removeClass('selected').each(function(){
                if (survey.situation && $(this).data('value') == survey.situation.value) {
                    $(this).addClass('selected');
                    return false;
                }
            });
            $('#message').val(survey.message.value);
            $('#price-slider').slider('option', 'value', survey.price.value);
            $("#price-val").text(survey.price.value + '元');
        }
    }
    init_survey_more();

    // selector in survey more
    $('#survey-more .line .selector li,#survey-more .line .image-selector li').click(function(){
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

    if ($('#fileupload').size() > 0){
        $('#fileupload').fileupload({
            dataType: 'json',
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);
                $('#upload_process b').text(progress+'%');
                $('#upload_process').show();
            },
            done: function(e, data) {
                $('#upload_process').hide();
                if (data.result.success) {
                    $('#photos').append('<li><img width="128" src="{url}" /><a data-id="{id}" href="javascript:void(0)"><span class="glyphicon glyphicon-remove"></span></a></li>'.replace('{url}', data.result.path).replace('{id}', data.result.id));
                }
            }
        });
    }

    // remove photo
    $(document).on('click', '#photos a', function(){
        if (!confirm('确定删除？')) return;
        var $this = $(this);
        $.ajax({
            url: $('#photos').data('url'),
            data: {'id': $this.data('id')},
            success: function(data) {
                $this.parents('li').remove();
            }
        });
    });

    // save user survey to localStorage
    function save_survey(){
        try {
            var survey = JSON.parse(localStorage.survey || '{}');
        } catch(err){
            var survey = {};
        }
        if ($('#height').length) {
            survey.height = {
                label: $('#height').val() + '厘米',
                value: $('#height').val()
            };
        }
        if ($('#weight').length) {
            survey.weight = {
                label: $('#weight').val() + '公斤',
                value: $('#weight').val()
            };
        }
        if ($('#age').length) {
            survey.age = {
                label: $('#age li.selected').text(),
                value: $('#age li.selected').data('value')
            };
        }
        if ($('#clothing_size').length) {
            survey.clothing_size = {
                label: $('#clothing_size li.selected').text(),
                value: $('#clothing_size li.selected').data('value')
            };
        }
        if ($('#pants_size').length) {
            survey.pants_size = {
                label: $('#pants_size li.selected').text(),
                value: $('#pants_size li.selected').data('value')
            };
        }
        if ($('#shoe_size').length) {
            survey.shoe_size = {
                label: $('#shoe_size li.selected').text(),
                value: $('#shoe_size li.selected').data('value')
            };
        }
        if ($('#pants_style').length) {
            survey.pants_style = {
                label: $('#pants_style li.selected').text(),
                value: $('#pants_style li.selected').data('value')
            };
        }
        if ($('#color').length) {
            survey.color = {
                label: $('#color li.selected').data('label'),
                value: $('#color li.selected').data('value')
            };
        }
        if ($('#situation').length) {
            survey.situation = {
                label: $('#situation li.selected').text(),
                value: $('#situation li.selected').data('value')
            };
        }
        if ($('#price').length) {
            survey.price = {
                label: $('#price .option.selected').data('label'),
                value: $('#price .option.selected').data('value')
            };
        }
        if ($('#style').length) {
            survey.style = {
                label: $('#style .option.selected').data('label'),
                value: $('#style .option.selected').data('value')
            };
        }
        if ($('#designer').length) {
            survey.designer = {
                label: $('#designer .option.selected').data('label'),
                value: $('#designer .option.selected').data('value'),
                avatar: $('#designer .option.selected').data('avatar')
            };
        }
        if ($('#style_again').length) {
            survey.style = {
                label: $('#style_again li.selected .name').text(),
                value: $('#style_again li.selected').data('value')
            };
        }
        if ($('#designer_again').length) {
            survey.designer = {
                label: $('#designer_again li.selected .name').text(),
                value: $('#designer_again li.selected').data('value'),
                avatar: $('#designer_again li.selected').data('avatar')
            };
        }
        if ($('#message').length) {
            survey.message = {
                label: $('#message').val(),
                value: $('#message').val()
            };
        }
        if ($('#price-slider').length) {
            survey.price = {
                label: $('#price-slider').slider('value') + '左右',
                value: $('#price-slider').slider('value')
            };
        }

        localStorage.survey = JSON.stringify(survey);
    }

    // validate fields
    function validate_fields() {
        $('#survey-more .line').removeClass('required');
        var $first_error_selector = undefined;

        var height = parseFloat($('#height').val());
        var weight = parseFloat($('#weight').val());
        if (!height || !weight) {
            $first_error_selector = $('#height').parents('.line').addClass('required');
            $('#height').val(height?height:'');
            $('#weight').val(weight?weight:'');
        }

        $('#survey-more .line .selector,#survey-more .line .image-selector').each(function(){
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
    $('#submit-more-survey-btn').click(function(){
        if (!validate_fields())
            return;
        save_survey();
        location.href=$(this).data('url');
    });

    $('.modal').on('show.bs.modal', function (e) {
        $('img', $(this)).each(function() {
            if ($(this).data('src')) {
                $(this).prop('src', $(this).data('src'));
                $(this).data('src', undefined);
            }
        });
    });
});
