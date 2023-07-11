$('form#register-form').on('submit', function (e) {
    e.preventDefault()
    $.ajax(
        {
            url: '/api/register',
            contentType: 'application/json',
            dataType: 'json',
            method: 'post',
            data: JSON.stringify(
                {
                    name: this.name.value,
                    email: this.email.value,
                    password: this.password.value
                }
            ),
            success: function (data) {
                window.location.href = '/login'
            },
            error: function (data) {
              console.log(data)
                document.querySelector('div.status').innerHTML = 'ERROR'
            }
        }
    )
})