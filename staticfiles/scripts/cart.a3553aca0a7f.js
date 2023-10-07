// cart.js

$(document).ready(function() {
    const csrfToken = $("#csrf_token").val();

    function updateCart(itemId, newQuantity) {
        $.ajax({
            url: `/update_cart/${itemId}/${newQuantity}/`,  // URL you defined in urls.py
            type: "GET",
            dataType: "json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function(data) {
                // Update the quantity and total price in the HTML
                $(`#quantity-${itemId}`).text(data.quantity);
                $(`#price-${itemId}`).text('$' + data.total_price.toFixed(2));
                
                // Update the total items and total price at the top of the page
                $("#cart-item-count").text(data.cart_item_count);
                $("#cart-total-price").text('$' + data.cart_total_price.toFixed(2));
            },
            error: function(error) {
                console.error(error);
            }
        });
    }

    // Handle quantity increment and decrement
    $(".decrement-quantity, .increment-quantity").on("click", function() {
        const itemId = $(this).data("item-id");
        const quantityElement = $(`#quantity-${itemId}`);
        let quantity = parseInt(quantityElement.text());

        if ($(this).hasClass("decrement-quantity") && quantity > 0) {
            quantity--;
        } else if ($(this).hasClass("increment-quantity")) {
            quantity++;
        }

        quantityElement.text(quantity);
        updateCart(itemId, quantity);
    });
});
