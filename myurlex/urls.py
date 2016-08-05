from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.urls_list, name='urls_list'),
    url(r'^url/(?P<pk>[0-9]+)/$', views.url_detail, name='url_detail'),
    url(r'^url/new/$', views.url_new, name='url_new'),
    url(r'^url/(?P<pk>[0-9]+)/edit/$', views.url_edit, name='url_edit'),
    url(r'^url/(?P<pk>[0-9]+)/remove/$', views.url_remove, name='url_remove'),
]
