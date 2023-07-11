function renderProductPreview(product, querySelector) {
    document.querySelector(querySelector).innerHTML += [
       `<div class="col-md-4 col-sm-6" style="padding: 0 10px;">`,
            `<span class="product-item">`,
                `<img src="/media/${product.image}" class="img-fluid product-thumbnail">`,
                `<h3 class="product-title">${product.name}</h3>`,
                `<strong class="product-price">$ ${product.price}</strong>`,
                `<a onclick="shop(event, ${product.id})" class="icon-cross wishlist" href="#">`,
                    `<img src="/static/shop/assets/images/cross.svg" class="img-fluid">`,
                `</a>`,
            `</span>`,
        `</div>`,
        ].join('\n')
    }

$(document).ready(function () {
    $.ajax(
        {
            url: '/api/product',
            contentType: 'application/json',
            dataType: 'json',
            method: 'get'
        }
    ).done(function (data) {
        document.querySelector('div#shop-content').innerHTML = ''
        for (let i = 0; i < data.length; i++) {
            renderProductPreview(data[i], 'div#shop-content')
        }
    })
})


$('form#search').on('submit', function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/product',
            contentType: 'application/json',
            dataType: 'json',
            method: 'get',
            data: {
                q: this.q.value,
            }
        }
    ).done(function (data) {
        document.querySelector('div#shop-content').innerHTML = ''
        for (let i = 0; i < data.length; i++) {
            renderProductPreview(data[i], 'div#shop-content')
        }
    })
})


$('a#clear').click(function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/product',
            contentType: 'application/json',
            dataType: 'json',
            method: 'get'
        }
    ).done(function (data) {
        document.querySelector('div#shop-content').innerHTML = ''
        document.querySelector('input#q').value = ''
        for (let i = 0; i < data.length; i++) {
            renderProductPreview(data[i], 'div#shop-content')
        }
    })
})

function shop(e, product_id) {
    e.preventDefault()
    let token = localStorage.getItem('access_token')
    if (token) {
        token = JSON.parse(token)
        $.ajax(
            {
                url: '/api/wishlist?product_id=' + product_id,
                contentType: 'application/json',
                dataType: 'json',
                method: 'post',
                headers: {
                    Authorization: `${token.token_type} ${token.access_token}`
                },
                success: function (data) {
                    console.log('Добавлено!')
                },
                error: function (error) {
                    window.location.href = '/login'
                }
            }
        )
    }
}
