# import json
# import time
# from django.core import serializers
# from django.views.decorators.csrf import csrf_exempt
# import app.models as my_models
# from . import utils


# def web_error(request):
#     if request.method != 'GET':
#         return utils.response_fail("MethodError", "不是GET请求")

#     try:
#         hostname = request.GET.get("url")
#         time_type = request.GET.get("timeType")
#         data_type = request.GET.get("dataType")

#         filter_data = {"hostname": hostname}
#         time_list = []
#         if time_type == "week":
#             redundant_time = time.time() % (24*3600)
#             week_ago = time.time() - 6*24*3600 - redundant_time
#             filter_data["timestamp__gte"] = week_ago*1000
#             for i in range(7):
#                 day = time.strftime(
#                     "%m-%d", time.localtime(week_ago+i*24*3600))
#                 time_list.append({"time": day, "http_count": 0})
#         elif time_type == "day":
#             redundant_time = time.time() % 3600
#             day_ago = time.time() - 23*3600 - redundant_time
#             filter_data["timestamp__gte"] = day_ago*1000
#             for i in range(24):
#                 hour = time.strftime(
#                     "%H:00", time.localtime(day_ago+i*3600))
#                 time_list.append({"time": hour, "count": 0})
#         else:
#             return utils.response_fail("TimeTypeError", "未知timeType")

#         data = my_models.Performance.objects.filter(**filter_data)
#         res_data = utils.get_traffic_data(data)

#         data = serializers.serialize("json", data)
#         data = json.loads(data)
#         res_data = []

#         for item in data:
#             if time_type == "week":
#                 day = time.strftime(
#                     "%m-%d", time.localtime(item["fields"]["timestamp"]/1000))
#                 if day not in time_list:
#                     print("day not in time_list")
#                     continue
#                 day_index = time_list.index(day)
#                 res_data[day_index]["count"] += 1
#             elif time_type == "day":
#                 hour = time.strftime(
#                     "%H:00", time.localtime(item["fields"]["timestamp"]/1000))
#                 if hour not in time_list:
#                     print("day not in time_list")
#                     continue
#                 day_index = time_list.index(hour)
#                 res_data[day_index]["count"] += 1

#         return utils.response_success_with_data("成功（测试接口）", res_data)

#     except Exception as err:
#         return utils.response_fail(type(err).__name__, repr(err))
