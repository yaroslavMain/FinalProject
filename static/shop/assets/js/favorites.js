function renderProductPreview(product, querySelector) {
    document.querySelector(querySelector).innerHTML += [
         `<tr id="${product.id}">`,
          `<td class="product-thumbnail">`,
            `<img src="/media/${product.image}" alt="Image" class="img-fluid">`,
          `</td>`,
          `<td class="product-name">`,
            `<h2 class="h5 text-black">${product.name}</h2>`,
          `</td>`,
          `<td>$ ${product.price}</td>`,
          `<td><a class="delete-product" onclick="favotite(event, ${product.id})" href="#">❌</a></td>`,
        `</tr>`,
    ].join('\n')
}



$(document).ready(function () {
    let token = localStorage.getItem('access_token')
    if (token) {
        token = JSON.parse(token)
        $.ajax(
            {
                url: '/api/wishlist',
                contentType: 'application/json',
                dataType: 'json',
                method: 'get',
                headers: {
                    Authorization: `${token.token_type} ${token.access_token}`
                },
                success: function(products_id) {
                    let url = '';
                    $.each(products_id, function(index, productId){
                      url += "products_id=" + productId;
                      if(index !== products_id.length - 1){
                        url += "&";
                      }
                    });
                    $.ajax(
                    {
                        url: '/api/product?' + url,
                        contentType: 'application/json',
                        dataType: 'json',
                        method: 'get',
                    }
                    )
                    .done(function (data) {
                        document.querySelector('tbody.content').innerHTML = ''
                        for (let i = 0; i < data.length; i++) {
                            renderProductPreview(data[i], 'tbody.content')
                        }
                    })

                },
                error: function (data) {
                    console.log(data)
                }
            }
        )
    }
})

function favotite(e, product_id) {
    e.preventDefault()
    let token = localStorage.getItem('access_token')
    if (token) {
        token = JSON.parse(token)
         $.ajax(
            {
                url: '/api/wishlist?product_id=' + product_id,
                method: 'delete',
                headers: {
                    Authorization: `${token.token_type} ${token.access_token}`
                },
                contentType: 'application/json',
                dataType: 'json',
            }
        ).done(function (data) {
            $('tr#' + data.product_id).remove();
        })
    }
}