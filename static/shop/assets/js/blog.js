function renderBlogPreview(article, querySelector) {
    document.querySelector(querySelector).innerHTML += [
            `<div class="col-12 col-sm-6 col-md-4 mb-5" style="padding: 0 10px;">`,
						`<div class="post-entry">`,
							`<a href="/article/${article.slug}" class="post-thumbnail">`,
							    `<img src="/media/${article.image}" alt="Image" class="img-fluid">`,
							`</a>`,
							`<div class="post-content-entry">`,
								`<h3><a href="#">${article.name}</a></h3>`,
								`<div class="meta">`,
									`<span>on <a href="#">${article.date_publish}</a></span>`,
								`</div>`,
							`</div>`,
						`</div>`,
					`</div>`,
        ].join('\n')
    }


$(document).ready(function () {
    $.ajax(
        {
            url: '/api/article',
            contentType: 'application/json',
            dataType: 'json',
            method: 'get',
        }
    ).done(function (data) {
        console.log(data)
        document.querySelector('div#blog-content').innerHTML = ''
        for (let i = 0; i < data.length; i++) {
            renderBlogPreview(data[i], 'div#blog-content')
        }
    })
})

$('a.nav-item').click(function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/article',
            data: {
                category_id: this.id,
            },
            contentType: 'application/json',
            dataType: 'json',
            method: 'get'
        }
    ).done(function (data) {
        document.querySelector('div#blog-content').innerHTML = ''
        for (let i = 0; i < data.length; i++) {
            renderBlogPreview(data[i], 'div#blog-content')
        }
    })
})


$('form#search').on('submit', function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/article',
            data: {
                q: this.q.value,
            },
            contentType: 'application/json',
            dataType: 'json',
            method: 'get',
        }
    ).done(function (data) {
        document.querySelector('div#blog-content').innerHTML = ''
        for (let i = 0; i < data.length; i++) {
            renderBlogPreview(data[i], 'div#blog-content')
        }
    })
})


$('a#clear').click(function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/article',
            contentType: 'application/json',
            dataType: 'json',
            method: 'get',
        }
    ).done(function (data) {
        document.querySelector('div#blog-content').innerHTML = ''
        document.querySelector('input#q').value = ''
        for (let i = 0; i < data.length; i++) {
            renderBlogPreview(data[i], 'div#blog-content')
        }
    })
})
