$(document).ready(function(){
    $('.select-design-btn').click(function(){
        var all = $('.design-clothings .wanted:not(:checked)').size() == 0;
        if ($('.design-clothings .wanted:checked').size() == 0) {
            alert('您忘记选择衣服了');
            return;
        }
        var ids = [];
        $('.design-clothings .wanted:checked').each(function(){
            ids.push($(this).data('id'));
        });
        location.href = $(this).data('url') + '?all=' + all + '&ids=' + ids.join(',');
    });
});
