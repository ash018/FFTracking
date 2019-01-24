from django.db import connection, connections
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import re
import csv
import time
import sys
from .models import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import urllib3
import json
import urllib.request
import requests
import numpy
import pandas as pd
from django.views.generic import FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from .modelHitCount import *
from datetime import datetime, timedelta
from django.http import JsonResponse


def LiveTracking(request):
    msr_initial_locations = GetInitialMSRPosition()
    for msr in msr_initial_locations:
        msr['MaxUpdateTime'] = str(msr['MaxUpdateTime'])
        msr['Latitude'] = float(msr['Latitude'])
        msr['Longitude'] = float(msr['Longitude'])

    context = {
                'Latest_MSR_Locations': json.dumps(msr_initial_locations)
               }
    return render(request, 'MotorMSRGeoTrackingApp/LiveTracking.html', context)

def PharmaFFTracking(request):
    pharmaff_initial_locations = GetInitialPharmaFFPosition()
    for ff in pharmaff_initial_locations:
        ff['MaxUpdateTime'] = str(ff['MaxUpdateTime'])
        ff['Latitude'] = float(ff['Latitude'])
        ff['Longitude'] = float(ff['Longitude'])

    context = {
                'Latest_PharmaFF_Locations': json.dumps(pharmaff_initial_locations)
               }
    return render(request, 'MotorMSRGeoTrackingApp/PharmaFFTracking.html', context)



def MSRCurrentLocation(request):
    current_msr_locations = CurrentMSRLocation.objects.all().using('MotorDashboard')
    current_msr_locations = list(current_msr_locations.values())
    for msr in current_msr_locations:
        msr['Time'] = msr['Time'].strftime("%Y-%m-%d %H:%M:%S")
        msr['Latitude'] = float(msr['Latitude'])
        msr['Longitude'] = float(msr['Longitude'])

    context = {
                'Current_MSR_Locations': json.dumps(current_msr_locations)
               }
    return render(request, 'MotorMSRGeoTrackingApp/CurrentMSRLocation.html', context)

def LocationAnalysis(request):
    #current_place_locations = GetBoundedPlaceLocationData(25.964849, 25.201849, 89.885888, 88.836694)
    current_place_locations = GetPlaceLocation()
    center_latitude = 0
    center_longitude = 0
    for loc in current_place_locations:
        loc['EntryDate'] = loc['EntryDate'].strftime("%Y-%m-%d %H:%M:%S")
        loc['Latitude'] = float(loc['Latitude'])
        loc['Longitude'] = float(loc['Longitude'])
        center_latitude += loc['Latitude']
        center_longitude += loc['Longitude']

    center_latitude = center_latitude / len(current_place_locations)
    center_longitude = center_longitude / len(current_place_locations)

    context = {
                'Current_Place_Locations': json.dumps(current_place_locations),
                'Center_Latitude': center_latitude,
                'Center_Longitude': center_longitude
               }
    return render(request, 'MotorMSRGeoTrackingApp/LocationAnalysis.html', context)


def PathTracking(request):
    selected_msr = 'C29410'
    center_latitude = 0
    center_longitude = 0
    #Dropdown for MSR UserIds and Level1Names
    msr_codes_dropdown_data = CurrentMSRLocation.objects.filter(Userid__isnull=False).values('Userid', 'Level1Name').distinct().using('MotorDashboard')
    msr_codes_dropdown_data = list(msr_codes_dropdown_data)

    #Get path of an MSR on the map sorted by date. selected_msr is by default an MSR when first load. Taking last 3 days patha data
    msrs = MSRMovement.objects.filter(Userid=selected_msr, ServerTime__range=(  datetime.now() - timedelta(days=3), datetime.now()  )).order_by('-ServerTime').using('MotorDashboard')
    msrs = list(msrs.values())

    for item in msrs:
        item['ServerTime'] = item['ServerTime'].strftime("%Y-%m-%d %H:%M:%S")
        item['Latitude'] = float(item['Latitude'])
        item['Longitude'] = float(item['Longitude'])
        center_latitude += item['Latitude']
        center_longitude += item['Longitude']

    if len(msrs) == 0:
        center_latitude = 23.777176
        center_longitude = 90.399452
    else:
        center_latitude = center_latitude / len(msrs)
        center_longitude = center_longitude / len(msrs)

    context = {
        'MSR_Movements': json.dumps(msrs),
        'Center_Latitude': center_latitude,
        'Center_Longitude': center_longitude,
        'Selected_Msr': selected_msr,
        'Msr_Codes_Dropdown_Data': msr_codes_dropdown_data
    }
    return render(request, 'MotorMSRGeoTrackingApp/PathTracking.html', context)


# AJAX call to get bounded map search when the map is dragged or zoomed
def GetBoundedPlaceLocation(request):
    latUpper = request.GET.get('latUpper', None)
    latBottom = request.GET.get('latBottom', None)
    lngUpper = request.GET.get('lngUpper', None)
    lngBottom = request.GET.get('lngBottom', None)

    current_place_locations = GetBoundedPlaceLocationData(latUpper, latBottom, lngUpper, lngBottom)
    for loc in current_place_locations:
        loc['EntryDate'] = loc['EntryDate'].strftime("%Y-%m-%d %H:%M:%S")
        loc['Latitude'] = float(loc['Latitude'])
        loc['Longitude'] = float(loc['Longitude'])

    return HttpResponse(json.dumps({'result': current_place_locations}), content_type="application/json")


# AJAX call to get path by date filtered
def GetMSRPath(request):
    FromDate = request.GET.get('FromDate', None)
    ToDate = request.GET.get('ToDate', None)
    print(FromDate)
    print(ToDate)
    FromDate = datetime.strptime(FromDate + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
    ToDate = datetime.strptime(ToDate + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    if (ToDate - FromDate).days > 15:
        print('minimizing')
        FromDate = ToDate - timedelta(days=15)

    print(FromDate)
    print(ToDate)
    MSRCode = request.GET.get('MSRCode', None)
    print(MSRCode)
    msrs = MSRMovement.objects.filter(Userid=MSRCode, ServerTime__range=(FromDate, ToDate)).order_by('-ServerTime').using('MotorDashboard')
    msrs = list(msrs.values())
    center_latitude = 0
    center_longitude = 0
    for item in msrs:
        item['ServerTime'] = item['ServerTime'].strftime("%Y-%m-%d %H:%M:%S")
        item['Latitude'] = float(item['Latitude'])
        item['Longitude'] = float(item['Longitude'])
        center_latitude += item['Latitude']
        center_longitude += item['Longitude']

    if len(msrs) == 0:
        center_latitude = 23.777176
        center_longitude = 90.399452
    else:
        center_latitude = msrs[0]['Latitude']
        center_longitude = msrs[0]['Longitude']

    print(msrs)
    return HttpResponse(json.dumps({'data': msrs, 'Center_Latitude': center_latitude, 'Center_Longitude': center_longitude }), content_type="application/json")