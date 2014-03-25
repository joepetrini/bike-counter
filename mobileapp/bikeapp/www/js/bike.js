var slider = new PageSlider($("#container"));
$(window).on('hashchange', route);

window.addEventListener('load', function () {
    new FastClick(document.body);
}, false);

function route(event) {
    var page,
        hash = window.location.hash;

    if (hash === "#page1") {
        page = 'page1';
        //page = merge(detailsPage, {img: "buildbot.jpg", name: "Build Bot", description: "Lorem Ipsum"});
        //slider.slide($(page), "right");
    }
    else {
        page = '<a href="#page1">page1</a>';//homePage;
        //slider.slide($(homePage), "left");
    }

    slider.slidePage($(page));
}

route();