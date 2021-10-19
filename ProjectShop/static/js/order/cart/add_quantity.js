var upperizers = document.getElementsByClassName('upperize');

for(i=0; i<upperizers.length; i++){
    upperizers[i].addEventListener('click', function (){
        var productId = this.dataset.id;


        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/order/add/',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                productId: productId,
                action: 'post',
            },
            success: function (json){
                document.getElementById("order-item-count-num" + productId).innerHTML = json.qty
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })}


