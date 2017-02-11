import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext

from admin.general.models import Client, Card


@login_required
def dashboard(request):
    template_name = 'dashboard.html'

    context = {
        'clients_all': len(Client.objects.filter(company__user=request.user)),
        'clients_today': len(Client.objects.filter(company__user=request.user)
                             .filter(created_at__gt=datetime.date.today())),
        'cards_converted': len(Card.objects.filter(client__company__user=request.user).filter(converted=1))
    }

    return render(request, template_name, context)


def login(request):
    template_name = 'login.html'

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/admin')
            else:
                messages.success(request, 'Conta inativa.')
        else:
            messages.success(request, 'Usuário ou senha incorretos.')

    return render(request, template_name)


def logout(request):
    auth_logout(request)

    return redirect('/admin/login')


def handler404(request):
    template_name = '404.html'

    response = render_to_response(template_name, {}, context_instance=RequestContext(request))
    response.status_code = 404

    return response

