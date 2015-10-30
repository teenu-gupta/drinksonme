from django.conf.urls import patterns, include, url
from notifications import views

urlpatterns = patterns('',
    url(r'^apple_registration/$', views.AppleView.as_view(), name='apple_registration'),
    url(r'^android_registration/$', views.AndroidView.as_view(), name='android_registration'),

)