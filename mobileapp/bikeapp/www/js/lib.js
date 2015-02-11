// Console log helper
function _l(msg){
    if (typeof console == "object") {
        console.log(msg);
    }
    LE.log(platform+':'+msg);
}

// Set value helper
function _set(key, v){
    _l('setting:' + key + ' to ' + v);
    if (v == null) {
        window.localStorage.removeItem(key);
    }
    else {
        window.localStorage.setItem(key, v);
    }
    return;
}

// Get value helper
function _get(key) {
    var ret = window.localStorage.getItem(key);
    _l('getting:' + key + ' as ' + ret);
    if (ret == 'null' | ret == 'NaN'){
        return null;
    }
    return ret;
}

// Set data helper
function _setdict(key, v){
    if (v == null) {
        window.localStorage.removeItem(key);
    }
    else {
        window.localStorage.setItem(key, JSON.stringify(v));
    }
}

// Get data helper
function _getdict(key) {
    var ret = window.localStorage.getItem(key);
    if (ret != null){
        return JSON.parse(ret);
    }
    return [];
}

// API request
function _req(params){
    var headers = {};
    if (params['url'] != 'auth'){
        headers = {"Authorization": 'Token ' + _get('token')}
    }
    params['headers'] = headers;
    params['crossDomain'] = true;
    params['url'] = config['apiUrl'] + params['url'];
    params['dataType'] = 'json';
    params['async'] = false;
    $.ajax(params);
}

function check_login() {
    if (_get('token') == null){
        logout();
    }
}

function logout() {
    _set('token', null);
    _set('cur_appt', null);
    _set('cur_app_rider_count', null);
    _set('cur_app_total_time', null);
    clearInterval(timerInterval);
    clearInterval(surveyInterval);
    window.location.replace('');
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
    _l('posting to /auth ' + username + ':' + password);
    $.ajax({
        type: "POST",
        url: config['apiUrl'] + 'auth?z=' + jQuery.now(),
        crossDomain: true,
        /*async: false,*/
        cache: false,
        data: {username:username, password:password},
        success: function (data){
            _l('success from auth ' + data);
            if (data.token){
                _l('logged in.  redir to #home');
                _set('token', data.token);
                window.location.replace('#home');
            }
            else {
                $('#err-login').html(data.message).show();
            }
        },
        error: function (data, status, err){
            _l('login error data: ' + data + ' status:' + data.status + ' err:' + err);
            _l('login error token: ' + data.token);
            $('#login_error').html('Invalid login').show();
        }
    });
}


function guid() {
    function _p8(s) {
        var p = (Math.random().toString(16)+"000000000").substr(2,8);
        return s ? "-" + p.substr(0,4) + "-" + p.substr(4,4) : p ;
    }
    return _p8() + _p8(true) + _p8(true) + _p8();
}

function boxClick(d){
    //_l('a');
    // Clear any selected value
    var metric = $(d).attr('name');
    var value = $(d).val();
    _l('clicked value:' + metric + ' : ' + value);
    //$('.'+metric).css('background-color','#FFF');

    // Select this one
    //$(d).css('background-color','#ddf');

    // Update survey value
    //survey[metric] = String(d.id).replace(metric+'_','');
    survey[metric] = String(value);
    // Check if done
    tryComplete();
}

function tryComplete(){
    var complete = true;

    metric_len = Object.keys(survey).length;
    _l('Survey key len:' + metric_len);

    // If any metric is not filled out break
    for (i=0; i < Object.keys(survey).length; i++){

        _l(Object.keys(survey)[i] + ' = ' + survey[Object.keys(survey)[i]]);

        if (survey[Object.keys(survey)[i]] == null){
            complete = false;
            //break;
        }
    }

    _l('tryComplete: ' + complete);

    if (complete == true) {
        $('#btn_save').prop('disabled', false);
    } else {
        $('#btn_save').prop('disabled', true);
    }
    /*
    if (complete == true){
        saveSurvey();
        window.scrollTo(0, 0);
        // TODO: Reload survey
        for (i=0; i < Object.keys(survey).length; i++){
            survey[Object.keys(survey)[i]] = null;
        }
        $('.box').css('background-color', '#FFF');
        _l('saved');
    }
    */
}

function showPage(p){
    $('.page').hide();
    $('#page'+p).show();
}

function clearSurveys(){
    _setdict('surveys_to_save', null);
}

function pause(){
    // Unpause
    if (paused){
        paused = false;
        $('#btn_pause').prop('disabled', false);
        $('#btn_end').prop('disabled', false);
        $('#btn_pause').val('Pause');
        $('.rec_content').show();
        $('#events_div').show();
    }
    // Pause
    else {
        paused = true;
        pause_start = new Date().getTime();
        $('#btn_pause').prop('disabled', false);
        $('#btn_end').prop('disabled', true);
        $('#btn_pause').val('Unpause');
        $('.rec_content').hide();
        $('#events_div').hide();
    }
    $('#btn_pause').blur();
}

function updateTime(){
    if (paused) {return;}

    // Add 1000 ms to total time
    total_time += 1000;
    _set('cur_app_total_time', total_time);

    var diff = (config['session_len'] * 6000 - 1) - total_time;
    var minutes = Math.floor(diff / 60000);
    var seconds = String(Math.round(diff / 1000));
    seconds = seconds % 60;

    // Check if the session is done recording
    if (diff < 0){
        clearInterval(surveyInterval);
        clearInterval(timerInterval);
        var appt = _get('cur_appt');
        endSession(appt);
        //window.location.replace('#done/'+appt);
    }
    else {
        $('#timer').html(String(minutes)+':'+String(seconds)+' remaining');
    }

    /*
    start = _get('start_time');
    var now = new Date().getTime();
    var diff = (config['session_len'] * 6000 - 1) - (now - start);
    var minutes = Math.floor(diff / 60000);
    var seconds = String(Math.round(diff / 1000));

    seconds = seconds % 60;

    // Check if the session is done recording
    if (diff < 0){
        clearInterval(surveyInterval);
        clearInterval(timerInterval);
        var appt = _get('cur_appt');
        endSession(appt);
        //window.location.replace('#done/'+appt);
    }
    else {
        $('#timer').html(String(minutes)+':'+String(seconds)+' remaining');
    }
    */
}

function saveEvent(id){
    // Generate unique id for event
    //var guid = guid();

    // Get the unposted array
    s = _getdict('events_to_save');
    if (s == null){
        s = [];
    }

    // Add this survey to the array
    data = {'event_id': id, 'guid': guid()};
    s.push(data);

    // Push the array back to the queue
    _l('Adding survey to queue, total len=' + s.length);
    _setdict('events_to_save', s);

    // Increase count
    event_count[id]++;
    $('#eventcount_' + id).fadeOut(500, function() {
        $(this).html(event_count[id]).fadeIn(1000);
        $('#btn_event_' + id).blur();
    });
}

function saveSurvey(){
    // tryComplete first
    if (tryComplete() == false){
        return;
    }

    var data = {};

    // Get the time taken
    var time_taken = new Date().getTime() - start;

    // Generate unique id for survey
    data['guid'] = guid();

    // Build the data to save
    for (i=0; i < Object.keys(survey).length; i++){
        data[Object.keys(survey)[i]] = survey[Object.keys(survey)[i]];
    }

    // Add time related info
    data['time_taken'] = time_taken;
    data['timestamp'] = new Date().getTime();

    // Get the unposted array
    s = _getdict('surveys_to_save');
    if (s == null){
        s = [];
    }
    // Add this survey to the array
    s.push(data);

    // Push the array back to the queue
    _l('Adding survey to queue, total len=' + s.length);
    _setdict('surveys_to_save', s);

    // Clear all the buttons and what not
    $(':radio').prop('checked', false);
    $('.btn-group label').removeClass('active');

    // Clear internal survey value array
    for (i=0; i < Object.keys(survey).length; i++){
        _l('survey key : ' + Object.keys(survey)[i]);
        var k = Object.keys(survey)[i];
        // TODO - update to respect default values, not hardcode
        if (k != 'sidewalk' && k != 'wrong_way' && k != 'gender') {
            _l('null out key : ' + k);
            survey[Object.keys(survey)[i]] = null;
        }
    }

    // Set all defaults back
    $('input[data-default]').prop('checked', true);
    $('input[data-default]').parent().addClass('active');
    $('#btn_save').prop('disabled', true);

    // Increase count
    rider_count = rider_count + 1;
    _set('cur_app_rider_count', rider_count);
    $('#total_riders').html(rider_count);
    $('#riders_outer').fadeOut(500).fadeIn(500);

    // Restart the timer
    start = new Date().getTime();
}

function postSurveys(){
    // Check for unposted surveys and events
    surveys = _getdict('surveys_to_save');
    events = _getdict('events_to_save');

    //    if (surveys == null || surveys.length == 0) {return;}
    if (events.length == 0 && surveys.length == 0) {return;}


    _l(surveys.length + ' surveys to post');
    if (surveys.length > 0){
        // Pop a survey off the queue
        var survey = surveys.pop();
        _l('Posting survey data: ' + survey);

        // Resave the queue
        _setdict('surveys_to_save', surveys);

        // Post the survey
        var params = {'type': 'POST'};
        params['url'] = 'session/' + _get('cur_appt') + '/survey/';
        params['data'] = survey;
        _req(params);
    }

    // TODO - Test all this!
    _l(events.length + ' events to post');
    if (events.length > 0){
        // Pop an evetn off the queue
        var event = events.pop();
        _l('Posting event data: ' + event);

        // Resave the queue
        _setdict('events_to_save', events);

        // Post the survey
        var params = {'type': 'POST'};
        params['url'] = 'session/' + _get('cur_appt') + '/event/';
        params['data'] = event;
        _req(params);
    }

}


function getOrg(id){
    var d = _getdict('data');
    for (i=0; i<d['membership_set'].length; i++){
        if (d['membership_set'][i].organization.id == id){
            return d['membership_set'][i].organization;
        }
    }
}

function getAppointment(id) {
    var d = _getdict('data');
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
            _setdict('data',data);
            d = data;
        }
    });
    return d;
}

function startSession(id){
    // API call to start
    if (_get('token')){
        $.ajax
        ({
            type: "POST",
            url: config['apiUrl'] + 'session/'+id+'/start',
            async: false,
            crossDomain: true,
            headers: {"Authorization": 'Token ' + _get('token')},
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

function endSession(appt){
    // API call to end session
    id = _get('cur_appt');
    if (_get('token')){
        if (confirm('Confirm end session?')) {
            $.ajax
            ({
                type: "POST",
                url: config['apiUrl'] + 'session/'+id+'/end',
                /*async: false,*/
                crossDomain: true,
                data: {'total_time': total_time, 'total_paused': total_paused, 'longest_pause': longest_pause, 'total_away': total_away},
                headers: {"Authorization": 'Token ' + _get('token')},
                success: function (data){
                    // Load the recording page
                    _set('cur_appt', null);
                    _set('cur_app_total_time', null);
                    _set('cur_app_rider_count', 0);
                    clearInterval(timerInterval);
                    clearInterval(surveyInterval);
                    window.location.replace('#done/'+id);
                },
                error: function(data){
                    return;
                }
            });
        }
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