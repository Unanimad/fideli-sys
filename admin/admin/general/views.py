from django.shortcuts import render
from django.contrib import messages

from .forms import *


def list_client(request):
    template_name = 'client/list.html'

    context = {}

    instances = Client.objects.filter(company__user=request.user)

    context['instances'] = instances

    return render(request, template_name, context)


def add_client(request):
    template_name = 'client/add.html'

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        service = request.POST['service']
        configuration = request.POST['configuration']

        company = Company.objects.get(user=request.user)
        service = Service.objects.get(id=service)
        configuration = CardConfiguration.objects.get(id=configuration)

        client = Client(name=name, phone=phone, company=company)
        client.save()

        if client.id:
            card = Card(company=company, client=client, service=service, configuration=configuration)
            card.save()

            messages.success(request, 'Cadastrado com sucesso!')

        else:
            messages.warning(request, 'Falha ao cadastrar.')

    card_form = CardForm(auto_id=False)
    card_form.fields["service"].queryset = Service.objects.filter(company__user=request.user)
    card_form.fields["configuration"].queryset = CardConfiguration.objects.filter(company__user=request.user)

    context = {
        'form': ClientForm(auto_id=False),
        'form_card': card_form
    }

    return render(request, template_name, context)


def edit_client(request, pk):
    template_name = 'client/add.html'

    instance = Client.objects.get(id=pk)

    if request.method == 'POST':
        Client.objects.filter(id=pk).update(name=request.POST['name'], phone=request.POST['phone'])
        instance = Client.objects.get(id=pk)

        messages.success(request, 'Atualizado com sucesso!')

    context = {
        'form': ClientForm(instance=instance)
    }

    return render(request, template_name, context)


def list_service(request):
    template_name = 'service/list.html'

    instances = Service.objects.filter(company__user=request.user)

    context = {
        'instances': instances
    }

    return render(request, template_name, context)


def add_service(request):
    template_name = 'service/add.html'

    if request.method == 'POST':
        name = request.POST['name']

        company = Company.objects.get(user=request.user)

        service = Service(name=name, company=company)
        service.save()

        if service.id:
            messages.success(request, 'Cadastrado com sucesso!')

        else:
            messages.error(request, 'Falha ao cadastrar.')

    context = {
        'form': ServiceForm(auto_id=False)
    }

    return render(request, template_name, context)


def edit_service(request, pk):
    template_name = 'service/add.html'

    instance = Service.objects.get(id=pk)

    if request.method == 'POST':
        Service.objects.filter(id=pk).update(name=request.POST['name'])
        instance = Service.objects.get(id=pk)

        messages.success(request, 'Atualizado com sucesso!')

    context = {
        'form': ServiceForm(instance=instance)
    }

    return render(request, template_name, context)


def list_card_configuration(request):
    template_name = 'card_configuration/list.html'

    instances = CardConfiguration.objects.filter(company__user=request.user)

    context = {
        'instances': instances
    }

    return render(request, template_name, context)


def add_card_configuration(request):
    template_name = 'card_configuration/add.html'

    if request.method == 'POST':
        expire = request.POST['expire']
        limit = request.POST['limit']

        company = Company.objects.get(user=request.user)

        configuration = CardConfiguration(expire=expire, limit=limit, company=company)
        configuration.save()

        if configuration.id:
            messages.success(request, 'Cadastrado com sucesso!')
        else:
            messages.error(request, 'Falha ao cadastrar.')

    context = {
        'form': CardConfigurationForm(auto_id=False)
    }

    return render(request, template_name, context)


def edit_card_configuration(request, pk):
    template_name = 'card_configuration/add.html'

    instance = CardConfiguration.objects.get(id=pk)

    if request.method == 'POST':
        CardConfiguration.objects.filter(id=pk).update(expire=request.POST['expire'], limit=request.POST['limit'])
        instance = CardConfiguration.objects.get(id=pk)

        messages.success(request, 'Atualizado com sucesso!')

    context = {
        'form': CardConfigurationForm(instance=instance)
    }

    return render(request, template_name, context)
