
$(function(){
    $.ajax({
        type: "POST",
        url: remove_from_cart_url,
        data: {'item-slug':item_slug},
        headers:{'X-CSRFToken':csrftoken},
        success: function (response) {
            if(response.success) {
                console.log("item removed")
                $("#"+item_slug).fadeOut(300,function(){
                    this.remove();
                    data=response;
                    items_in_cart=parseInt($('#items-in-cart').text());
                    $('#items-in-cart').text(items_in_cart-1);
                    if(items_in_cart-1<=0){
                        $('.cart-container').remove();
                        $('.container').append(create_cart_is_empty_html);
                    } else {

                        $('.total-payable').text(data['total-payable']);
                        $('#proceed-to-pay-btn span').text(data['total-payable']);
                        $('#total-actual-price').text(data['total-actual-price']);
                        $('#total-discount-price').text(data['total-discount-price']);
                        $('#total-shipping-price').text(data['total-shipping-price']);
                        $('#total-payable').text(data['total-payable']);
                    }
                 });

            }
            },
        error: function (response) {
            alert(response);
        }

    });
});