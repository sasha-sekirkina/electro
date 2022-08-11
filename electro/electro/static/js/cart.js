    $(document).on('click', '#add_to_cart', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '{% url "cart:add_to_cart" %}',
            data: {
                productid: $('#add_to_cart').val(),
                csrfmiddlewaretoken: "{{csrf_token}}",
                action: 'post'
            },
            success: function (json) {
            },
            error: function (xhr, errmsg, err) {}
        });
    })