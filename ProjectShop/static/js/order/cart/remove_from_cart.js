let deleteIcons = document.getElementsByClassName('item-delete');


for (let element of deleteIcons){
    element.addEventListener('click', function (){

        let productId = this.dataset.id;
        let action = this.dataset.action;

        $.ajax({
            type: 'POST',
            url: '/order/remove/',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                productId: productId,
                action: action,
            },
            success: function (json){
                $("#" + productId).remove();
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })
}