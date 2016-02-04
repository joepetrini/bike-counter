#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Rich
#
# Created:     02/02/2016
# Copyright:   (c) Rich 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from django.test import *
#from .models import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, LocationSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



def main():
    c = Client()
    response = c.post('phl-bike/reports/report_export_to_csv/', {'year_selection':'2016', 'appt_selection': 'ALL'})
    #r'^(?P<slug>[-\w]+)/reports/report_export_to_csv/?
    #response.status_code
    # response = c.get('/customer/details/')
    #response.content


if __name__ == '__main__':
    main()
