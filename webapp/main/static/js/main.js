function reset_appt(id){
    $.get('/api/session/'+id+'/reset', function(data) {
        $('#rst_span_'+id).fadeOut().html('Not started').fadeIn();
        $('#rst_btn_'+id).fadeOut().remove();
    });
}