$(document).ready(function(){
    // address select
    $('#province, #city, #country').change(function(){
        $(this).nextAll('select').addClass('hidden').children('option[value!=-1]').remove();
        var pk = $(this).val();
        if (pk != -1) {
            var $target = $($(this).data('target'));
            $.get($(this).data('url'), {pk: pk}, function(data){
                $.each(data, function(){
                    $('<option>').val(this.pk).text(this.fields.name).appendTo($target);
                });
                if (data.length > 0) {
                    $target.removeClass('hidden');
                }
            });
        }
    });

    // update address
    $('select.address').change(function(){
        var address = '';
        $('select.address').each(function(){
            if ($(this).val() != -1) {
                address += $('option:selected', this).text();
            }
        });
        if (address.length > 0) {
            address += '  ';
        }
        $('#address').text(address);
    });

    // load price and personal requirement from local storage
    var designer =JSON.parse(localStorage.designer);
    var requirement = localStorage.requirement?localStorage.requirement:'没要求';
    if ($('#create-order').size() > 0) {
        $('#price').text(localStorage.price);
        $('#designer').text(designer.name);
        $('#personal-requirement').text(requirement);
    }

    // create order
    $('#create-order-btn').click(function(){
        var $btn = $(this);
        $btn.button('loading');
        $.ajax({
            url: $btn.data('url'),
            type: 'post',
            dataType: 'json',
            data: {
                total_price: parseInt(localStorage.price),
                message: requirement,
                preferred_designer: designer.id,
                address: $('#address').text().trim() + $('#address').next('input').val(),
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


    // order detail photo slide
    if ($('#design-photos').size() > 0) {
        $('#design-photos').carousel();
    }
});
