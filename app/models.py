from django.db import models

# Create your models here.


# 网站列表
class Website(models.Model):
    hostname = models.TextField()
    create_time = models.BigIntegerField()
    name = models.TextField(default="")
    tags = models.TextField(default="")


class ErrorPublic(models.Model):
    # 公共字段
    hostname = models.TextField()
    title = models.TextField()
    url = models.TextField()
    timestamp = models.BigIntegerField()
    full_ua = models.TextField()
    browser_name = models.TextField()
    browse_version = models.TextField()
    os = models.TextField()
    # type = models.TextField()
    # kind = models.TextField()
    # error_type = models.TextField()

    class Meta:
        abstract = True


class JSError(ErrorPublic):
    message = models.TextField()
    position = models.TextField()  # 3:4 行与列
    stack = models.TextField()
    selector = models.TextField()


class PromiseError(ErrorPublic):
    message = models.TextField()
    stack = models.TextField()
    selector = models.TextField()


class ResourceError(ErrorPublic):
    message = models.TextField()
    filename = models.TextField()
    tag_name = models.TextField()
    selector = models.TextField()


class WhiteScreenError(ErrorPublic):
    # message = models.TextField()
    empty_points = models.TextField()
    screen = models.TextField()
    view_point = models.TextField()
    selector = models.TextField()


class XhrError(ErrorPublic):
    pathname = models.TextField()
    status = models.TextField()
    duration = models.IntegerField()
    response = models.TextField()
    method = models.TextField()
    params = models.TextField()
    is_async = models.BooleanField()
    create_time = models.BigIntegerField()


class Performance(models.Model):
    hostname = models.TextField()
    from_ip = models.TextField()
    title = models.TextField()
    url = models.TextField()
    timestamp = models.BigIntegerField()
    full_ua = models.TextField()
    browser_name = models.TextField()
    browse_version = models.TextField()
    os = models.TextField()
    # type = models.TextField()
    # kind = models.TextField()

    dns = models.FloatField()
    connect = models.FloatField()
    ttfb = models.FloatField()
    response = models.FloatField()
    parse_dom = models.FloatField()
    dom_ready = models.FloatField()
    dom_content_loaded = models.FloatField()
    to_interactive = models.FloatField()
    load = models.FloatField()
    first_paint = models.FloatField()
    first_content_paint = models.FloatField()
    first_meaningful_paint = models.FloatField()
    largest_contentful_paint = models.FloatField()


class PV(models.Model):
    hostname = models.TextField()
    title = models.TextField()
    url = models.TextField()
    timestamp = models.BigIntegerField()
    full_ua = models.TextField()
    browser_name = models.TextField()
    browse_version = models.TextField()
    os = models.TextField()

    ip = models.TextField(default="127.0.0.1")
    start_time = models.BigIntegerField()
    page_url = models.TextField()
    referrer = models.TextField()


class UV(models.Model):
    hostname = models.TextField()
    title = models.TextField()
    url = models.TextField()
    timestamp = models.BigIntegerField()
    full_ua = models.TextField()
    browser_name = models.TextField()
    browse_version = models.TextField()
    os = models.TextField()

    ip = models.TextField()
    start_time = models.BigIntegerField()
    page_url = models.TextField()
    referrer = models.TextField()


class Duration(models.Model):
    hostname = models.TextField()
    title = models.TextField()
    url = models.TextField()
    timestamp = models.BigIntegerField()
    full_ua = models.TextField()
    browser_name = models.TextField()
    browse_version = models.TextField()
    os = models.TextField()

    ip = models.TextField(default="127.0.0.1")
    start_time = models.BigIntegerField(default=0)
    duration = models.FloatField()
    page_url = models.TextField()
