/*************************
    Global Vars
*************************/
// Google map
// var map;
var platform = 'brw';
// Key val dictionary for storing selected values
var survey = {};
// Loaded one time and used to reset survey variable on save
var survey_orig = {};
// Total number of surveys submitted
var rider_count = 0;
// Array for all event counts
var event_count = [];

var appts = [];

//var events_for_loc = [];
//var tmp = null;
// Appt start time
var start = null;//new Date().getTime();
// Time in ms for current appt, see updateTime() func
var total_time = 0; // Total recording time in ms
// To Track if in paused state
var paused = false;
// Track time when pause started
var pause_start = null;
// Track time when away started
var away_start = null;
var total_away = 0;
// For updating time elapsed
var timerInterval = null;
// For posting surveys queued up
var surveyInterval = null;

var config = {
    surveyType:'default', // For configurable survey interfaces
    version: '0.2.03', // This should match the webapp version
    // Overridden from org setting
    session_len: 5 // Number of minutes for a recording session
}

/* Change api url depending on host */


if (location.hostname == 'localhost'){
    //_l('settign apiUrl');
    config['apiUrl'] = 'http://127.0.0.1:8001/api/';
}
else if (location.hostname == 'qa.bikecounts.com') {
    config['apiUrl'] = 'http://qa.bikecounts.com/api/';
    // rich commenting out below code as  I wasn't sure what this did
    //if (navigator.userAgent.match(/(Android|BlackBerry)/)) {
      //  config['apiUrl'] = 'http://10.0.2.2:8001/api/';
    //}
}
else {
    config['apiUrl'] = 'https://www.bikecounts.com/api/';
}

if (_get('apiUrl')){
    config['apiUrl'] = _get('apiUrl');
}

/* Wire up page routing */
$(window).on('hashchange', route);


/* Event handlers - set in index.html head */
function onAppLoad(){
    // Set device version
    if (typeof window.device !== 'undefined'){
        platform = window.device.platform.substring(0,3);
    }

    // Logout user on version change
    var v = _get('version');
    if (config['version'] != v){
        _set('version', config['version']);
        logout();
        return;
    }

    // Check for an open appt
    var appt = _get('cur_appt');
    _l('cur appt : ' + appt);
    if (appt != null){
        _l('redirecting to record appt ' + appt);
        window.location.replace('#record/' + appt);
        // Open in a paused state
        setTimeout(pause, 500);
        return;
    }

    if (_get('token') != null){
        window.location.replace('#home');
        return;
    }

}

function goBack(){}
function onAway(){
    _l('onAway fired');
    away_start = new Date().getTime();
}
function onResume(){
    _l('onResume fired');
}

function route(event) {


    var page,
        hash = window.location.hash;

    if (hash != '' && hash != '#admin') {
        check_login();

    }
    if (hash === "#pick_org") {
        var template = $('#tpl-pick-org').html();
        page = Mustache.to_html(template, {});

    }
    // Home screen
    if (hash === "#home") {
        var template = $('#tpl-home').html();
        page = Mustache.to_html(template);//, appts);

    }
    // Help screen
    if (hash === "#help") {
        var template = $('#tpl-help').html();
        page = Mustache.to_html(template);

    }
    // Admin screen
    if (hash === "#admin") {
        var template = $('#tpl-admin').html();
        page = Mustache.to_html(template, _tdata({}));

    }
    // Logout
    if (hash === '#logout') {

        logout();

    }
    // Upcoming appts screen
    if (hash === "#upcoming") {
        appts = getAppointments();
        // adding logic to enable scrolling on this view


        var template = $('#tpl-upcoming').html();
        page = Mustache.to_html(template, appts);
        reloadScrollBars();

    }
    // Finished view
    var match = hash.match(/^#done\/(\d{1,})/);
    if (match) {
        // Get the appointment data
        var appt_id = Number(match[1]);
        appt = getAppointment(appt_id);

        // Build the template
        var template = $('#tpl-done').html();
        page = Mustache.to_html(template, appt);

    }
    // Appointment view
    var match = hash.match(/^#appt\/(\d{1,})/);
    if (match) {
        // Get the appointment data
        var appt_id = Number(match[1]);
        appt = getAppointment(appt_id);

        // Build the template
        var template = $('#tpl-appt').html();
        page = Mustache.to_html(template, appt);

        reloadScrollBars();
        // Render the map
        setTimeout(function() {
            var myLatlng = new google.maps.LatLng(appt.location.latitude, appt.location.longitude);
            console.log('lat:' + appt.location.latitude);
            var map = initializeMap(appt.location.latitude, appt.location.longitude);
            var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: appt.location.name
            });
            window.scrollTo(0, 1);

            // Set map center to user's current location
            /*
            if(navigator.geolocation) {
                browserSupportFlag = true;
                navigator.geolocation.getCurrentPosition(function(position) {
                    initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
                    map.setCenter(initialLocation);
                }, function() {
                    handleNoGeolocation(browserSupportFlag);
                });
            }
            */
        }, 0);
    }
    // AppointmentStats view
    var match = hash.match(/^#apptstats\/(\d{1,})/);
    if (match) {
        // Get the appointment data
        var appt_id = Number(match[1]);
        appt = getAppointment(appt_id);
        theApptStats = getApptStats(appt_id)
        // Build the template
        var template = $('#tpl-apptstats').html();
        page = Mustache.to_html(template, theApptStats);
        window.scrollTo(0, 1);

    }
    // Record survey view
    var match = hash.match(/^#record\/(\d{1,})/);
    if (match) {
        var appt_id = Number(match[1]);
        //_l('in #record cur_app:' + appt_id);
        _set('cur_appt', appt_id);
        var org = getOrg(getAppointment(appt_id).location.organization);
        var loc = getAppointment(appt_id).location;
        config['session_len'] = parseInt(org.session_length);

        // Blank out survey vals
        /*
        _l('metric length:' + org.organizationmetrics_set.length);
        survey = {};
        for (i=0; i<org.organizationmetrics_set.length; i++){
            _l('adding ' + org.organizationmetrics_set[i].metric.system_name + ' to metrics');
            survey[org.organizationmetrics_set[i].metric.system_name] = null;
        }
        // Add direction in
        survey['direction'] = null;
        */
        // Create base survey array
        survey_orig = {};
        for (i=0; i<org.organizationmetrics_set.length; i++){
            survey_orig[org.organizationmetrics_set[i].metric.system_name] = null;
            /*  TODO: allow defaults at the orgmetric level
            for (j=0; j < org.organizationmetrics_set[i].metric.value_set.value_set.length; j++){
                if (org.organizationmetrics_set[i].metric.value_set.value_set[j].is_default){
                    survey_orig[org.organizationmetrics_set[i].metric.system_name] = org.organizationmetrics_set[i].metric.value_set.value_set[j].stored_value;
                }
            }
            */
        }
        survey_orig['wrong_way'] = 'no';
        survey_orig['sidewalk'] = 'no';
        survey_orig['gender'] = 'm';
        survey_orig['bike_share'] = 'no';
        // Add direction in
        survey_orig['direction'] = null;
        // Set working survey to orig, use jquery extend to make object copy
        survey = $.extend({}, survey_orig);


        // Reset rider count, unless restoring session
        rider_count = 0;
        if (_get('cur_app_rider_count') != null){
            rider_count = parseInt(_get('cur_app_rider_count'));
        }

        // Rebuild event count array
        // TODO restore session counts
        events_for_loc = [];
        event_count = new Array();
        if (_getdict('event_counts')){
            event_count = _getdict('event_counts');
            _l('event_counts found setting local var : ' + event_count);
        }
        for (i=0; i < org.organizationevents_set.length; i++){
            var ev = org.organizationevents_set[i];
            // Don't count pedestrians at intersections
            if (ev.event.system_name == 'pedestrian' && loc.type == 'intersection') {
                continue;
            }
            _l('loading event: ' + ev);
            if (typeof event_count[ev.event.id] == 'undefined'){
                event_count[ev.event.id] = 0;
            }
            events_for_loc.push({'event': {'id': ev.event.id, 'name': ev.event.name, 'count': event_count[ev.event.id]}});
        }

        // Start timer, restore if in session
        total_time = 0;
        if (_get('cur_app_total_time') != null){
            total_time = parseInt(_get('cur_app_total_time'));
        }
        paused = false;
        //start = new Date().getTime();
        //_set('start_time', start);

        // Build dynamic list of direction options
        // changed with adding dir1/dir2
        /*
        var dirs = Array();
        if (loc.has_north) {dirs.push('north');}
        if (loc.has_south) {dirs.push('south');}
        if (loc.has_east) {dirs.push('east');}
        if (loc.has_west) {dirs.push('west');}
        */

        var template = $('#tpl-record').html();
        page = Mustache.to_html(template, {'org': org, 'loc': loc, 'events': events_for_loc});
        window.scrollTo(0, 1);
        unloadScrollBars();

        // Set dynamic button height/width
        /*
        var h = ($(window).height() - 100) / 3;
        $('.btn').css('height', h + 'px');
        $('.btn').css('padding-top', (h/2 - 14) + 'px');
        var w = ($(window).width() - 90) / 6;
        $('.btn-val').css('width', w + 'px');
        w = ($(window).width() - 250) / 9;
        if (w > 150) {w = 150;}
        $('.btn-event').css('width', w + 'px');
        */
        setTimeout(function() {
            $('#total_riders').html(rider_count);

        }, 1);

        // Run the post survey every 10 seconds
        surveyInterval = setInterval(postSurveys, 3000);
        timerInterval = setInterval(updateTime, 1000);
    }
    // Login
    if (hash == '') {
        var template = $('#tpl-login').html();
        page = Mustache.to_html(template, _tdata({}));
         unloadScrollBars();
    }
    $('#container').html(page);
}
route();


function displayYourAppts() {

     reloadScrollBars();
    var currentapts = getAppointments();
    currentapts = currentapts['appointment_set'];
    var table = document.getElementById("upcomingtable");
    //console.log("we got here!-- " + currentapts);
    for (i=0; i < currentapts.length; i++){


        var row = table.insertRow(i+1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell1Text = document.createTextNode(currentapts[i].location.name);
        var link = document.createElement("a");

        if (currentapts[i].status == "Complete"){
            link.setAttribute("href","#apptstats/" + currentapts[i].id);
            link.appendChild(cell1Text);
            cell1.appendChild(link);
            cell2.innerHTML = "Complete";
            cell2.style.color = "#009933";
            cell2.style.fontWeight = "bold";

        }else if (currentapts[i].status == "In Progess"){
            // do something else ... let people continue, I assume
            link.setAttribute("href","#appt/"  + currentapts[i].id);
            link.appendChild(cell1Text);
            cell1.appendChild(link);

            cell2.innerHTML = "In Progress";

        }else{
            //Not Started with session link
            link.setAttribute("href","#appt/" + currentapts[i].id);
            link.appendChild(cell1Text);
            cell1.appendChild(link);

            cell2.innerHTML = "Not Started";
        }
    }
     var row = table.insertRow(currentapts.length+1);
     var cellEnd = row.insertCell(0);
      var cellENDText = document.createTextNode('Click here to go sign-up for more appointments!');
      var link = document.createElement("a");

       link.setAttribute("href",get_appt_signup_URL());
            link.appendChild(cellENDText);
            cellEnd.appendChild(link);

};


