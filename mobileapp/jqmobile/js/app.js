//$.mobile.changePage.defaults.allowSamePageTransition = true;
storage=$.localStorage;
//api = 'http://localhost:5000/api/'
api = 'http://bikecounter.traklis.com/api/'


function _api(url, cb){
    $.ajax
    ({
        type: "GET",
        url: api + url + '?api_key='+_g('api_key'),
        dataType: 'json',
        crossDomain: true,
        success: cb
    });
}

/* LocalStorage get/set functions */
function _g(k){
    return storage.get(k);
}

function _s(k, v){
    storage.set(k, v);
}

function login(){
    u = $('#username').val();
    p = $('#password').val();
    $.mobile.loading( 'show', {
        text: 'Logging In',
        textVisible: true,
        theme: 'z',
        html: ""
    });    
    $.ajax({
      type: "POST",
      url: api + 'auth',
      crossDomain: true,
      data: {username:u, password:p},
      success: function (data){
        if (data.token){
            _s('token', data.token);
            _s('logged_in', true);
            $.mobile.changePage('#page-lists');
        }
        else {
            $.mobile.loading( 'hide' )
            $('#login_error').html(data.message).show();
        }
      },
      error: function (data){
        $.mobile.loading( 'hide' )
        $('#login_error').html('Invalid login').show();
        }
    });         
}

function select_list(l){
    _s('list_id',l);
    $.mobile.changePage('#page-messages');//, {reloadPage:true});
    //document.location='#page-messages';  
}

function select_message(m){
    _s('msg_id',m);
    $.mobile.changePage('#page-message');
}
/*
function init(){
    //_s('logged_in',null);
    if (_g('logged_in')){
        if (_g('page')) {
            window.location = _g('page') + '.html'
            //change_page(_g('page'));
        }
        else {
            //change_page('lists');
            window.location = 'lists.html';
        }
        //change_page('login');
        //('#page-login').show();
    }
    else {
        window.location = 'login.html';
    }
}
*/
/* Get query value helper */
function _q(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) { 
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};