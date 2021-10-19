var lowerizers = document.getElementsByClassName('lowerize');

    for(i=0; i<upperizers.length; i++){
        lowerizers[i].addEventListener('click', function (){
            var productId = this.dataset.id;


        $.ajax({
         type: 'POST',
         dataType: 'json',
         url: '/order/substract/',
         headers: {
            'X-CSRFToken': csrftoken,
         },
         data: {
             productId: productId,
             action: 'substract',
         },
         success: function (json){
             if (json.qty <= 0){
                 $("#" + productId).remove();
             } else{
              document.getElementById("order-item-count-num" + productId).innerHTML = json.qty
             }
         },
         error: function (xhr, errmsg, err) {
         }
        });
        })}