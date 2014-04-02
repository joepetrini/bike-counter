var map;
var config = {
    //apiUrl:'http://bikecounter.traklis.com/api/',
    apiUrl:'http://localhost:8001/api/',
    surveyType:'default', // For configurable survey interfaces
    version: '0.1.0' // This should match the webapp version
}

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
        appts = getAppointments();
        console.log('appts: ' + appts);
        var template = $('#tpl-home').html();
        page = Mustache.to_html(template, appts);
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
        var org = getOrg(getAppointment(appt_id).location.organization);
        var template = $('#tpl-record').html();
        page = Mustache.to_html(template, {'org': org});
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