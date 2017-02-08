from json import dumps
from django.http import HttpResponse


def dump_json(json_list):

    json_data = dumps(json_list)

    return HttpResponse(json_data, content_type='application/json')
