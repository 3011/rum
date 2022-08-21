
import json
from django.views.decorators.csrf import csrf_exempt
from . import utils
import app.models as my_models


def post_err(body):
    pub_data = {
        "title": body["title"],
        "url": body["url"],
        # 通过url提取hostname
        "hostname": utils.url_to_hostname(body["url"]),
        "timestamp": body["timestamp"],
        "full_ua": body["userAgent"]["full"],
        "browser_name": body["userAgent"]["name"],
        "browse_version": body["userAgent"]["version"],
        "os": body["userAgent"]["os"],
        # "error_type": body["type"],
        # "kind": body["kind"],
    }

    error_type = body["errorType"]
    if error_type == "jsError":
        new_Error = my_models.JSError(
            message=body["message"],
            position=body["position"],
            stack=body["stack"],
            selector=body["selector"],
            **pub_data,
        )

    elif error_type == "PromiseError":
        new_Error = my_models.PromiseError(
            message=body["message"],
            stack=body["stack"],
            selector=body["selector"],
            **pub_data,
        )

    elif error_type == "resourceError":
        new_Error = my_models.ResourceError(
            message=body["message"],
            filename=body["filename"],
            tag_name=body["tagName"],
            # position=body["position"],
            selector=body["selector"],
            **pub_data,
        )

    elif error_type == "whiteScreenError":
        new_Error = my_models.WhiteScreenError(
            # message=body["message"],
            empty_points=body["emptyPoints"],
            screen=body["screen"],
            view_point=body["viewPoint"],
            selector=body["selector"],
            **pub_data,
        )

    elif error_type == "xhrError":
        new_Error = my_models.XhrError(
            pathname=body["pathname"],
            status=body["status"],
            duration=body["duration"],
            method=body["method"],
            response=body["response"],
            params=body["params"],
            is_async=body["async"],
            create_time=body["createTime"],
            **pub_data,
        )
    else:
        return utils.response_fail("TypeError", "未知类型")

    new_Error.save()  # 保存至数据库
    return utils.response_success("成功")


def post_performance(request, body):
    # 获取来源ip
    if "HTTP_X_FORWARDED_FOR" in request.META:
        from_ip = request.META["HTTP_X_FORWARDED_FOR"].split(',')[0]
    else:
        from_ip = request.META["REMOTE_ADDR"]

    data = {
        "title": body["title"],
        "url": body["url"],
        "hostname": utils.url_to_hostname(body["url"]),
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
    return utils.response_success("成功")


def post_user_action(body):
    if body["type"] == "pv":
        my_models.PV(
            url=body["url"],
            hostname=utils.url_to_hostname(body["url"]),
            timestamp=body["timestamp"],
            full_ua=body["userAgent"]["full"],
            browser_name=body["userAgent"]["name"],
            browse_version=body["userAgent"]["version"],

            os=body["userAgent"]["os"],
            start_time=body["startTime"],
            page_url=body["pageURL"],
            referrer=body["referrer"],
        ).save()
        utils.create_website(utils.url_to_hostname(
            body["url"]), body["title"])
        return utils.response_success("成功")
    elif body["type"] == "uv":
        my_models.UV(
            url=body["url"],
            hostname=utils.url_to_hostname(body["url"]),
            timestamp=body["timestamp"],
            full_ua=body["userAgent"]["full"],
            browser_name=body["userAgent"]["name"],
            browse_version=body["userAgent"]["version"],
            os=body["userAgent"]["os"],

            start_time=body["startTime"],
            ip=body["ip"],
            page_url=body["pageURL"],
            referrer=body["referrer"],
        ).save
        return utils.response_success("成功")
    elif body["type"] == "duration":
        my_models.Duration(
            url=body["url"],
            hostname=utils.url_to_hostname(body["url"]),
            timestamp=body["timestamp"],
            full_ua=body["userAgent"]["full"],
            browser_name=body["userAgent"]["name"],
            browse_version=body["userAgent"]["version"],
            os=body["userAgent"]["os"],

            duration=body["duration"],
            page_url=body["pageURL"],
        ).save
        return utils.response_success("成功")
    else:
        return utils.response_fail("TypeError", "未知类型")


def post_xhr(body):
    my_models.XhrError(
        title=body["title"],
        url=body["url"],
        hostname=utils.url_to_hostname(body["url"]),
        timestamp=body["timestamp"],
        full_ua=body["userAgent"]["full"],
        browser_name=body["userAgent"]["name"],
        browse_version=body["userAgent"]["version"],
        os=body["userAgent"]["os"],

        pathname=body["pathname"],
        status=body["status"],
        duration=body["duration"],
        method=body["method"],
        response=body["response"],
        params=body["params"],
        is_async=body["async"],
        create_time=body["createTime"],
    ).save()
    return utils.response_success("成功")


@csrf_exempt
def post_data(request):
    if request.method != 'POST':
        return utils.response_fail("MethodError", "不是POST请求")

    try:
        body = json.loads(request.body)
    except:
        return utils.response_fail("JSONError", "JSON格式有误")

    #  TODO: JSON数据校验
    try:
        if body["kind"] == "stability" and body["type"] == "error":
            return post_err(body)
        elif body["kind"] == "stability" and body["eventType"] == "load":
            return post_xhr(body)
        elif body["kind"] == "experience" and body["type"] == "timing":
            return post_performance(request, body)
        elif body["kind"] == "userAction":
            return post_user_action(body)
        else:
            return utils.response_fail("TypeError", "未知类型")

    except Exception as err:
        return utils.response_fail(type(err).__name__, repr(err))
