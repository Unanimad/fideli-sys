from django.shortcuts import render

from admin.general.models import *


def dashboard(request):
    template_name = 'base.html'

    return render(request, template_name)


def list_client(request):

    template_name = 'base.html'

    context = {}

    instances = Client.objects.filter(company__user=request.user)

    context['instances'] = instances

    return render(request, template_name, context)
