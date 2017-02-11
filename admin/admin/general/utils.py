import hashlib

from .models import *


def create_token(name):
    token = hashlib.sha1()

    str_company = name + 'india'

    token.update(str_company.encode('utf-8'))

    return token.hexdigest()


def check_company(token):
    company = Company.objects.get(token=token)

    if company.user.is_active:
        return True
    else:
        return False
