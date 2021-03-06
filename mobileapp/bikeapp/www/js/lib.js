// Console log helper
function _l(msg){
    if (typeof console == "object") {
      //  console.log(msg);
    }
    LE.log(platform+':'+_get('username')+':'+msg);
}

// Vibrate helper
function _vib(){
    try {
        navigator.vibrate(100);
    }
    catch (err){
        _l(err);
    }
}

// Pad zeros
function _pad(num){
    return ("0000" + num).substr(-2,2);
}

//functions to toggle scroll capabilties as on the upcoming appts screen we need a scroll bar
function reloadScrollBars() {
   document.documentElement.style.overflow = 'auto';  // firefox, chrome
    document.body.scroll = "yes"; // ie only
}

function unloadScrollBars() {
    document.documentElement.style.overflow = 'hidden';  // firefox, chrome
    document.body.scroll = "no"; // ie only
}

// Wrapper for passing data to template
function _tdata(dict){
    dict['version'] = config.version;
    dict['is_superuser'] = _getdict('data').is_superuser;
    dict['config'] = config;
    return dict;
}

function _sel(b1, b2, key, val){
    b1 = document.getElementById(b1);
    b1.classList.add('active');
    b2 = document.getElementById(b2);
    b2.classList.remove('active');
    survey[key] = val;
    tryComplete();
}

// Set value helper
function _set(key, v){
    //_l('setting:' + key + ' to ' + v);
    if (v == null) {
        window.localStorage.removeItem(key);
    }
    else {
        window.localStorage.setItem(key, v);
    }
    return;
}

// Get value helper
function _get(key, defval) {
    defval = defval || null;
    var ret = window.localStorage.getItem(key);
    //_l('getting:' + key + ' as ' + ret);
    if (ret == null | ret == 'null' | ret == 'NaN'){
        return defval;
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

function change_api_url(url){
    _l('url: ' + url);
    _set('apiUrl', url);
    config['apiUrl'] = url;
    $('#api_url').html(url);
    window.location.replace('#admin');
    console.log("API version changed to - " +  config['apiUrl']);
}

function get_appt_signup_URL(){
    var current_API_URL =   _get('apiUrl');
    switch(current_API_URL){
        case 'https://127.0.0.1:1080/api/':
            return 'https://127.0.0.1:8001/phl-bike/home';
        case 'https://qa.bikecounts.com/api/':
            return 'https://qa.bikecounts.com/phl-bike/home';
        case 'https://www.bikecounts.com/api/':
            return 'https://www.bikecounts.com/phl-bike/home';
    }
    //console.log(theURL);

}

function check_login() {
    if (_get('token') == null){
        logout();
    }
}

function logout() {
    _set('token', null);
    _set('username', null);
    _set('cur_appt', null);
    _set('cur_app_rider_count', null);
    _set('cur_app_total_time', null);
    _set('local_appt_session_start', null);
    _set('expected_end_time', null);
    _setdict('event_counts', null);
    clearInterval(timerInterval);
    clearInterval(surveyInterval);
    window.location.replace('');
}

function login() {
    $('#err-login').hide();
    console.log("login is using - " + config['apiUrl'] );
    // Validate
    var username = $('#username').val();
    var password = $('#password').val();
    if (username == '' || password == '') {
        $('#err-login').html('Invalid username or password').show();
        return;
    }
    _set('username', username);
    _l('posting to /auth ' + username);
    $.ajax({
        type: "POST",
        url: config['apiUrl'] + 'auth?z=' + jQuery.now(),
        crossDomain: true,
        cache: false,
        data: {username:username, password:password},
        success: function (data){
            if (data.token){
                _l('logged in. redir to #home');
                _set('token', data.token);
                //window.location.replace('#home');
                window.location.replace('#upcoming');
            }
            else {
                $('#err-login').html(data.message).show();
            }
        },
        error: function (data, status, err){
            _l('login error data: ' + data + ' status:' + data.status + ' err:' + err);
            $('#err-login').html('Invalid login').show();
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

function middleClick(d){
    if ($('#'+ d.id).data('data-on') == 'Y'){
        $('#'+ d.id).data('data-on', 'N');
        // Rich switched these colors to what they are now on 12/22/15 as I think they were backwards from what the UX should be
        $('#'+ d.id).css('background-color','#b28585');
    }
    else {
        $('#'+ d.id).data('data-on', 'Y');
        $('#'+ d.id).css('background-color','#e05a31');
    }
}

function boxClick(d){
    // Clear any selected value
    var metric = $(d).attr('name');
    var value = $(d).val();

    //_l('clicked value:' + metric + ' : ' + value);
    //$('.'+metric).css('background-color','#FFF');

    // Select this one
    //$(d).css('background-color','#ddf');

    // Update survey value
    //survey[metric] = String(d.id).replace(metric+'_','');
    survey[metric] = String(value);

    // Check if done
    tryComplete();
    //$('#btn_save').prop('disabled', false);
}

function tryComplete(){
    var complete = true;

    metric_len = Object.keys(survey).length;

    // If any metric is not filled out break
    for (i=0; i < Object.keys(survey).length; i++){
        //_l(Object.keys(survey)[i] + ' = ' + survey[Object.keys(survey)[i]]);
        if (survey[Object.keys(survey)[i]] == null){
            complete = false;
            break;
        }
    }

    if (complete == true) {
        $('#btn_save').prop('disabled', false);
    } else {
        $('#btn_save').prop('disabled', true);
    }
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
        _set('current_pause', 0);
        $('#btn_pause').prop('disabled', false);
        $('#btn_end').prop('disabled', false);
        $('#btn_pause').val('Pause');
        $('.rec_content').show();
        $('#events_div').show();
        $('#checkbox_div').show();
        $('#innerLeft').show();
        $('#hidden_pause_timers').hide();
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
        $('#checkbox_div').hide();
        $('#innerLeft').hide();
        $('#hidden_pause_timers').show();
    }
    $('#btn_pause').blur();
}

function updateTime(){
    var now = new Date().getTime();
    if (paused) {
        current_pause = parseInt(_get('current_pause', 0));
        total_pause = parseInt(_get('total_pause', 0));
        longest_pause = parseInt(_get('longest_pause', 0));
        total_pause += 1000;
        current_pause += 1000;
        if (current_pause > longest_pause){
            _set('longest_pause', current_pause);
        }
        _set('total_pause', total_pause);
        _set('current_pause', current_pause);


        //trying to display the current pause timer in seconds only when in pause
        var curr_paused_seconds = String(Math.round(current_pause / 1000));
        $('#hidden_pause_timers').html(_pad(String(curr_paused_seconds)) +' elapsed seconds in this pause');

        // add a new second to the remaining time for each second spent in pause

        var old_end = parseInt(_get('expected_end_time')) ;

        var new_expected_end_time_with_pause = 1000 + old_end;
        _set('expected_end_time', new_expected_end_time_with_pause);
        // console.log(new_expected_end_time_with_pause);
        var diff = new_expected_end_time_with_pause - now ;
        var minutes = Math.floor(diff / 60000);
        var seconds = String(Math.round(diff / 1000));
        seconds = seconds % 60;
        $('#timer').html(_pad(String(minutes))+':'+_pad(String(seconds))+' remaining when you unpause');

        return;
    }


    // update  total time spend within this session - in or outside of webapp

    total_time = now - _get('local_appt_session_start');

    _set('cur_app_total_time', total_time);

    // Joe's original code that tracked the count down timer
        //var diff = (config['session_len'] * 60 * 1000 -1 ) - total_time;

    // Rich's new method of tracking against expected end time minus the current time
    var diff = parseInt(_get('expected_end_time')) - now ;

    // split, prep and formatting of remaining time
    var minutes = Math.floor(diff / 60000);
    var seconds = String(Math.round(diff / 1000));
    seconds = seconds % 60;

    // Check if the session is done recording
    if (diff < 0){
        clearInterval(surveyInterval);
        clearInterval(timerInterval);
        var appt = _get('cur_appt');
        endSession(appt, true);
        //window.location.replace('#done/'+appt);
    }
    else {
        $('#timer').html(_pad(String(minutes))+':'+_pad(String(seconds))+' remaining');
    }
}

function saveEvent(id){
    // Get the unposted array
    s = _getdict('events_to_save');
    if (s == null){
        s = [];
    }

    // Vibrate
    _vib();

    // Add this survey to the array
    data = {'event_id': id, 'guid': guid()};
    s.push(data);

    // Push the array back to the queue
    //_l('Adding survey to queue, total len=' + s.length);
    _setdict('events_to_save', s);

    // Increase count
    event_count[id]++;

    // Persist counts array
    _setdict('event_counts', event_count);

    $('#eventcount_' + id).fadeOut(500, function() {
        $(this).html(event_count[id]).fadeIn(1000);
        $('#btn_event_' + id).blur();
        // TODO - store event counts for loading on session restore
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

    // Set values based on how middle buttons are set
    if ($('#btn_sidewalk').data('data-on')=='Y'){
        survey['sidewalk'] = 'yes';
    }
    if ($('#btn_wrongway').data('data-on')=='Y'){
        survey['wrong_way'] = 'yes';
    }


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

    // Vibrate
    _vib();
    // Flash background
    $("body").animate({ backgroundColor: "#FFDCC9" }, 100).animate({ backgroundColor: "#FFF" }, 50);


    // Push the array back to the queue
    //_l('Adding survey to queue, total len=' + s.length);
    _setdict('surveys_to_save', s);

    // Clear all the buttons and what not
    /*
    $(':radio').prop('checked', false);
    $('.btn-group label').removeClass('active');

    // Clear internal survey value array

    for (i=0; i < Object.keys(survey).length; i++){
        //_l('survey key : ' + Object.keys(survey)[i]);
        var k = Object.keys(survey)[i];
        // TODO - update to respect default values, not hardcode
        if (k != 'sidewalk' && k != 'wrong_way' && k != 'gender') {
            //_l('null out key : ' + k);
            survey[Object.keys(survey)[i]] = null;
        }
    }

    // Set all defaults back
    $('input[data-default]').prop('checked', true);
    $('input[data-default]').parent().addClass('active');
    */

    // Set all UI back
    $('.btn-val').removeClass('active');
    $('#gender_1').addClass('active');
    $('#bike_share_2').addClass('active');

   // var sidewalkBTN = $("#lastname")
    $("#btn_sidewalk").data('data-on', 'N');
    $("#btn_sidewalk").css('background-color','#b28585');

    $("#btn_wrongway").data('data-on', 'N');
    $("#btn_wrongway").css('background-color','#b28585');

    // Rich commenting out the two lines below as I don't believe they really were resetting the button values
    //$('#cbx_wrongway').prop('checked', false).change();
    //$('#cbx_sidewalk').prop('checked', false).change();




    // Set underlying survey vals back to original
    survey = $.extend({}, survey_orig);

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


    //_l(surveys.length + ' surveys to post');
    if (surveys.length > 0){
        // Pop a survey off the queue
        var survey = surveys.pop();
        //_l('Posting survey data: ' + survey);

        // Resave the queue
        _setdict('surveys_to_save', surveys);

        // Post the survey
        var params = {'type': 'POST'};
        params['url'] = 'session/' + _get('cur_appt') + '/survey/';
        params['data'] = survey;
        _req(params);
    }

    // TODO - Test all this!
    //_l(events.length + ' events to post');
    if (events.length > 0){
        // Pop an evetn off the queue
        var event = events.pop();
        //_l('Posting event data: ' + event);

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

function getApptStats(id) {
    var d;
    _req({type: "GET", url: 'apptStats/session/'+id,
        success: function (data){
            _setdict('data',data);
            d = data;
        }
    });
    return d;
}


function getAppointments() {
    var d;
    _req({type: "GET", url: 'appts',
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
                // _set('actual_start', Date().getTime());
                _set('total_pause', 0);
                _set('longest_pause', 0);
                _set('current_pause', 0);

                // testing out saving new variables to track locallly session start AND expected end time to better manage when webapp is backgrounded

                 var now = new Date().getTime();
                 var remainingTime = now + 1000 * 60 * config['session_len'] ;
                 endTime = new Date(remainingTime).getTime();

                _set('local_appt_session_start', now);
                _set('expected_end_time', endTime);


                _setdict('event_counts', null);
                                // Load the recording page
                window.location.replace('#record/'+id);
            },
            error: function(data){
                return;
            }
        });
    }
}

function endSession(appt, force){
    // API call to end session
    id = _get('cur_appt');
    if (_get('token')){
        var confirmed = true;
        if (force == null){
            confirmed = confirm('Confirm end session?');
        }
        //if (confirm('Confirm end session?')) {
        if (force == true || confirmed){
            total_pause = _get('total_pause');
            longest_pause = _get('longest_pause', 0);
            _l('totalp: ' + total_pause + ' longp:'+longest_pause);
            $.ajax
            ({
                type: "POST",
                url: config['apiUrl'] + 'session/'+id+'/end',
                /*async: false,*/
                crossDomain: true,
                data: {'total_time': total_time, 'total_pause': total_pause, 'longest_pause': longest_pause, 'total_away': total_away},
                headers: {"Authorization": 'Token ' + _get('token')},
                success: function (data){
                    // Load the recording page
                    _set('cur_appt', null);
                    _set('cur_app_total_time', null);
                    _set('local_appt_session_start', null);
                    _set('expected_end_time', null);
                    _set('cur_app_rider_count', 0);
                    _setdict('event_counts', null);
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


