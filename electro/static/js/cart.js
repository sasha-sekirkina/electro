$(document).on('click', '#add_to_cart', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "cart:cart_add" %}',
        data: {
            productid: $('#add_to_cart').val(),
            productqty: $('#select option:selected').val(),
            csrfmiddlewaretoken: "{{csrf_token}}",
            action: 'post'
        },
        success: function (json) {
            document.getElementById("basket-qty").innerHTML = json.qty
        },
        error: function (xhr, errmsg, err) {}
    });
})
