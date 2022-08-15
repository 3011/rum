import json
import time
from django.core import serializers
import app.models as my_models
from . import utils


def get_all_err(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    error_type = request.GET.get("errortype", default="")

    if error_type == "jsError":
        data = serializers.serialize("json", my_models.JSError.objects.all())

    elif error_type == "promiseError":
        data = serializers.serialize(
            "json", my_models.PromiseError.objects.all())

    elif error_type == "resourceError":
        data = serializers.serialize(
            "json", my_models.ResourceError.objects.all())

    elif error_type == "xhrError":
        data = serializers.serialize("json", my_models.XhrError.objects.all())

    elif error_type == "whiteScreenError":
        data = serializers.serialize(
            "json", my_models.WhiteScreenError.objects.all())

    else:
        return utils.response_fail_with_data("TypeError",     "未知类型")

    data = json.loads(data)
    return utils.response_success_with_data("成功（测试接口）", data)


def get_website_list(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    data = serializers.serialize(
        "json", my_models.Website.objects.all())
    data = json.loads(data)
    website_list = []
    for item in data:
        website_list.append(item["fields"])
    return utils.response_success_with_data("成功（测试接口）", website_list)


def get_errors(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    try:
        hostname = request.GET.get("hostname", default="")
        timelimit = request.GET.get("time", default="")
        if hostname == "":
            return utils.response_fail("HostnameError", "hostname为空")

        filter_data = {
            "hostname": hostname,
        }
        if timelimit != "":
            filter_data["timestamp__gte"] = int(
                (time.time()-int(timelimit)*60*60)*1000)
        # print(int((time.time()-24*60*60)*1000))
        print(filter_data)
        js_error = my_models.JSError.objects.filter(**filter_data)
        promise_error = my_models.PromiseError.objects.filter(**filter_data)
        resource_error = my_models.ResourceError.objects.filter(**filter_data)
        xhr_error = my_models.XhrError.objects.filter(**filter_data)
        white_screen_error = my_models.WhiteScreenError.objects.filter(
            **filter_data)

        errors = {"js_error": q1(js_error),
                  "promise_error": q1(promise_error),
                  "resource_error": q1(resource_error),
                  "xhr_error": q1(xhr_error),
                  "white_screen_error": q1(white_screen_error),
                  }

        return utils.response_success_with_data("成功（测试接口）", errors)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))


def q1(a):
    data = serializers.serialize("json", a)
    data = json.loads(data)
    data_list = []
    for item in data:
        data_list.append(item["fields"])
    return {
        "count": a.count(),
        "data": data_list
    }
