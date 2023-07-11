$('form#form').on('submit', function (e) {
    e.preventDefault()
    let token = localStorage.getItem('access_token')
    if (token) {
        token = JSON.parse(token)
        $.ajax(
            {
                url: '/api/comment_article?article_id=' + this.btn.name,
                method: 'post',
                contentType: 'application/json',
                dataType: 'json',
                headers: {
                    Authorization: `${token.token_type} ${token.access_token}`
                },
                data: JSON.stringify({
                    comment: this.inputcomment.value,
                }),
            }
        ).done(function (data) {
            document.querySelector('div#comments').innerHTML += [`<ul><li>${ data.comment } : ${ data.date_created }</li></ul>`]
        })
    }
})