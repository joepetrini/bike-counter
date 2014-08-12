var HomeView = function (adapter, template) {

    this.initialize = function () {
        // Define a div wrapper for the view. The div wrapper is used to attach events.
        this.el = $('<div/>');
        //this.el.on('keyup', '.search-key', this.findByName);
        //this.el.on('click', '#btn-login', this.Login);
    };

    this.render = function() {
        // Refresh org, location, appt data

        console.log('in render data:' + this.myData);
        this.el.html(template({'names':[{'name':'name1'},{'name':'name2'}]}));
        return this;
    };

    this.initialize();
}