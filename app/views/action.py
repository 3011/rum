import json
import time
from django.core import serializers
import app.models as my_models
from . import utils


def user_action(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    try:
        hostname = request.GET.get("url")
        time_type = request.GET.get("timeType")
        data_type = request.GET.get("dataType")

        if data_type == "userAciton":
            res_data = get_user_action(hostname, time_type)
        elif data_type == "HTTPdata":
            res_data = get_http_data(hostname, time_type)
        else:
            return utils.response_fail("DataTypeError", "未知dataType")

        return utils.response_success_with_data("成功（测试接口）", res_data)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))


def get_user_action(hostname, time_type):

    filter_data = {"hostname": hostname}
    time_list = []
    res_data = []
    temp_list = []
    if time_type == "week":
        redundant_time = time.time() % (24*3600)
        week_ago = time.time() - 5*24*3600 - redundant_time
        filter_data["timestamp__gte"] = week_ago*1000
        for i in range(7):
            day = time.strftime(
                "%m-%d", time.localtime(week_ago+i*24*3600))
            time_list.append(day)
            res_data.append({"time": day, "pvCount": 0,
                            "uvCount": 0, "ipCount": 0})
            temp_list.append({"ip_list": [], "uv_list": []})
    elif time_type == "day":
        redundant_time = time.time() % 3600
        day_ago = time.time() - 23*3600 - redundant_time
        filter_data["timestamp__gte"] = day_ago*1000
        for i in range(24):
            hour = time.strftime(
                "%H:00", time.localtime(day_ago+i*3600))
            time_list.append(hour)
            res_data.append({"time": hour, "pvCount": 0,
                            "uvCount": 0, "ipCount": 0})
            temp_list.append({"ip_list": [], "uv_list": []})

    else:
        return utils.response_fail("TimeTypeError", "未知timeType")

    data = my_models.Performance.objects.filter(**filter_data)

    data = serializers.serialize("json", data)
    data = json.loads(data)

    for item in data:
        if time_type == "week":
            day = time.strftime(
                "%m-%d", time.localtime(item["fields"]["timestamp"]/1000))
            if day not in time_list:

                continue
            time_index = time_list.index(day)
            if item["fields"]["from_ip"] not in temp_list[time_index]["ip_list"]:
                temp_list[time_index]["ip_list"].append(
                    item["fields"]["from_ip"])
            if item["fields"]["from_ip"]+item["fields"]["full_ua"] not in temp_list[time_index]["uv_list"]:
                temp_list[time_index]["uv_list"].append(
                    item["fields"]["from_ip"]+item["fields"]["full_ua"])

            res_data[time_index]["count"] += 1
        elif time_type == "day":
            hour = time.strftime(
                "%H:00", time.localtime(item["fields"]["timestamp"]/1000))
            if hour not in time_list:

                continue
            time_index = time_list.index(hour)
            if item["fields"]["from_ip"] not in temp_list[time_index]["ip_list"]:
                temp_list[time_index]["ip_list"].append(
                    item["fields"]["from_ip"])
            if item["fields"]["from_ip"]+item["fields"]["full_ua"] not in temp_list[time_index]["uv_list"]:
                temp_list[time_index]["uv_list"].append(
                    item["fields"]["from_ip"]+item["fields"]["full_ua"])

    for i, n in enumerate(temp_list):
        res_data[i]["pvCount"] = len(n["ip_list"])
        res_data[i]["uvCount"] = len(n["uv_list"])
        res_data[i]["ipCount"] = len(n["ip_list"])

    return res_data


def get_http_data(hostname, time_type):
    filter_data = {"hostname": hostname}
    time_list = []
    res_data = []
    if time_type == "week":
        redundant_time = time.time() % (24*3600)
        week_ago = time.time() - 5*24*3600 - redundant_time
        filter_data["timestamp__gte"] = week_ago*1000
        for i in range(7):
            day = time.strftime(
                "%m-%d", time.localtime(week_ago+i*24*3600))
            time_list.append(day)
            res_data.append({"time": day, "HTTPCount": 0,
                            "HTTPFail": 0})
    elif time_type == "day":
        redundant_time = time.time() % 3600
        day_ago = time.time() - 23*3600 - redundant_time
        filter_data["timestamp__gte"] = day_ago*1000
        for i in range(24):
            hour = time.strftime(
                "%H:00", time.localtime(day_ago+i*3600))
            time_list.append(hour)
            res_data.append({"time": hour, "HTTPCount": 0,
                            "HTTPFail": 0})
    else:
        return utils.response_fail("TimeTypeError", "未知timeType")

    data = my_models.XhrError.objects.filter(**filter_data)

    data = serializers.serialize("json", data)
    data = json.loads(data)

    for item in data:
        if time_type == "week":
            day = time.strftime(
                "%m-%d", time.localtime(item["fields"]["timestamp"]/1000))
            if day not in time_list:
                continue
            time_index = time_list.index(day)
            res_data[time_index]["HTTPCount"] += 1
            if "200" not in item["fields"]["status"]:
                res_data[time_index]["HTTPFail"] += 1

        elif time_type == "day":
            hour = time.strftime(
                "%H:00", time.localtime(item["fields"]["timestamp"]/1000))
            if hour not in time_list:
                continue
            time_index = time_list.index(hour)
            res_data[time_index]["HTTPCount"] += 1
            if "200" not in item["fields"]["status"]:
                res_data[time_index]["HTTPFail"] += 1

    return res_data
