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
        } else if ($selector.is('.last-slide')) {
            save_survey();
            location.href = $selector.data('url');
        }
    });

    // save user survey to localStorage
    function save_survey(){
        try {
            var survey = JSON.parse(localStorage.survey || '{}');
        } catch(err){
            var survey = {};
        }
        if ($('#style').length) {
            survey.style = {
                label: $('#style .option.selected').data('label'),
                value: $('#style .option.selected').data('value')
            };
        }
        if ($('#age').length) {
            survey.age = {
                label: $('#age .option.selected').data('label'),
                value: $('#age .option.selected').data('value')
            };
        }
        if ($('#price').length) {
            survey.price = {
                label: $('#price .option.selected').data('label'),
                value: $('#price .option.selected').data('value')
            };
        }
        if ($('#designer').length) {
            survey.designer = {
                label: $('#designer .option.selected').data('label'),
                value: $('#designer .option.selected').data('value'),
                avatar: $('#designer .option.selected').data('avatar')
            };
        }
        localStorage.survey = JSON.stringify(survey);
    }

    // price select in survey more page
    $('#survey-more .prices .option').click(function(){
        var $prices = $('#survey-more .prices');
        $prices.find('.option').removeClass('selected');
        $(this).addClass('selected');
    });


    // submit more survey data
    $('#submit-more-survey-btn').click(function(){
        // check price first
        if ($('#survey-more .prices .option.selected').size() == 0) {
            alert('请先选择价位');
            return;
        }

        // save data to localStorage
        try {
            var survey = JSON.parse(localStorage.survey || '{}');
        } catch(err){
            var survey = {};
        }
        survey.price = {
            label: $('#survey-more .prices .option.selected').data('label'),
            value: $('#survey-more .prices .option.selected').data('value')
        };
        survey.requirements = $('#requirements').val();
        localStorage.survey = JSON.stringify(survey);

        // form submit
        $('#survey-more form').submit();
    });
});
