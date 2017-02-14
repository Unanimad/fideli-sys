import datetime

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from .utils import *
from .forms import *


def list_company(request):
    template_name = 'company/list.html'

    instances = Company.objects.all()

    context = {
        'instances': instances
    }

    return render(request, template_name, context)


def add_company(request):

    if request.user.is_superuser:

        template_name = 'company/add.html'

        context = {}

        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            password = request.POST['password']
            image = request.FILES['image']

            user = User.objects.create_user(username=username, password=password, first_name=name)
            user.is_staff = True
            user.save()

            company = Company(name=name, user=user, image=image)
            company.token = create_token(name)

            company.save()

            messages.success(request, 'Cadastrado com sucesso!')

        context['form'] = CompanyForm(auto_id=False)
        context['form_user'] = UserForm(auto_id=False)

        return render(request, template_name, context)

    else:
        return redirect('/admin')


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

    card_form = CardForm(auto_id=False)
    card_form.fields["service"].queryset = Service.objects.filter(company__user=request.user)
    card_form.fields["configuration"].queryset = CardConfiguration.objects.filter(company__user=request.user)

    context['instances'] = instances
    context['form_card'] = card_form

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

        try:
            user = User.objects.create_user(phone, None, 123456)

            client = Client(name=name, phone=phone, user=user)
            client.save()
            client.company.add(company)
            client.save()

        except IntegrityError as e:
            user = User.objects.get(username=phone)

            client = Client.objects.get(user=user)
            client.company.add(company)
            client.save()

        if user.is_staff:
            messages.error(request, 'Favor informar outro número')

        else:

            if client.id:

                cards = Card.objects.filter(client=client).filter(service=service).order_by('-expire_at')

                if len(cards) > 0:

                    if cards[0].expired is False:
                        cards[0].expired = True
                        cards[0].save()

                expire_at = datetime.datetime.now() + datetime.timedelta(days=configuration.expire)

                card = Card(expire_at=expire_at, company=company, client=client,
                            service=service, configuration=configuration)

                card.reward = service.reward
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

        company = Company.objects.get(user=request.user)

        if client.company.all()[0].user == request.user:
            client.company.remove(company)

            messages.success(request, 'Deletado com sucesso!')

        else:
            messages.error(request, 'Sem permissão.')

    return redirect('/admin/general/client')


def list_card(request):
    template_name = 'card/list.html'

    instances = Card.objects.filter(client__company__user=request.user).filter(converted=0).filter(expired=0)

    context = {
        'instances': instances
    }

    return render(request, template_name, context)


def add_card(request):
    template_name = 'client/list.html'

    if request.method == 'POST':
        client_id = request.POST['client_id']
        service_id = request.POST['service']
        configuration_id = request.POST['configuration']

        company = Company.objects.get(user=request.user)
        client = Client.objects.get(id=client_id)
        service = Service.objects.get(id=service_id)
        configuration = CardConfiguration.objects.get(id=configuration_id)

        card = Card.objects.filter(client=client).filter(service=service).order_by('-expire_at')[0]

        card.expired = 1
        card.save()

        expire_at = datetime.datetime.now() + datetime.timedelta(days=configuration.expire)

        new_card = Card(expire_at=expire_at, company=company, client=client,
                        service=service, configuration=configuration)
        new_card.save()

        messages.success(request, 'Cadastrado com sucesso!')

    return render(request, template_name)


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
        reward = request.POST['reward']

        company = Company.objects.get(user=request.user)

        service = Service(name=name, reward=reward, company=company)
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
            post_times = request.POST['times']

            if post_times == '' or post_times < 1:
                times = 1
            else:
                times = int(post_times)

            score = Score(card=card)

            for x in range(times):

                scores = len(Score.objects.filter(card=card))
                score = Score(card=card)

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
