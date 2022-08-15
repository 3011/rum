import json
import time
from django.http import HttpResponse
from urllib.parse import urlparse
import app.models as my_models


def response_success(msg):
    return HttpResponse(json.dumps({"ok": 1, "err_type": "", "msg": msg}, ensure_ascii=False), content_type='application/json')


def response_fail(err_type, msg):
    return HttpResponse(json.dumps({"ok": 0, "err_type": err_type, "msg": msg}, ensure_ascii=False), content_type='application/json')


def response_success_with_data(msg, data):
    return HttpResponse(json.dumps({"ok": 1, "err_type": "", "msg": msg, "data": data}, ensure_ascii=False), content_type='application/json')


def response_fail_with_data(err_type, msg):
    return HttpResponse(json.dumps({"ok": 0, "err_type": err_type, "msg": msg, "data": []}, ensure_ascii=False), content_type='application/json')


# 通过url提取hostname
def url_to_hostname(url):
    return urlparse(url).hostname


# 维护网站列表
def create_website(hostname):
    website = my_models.Website.objects.filter(hostname=hostname)
    if not website.exists():
        now_timestamp = int(time.time()*1000)
        my_models.Website(hostname=hostname, create_time=now_timestamp).save()
