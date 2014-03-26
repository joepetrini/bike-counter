var map;
var config = {
    //apiUrl:'http://bikecounter.traklis.com/api/',
    apiUrl:'http://localhost:8001/api/',
    surveyType:'default' // For configurable survey interfaces
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
        var appt_id = Number(match[1]);
        appt = getAppointment(appt_id);
        //map.setCenter(appt.location.latitude, appt.location.longitude);
        var template = $('#tpl-appt').html();
        page = Mustache.to_html(template, appt);
        window.addEventListener('load', function () {
            console.log('lat:' + appt.location.latitude);
            var map = initializeMap(appt.location.latitude, appt.location.longitude);
        });
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