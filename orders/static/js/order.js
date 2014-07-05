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

    // load price and personal requirement from local storage
    var survey = JSON.parse(localStorage.survey);
    if ($('#create-order').size() > 0) {
        $('#style .content span').text(survey.style.label).data('value', survey.style.value);
        $('#style form select').val(survey.style.value);
        $('#age .content span').text(survey.age.label).data('value', survey.age.value);
        $('#age form select').val(survey.age.value);
        $('#price .content span').text(survey.price.label).data('value', survey.price.value);
        $('#price form select').val(survey.price.value);
        $('#designer .content span').text(survey.designer.label).data('value', survey.designer.value);
        $('#designer .content img').attr('src', survey.designer.avatar);
        $('#designer form select').val(survey.designer.value);
    }

    $('.edit-requirement-btn').click(function(){
        var $content = $(this).parents('.content');
        var $form = $(this).parents('td').find('form');
        $form.removeClass('hidden');
        $content.addClass('hidden');
    });

    $('.cancel-edit-btn').click(function(){
        var $form = $(this).parents('form');
        var $content = $(this).parents('td').find('.content');
        $form.addClass('hidden');
        $content.removeClass('hidden');
    });

    $('.save-btn').click(function(){
        var $form = $(this).parents('form');
        var $content = $(this).parents('td').find('.content');
        $form.addClass('hidden');
        $content.removeClass('hidden');

        var $selected_option = $('option:selected', $form);
        $('span', $content).text($selected_option.text()).data('value', $selected_option.val());
        if ($(this).parents('td').attr('id') == 'designer') {
            $('img', $content).attr('src', $selected_option.data('avatar'));
        }
    });

    // create order
    $('#create-order-btn').click(function(){
        if ($('#address-edit-panel').is(':visible')) {
            alert('请先保存配送信息');
            return;
        }
        var $btn = $(this);
        $btn.button('loading');
        var data = {
            price_group: parseInt($('#price .content span').data('value')),
            message: $('#requirement').val() || '',
            preferred_designer: $('#designer .content span').data('value'),
            style: $('#style .content span').data('value'),
            age_group: $('#age .content span').data('value'),
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
});
