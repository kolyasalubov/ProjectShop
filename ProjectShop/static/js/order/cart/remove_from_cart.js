let deleteIcons = document.getElementsByClassName('item-delete');


for (let element of deleteIcons){
    element.addEventListener('click', function (){

        let productId = this.dataset.id;
        let action = this.dataset.action;

        $.ajax({
            type: 'POST',
            url: action,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                productId: productId,
            },
            success: function (json){
                $("#" + productId).remove();
                document.getElementById("subtotal").innerHTML = json.subtotal;
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })
}
