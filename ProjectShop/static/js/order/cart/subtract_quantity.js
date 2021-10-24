var subtract_hrefs = document.getElementsByClassName('subtract-from-cart');

    for(i=0; i<subtract_hrefs.length; i++){
        subtract_hrefs[i].addEventListener('click', function (){
            let productId = this.dataset.id;
            let action = this.dataset.action;

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
                 if (json.qty <= 0){
                     $("#" + productId).remove();
                 } else{
                  document.getElementById("order-item-count-num" + productId).innerHTML = json.qty;
                  document.getElementById("price" + productId).innerHTML = json.price + "$";
                 }
             },
             error: function (xhr, errmsg, err) {
             }
            });
        })}
