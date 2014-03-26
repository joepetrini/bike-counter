/* http://coenraets.org/blog/cordova-phonegap-3-tutorial/ */

// We use an "Immediate Function" to initialize the application to avoid leaving anything behind in the global scope
(function () {
    /* ---------------------------------- Config values ---------------------------------- */
    // Loaded into local storage on app launch
    var config = {
        //apiUrl:'http://bikecounter.traklis.com/api/',
        apiUrl:'http://localhost:8001/api/',
        surveyType:'default' // For configurable survey interfaces
    }

    /* ---------------------------------- Local Variables ---------------------------------- */
    var homeTpl = Handlebars.compile($("#tpl-home").html());
    var loginTpl = Handlebars.compile($("#tpl-login").html());
    //var employeeLiTpl = Handlebars.compile($("#employee-li-tpl").html());
    //var employeeTpl = Handlebars.compile($("#employee-tpl").html());

    var homeUrl = /^#home/;
    //var detailsURL = /^#employees\/(\d{1,})/;

    var slider = new PageSlider($('body'));

    var adapter = new LocalStorageAdapter();
    adapter.initialize(config).done(function () {
        route();
    });

    /* --------------------------------- Event Registration -------------------------------- */
    $(window).on('hashchange', route);

    document.addEventListener('deviceready', function () {

        FastClick.attach(document.body);

        if (navigator.notification) { // Override default HTML alert with native dialog
            window.alert = function (message) {
                navigator.notification.alert(
                    message,    // message
                    null,       // callback
                    "Workshop", // title
                    'OK'        // buttonName
                );
            };
        }
    }, false);

    /* ---------------------------------- Local Functions ---------------------------------- */
    function route() {
        var hash = window.location.hash;
        if (!hash) {
            slider.slidePage(new LoginView(adapter, loginTpl).render().el);
            return;
        }
        if (hash.match(homeUrl)){
            adapter.refreshData(function() {
                slider.slidePage(new HomeView(adapter, homeTpl).render().el);
            })
        }
        /*
        var match = hash.match(detailsURL);
        if (match) {
            adapter.findById(Number(match[1])).done(function(employee) {
                slider.slidePage(new EmployeeView(adapter, employeeTpl, employee).render().el);
            });
        }
        */
    }

}());