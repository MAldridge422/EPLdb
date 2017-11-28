from django.conf.urls import url, include
from django.contrib import admin
from frontend import views as fe_views

urlpatterns = [
    url(r'^$', fe_views.index, name='index'),
]
