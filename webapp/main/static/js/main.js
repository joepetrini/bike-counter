function reset_appt(id){
    var r = confirm("This action will delete all survey data for this count session");
    if (r == true) {
        $.get('/api/session/' + id + '/reset', function (data) {
            $('#rst_span_' + id).fadeOut().html('Not started').fadeIn();
            $('#rst_btn_' + id).fadeOut().remove();
        });
    }
}