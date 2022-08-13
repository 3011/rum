from statistics import mode
from django.db import models

# Create your models here.


# 网站列表
class Website(models.Model):
    host = models.TextField(primary_key=True)
    create_time = models.BigIntegerField()


class ErrorPublic(models.Model):
    # 公共字段
    host = models.TextField()
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
    message = models.TextField()

    class Meta:
        abstract = True


class JSError(ErrorPublic):
    position = models.TextField()  # 3:4 行与列
    stack = models.TextField()
    selector = models.TextField()


class PromiseError(ErrorPublic):
    stack = models.TextField()
    selector = models.TextField()


class ResourceError(ErrorPublic):
    filename = models.TextField()
    tag_name = models.TextField()
    position = models.TextField()
    selector = models.TextField()


class XhrError(ErrorPublic):
    status = models.TextField()
    duration = models.IntegerField()
    response = models.TextField()
    params = models.TextField()


class WhiteScreenError(ErrorPublic):
    empty_points = models.TextField()
    screen = models.TextField()
    view_point = models.TextField()
    selector = models.TextField()


class Performance(models.Model):
    host = models.TextField()
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

    dns = models.DecimalField(max_digits=10, decimal_places=3)
    connect = models.DecimalField(max_digits=10, decimal_places=3)
    ttfb = models.DecimalField(max_digits=10, decimal_places=3)
    response = models.DecimalField(max_digits=10, decimal_places=3)
    parse_dom = models.DecimalField(max_digits=10, decimal_places=3)
    dom_ready = models.DecimalField(max_digits=10, decimal_places=3)
    ttfb = models.DecimalField(max_digits=10, decimal_places=3)
    dom_content_loaded = models.DecimalField(max_digits=10, decimal_places=3)
    to_interactive = models.DecimalField(max_digits=10, decimal_places=3)
    load = models.DecimalField(max_digits=10, decimal_places=3)
    first_paint = models.DecimalField(max_digits=10, decimal_places=3)
    first_content_paint = models.DecimalField(max_digits=10, decimal_places=3)
    first_meaningful_paint = models.DecimalField(
        max_digits=10, decimal_places=3)
    largest_contentful_paint = models.DecimalField(
        max_digits=10, decimal_places=3)
