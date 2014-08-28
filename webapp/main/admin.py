from django.contrib import admin
from .models import *


class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ('user',)


admin.site.register(Organization)
admin.site.register(Membership)
admin.site.register(Location)
admin.site.register(ValueSet)
admin.site.register(Value)
admin.site.register(Metric)
admin.site.register(OrganizationMetrics)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Survey)
admin.site.register(SurveyValue)
admin.site.register(Event)
admin.site.register(OrganizationEvents)