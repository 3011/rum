from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import app.models as my_models
from urllib.parse import urlparse
import json
import time


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


@csrf_exempt
def post_err(request):
    if request.method != 'POST':
        return response_fail("MethodError", "不是POST请求")

    try:
        body = json.loads(request.body)
    except:
        return response_fail("JSONError", "JSON格式有误")

    #  TODO: JSON数据校验
    try:

        pub_data = {
            "title": body["title"],
            "url": body["url"],
            # 通过url提取hostname
            "hostname": url_to_hostname(body["url"]),
            "timestamp": body["timestamp"],
            "full_ua": body["userAgent"]["full"],
            "browser_name": body["userAgent"]["name"],
            "browse_version": body["userAgent"]["version"],
            "os": body["userAgent"]["os"],
            "message": body["message"],
            # "error_type": body["type"],
            # "kind": body["kind"],
        }

        error_type = body["errorType"]
        if error_type == "jsError":
            new_Error = my_models.JSError(
                position=body["position"],
                stack=body["stack"],
                selector=body["selector"],
                **pub_data,
            )

        elif error_type == "promiseError":
            new_Error = my_models.PromiseError(
                stack=body["stack"],
                selector=body["selector"],
                **pub_data,
            )

        elif error_type == "resourceError":
            new_Error = my_models.ResourceError(
                filename=body["filename"],
                tag_name=body["tagName"],
                position=body["position"],
                selector=body["selector"],
                **pub_data,
            )

        elif error_type == "xhrError":
            new_Error = my_models.XhrError(
                status=body["status"],
                duration=body["duration"],
                response=body["response"],
                params=body["params"],
                **pub_data,
            )

        elif error_type == "whiteScreenError":
            new_Error = my_models.WhiteScreenError(
                empty_points=body["emptyPoints"],
                screen=body["screen"],
                view_point=body["viewPoint"],
                selector=body["selector"],
                **pub_data,
            )

        else:
            return response_fail("TypeError", "未知类型")

        new_Error.save()  # 保存至数据库
        create_website(url_to_hostname(body["url"]))  # 包括端口
        return response_success("成功")

    except Exception as err:
        return response_fail(type(err).__name__, repr(err))


@csrf_exempt
def post_performance(request):
    if request.method != 'POST':
        return response_fail("MethodError", "不是POST请求")

    try:
        body = json.loads(request.body)
    except:
        return response_fail("JSONError", "JSON格式有误")

    #  TODO: JSON数据校验
    try:
        # 获取来源ip
        if "HTTP_X_FORWARDED_FOR" in request.META:
            from_ip = request.META["HTTP_X_FORWARDED_FOR"].split(',')[0]
        else:
            from_ip = request.META["REMOTE_ADDR"]

        data = {
            "title": body["title"],
            "url": body["url"],
            "hostname": url_to_hostname(body["url"]),
            "from_ip": from_ip,
            "timestamp": body["timestamp"],
            "full_ua": body["userAgent"]["full"],
            "browser_name": body["userAgent"]["name"],
            "browse_version": body["userAgent"]["version"],
            "os": body["userAgent"]["os"],
            # "error_type": body["type"],
            # "kind": body["kind"],

            "dns": body["DNSTime"],
            "connect": body["connectTime"],
            "ttfb": body["ttfbTime"],
            "response": body["responseTime"],
            "parse_dom": body["parseDOMTime"],
            "dom_ready": body["DOMReady"],
            "ttfb": body["ttfbTime"],
            "dom_content_loaded": body["domContentLoadedTime"],
            "to_interactive": body["timeToInteractive"],
            "load": body["loadTime"],
            "first_paint": body["firstPaint"],
            "first_content_paint": body["firstContentPaint"],
            "first_meaningful_paint": body["firstMeaningfulPaint"],
            "largest_contentful_paint": body["largestContentfulPaint"],
        }

        my_models.Performance(**data).save()
        create_website(url_to_hostname(body["url"]))
        return response_success("成功")

    except Exception as err:
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
        return response_fail_with_data("TypeError",     "未知类型")

    data = json.loads(data)
    return response_success_with_data("成功（测试接口）", data)


def get_website_list(request):
    if request.method != 'GET':
        return response_fail("MethodError", "不是GET请求")

    data = serializers.serialize(
        "json", my_models.Website.objects.all())
    data = json.loads(data)
    website_list = []
    for item in data:
        website_list.append(item["fields"])
    return response_success_with_data("成功（测试接口）", website_list)
