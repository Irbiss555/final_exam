let baseUrl = 'http://127.0.0.1:8000/'

$(document).ready(
    function () {
        $('#btn-sing-out').click(
            function (e) {
                $.ajax(
                    {
                        method: 'POST',
                        url: `${baseUrl}api/logout/`,
                        headers: {Authorization: 'Token ' + localStorage.getItem('auth_token')},
                        success: function (response) {
                            console.log(response)
                        },
                        error: function (response) {
                            console.log('error')
                        }
                    }
                )
            }
        )
        $('#sign-in-btn').click(
            function (e) {
                e.preventDefault()
                let form_element = $('#login-form')
                let inputs = $(form_element).serializeArray()
                let form = {}
                inputs.forEach(function (value) {
                    if (value['name'] === 'username') {
                        form.username = value['value']
                    } else if (value['name'] === 'password') {
                        form.password = value['value']
                    }
                })
                $.ajax(
                    {
                        method: 'POST',
                        url: `${baseUrl}api/login/`,
                        data: JSON.stringify({username: form.username, password: form.password}),
                        contentType: 'application/json',
                        success: function (response) {
                            localStorage.setItem('auth_token', response.token)
                        },
                        error: function (response) {
                            console.log(response)
                        }
                    }
                ).then(form_element.submit())
            })
        $('#btn-moderation-valid').click(
            function (e) {
                e.preventDefault()
                $.ajax({
                        method: 'POST',
                        url: baseUrl + `api/publication/${$(e.currentTarget).data('id')}/valid/`,
                        headers: {Authorization: 'Token ' + localStorage.getItem('auth_token')},
                        success: function (response) {
                            let modText = $(`#moderation-text`)
                            modText.text(`${response.moderation_status}`)
                            modText.removeClass('text-danger text-primary')
                            modText.addClass('text-success')
                        },
                        error: function (response) {
                            console.log(response)
                        }
                    }
                )
            }
        )
        $('#btn-moderation-invalid').click(
            function (e) {
                e.preventDefault()
                $.ajax({
                        method: 'POST',
                        url: baseUrl + `api/publication/${$(e.currentTarget).data('id')}/invalid/`,
                        headers: {Authorization: 'Token ' + localStorage.getItem('auth_token')},
                        success: function (response) {
                            let modText = $(`#moderation-text`)
                            modText.text(`${response.moderation_status}`)
                            modText.removeClass('text-success text-primary')
                            modText.addClass('text-danger')
                            console.log(response)
                        },
                        error: function (response) {
                            console.log(response)
                        }
                    }
                )
            }
        )
    }
)