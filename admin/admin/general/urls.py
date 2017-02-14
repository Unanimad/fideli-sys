from django.conf.urls import url

from admin.general.views import *

urlpatterns = [
    url(r'^company/$', list_company, name='companies'),
    url(r'^company/add/$', add_company, name='add_company'),

    url(r'^client/$', list_client, name='clients'),
    url(r'^client/add/$', add_client, name='add_client'),
    url(r'^client/delete/$', delete_client, name='delete_client'),
    url(r'^client/(?P<pk>\w+)/$', edit_client, name='edit_client'),

    url(r'^service/$', list_service, name='services'),
    url(r'^service/add/$', add_service, name='add_service'),
    url(r'^service/(?P<pk>\w+)/$', edit_service, name='edit_service'),

    url(r'^card_configuration/$', list_card_configuration, name='cards_configurations'),
    url(r'^card_configuration/add/$', add_card_configuration, name='add_card_configuration'),
    url(r'^card_configuration/(?P<pk>\w+)/$', edit_card_configuration, name='edit_card_configuration'),

    url(r'^card/$', list_card, name='cards'),
    url(r'^card/add/$', add_card, name='add_card'),
    url(r'^card/convert/$', convert_card, name='convert_card'),

    url(r'^score/add/$', add_score, name='add_score')

]
