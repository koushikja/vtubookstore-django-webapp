function add_to_cart(book_id){
    console.log(book_id);
    let json_data = {}
    json_data["quantity"] = $(`#quantity-${book_id}`).val();
    json_data["book_id"] = book_id;
    json_data["csrfmiddlewaretoken"] = $('[name="csrfmiddlewaretoken"]').val();
    console.log(json_data)
    $.ajax({
        url: `/addtocart/${book_id}/`,
        method:"POST",
        type: "application/json",
        data: json_data,
        success: function(response){
            alert(response.message)
        }
    })
}