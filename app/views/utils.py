import json
import time
from django.http import HttpResponse
from django.core import serializers
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
def create_website(hostname, name):
    website = my_models.Website.objects.filter(hostname=hostname)
    if not website.exists():
        now_timestamp = int(time.time()*1000)
        my_models.Website(hostname=hostname,
                          create_time=now_timestamp, name=name).save()


def format_errors(errors):
    data = serializers.serialize("json", errors)
    data = json.loads(data)
    data_list = []
    for item in data:
        data_list.append(item["fields"])
    return {
        "count": errors.count(),
        "data": data_list
    }


def get_traffic_data(data):
    data = serializers.serialize("json", data)
    data = json.loads(data)
    from_ip_list = []
    uv_list = []
    # data_list = []
    for item in data:
        # data_list.append(item["fields"])
        if item["fields"]["from_ip"] not in from_ip_list:
            from_ip_list.append(item["fields"]["from_ip"])
        if item["fields"]["from_ip"]+item["fields"]["full_ua"] not in uv_list:
            uv_list.append(
                item["fields"]["from_ip"]+item["fields"]["full_ua"])

    return {
        "ip": len(from_ip_list),
        "uv": len(uv_list),
        "pv": len(data)
    }


def get_time_list(time_type):
    time_list = []
    if time_type == "week":
        for i in range(7):
            time_list.insert(0, time.strftime(
                "%Y-%m-%d", time.localtime(time.time() - i*24*3600)))
    elif time_type == "day":
        for i in range(24):
            time_list.insert(0, time.strftime(
                "%H:00", time.localtime(time.time() - i*3600)))
    return time_list
