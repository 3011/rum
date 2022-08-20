import json
import time
from django.core import serializers
import app.models as my_models
from . import utils


def timing(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    try:
        hostname = request.GET.get("url")
        time_type = request.GET.get("timeType")
        data_type = request.GET.get("dataType")

        if data_type == "timing":
            res_data = get_timing(hostname, time_type)
        else:
            return utils.response_fail("DataTypeError", "未知dataType")
        return utils.response_success_with_data("成功", res_data)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))


def get_timing(hostname, time_type):
    filter_data = {"hostname": hostname}
    time_list = []
    if time_type == "week":
        redundant_time = time.time() % (24*3600)
        week_ago = time.time() - 6*24*3600 - redundant_time
        filter_data["timestamp__gte"] = week_ago*1000
        for i in range(7):
            day = time.strftime(
                "%m-%d", time.localtime(week_ago+i*24*3600))
            time_list.append(day)
    elif time_type == "day":
        redundant_time = time.time() % 3600
        day_ago = time.time() - 23*3600 - redundant_time
        filter_data["timestamp__gte"] = day_ago*1000
        for i in range(24):
            hour = time.strftime(
                "%H:00", time.localtime(day_ago+i*3600))
            time_list.append(hour)
    else:
        return utils.response_fail("TimeTypeError", "未知timeType")

    data = my_models.Performance.objects.filter(**filter_data)

    if time_type == "week":
        res_data = get_performance_7d(data, time_list)
    elif time_type == "day":
        res_data = get_performance_24h(data, time_list)

    return res_data


def get_performance_24h(data, time_list):
    data = serializers.serialize("json", data)
    data = json.loads(data)

    res_data = []
    for item in time_list:
        res_data.append({
            "time": item,
            "type": "7d",
            "count": 0,
            "dns": 0,
            # "connect": 0,
            # "ttfb": 0,
            # "response": 0,
            # "parse_dom": 0,
            "dom_ready": 0,
            # "dom_content_loaded": 0,
            # "to_interactive": 0,
            "load": 0,
            "first_paint": 0,
            "first_content_paint": 0,
            # "first_meaningful_paint": 0,
            "largest_contentful_paint": 0
        })

    for item in data:
        hour = time.strftime("%H:00", time.localtime(
            item["fields"]["timestamp"]/1000))

        if hour not in time_list:
            continue

        hour_index = time_list.index(hour)
        for key in res_data[hour_index]:
            if key in ("time", "type"):
                continue
            if key == "count":
                res_data[hour_index][key] += 1
                continue
            res_data[hour_index][key] += item["fields"][key]

    for key in res_data:
        for k in key:
            if k in ("time", "type"):
                continue
            if k == "count":
                if key[k] == 0:
                    break
                continue
            key[k] = round(
                key[k]/key["count"], 3)

    return res_data


def get_performance_7d(data, time_list):
    data = serializers.serialize("json", data)
    data = json.loads(data)

    res_data = []
    for item in time_list:
        res_data.append({
            "time": item,
            "type": "7d",
            "count": 0,
            "dns": 0,
            # "connect": 0,
            # "ttfb": 0,
            # "response": 0,
            # "parse_dom": 0,
            "dom_ready": 0,
            # "dom_content_loaded": 0,
            # "to_interactive": 0,
            "load": 0,
            "first_paint": 0,
            "first_content_paint": 0,
            # "first_meaningful_paint": 0,
            "largest_contentful_paint": 0
        })

    for item in data:
        day = time.strftime("%m-%d", time.localtime(
            item["fields"]["timestamp"]/1000))

        if day not in time_list:
            continue

        day_index = time_list.index(day)
        for key in res_data[day_index]:
            if key in ("time", "type"):
                continue
            if key == "count":
                res_data[day_index][key] += 1
                continue
            res_data[day_index][key] += item["fields"][key]

    for key in res_data:
        for k in key:
            if k in ("time", "type"):
                continue
            if k == "count":
                if key[k] == 0:
                    break
                continue
            key[k] = round(
                key[k]/key["count"], 3)

    return res_data


def time_list(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    try:
        hostname = request.GET.get("url")
        data = my_models.Performance.objects.filter(hostname=hostname)
        data = utils.format_errors(data)
        return utils.response_success_with_data("成功", data)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))
