import json
import time
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import app.models as my_models
from . import utils


def get_all_web(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    data = serializers.serialize(
        "json", my_models.Website.objects.all())
    data = json.loads(data)
    website_list = []
    for item in data:
        website_list.append(item["fields"])
    for item in website_list:
        item["url"] = item.pop("hostname")
    return utils.response_success_with_data("成功查询", website_list)


@csrf_exempt
def change_web_name(request):
    if request.method != 'POST':
        return utils.response_fail("MethodError", "不是POST请求")

    try:
        body = json.loads(request.body)
    except:
        return utils.response_fail("JSONError", "JSON格式有误")

    try:
        hostname = body["url"]
        name = body["name"]
        res = my_models.Website.objects.filter(
            hostname=hostname).update(name=name)
        if not res:
            return utils.response_fail("URLError", "URL错误")
        return utils.response_success("修改成功")
    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))


@csrf_exempt
def change_web_tag(request):
    if request.method != 'POST':
        return utils.response_fail("MethodError", "不是POST请求")

    try:
        body = json.loads(request.body)
    except:
        return utils.response_fail("JSONError", "JSON格式有误")

    try:
        hostname = body["url"]
        tags = body["tags"]
        res = my_models.Website.objects.filter(
            hostname=hostname).update(tags=tags)
        if not res:
            return utils.response_fail("URLError", "URL错误")
        return utils.response_success("修改成功")
    except Exception as err:
        return utils.response_fail(type(err).__name__, "repr(err)")
