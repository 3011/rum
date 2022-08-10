# from django.shortcuts import render
from email.policy import default
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import app.models as my_models
import json
import time


def response_success(msg):
    return HttpResponse(json.dumps({"ok": 1, "err_type": "", "msg": msg}, ensure_ascii=False))


def response_fail(err_type, msg):
    return HttpResponse(json.dumps({"ok": 0, "err_type": err_type, "msg": msg}, ensure_ascii=False))


def response_success_with_data(msg, data):
    return HttpResponse(json.dumps({"ok": 1, "err_type": "", "msg": msg, "data": data}, ensure_ascii=False))


def response_fail_with_data(err_type, msg):
    return HttpResponse(json.dumps({"ok": 0, "err_type": err_type, "msg": msg, "data": []}, ensure_ascii=False))


@csrf_exempt
def post_err(request):
    if request.method != 'POST':
        return response_fail("MethodError", "不是POST请求")

    try:
        json_data = json.loads(request.body)
    except:
        return response_fail("JSONError", "JSON格式有误")

    #  TODO: JSON数据校验
    try:

        pub_data = {
            "title": json_data["title"],
            "url": json_data["url"],
            "timestamp": json_data["timestamp"],
            "full_ua": json_data["userAgent"]["full"],
            "browser_name": json_data["userAgent"]["name"],
            "browse_version": json_data["userAgent"]["version"],
            "os": json_data["userAgent"]["os"],
            "message": json_data["message"],
            # "error_type": json_data["type"],
            # "kind": json_data["kind"],
        }

        if json_data["errorType"] == "jsError":
            new_Error = my_models.JSError(
                position=json_data["position"],
                stack=json_data["stack"],
                selector=json_data["selector"],
                **pub_data,
            )
            new_Error.save()  # 保存至数据库

        elif json_data["errorType"] == "promiseError":
            new_Error = my_models.PromiseError(
                stack=json_data["stack"],
                selector=json_data["selector"],
                **pub_data,
            )
            new_Error.save()  # 保存至数据库

        elif json_data["errorType"] == "resourceError":
            new_Error = my_models.ResourceError(
                filename=json_data["filename"],
                tag_name=json_data["tagName"],
                position=json_data["position"],
                selector=json_data["selector"],
                **pub_data,
            )
            new_Error.save()  # 保存至数据库

        elif json_data["errorType"] == "xhrError":
            new_Error = my_models.XhrError(
                status=json_data["status"],
                duration=json_data["duration"],
                response=json_data["response"],
                params=json_data["params"],
                **pub_data,
            )
            new_Error.save()  # 保存至数据库

        elif json_data["errorType"] == "whiteScreenError":
            new_Error = my_models.WhiteScreenError(
                empty_points=json_data["emptyPoints"],
                screen=json_data["screen"],
                view_point=json_data["viewPoint"],
                selector=json_data["params"],
                **pub_data,
            )
            new_Error.save()  # 保存至数据库

        else:
            return response_fail("TypeError", "未知类型")

        return response_success("成功")

    except Exception as err:
        print(err)
        return response_fail(type(err).__name__, repr(err))


def get_all_err(request):
    if request.method != 'GET':
        return response_fail("MethodError", "不是GET请求")

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
        return response_fail_with_data("TypeError", "未知类型")

    data = json.loads(data)
    return response_success_with_data("成功（测试接口）", data)

# def get_err_by_browser_name
