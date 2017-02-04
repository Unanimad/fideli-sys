from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),

    url(r'^client/$', list_client, name='clients'),
]
