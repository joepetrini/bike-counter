from django import forms
from .models import Appointment, Organization
from .logic import *
from datetime import datetime

class CSV_report_selection_form(forms.Form):

    year_selection = forms.ChoiceField(label='Count Year', required=True,
        widget=forms.Select(attrs={"onChange":'ajaxYearSelection()'})
        )

    appt_selection = forms.ChoiceField(label='Appointment Selection', required=True, widget=forms.Select(attrs={"onChange" : 'enableCSVButton()'}) )


    def __init__(self, yr_choices=None, yrinit=None, appt_choices=[('default', '--Pick--')], default_appt='default', *args,**kwargs):


        super(CSV_report_selection_form,self).__init__(*args,**kwargs)

        self.fields['year_selection']._set_choices(yr_choices)
        self.fields['year_selection'].initial = yrinit

        self.fields['appt_selection']._set_choices(appt_choices)
        self.fields['appt_selection'].initial = default_appt


