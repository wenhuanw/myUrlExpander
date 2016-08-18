from django.conf.urls import url
from . import views
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api/create/$',views.url_create_api,name='url_create_api'),
    url(r'^api/list/$', views.url_list_api, name='url_list_api'),
    url(r'^api/edit/(?P<pk>[0-9]+)/$', views.url_edit_api, name='url_edit_api'),

    url(r'^url/list/$', views.url_list, name='url_list'),
    url(r'^url/(?P<pk>[0-9]+)/$', views.url_detail, name='url_detail'),
    url(r'^url/create/$', views.url_create, name='url_create'),
    url(r'^url/(?P<pk>[0-9]+)/edit/$', views.url_edit, name='url_edit'),
    url(r'^url/(?P<pk>[0-9]+)/delete/$', views.url_delete, name='url_delete'),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': 'django.contrib.auth.views.login'}),

]

urlpatterns = format_suffix_patterns(urlpatterns)
