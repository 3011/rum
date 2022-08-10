# from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from app.models import Error
import json


def response_success(msg):
    return HttpResponse(json.dumps({"ok": 1, "err_type": "", "msg": msg}, ensure_ascii=False))


def response_fail(err_type, msg):
    return HttpResponse(json.dumps({"ok": 0, "err_type": err_type, "msg": msg}, ensure_ascii=False))


def response_success_with_data(msg, data):
    return HttpResponse(json.dumps({"ok": 1, "err_type": "", "msg": msg, "data": data}, ensure_ascii=False))


@csrf_exempt
def post_err(request):
    if request.method != 'POST':
        return response_fail("MethodError", "不是POST请求")

    try:
        json_data = json.loads(request.body)
        print(json_data)
    except:
        return response_fail("JSONError", "JSON格式有误")

    #  TODO: JSON数据校验
    try:
        newErr = Error(title=json_data["title"],
                       url=json_data["url"],
                       timestamp=json_data["timestamp"],
                       full_ua=json_data["userAgent"]["full"],
                       browser_name=json_data["userAgent"]["name"],
                       browse_version=json_data["userAgent"]["version"],
                       os=json_data["userAgent"]["os"],

                       error_type=json_data["errorType"],
                       kind=json_data["kind"],
                       message=json_data["message"],
                       position=json_data["position"],
                       stack=json_data["stack"],
                       selector=json_data["selector"],
                       )
        newErr.save()  # 保存至数据库
        return response_success("成功")
    except Exception as err:
        return response_fail(type(err).__name__, repr(err))


def get_all_err(request):
    if request.method != 'GET':
        return response_fail("MethodError", "不是GET请求")

    data = serializers.serialize("json", Error.objects.all())
    data = json.loads(data)
    return response_success_with_data("成功（测试接口）", data)
