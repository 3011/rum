from statistics import mode
from django.db import models

# Create your models here.


class ErrorPublic(models.Model):
    # 公共字段
    domain = models.TextField()
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
