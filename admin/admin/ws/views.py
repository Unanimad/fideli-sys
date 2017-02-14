from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from admin.general.models import *

from .utils import *


@csrf_exempt
def login(request):
    context = {
        'status': 0
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                client = Client.objects.get(user=user)

                context['name'] = client.name
                context['username'] = username
                context['status'] = 1

            else:
                context['msg'] = 'Conta inativa.'
        else:
            context['msg'] = 'Usuário ou senha incorretos.'

    return dump_json(context)


@csrf_exempt
def get_cards(request):
    if request.method == 'POST':
        username = request.POST['username']
        token = request.POST['token']
        company = Company.objects.get(token=token)

        client = Client.objects.get(user__username=username)

        cards = list(
            Card.objects
                .filter(client=client)
                .filter(company=company)
                .values('id', 'expire_at', 'service__reward', 'configuration__limit')
                .order_by('expire_at')
        )

        for card in cards:
            expire_at = card['expire_at']
            card['total'] = len(Score.objects.filter(card__id=card['id']))
            card['expire_at'] = str(expire_at.day) + '/' + str(expire_at.month) + '/' + str(expire_at.year)

    return dump_json(cards)


@csrf_exempt
def get_card(request):
    if request.method == 'POST':
        card_id = request.POST['card_id']

        card = Card.objects.get(id=card_id)
        scores = list(Score.objects.filter(card=card).values('created_at'))

        for score in scores:
            score['created_at'] = str(score['created_at'].day) + '/' \
                                  + str(score['created_at'].month) + '/' \
                                  + str(score['created_at'].year)

        context = {
            'limit': card.configuration.limit,
            'scores': scores
        }

    return dump_json(context)


@csrf_exempt
def edit(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.get(username=username)
        user.set_password(password)

        client = Client.objects.get(user=user)
        client.name = name
        client.save()

        user.username = username
        user.save()

        context = {
            'name': name,
            'msg': 'Atualizado com sucesso!',
        }

        return dump_json(context)
