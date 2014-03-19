from django.contrib import admin
from .models import *


admin.site.register(Profile)
admin.site.register(Organization)
admin.site.register(Membership)
admin.site.register(Location)
admin.site.register(ValueSet)
admin.site.register(Value)
admin.site.register(Metric)
admin.site.register(OrganizationMetrics)
admin.site.register(Appointment)
admin.site.register(Survey)
admin.site.register(SurveyValue)