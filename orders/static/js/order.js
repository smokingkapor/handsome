$(document).ready(function(){
    // address select
    $('#province, #city').change(function(){
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
        $('#region').text(address);
    });

    // validate all the fields in the address form
    function validate_address_form() {
        var fields = ['#name', '#phone', '#house'];
        for (var i in fields) {
            var $field = $(fields[i]);
            var val = $field.val();
            if (!val) {
                $field.parents('.form-group').addClass('has-error');
            } else {
                $field.parents('.form-group').removeClass('has-error');
            }
        }

        $('select.address:hidden').each(function(){
            $(this).parents('.form-group').removeClass('has-error');
        });

        $('select.address:visible').each(function(){
            if ($(this).val() == '-1') {
                $(this).parents('.form-group').addClass('has-error');
            } else {
                $(this).parents('.form-group').removeClass('has-error');
            }
        });

        return $('#create-order .has-error').size() == 0;
    }

    // cancel address edit
    $('#cancel-edit-address-btn').click(function() {
        $('#address-edit-panel').addClass('hidden');
        $('#full-adress').removeClass('hidden');
    });

    // save the address info
    $('#save-address-btn').click(function(){
        if (!validate_address_form()) {
            return;
        }
        var data = {
            address_id: $('#address-pk').val(),
            name: $('#name').val(),
            phone: $('#phone').val(),
            house: $('#house').val(),
            province: $('#province').val()
        };
        if ($('#city').is(':visible')) {
            data['city'] = $('#city').val();
        }
        if ($('#country').is(':visible')) {
            data['country'] = $('#country').val();
        }
        $.ajax({
            url: $(this).data('url'),
            data: data,
            success: function(data) {
                $('#address-pk').val(data.id);
                $('#address-edit-panel').addClass('hidden');
                $('#full-adress').removeClass('hidden');
                $('#full-adress span:first').text(data.address);
            }
        });
    });

    $('#edit-address-btn').click(function() {
        $('#address-edit-panel').removeClass('hidden');
        $('#full-adress').addClass('hidden');
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
        if ($('#address-edit-panel').is(':visible')) {
            alert('请先保存配送信息');
            return;
        }
        var $btn = $(this);
        $btn.button('loading');
        var data = {
            total_price: parseInt(localStorage.price),
            message: requirement,
            preferred_designer: designer.id,
            address: $('#address-pk').val(),
            csrfmiddlewaretoken: get_cookie('csrftoken')
        };
        $.ajax({
            url: $btn.data('url'),
            type: 'post',
            dataType: 'json',
            data: data,
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
