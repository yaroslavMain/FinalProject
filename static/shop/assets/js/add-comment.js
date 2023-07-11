$('form#comment').on('submit', function (e) {
    e.preventDefault()
    let token = localStorage.getItem('access_token')
    if (token) {
        token = JSON.parse(token)
        console.log(token)
        $.ajax({
            url: '/api/comment',
            contentType: 'application/json',
            dataType: 'json',
            method: 'post',
            headers: {
                Authorization: `${token.token_type} ${token.access_token}`
            },
            data: JSON.stringify({
                body: this.body.value,
                name: this.name.value,
                role: this.role.value,
            }),
        }).done(function (data) {
            document.querySelector('input#body').value = ''
            document.querySelector('input#role').value = ''
        })
    }
})