// Set value helper
function _s(key, v){
    window.localStorage.setItem(key, v);
}

// Get value helper
function _g(key) {
    return window.localStorage.getItem(key);
}

// Set data helper
function _sd(key, v){
    window.localStorage.setItem(key, JSON.stringify(v));
}

// Get data helper
function _gd(key) {
    return JSON.parse(window.localStorage.getItem(key));
}

function login() {
    $('#err-login').hide();

    // Validate
    var username = $('#username').val();
    var password = $('#password').val();
    if (username == '' || password == '') {
        $('#err-login').html('Invalid username or password').show();
        return;
    }

    $.ajax({
        type: "POST",
        url: config['apiUrl'] + 'auth',
        crossDomain: true,
        data: {username:username, password:password},
        success: function (data){
            if (data.token){
                _s('token', data.token);
                //$("<a />").attr("href", '/#home').click();
                window.location.replace('/#home');
                //$('#a_home').click();
            }
            else {
                $('#err-login').html(data.message).show();
            }
        },
        error: function (data){
            $('#login_error').html('Invalid login').show();
        }
    });
}

function getAppointment(id) {
    var d = _gd('data');
    for (i=0; i<d['appointment_set'].length; i++){
        if (d['appointment_set'][i].id == id){
            return d['appointment_set'][i];
        }
    }
}

function getAppointments() {
    var d;
    if (_g('token')){
        $.ajax
        ({
            type: "GET",
            url: config['apiUrl'] + 'me',
            dataType: 'json',
            async: false,
            crossDomain: true,
            headers: {"Authorization": 'Token ' + _g('token')},
            success: function (data){
                _sd('data',data);
                d = data;
            }
        });
    }
    return d;
}