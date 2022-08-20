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

        js_error = my_models.JSError.objects.filter(**filter_data)
        promise_error = my_models.PromiseError.objects.filter(**filter_data)
        resource_error = my_models.ResourceError.objects.filter(**filter_data)
        xhr_error = my_models.XhrError.objects.filter(**filter_data)
        white_screen_error = my_models.WhiteScreenError.objects.filter(
            **filter_data)

        errors = {"js_error": utils.utils.format_errors(js_error),
                  "promise_error": utils.format_errors(promise_error),
                  "resource_error": utils.format_errors(resource_error),
                  "xhr_error": utils.format_errors(xhr_error),
                  "white_screen_error": utils.format_errors(white_screen_error),
                  }

        return utils.response_success_with_data("成功（测试接口）", errors)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))


def get_traffic(request):
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
                (time.time()-int(timelimit)*60*60)*1000)  # 获取n小时前的时间戳

        data = my_models.Performance.objects.filter(**filter_data)
        res_data = utils.get_traffic_data(data)

        return utils.response_success_with_data("成功（测试接口）", res_data)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))


def get_performance(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    # try:
    hostname = request.GET.get("hostname", default="")

    if hostname == "":
        return utils.response_fail("HostnameError", "hostname为空")

    filter_data = {
        "hostname": hostname,
        "timestamp__gte": int((time.time()-7*24*60*60)*1000)  # 7天前的时间戳
    }

    data = my_models.Performance.objects.filter(**filter_data)
    res_data = [get_performance_24h(data),
                get_performance_7d(data)]

    return utils.response_success_with_data("成功（测试接口）", res_data)

    # except Exception as err:
    #     return utils.response_fail(type(err).__name__, repr(err))


def get_performance_24h(data):
    data = serializers.serialize("json", data)
    data = json.loads(data)

    res_data = {}
    now = time.time()
    for i in range(23, -1, -1):
        res_data[time.strftime("%H:00", time.localtime(now-i*60*60))] = {
            "count": 0,
            "dns": 0,
            "connect": 0,
            "ttfb": 0,
            "response": 0,
            "parse_dom": 0,
            "dom_ready": 0,
            "dom_content_loaded": 0,
            "to_interactive": 0,
            "load": 0,
            "first_paint": 0,
            "first_content_paint": 0,
            "first_meaningful_paint": 0,
            "largest_contentful_paint": 0
        }

    for item in data:
        hour = time.strftime("%H:00", time.localtime(
            item["fields"]["timestamp"]/1000))

        for key in res_data[hour]:
            if key == "count":
                res_data[hour][key] += 1
                continue
            res_data[hour][key] += item["fields"][key]

    for key in res_data:
        for k in res_data[key]:
            if k == "count":
                if res_data[key][k] == 0:
                    break
                continue
            res_data[key][k] = round(
                res_data[key][k]/res_data[key]["count"], 3)
    res_data["type"] = "24h"
    return res_data


def get_performance_7d(data):
    data = serializers.serialize("json", data)
    data = json.loads(data)

    res_data = []
    time_list = []
    now = time.time()
    for i in range(6, -1, -1):
        day = time.strftime(
            "%m-%d", time.localtime(now-i*24*60*60))
        time_list.append(day)
        res_data.append({
            "name": day,
            "type": "7d",
            "count": 0,
            "dns": 0,
            "connect": 0,
            "ttfb": 0,
            "response": 0,
            "parse_dom": 0,
            "dom_ready": 0,
            "dom_content_loaded": 0,
            "to_interactive": 0,
            "load": 0,
            "first_paint": 0,
            "first_content_paint": 0,
            "first_meaningful_paint": 0,
            "largest_contentful_paint": 0
        })

    for item in data:
        day = time.strftime("%m-%d", time.localtime(
            item["fields"]["timestamp"]/1000))

        if day not in time_list:
            continue

        day_index = time_list.index(day)
        for key in res_data[day_index]:
            if key in ("name", "type"):
                continue
            if key == "count":
                res_data[day_index][key] += 1
                continue
            res_data[day_index][key] += item["fields"][key]

    for key in res_data:
        for k in key:
            if k in ("name", "type"):
                continue
            if k == "count":
                if key[k] == 0:
                    break
                continue
            key[k] = round(
                key[k]/key["count"], 3)

    # retrun_data = {
    #     "type": "7d",
    #     "count": 0,
    #     "name": [],
    #     "dns": [],
    #     "connect": [],
    #     "ttfb": [],
    #     "response": [],
    #     "parse_dom": [],
    #     "dom_ready": [],
    #     "dom_content_loaded": [],
    #     "to_interactive": [],
    #     "load": [],
    #     "first_paint": [],
    #     "first_content_paint": [],
    #     "first_meaningful_paint": [],
    #     "largest_contentful_paint": []
    # }

    # for key in res_data:
    #     retrun_data["name"].append(key)
    #     for k in retrun_data:
    #         if k in ("name", "type"):
    #             continue
    #         if k == "count":
    #             retrun_data[k] += 1
    #             continue
    #         retrun_data[k].append(res_data[key][k])
    return res_data
