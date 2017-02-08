from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),

    url(r'^cards/$', get_cards, name='cards'),
]
