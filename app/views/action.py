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

        if data_type == "userAction":
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
    now = time.time()
    if time_type == "week":
        for i in range(7):
            day = time.strftime("%m-%d", time.localtime(now))
            time_list.insert(0, day)
            res_data.insert(0, {"time": day, "pvCount": 0,
                            "uvCount": 0, "ipCount": 0})
            temp_list.insert(0, {"ip_list": [], "uv_list": []})
            now = now - 24*3600
        filter_data["timestamp__gte"] = (now+16*3600-now % (24*3600))*1000
    elif time_type == "day":
        for i in range(24):
            hour = time.strftime("%H:00", time.localtime(now))
            time_list.insert(0, hour)
            res_data.insert(0, {"time": hour, "pvCount": 0,
                            "uvCount": 0, "ipCount": 0})
            temp_list.insert(0, {"ip_list": [], "uv_list": []})
            now = now - 3600
        filter_data["timestamp__gte"] = (now+3600-now % (3600))*1000
    else:
        return utils.response_fail("TimeTypeError", "未知timeType")

    pv_data = my_models.PV.objects.filter(**filter_data)
    # uv_data = my_models.UV.objects.filter(**filter_data)

    pv_data = serializers.serialize("json", pv_data)
    pv_data = json.loads(pv_data)
    # uv_data = serializers.serialize("json", uv_data)
    # uv_data = json.loads(uv_data)

    for item in pv_data:
        if time_type == "week":
            day = time.strftime(
                "%m-%d", time.localtime(item["fields"]["timestamp"]/1000))
            if day not in time_list:
                continue
            time_index = time_list.index(day)
            res_data[time_index]["pvCount"] += 1

            ####
            if item["fields"]["ip"]+item["fields"]["full_ua"] not in temp_list[time_index]["uv_list"]:
                temp_list[time_index]["uv_list"].append(
                    item["fields"]["ip"]+item["fields"]["full_ua"])
            if item["fields"]["ip"] not in temp_list[time_index]["ip_list"]:
                temp_list[time_index]["ip_list"].append(
                    item["fields"]["ip"])

        elif time_type == "day":
            hour = time.strftime(
                "%H:00", time.localtime(item["fields"]["timestamp"]/1000))
            if hour not in time_list:
                continue
            time_index = time_list.index(hour)
            res_data[time_index]["pvCount"] += 1

            ####
            if item["fields"]["ip"]+item["fields"]["full_ua"] not in temp_list[time_index]["uv_list"]:
                temp_list[time_index]["uv_list"].append(
                    item["fields"]["ip"]+item["fields"]["full_ua"])
            if item["fields"]["ip"] not in temp_list[time_index]["ip_list"]:
                temp_list[time_index]["ip_list"].append(
                    item["fields"]["ip"])

    # for item in uv_data:
    #     if time_type == "week":
    #         day = time.strftime(
    #             "%m-%d", time.localtime(item["fields"]["timestamp"]/1000))
    #         if day not in time_list:
    #             continue
    #         time_index = time_list.index(day)

    #         if item["fields"]["ip"]+item["fields"]["full_ua"] not in temp_list[time_index]["uv_list"]:
    #             temp_list[time_index]["uv_list"].append(
    #                 item["fields"]["ip"]+item["fields"]["full_ua"])
    #         if item["fields"]["ip"] not in temp_list[time_index]["ip_list"]:
    #             temp_list[time_index]["ip_list"].append(
    #                 item["fields"]["ip"])

    #     elif time_type == "day":
    #         hour = time.strftime(
    #             "%H:00", time.localtime(item["fields"]["timestamp"]/1000))
    #         if hour not in time_list:
    #             continue
    #         time_index = time_list.index(hour)

    #         if item["fields"]["ip"]+item["fields"]["full_ua"] not in temp_list[time_index]["uv_list"]:
    #             temp_list[time_index]["uv_list"].append(
    #                 item["fields"]["ip"]+item["fields"]["full_ua"])
    #         if item["fields"]["ip"] not in temp_list[time_index]["ip_list"]:
    #             temp_list[time_index]["ip_list"].append(
    #                 item["fields"]["ip"])

    for i, n in enumerate(temp_list):
        res_data[i]["uvCount"] = len(n["uv_list"])
        res_data[i]["ipCount"] = len(n["ip_list"])

    return res_data


def get_http_data(hostname, time_type):
    filter_data = {"hostname": hostname}
    time_list = []
    res_data = []
    now = time.time()
    if time_type == "week":
        for i in range(7):
            day = time.strftime("%m-%d", time.localtime(now))
            time_list.insert(0, day)
            res_data.insert(0, {"time": day, "HTTPCount": 0,
                            "HTTPFail": 0})
            now = now - 24*3600
        filter_data["timestamp__gte"] = (now+16*3600-now % (24*3600))*1000
    elif time_type == "day":
        for i in range(24):
            hour = time.strftime("%H:00", time.localtime(now))
            time_list.insert(0, hour)
            res_data.insert(0, {"time": hour, "HTTPCount": 0,
                            "HTTPFail": 0})
            now = now - 3600
        filter_data["timestamp__gte"] = (now+3600-now % (3600))*1000
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


def get_list(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    try:
        hostname = request.GET.get("url")
        data_type = request.GET.get("dataType")

        if data_type == "pv":
            data = my_models.PV.objects.filter(hostname=hostname)
        elif data_type == "uv":
            data = my_models.UV.objects.filter(hostname=hostname)
        elif data_type == "duration":
            data = my_models.Duration.objects.filter(hostname=hostname)
        else:
            return utils.response_fail("DataTypeError", "未知dataType")

        data = utils.format_errors(data)
        return utils.response_success_with_data("成功", data)

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))
