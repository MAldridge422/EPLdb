from django.conf.urls import url, include
from django.contrib import admin
from frontend import views as fe_views

urlpatterns = [
    url(r'^teams$', fe_views.teams, name='teams'),
    url(r'^positions$', fe_views.positions, name='positions'),
    url(r'^bookings$', fe_views.bookings, name='bookings'),
    url(r'^goals$', fe_views.goals, name='goals'),
    url(r'^raw_data$', fe_views.raw_data, name='raw_data'),
    url(r'^$', fe_views.index, name='index'),
]
