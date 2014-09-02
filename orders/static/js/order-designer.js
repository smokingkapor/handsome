$(document).ready(function(){
    // bind datetime picker
    $('input.datetime').datepicker();

    // send order
    $('.send-order-btn').click(function(){
        var express_provider = prompt('输入快递公司名字');
        var express_code = prompt('输入快递单号');
        if (!express_provider || !express_code) {
            alert('不能为空！');
        } else {
            $.ajax({
                url: $(this).data('url'),
                data: {express_provider: express_provider, express_code: express_code},
                success: function(data) {
                    location.reload();
                }
            });
        }
    });
});
