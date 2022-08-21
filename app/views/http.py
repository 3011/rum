import json
from django.core import serializers
import app.models as my_models
from . import utils


def error_list(request):
    if request.method != 'GET':
        return utils.response_fail("MethodError", "不是GET请求")

    try:
        hostname = request.GET.get("url")
        data = my_models.XhrError.objects.filter(hostname=hostname)
        data = serializers.serialize("json", data)
        data = json.loads(data)
        data_list = []
        count = 0
        for item in data:
            if "200" not in item["fields"]["status"]:
                data_list.append(item["fields"])
                count += 1

        return utils.response_success_with_data("成功", {"count": count, "data": data_list})

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))
