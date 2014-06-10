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
});
