let add_urls = document.getElementsByClassName('add-to-cart');

for(i=0; i<add_urls.length; i++){
    add_urls[i].addEventListener('click', function (){
        let productId = this.dataset.id;
        let action = this.dataset.action

        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: action,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                product_id: productId,
            },
            success: function (json){
                document.getElementById("order-item-count-num" + productId).innerHTML = json.qty
                document.getElementById("price" + productId).innerHTML = json.price + "$"
                document.getElementById("subtotal").innerHTML = json.subtotal;
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })}
