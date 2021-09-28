from django.contrib import admin
from django.urls import path, include
from .views import *
app_name = "search"
urlpatterns = [
    #path('', main, name="main"),
    path('NA', NA, name="NA"),
    #path('EUW', EUW, name="EU"),
    #path('KR', KR, name="KR"),
    #path('EUN', EUN, name="EUN"),
    #path('OCE', KR, name="OCE"),
    #path('BR', BR, name="BR"),
    #path('LAS', LAS, name="LAS"),
    #path('LAN', LAN, name="LAN"),
    #path('RUS', RUS, name="RUS"),
    #path('TUR', TUR, name="TUR"),
    path('search', search, name="search"),
]
