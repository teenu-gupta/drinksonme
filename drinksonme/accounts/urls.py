from accounts import views
from django.conf.urls import patterns, url


urlpatterns = patterns('',
	url(r'^register/$',views.Register.as_view(), name= 'register'),
	url(r'^login/$',views.Login.as_view(), name = 'login'),
	url(r'^logout/$',views.Logout.as_view(),name='logout'),
	url(r'^profilecreate/$', views.ProfileCreate.as_view(),name= 'profilecreate'),
	url(r'^profile/(?P<pk>[0-9]+)/$',views.ProfileUpdate.as_view(), name='profileupdate'),
	url(r'^profile-image/$', views.ProfileImageView.as_view(), name='profile_image'),
	)







