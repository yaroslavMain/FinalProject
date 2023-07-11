$('form#login-form').on('submit', function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/login',
            contentType: 'application/json',
            dataType: 'json',
            method: 'post',
            data: JSON.stringify(
                {
                    email: this.email.value,
                    password: this.password.value
                }
            ),
            success: function (data) {
//                document.querySelector('div.status').innerHTML = 'done'
                localStorage.setItem('access_token', JSON.stringify(data))
                window.location.href = '/shop'
            },
            error: function (data) {
                if (data.responseJSON.detail) {
                    document.querySelector('div.status').innerHTML = data.responseJSON.detail
                }
            }
        }
    )
})