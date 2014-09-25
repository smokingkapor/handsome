$(document).ready(function(){
    if ($('#create_success_popup').size() > 0) {
        $('#create_success_popup').modal({show: true});
    }

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

        if (!/^1[3-8]\d{9}$/.test($('#phone').val())) {
            alert('手机号码格式不正确');
            $('#phone').parents('.form-group').addClass('has-error');
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

    // init basic info
    try {
        var survey = JSON.parse(localStorage.survey || '{}');
    } catch(err){
        var survey = {};
    }
    if ($('#create-order').size() > 0 && !$('#create-order').is('.one-key')) {
        for (name in survey) {
            var $field = $('#' + name);
            if ($field.length) {
                $field.find('span').text(survey[name].label);
            }
        }
        if (survey.designer) {
            $('#designer img').attr('src', survey.designer.avatar);
        }
        if (survey.message) {
            $('#message').text(survey.message.label);
        }
    }

    // create order
    $('#create-order-btn').click(function(){
        if ($('#address-edit-panel').is(':visible')) {
            alert('请先保存配送信息');
            return;
        }
        try {
            var survey = JSON.parse(localStorage.survey || '{}');
        } catch(err){
            var survey = {};
        }
        var $btn = $(this);
        $btn.button('loading');
        var data = {
            age_group: survey.age.value,
            clothing_size: survey.clothing_size.value,
            color: survey.color.value,
            preferred_designer: survey.designer.value,
            height: survey.height.value,
            pants_size: survey.pants_size.value,
            pants_style: survey.pants_style.value,
            price_group: survey.price.value,
            message: survey.message.value,
            shoe_size: survey.shoe_size.value,
            situation: survey.situation.value,
            style: survey.style.value,
            weight: survey.weight.value,
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

    $('#confirm-selection-btn').click(function(){
        if ($(this).is('.loading')) return; else $(this).addClass('loading');
        if ($('.clothing.selected').size() == 0) {
            alert('您忘记选择衣服了');
            return;
        }
        var ids = [];
        $('.clothing.selected').each(function(){
            ids.push($(this).data('id'));
        });
        location.href = $(this).data('url') + '?ids=' + ids.join(',');
    });

    $('.return-btn').click(function(){
        $('#return').modal({show: true});
        $('#return .submit-return-btn').data('url', $(this).data('url'));
    });
    $('#return .submit-return-btn').click(function(){
        var $btn = $(this);
        var express_provider = $('#express_provider').val();
        var express_code = $('#express_code').val();
        var reason = $('#reason').val();
        if (!express_provider || express_code.length < 6) {
            alert('请输入正确的快递信息');
            return;
        }
        if (reason.length < 3) {
            alert('请提供退款原因');
            return;
        }
        $btn.button('loading');
         $.ajax({
             url: $btn.data('url'),
             type: 'post',
             dataType: 'json',
             data: {
                 express_provider: express_provider,
                 express_code: express_code,
                 reason: reason,
                 csrfmiddlewaretoken: get_cookie('csrftoken')
             },
             success: function(data) {
                 if (data.success) {
                     location.href = location.href;
                 }
              }
         }).always(function () {
            $btn.button('reset');
        });
    });

    function update_design_price() {
        var total_price = 0;
        $('.design').each(function(){
            var $design = $(this);
            var design_price = 0;
            $('.clothing.selected', $design).each(function() {
                design_price += parseFloat($(this).data('price'));
            });
            $('.price span', $design).text(design_price);
            total_price += design_price;
        });
        $('#order-detail .total_price').text(total_price);
    }

    $('#order-detail .clothings .clothing .zoom').click(function(evt){
        evt.stopPropagation();
    });

    $('#order-detail .clothings .clothing:not(.readonly)').click(function(){
        var $design = $(this).parents('.design');
        if ($(this).is('.selected')) {
            $(this).removeClass('selected');
            update_design_price($design);
        } else {
            $(this).addClass('selected');
            update_design_price($design);
        }
    });
    update_design_price();
});
