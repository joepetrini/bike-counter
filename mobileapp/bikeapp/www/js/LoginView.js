var LoginView = function (adapter, template) {

    this.initialize = function () {
        // Define a div wrapper for the view. The div wrapper is used to attach events.
        this.el = $('<div/>');
        //this.el.on('keyup', '.search-key', this.findByName);
        this.el.on('click', '#btn-login', this.Login);
    };

    this.render = function() {
        this.el.html(template());
        return this;
    };

    this.Login = function() {
        $('#err-login').hide();
        // Validate
        var username = $('#username').val();
        var password = $('#password').val();
        if (username == '' || password == '') {
            $('#err-login').html('Invalid username or password').show();
            return;
        }

        $.ajax({
            type: "POST",
            url: adapter.getConfig('apiUrl') + 'auth',
            crossDomain: true,
            data: {username:username, password:password},
            success: function (data){
                if (data.token){

                }
                else {
                    $('#err-login').html(data.message).show();
                    return;
                }
            },
            error: function (data){
                $('#login_error').html('Invalid login').show();
            }
        });
    /*
    adapter.findByName($('.search-key').val()).done(function(employees) {
        $('.employee-list').html(listItemTemplate(employees));
    });
    */
    };

    this.initialize();

}