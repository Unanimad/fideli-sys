import datetime

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *


def list_client(request):
    template_name = 'client/list.html'

    instances = []
    context = {}

    objects = Client.objects.filter(company__user=request.user)

    for object in objects:
        instance = {
            'object': object,
            'converted': len(Card.objects.filter(client=object).filter(converted=1))
        }

        instances.append(instance)

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

            expire_at = datetime.datetime.now() + datetime.timedelta(days=configuration.expire)

            card = Card(expire_at=expire_at, company=company, client=client,
                        service=service, configuration=configuration)
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
    template_name = 'client/edit.html'

    instance = Client.objects.get(id=pk)

    if request.method == 'POST':
        Client.objects.filter(id=pk).update(name=request.POST['name'], phone=request.POST['phone'])
        instance = Client.objects.get(id=pk)

        messages.success(request, 'Atualizado com sucesso!')

    context = {
        'form': ClientForm(instance=instance),
    }

    return render(request, template_name, context)


def delete_client(request):
    if request.method == 'POST':

        client_id = int(request.POST['client_id'])

        client = Client.objects.get(id=client_id)

        if client.company.user == request.user:
            client.delete()

            messages.success(request, 'Deletado com sucesso!')

        else:
            messages.error(request, 'Sem permissão.')

    return redirect('/admin/general/client')


def list_card(request):
    template_name = 'card/list.html'

    instances = Card.objects.filter(client__company__user=request.user).filter(converted=0)

    context = {
        'instances': instances
    }

    return render(request, template_name, context)


def convert_card(request):
    if request.method == 'POST':
        card_id = request.POST['card_id']

        card = Card.objects.get(id=card_id)

        if datetime.datetime.now() > card.expire_at.replace(tzinfo=None):
            card.expired = 1
            card.reward = card.service.reward
            card.save()

            messages.error(request, 'Cartão expirado.')

        else:
            card.reward = card.service.reward
            card.filled = 1
            card.converted = 1
            card.converted_at = datetime.datetime.now()
            card.save()

            messages.success(request, 'Cartão convertido.')

    return redirect('/admin/genera/card')


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
        Service.objects.filter(id=pk).update(name=request.POST['name'], reward=request.POST['reward'])
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


def add_score(request):
    if request.method == 'POST':
        card_id = request.POST['card_id']

        card = Card.objects.get(id=card_id)

        if datetime.datetime.now() > card.expire_at.replace(tzinfo=None):
            card.expired = 1
            card.reward = card.service.reward
            card.save()

            messages.error(request, 'Cartão expirado.')

        else:
            times = int(request.POST['times'])
            scores = len(Score.objects.filter(card=card))
            score = Score(card=card)

            for x in range(times):

                if scores < card.configuration.limit:
                    score.save()
                else:
                    card.reward = card.service.reward
                    card.filled = 1
                    card.save()

                    messages.success(request, 'Cartão completo.')

                    expire_at = datetime.datetime.now() + datetime.timedelta(days=card.configuration.expire)

                    new_card = Card(expire_at=expire_at, company=card.company, client=card.client,
                                    service=card.service, configuration=card.configuration)

                    new_card.save()

                    card = new_card

                    score = Score(card=card)
                    score.save()

            if score.id:
                messages.success(request, 'Cadastrado com sucesso!')

    return redirect('/admin/general/card')
