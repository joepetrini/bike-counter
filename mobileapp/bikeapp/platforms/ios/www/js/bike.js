var map;
var survey = [];
var start = new Date().getTime();


var config = {
    //apiUrl:'http://bikecounter.traklis.com/api/',
    //apiUrl:'http://i5imac:8001/api/',
    //apiUrl:'http://127.0.0.1:8001/api/',
    surveyType:'default', // For configurable survey interfaces
    version: '0.1.0', // This should match the webapp version
    session_len: 600 // Number of minutes for a recording session
}

if (location.host.indexOf('localhost') > -1){
    config['apiUrl'] = 'http://127.0.0.1:8001/api/';
}
else {
    config['apiUrl'] = 'http://bikecounter.traklis.com/api/';
}

var timerInterval = null;
var surveyInterval = null;

var slider = new PageSlider($("#container"));
$(window).on('hashchange', route);

window.addEventListener('load', function () {
    new FastClick(document.body);
    $('.clickable').click(function() {
        var href = $(this).find("a").attr("href");
        if(href) {window.location = href;}
    });
    /*
    var map = initializeMap();
    google.maps.event.addListenerOnce(map, 'tilesloaded', function(){
        map.setCenter(77,-39);
    });
    */
    }, false);

function route(event) {
    var page,
        hash = window.location.hash;

    if (hash === "#pick_org") {
        var template = $('#tpl-pick-org').html();
        page = Mustache.to_html(template, {});
    }
    // Home screen
    if (hash === "#home") {
        //appts = getAppointments();
        //console.log('appts: ' + appts);
        var template = $('#tpl-home').html();
        page = Mustache.to_html(template);//, appts);
    }
    // Help screen
    if (hash === "#help") {
        var template = $('#tpl-help').html();
        page = Mustache.to_html(template);
    }
    // Upcoming appts screen
    if (hash === "#upcoming") {
        appts = getAppointments();
        //console.log('appts: ' + appts);
        var template = $('#tpl-upcoming').html();
        page = Mustache.to_html(template, appts);
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

        // Render the map
        setTimeout(function() {
            var myLatlng = new google.maps.LatLng(appt.location.latitude, appt.location.longitude);
            console.log('lat:' + appt.location.latitude);
            map = initializeMap(appt.location.latitude, appt.location.longitude);
            var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: appt.location.name
            });

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
        /*
        window.addEventListener('load', function () {
            console.log('lat:' + appt.location.latitude);
            map = initializeMap(appt.location.latitude, appt.location.longitude);
        });
        */
    }
    // Record survey view
    var match = hash.match(/^#record\/(\d{1,})/);
    if (match) {
        var appt_id = Number(match[1]);
        _l('cur_app:' + appt_id);
        _set('cur_appt', appt_id);
        var org = getOrg(getAppointment(appt_id).location.organization);
        var loc = getAppointment(appt_id).location;

        // Blank out survey vals
        _l('metric length:' + org.organizationmetrics_set.length);
        survey = {};
        for (i=0; i<org.organizationmetrics_set.length; i++){
            survey[org.organizationmetrics_set[i].metric.system_name] = null;
        }

        // Start timer
        start = new Date().getTime();
        _set('start_time', start);

        var template = $('#tpl-record').html();
        page = Mustache.to_html(template, {'org': org, 'location': loc});

        // Run the post survey every 10 seconds
        surveyInterval = setInterval(postSurveys, 3000);
        timerInterval = setInterval(updateTime, 1000);
    }
    // Login
    if (hash == '') {
        var template = $('#tpl-login').html();
        page = Mustache.to_html(template, {'name':'joe'});
        //$('#container').html(page);
    }
    //slider.slidePage($(page));
    $('#container').html(page);
}

route();