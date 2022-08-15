import json
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
