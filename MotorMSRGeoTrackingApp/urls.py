from django.conf.urls import url
from .views import *
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^LiveTracking', views.LiveTracking, name='LiveTracking'),
    url(r'^PharmaFFTracking', views.PharmaFFTracking, name='PharmaFFTracking'),
    url(r'^MSRCurrentLocation', views.MSRCurrentLocation, name='MSRCurrentLocation'),
    url(r'^LocationAnalysis', views.LocationAnalysis, name='LocationAnalysis'),
    url(r'^GetBoundedPlaceLocation', views.GetBoundedPlaceLocation, name='GetBoundedPlaceLocation'),
    url(r'^PathTracking', views.PathTracking, name='PathTracking'),
    url(r'^GetMSRPath', views.GetMSRPath, name='GetMSRPath')

]