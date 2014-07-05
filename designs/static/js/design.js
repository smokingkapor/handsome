$(document).ready(function(){
    // ajax upload full body shot
    $('#fileupload').fileupload({
        url: $(this).data('url'),
        dataType: 'json',
        disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
        maxFileSize: 5000000,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        done: function (e, data) {
            if (data.result.success) {
                $('<img height="280">').data('filename', data.result.filename).attr('src', data.result.path).appendTo($('#photos'));
                update_photos_field();
            }
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            if (progress == 100) {
                $('#progress').text('');
            } else {
                $('#progress').text(progress + '%');
            }
        }
    }).prop('disabled', !$.support.fileInput).parent().addClass($.support.fileInput ? undefined : 'disabled');

    // update hidden photos field
    function update_photos_field() {
        var photos = [];
        $('#photos img').each(function(){
            photos.push($(this).data('filename'));
        });
        $('#design-photos').val(photos.join(';'));
    }

    // create design
    $('#create-design-btn').click(function(){
        var $btn = $(this);
        $btn.button('loading');
        $.ajax({
            url: $btn.data('url'),
            type: 'post',
            dataType: 'json',
            data: {
                comment: $('#comment').val(),
                photos: $('#design-photos').val(),
                selected_clothings: $('#selected-clothings-input').val(),
                total_price: $('#total_price').val(),
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

    // search clothings by category
    $('#category-select').change(function(){
        $('#search-clothing-input').val('');
        $('#clothing-list tbody').empty();
        search_clothing($(this).val());
    });

    // search clothings by category and name
    $('#search-clothing-input').change(function(){
        search_clothing($('#category-select').val(), $(this).val());
    });
    $('#search-clothing-input').keydown(function(evt){
        if (evt.keyCode == 13) {
            search_clothing($('#category-select').val(), $(this).val());
            return false;
        }
    });

    // search clothing
    function search_clothing(category, name, page) {
        $.ajax({
            url: '/clothings/search/',
            data: {category: category, name: name, page: page},
            success: function(data) {
                if (!page) {
                    $('#clothing-list tbody').empty();
                }
                var clothings = [];
                $.each(data, function(i, item) {
                    var clothing = item.fields;
                    clothing.pk = item.pk;
                    var colors = [];
                    var sizes =[];
                    $.each(clothing.colors.split(' '), function(i, color){
                        colors.push({pk: item.pk, color: color});
                    });
                    $.each(clothing.sizes.split(' '), function(i, size){
                        sizes.push({pk: item.pk, size: size});
                    });
                    clothing.popover_content = new Ractive({
                        template:'#select-popover-template',
                        data: {colors: colors, sizes: sizes, pk: item.pk}
                    }).toHTML();
                    clothings.push(clothing);
                });
                var ractive = new Ractive({
                    el: '#clothing-list tbody',
                    template: '#clothing-template',
                    data: {clothings: clothings},
                    complete: function() {
                        $.each(data, function(i, item) {
                            $('#clothing-' + item.pk).data('clothing', item);
                        });
                        $('.image-tooltip').tooltip();
                        $('.select-popover-btn').popover();
                    }
                });
            }
        });
    }

    // select clothing
    $(document).on('click', '.select-btn', function(){
        var id = $(this).data('id');
        var $select_popover = $(this).parents('.select-popover');
        var color = $('input:checked[name="color_' + id + '"]').val();
        var size = $('input:checked[name="size_' + id + '"]').val();
        if (!color || !size) {
            alert('请选择颜色和尺寸！');
            return;
        } else {
            $('#select-popover-btn-' + id).popover('hide');
        }
        if ($('#selected-clothing-' + id).size() > 0) {
            alert('该服装已添加!');
            return;
        }
        var clothing = $('#clothing-'+id).data('clothing');
        var selected_clothing = clothing.fields;
        selected_clothing.pk = clothing.pk;
        selected_clothing.color = color;
        selected_clothing.size = size;
        var ractive = new Ractive({
            template: '#selected-clothing-template',
            data: clothing.fields
        });
        $('#selected-clothings').append(ractive.toHTML());
        update_selected_clothing_ids();
    });

    $(document).on('click', '.close-popover', function(){
        $('#select-popover-btn-' + $(this).data('id')).popover('hide');
    });

    // remove selected clothing
    $(document).on('click', '.clothing-remove-btn', function(){
        $(this).parents('.selected-clothing').remove();
        update_selected_clothing_ids();
    });

    // update selected clothing ids field
    function update_selected_clothing_ids() {
        var selected_clothings = [];
        $('.selected-clothing').each(function(){
            selected_clothings.push({
                id: $(this).data('id'),
                color: $(this).data('color'),
                size: $(this).data('size'),
            });
        });
        $('#selected-clothings-input').val(JSON.stringify(selected_clothings));
    }
});
