from django.conf.urls import include
from django.contrib.admin import AdminSite

from .views import *


class Admin(AdminSite):
    def get_urls(self):
        from django.conf.urls import url
        urls = [
            url(r'^$', dashboard, name='dashboard'),
            url(r'^login/$', login, name='login'),
            url(r'^logout/$', logout, name='logout'),
            url(r'^general/', include('admin.general.urls', namespace='general')),
        ]
        return urls


admin_site = Admin()
