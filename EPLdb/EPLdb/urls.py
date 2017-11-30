from django.conf.urls import url, include
from django.contrib import admin
from frontend import views as fe_views

urlpatterns = [
    url(r'^teams/(?P<team>[ \w]+)$', fe_views.teams, name='teams'),
    url(r'^teams$', fe_views.teams, name='teams'),
    url(r'^positions$', fe_views.positions, name='positions'),
    url(r'^positions/(?P<pos>\w+)$', fe_views.positions, name='positions'),
    url(r'^bookings$', fe_views.bookings, name='bookings'),
    url(r'^bookings/(?P<col>\w+)$', fe_views.bookings, name='bookings'),
    url(r'^goals$', fe_views.goals, name='goals'),
    url(r'^managers$', fe_views.managers, name='managers'),
    url(r'^raw_data/(?P<tname>\w+)$', fe_views.raw_data, name='raw_data'),
    url(r'^$', fe_views.index, name='index'),
]
