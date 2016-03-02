function enableCSVButton(){
    currentChoice = document.getElementById("id_appt_selection").value;
    if (currentChoice != "default" ) {
         document.getElementById("csvSubmitButton").disabled = false;
    }
    else {
        document.getElementById("csvSubmitButton").disabled = true;
    }
}

function reset_appt(id){
    var r = confirm("This action will delete all survey data for this count session");
    if (r == true) {
        $.get('/api/session/' + id + '/reset',
            function (data) {
                $('#rst_span_' + id).fadeOut().html('Not started').fadeIn();
                $('#rst_btn_' + id).fadeOut().remove();
             }
        );
    }
}

// this function is for the report_export_to_csv.html page
// copied code from the mobile app JS files

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }



function ajaxYearSelection(){

    users_year_selection = document.getElementById("id_year_selection").value;


    $.ajax
        ({
            type: "POST",
            url: document.URL + "/get_csv_appts/",
            async: true,
            crossDomain: true,
            headers: {"X-CSRFToken": getCookie("csrftoken")} ,
            data : {
                year_selection : users_year_selection

            },
            success: function (data){
                appt_dropdown = document.getElementById("id_appt_selection");
                appt_dropdown.options.length = 0;


                for (i = 0; i < data.appointment_choices.length; i++) {
                    var option = document.createElement("option");
                    option.text = data.appointment_choices[i][1];
                    option.value = data.appointment_choices[i][0];
                    appt_dropdown.options.add(option,i) ;
                }
                 //$("#id_appt_selection").val("default");

            },
            error: function (data){ return; }

                //here is where I'll want to update the valid values for the appt drop down

       }) ;
    document.getElementById("csvSubmitButton").disabled = true;
}


