$(document).ready(function(){
    $('.carousel').carousel({
        wrap: false,
        interval: false
    });

    $('.carousel .previous').click(function(){
        $('.carousel').carousel('prev');
    });

    $(document).on('click', '#survey .option', function(){
        var $selector = $(this).parents('.item');
        var $option = $(this);
        $selector.find('.option').removeClass('selected');
        $option.addClass('selected');
        if ($selector.is('.problem')){
            render_problem_children($option.data('value'));
        }
    });
    $('#survey a.next').click(function(){
        var $selector = $(this).parents('.item');
        if ($selector.find('.option.selected').size() == 0) {
            alert('请先选择');
            return;
        }
        if ($selector.is('.last-slide')) {
            save_survey();
            location.href = $selector.data('url');
        } else {
            $('.carousel').carousel('next');
        }
    });

    // render the problem children slide
    function render_problem_children(problem) {
        var $slide_item = $('#survey .problem-children');
        var $option_template = $('.option-template', $slide_item);
        // remove follwing options
        $option_template.siblings('div').remove();
        for (var i in PROBLEMS) {
            if (PROBLEMS[i].value == problem) {
                $('.title', $slide_item).text(PROBLEMS[i].title);
                for (var j in PROBLEMS[i].children) {
                    var child = PROBLEMS[i].children[j];
                    var $new_option = $option_template.clone();
                    $new_option.removeClass('option-template hidden');
                    $('.option', $new_option).data('value', child[0]);
                    $('.option', $new_option).data('label', child[1]);
                    $('h4', $new_option).text(child[1]);
                    $option_template.before($new_option);
                }
                break;
            }
        }
    }

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

    // hide and show panel in survey more page
    $('#survey-more .collapse-btn').click(function(){
        var $target = $($(this).data('target'));
        if ($target.is('.hidden')) {
            $target.removeClass('hidden');
            var $icon = $(this).parents('.block').find('.collapse-btn.icon');
            $icon.removeClass('glyphicon-plus').addClass('glyphicon-minus');
        } else {
            $target.addClass('hidden');
            var $icon = $(this).parents('.block').find('.collapse-btn.icon');
            $icon.removeClass('glyphicon-minus').addClass('glyphicon-plus');
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
                    $('#photos').append('<li><img height="64" src="{url}" /><a data-id="{id}" href="javascript:void(0)"><span class="glyphicon glyphicon-remove"></span></a></li>'.replace('{url}', data.result.path).replace('{id}', data.result.id));
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
                $this.parent('li').remove();
            }
        });
    });

    // save user survey to localStorage
    function save_survey(){
        try {
            survey = JSON.parse(localStorage.survey || '{}');
        } catch(err){
            survey = {};
        }
        $survey = $('#survey');
        $surveyMore = $('#survey-more');

        if ($surveyMore.length) {
            $age = $('.age', $surveyMore);
            survey.age = {
                label: $age.val() + '岁',
                value:$age.val()
            };

            $height = $('.height', $surveyMore);
            survey.height = {
                label:$height.val() + 'CM',
                value: $height.val()
            };

            $weight = $('.weight', $surveyMore);
            survey.weight = {
                label:$weight.val() + 'CM',
                value: $weight.val()
            };

            $selectedOption = $('.clothing_size option:selected', $surveyMore);
            survey.clothing_size = {
                label: $selectedOption.text(),
                value: $selectedOption.data('value')
            };

            $selectedOption = $('.pants_size option:selected', $surveyMore);
            survey.pants_size = {
                label: $selectedOption.text(),
                value: $selectedOption.data('value')
            };

            $selectedOption = $('.pants_style option:selected', $surveyMore);
            survey.pants_style = {
                label: $selectedOption.text(),
                value: $selectedOption.data('value')
            };

            $message = $('.message', $surveyMore);
            survey.message = {
                label: $message.val(),
                value: $message.val()
            };

            $priceSlider = $('#price-slider');
            survey.price = {
                label: $priceSlider.slider('value') + '元',
                value: $priceSlider.slider('value')
            };
        }

        if ($survey.length) {
            $selectedOption = $('.problem .option.selected', $survey);
            survey.parent_problem = {
                label: $selectedOption.data('label'),
                value: $selectedOption.data('value')
            };

            $selectedOption = $('.problem-children .option.selected', $survey);
            survey.problem = {
                value: $selectedOption.data('value')
            };
            for (i in PROBLEMS) {
                if (PROBLEMS[i].value == survey.parent_problem.value) {
                    survey.problem.label = PROBLEMS[i].label + ',' + $selectedOption.data('label');
                }
            }
        }

        localStorage.survey = JSON.stringify(survey);
    }

    // re-store survey data from localStorage
    function init_survey(){
        var survey = JSON.parse(localStorage.survey||'{}');
        var $survey = $('#survey');
        var $surveyMore = $('#survey-more');

        if ($surveyMore.length) {
            $('.age', $surveyMore).val(survey.age?survey.age.value:$('.age', $surveyMore).val());
            $('.height', $surveyMore).val(survey.height?survey.height.value:$('.height', $surveyMore).val());
            $('.weight', $surveyMore).val(survey.weight?survey.weight.value:$('.weight', $surveyMore).val());
            $('.message', $surveyMore).val(survey.message?survey.message.value:'');
            $('#price-slider').slider('value', survey.price?survey.price.value:600);
            $('#price-val').text(survey.price?survey.price.label:'600元');
            $('.clothing_size option', $surveyMore).each(function(){
               if (survey.clothing_size && $(this).data('value') == survey.clothing_size.value) {
                   $(this).attr('selected', 'selected');
               }
            });
            $('.pants_size option', $surveyMore).each(function(){
               if (survey.pants_size && $(this).data('value') == survey.pants_size.value) {
                   $(this).attr('selected', 'selected');
               }
            });
            $('.pants_style option', $surveyMore).each(function(){
               if (survey.pants_style && $(this).data('value') == survey.pants_style.value) {
                   $(this).attr('selected', 'selected');
               }
            });
        }
    }
    init_survey();

    // validate fields
    function validate_fields() {
        $('#survey-more .input-group').removeClass('error');
        var allPass = true;
        var sels = ['#survey-more .age', '#survey-more .height', '#survey-more .weight'];
        for (var i in sels) {
            var $field = $(sels[i]);
            if (parseInt($field.val())) {
                $field.val(parseInt($field.val()));
            } else {
                allPass = false;
                $field.parent().addClass('error');
            }
        }
        return allPass;
    }

    // submit more survey data
    $('#submit-more-survey-btn').click(function(){
        if (!validate_fields())
            return;
        save_survey();
        location.href=$(this).data('url');
    });
});
