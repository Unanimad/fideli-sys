from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from admin.general.models import *

from .utils import *


@csrf_exempt
def login(request):
    context = {}

    if request.method == 'POST':
        # phone = request.POST['phone']
        phone = '79 99999-9999'
        username = 'raphael'
        password = '16031994'

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                client = Client.objects.filter(phone=phone).values('id', 'name', 'phone')[0]

                context['client'] = client
                context['token'] = get_token(request)
            else:
                context['msg'] = 'Conta inativa.'
        else:
            context['msg'] = 'Usuário ou senha incorretos.'

    return dump_json(context)


def get_cards(request):
    # if request.method == 'POST':
    client_id = 7

    client = Client.objects.get(id=client_id)

    cards = Card.objects.filter(client=client).values('id', 'expire_at', 'service__reward').order_by('expire_at')

    return dump_json(cards)
