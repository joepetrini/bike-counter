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

// API request
function _req(params){
    var headers = {};
    if (params['url'] != 'auth'){
        headers = {"Authorization": 'Token ' + _g('token')}
    }
    params['headers'] = headers;
    params['crossDomain'] = true;
    params['url'] = config['apiUrl'] + params['url'];
    params['dataType'] = 'json';
    params['async'] = false;
    $.ajax(params);
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
                window.location.replace('#home');
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


function getOrg(id){
    var d = _gd('data');
    for (i=0; i<d['membership_set'].length; i++){
        if (d['membership_set'][i].organization.id == id){
            return d['membership_set'][i].organization;
        }
    }
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
    _req({type: "GET", url: 'me',
        success: function (data){
            _sd('data',data);
            d = data;
        }
    });
    return d;
}

function startSession(id){
    // API call to start
    if (_g('token')){
        $.ajax
        ({
            type: "POST",
            url: config['apiUrl'] + 'session/'+id+'/start',
            async: false,
            crossDomain: true,
            headers: {"Authorization": 'Token ' + _g('token')},
            success: function (data){
                // Load the recording page
                window.location.replace('#record/'+id);
            },
            error: function(data){
                return;
            }
        });
    }
}

function initializeMap(lat, long) {
    var mapOptions = {
        'center': new google.maps.LatLng(lat, long),
        'zoom': 15,
        'mapTypeId': google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    return map;
}