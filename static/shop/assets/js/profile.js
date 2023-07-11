$(document).ready(function () {
    let token = localStorage.getItem('access_token')
    if (token) {
        token = JSON.parse(token)
        console.log(token)
        $.ajax({
            url: '/api/test',
            contentType: 'application/json',
            dataType: 'json',
            method: 'get',
            headers: {
                Authorization: `${token.token_type} ${token.access_token}`
            },
        }).done(function (data) {
            document.querySelector('h1#name').innerHTML = data.name
            document.querySelector('h1#email').innerHTML = data.email
            document.querySelector('h1#password').innerHTML = data.password
        })
    }
})