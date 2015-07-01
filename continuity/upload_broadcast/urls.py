from django.conf.urls import patterns, url
from upload_broadcast import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url('^', views.upload_broadcast_form, name = 'upload_broadcast_form'),
)
