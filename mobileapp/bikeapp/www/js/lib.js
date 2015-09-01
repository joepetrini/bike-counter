// Console log helper
function _l(msg){
    if (typeof console == "object") {
        console.log(msg);
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
    $('#api_url').html(url);
    window.location.replace('#admin');
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
    _setdict('event_counts', null);
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
        $('#'+ d.id).css('background-color','#e05a31');
    }
    else {
        $('#'+ d.id).data('data-on', 'Y');
        $('#'+ d.id).css('background-color','#b28585');
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
    }
    $('#btn_pause').blur();
}

function updateTime(){
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
        return;
    }

    // Add 1000ms to total time
    total_time += 1000;
    _set('cur_app_total_time', total_time);

    var diff = (config['session_len'] * 60 * 1000 - 1) - total_time;
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
        survey['wrongway'] = 'yes';
    }
    /*
    if ($('#cbx_sidewalk').prop('checked')) {
        survey['sidewalk'] = 'yes';
    }
    if ($('#cbx_wrongway').prop('checked')) {
        survey['wrong_way'] = 'yes';
    }
    /*

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

    $('#cbx_wrongway').prop('checked', false).change();
    $('#cbx_sidewalk').prop('checked', false).change();
    //$('#sidewalk_2').addClass('active');
    //$('#wrong_way_2').addClass('active');


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
                _set('total_pause', 0);
                _set('longest_pause', 0);
                _set('current_pause', 0);
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



/*! ========================================================================
 * Bootstrap Toggle: bootstrap-toggle.js v2.2.0
 * http://www.bootstraptoggle.com
 * ========================================================================
 * Copyright 2014 Min Hur, The New York Times Company
 * Licensed under MIT
 * ======================================================================== */
+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.toggle"),f="object"==typeof b&&b;e||d.data("bs.toggle",e=new c(this,f)),"string"==typeof b&&e[b]&&e[b]()})}var c=function(b,c){this.$element=a(b),this.options=a.extend({},this.defaults(),c),this.render()};c.VERSION="2.2.0",c.DEFAULTS={on:"On",off:"Off",onstyle:"primary",offstyle:"default",size:"normal",style:"",width:null,height:null},c.prototype.defaults=function(){return{on:this.$element.attr("data-on")||c.DEFAULTS.on,off:this.$element.attr("data-off")||c.DEFAULTS.off,onstyle:this.$element.attr("data-onstyle")||c.DEFAULTS.onstyle,offstyle:this.$element.attr("data-offstyle")||c.DEFAULTS.offstyle,size:this.$element.attr("data-size")||c.DEFAULTS.size,style:this.$element.attr("data-style")||c.DEFAULTS.style,width:this.$element.attr("data-width")||c.DEFAULTS.width,height:this.$element.attr("data-height")||c.DEFAULTS.height}},c.prototype.render=function(){this._onstyle="btn-"+this.options.onstyle,this._offstyle="btn-"+this.options.offstyle;var b="large"===this.options.size?"btn-lg":"small"===this.options.size?"btn-sm":"mini"===this.options.size?"btn-xs":"",c=a('<label class="btn">').html(this.options.on).addClass(this._onstyle+" "+b),d=a('<label class="btn">').html(this.options.off).addClass(this._offstyle+" "+b+" active"),e=a('<span class="toggle-handle btn btn-default">').addClass(b),f=a('<div class="toggle-group">').append(c,d,e),g=a('<div class="toggle btn" data-toggle="toggle">').addClass(this.$element.prop("checked")?this._onstyle:this._offstyle+" off").addClass(b).addClass(this.options.style);this.$element.wrap(g),a.extend(this,{$toggle:this.$element.parent(),$toggleOn:c,$toggleOff:d,$toggleGroup:f}),this.$toggle.append(f);var h=this.options.width||Math.max(c.outerWidth(),d.outerWidth())+e.outerWidth()/2,i=this.options.height||Math.max(c.outerHeight(),d.outerHeight());c.addClass("toggle-on"),d.addClass("toggle-off"),this.$toggle.css({width:h,height:i}),this.options.height&&(c.css("line-height",c.height()+"px"),d.css("line-height",d.height()+"px")),this.update(!0),this.trigger(!0)},c.prototype.toggle=function(){this.$element.prop("checked")?this.off():this.on()},c.prototype.on=function(a){return this.$element.prop("disabled")?!1:(this.$toggle.removeClass(this._offstyle+" off").addClass(this._onstyle),this.$element.prop("checked",!0),void(a||this.trigger()))},c.prototype.off=function(a){return this.$element.prop("disabled")?!1:(this.$toggle.removeClass(this._onstyle).addClass(this._offstyle+" off"),this.$element.prop("checked",!1),void(a||this.trigger()))},c.prototype.enable=function(){this.$toggle.removeAttr("disabled"),this.$element.prop("disabled",!1)},c.prototype.disable=function(){this.$toggle.attr("disabled","disabled"),this.$element.prop("disabled",!0)},c.prototype.update=function(a){this.$element.prop("disabled")?this.disable():this.enable(),this.$element.prop("checked")?this.on(a):this.off(a)},c.prototype.trigger=function(b){this.$element.off("change.bs.toggle"),b||this.$element.change(),this.$element.on("change.bs.toggle",a.proxy(function(){this.update()},this))},c.prototype.destroy=function(){this.$element.off("change.bs.toggle"),this.$toggleGroup.remove(),this.$element.removeData("bs.toggle"),this.$element.unwrap()};var d=a.fn.bootstrapToggle;a.fn.bootstrapToggle=b,a.fn.bootstrapToggle.Constructor=c,a.fn.toggle.noConflict=function(){return a.fn.bootstrapToggle=d,this},a(function(){a("input[type=checkbox][data-toggle^=toggle]").bootstrapToggle()}),a(document).on("click.bs.toggle","div[data-toggle^=toggle]",function(b){var c=a(this).find("input[type=checkbox]");c.bootstrapToggle("toggle"),b.preventDefault()})}(jQuery);
//# sourceMappingURL=bootstrap-toggle.min.js.map