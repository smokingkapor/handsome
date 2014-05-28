$(document).ready(function(){
    // bind datetime picker
    $('input.datetime').datepicker();

    // send order
    $('.send-order-btn').click(function(){
        var express_info = prompt('输入快递公司和运单号');
        if (express_info.length < 10) {
            alert('请重新填写！');
        } else {
            $.ajax({
                url: $(this).data('url'),
                data: {express_info: express_info},
                success: function(data) {
                    location.reload();
                }
            });
        }
    });
});
