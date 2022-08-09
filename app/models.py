from statistics import mode
from django.db import models

# Create your models here.


class Error(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    timestamp = models.DecimalField(max_digits=15, decimal_places=0)
    full_ua = models.CharField(max_length=100)
    browser_name = models.CharField(max_length=100)
    browse_version = models.CharField(max_length=100)
    os = models.CharField(max_length=100)

    # type = models.CharField(max_length=100)
    error_type = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    position = models.CharField(max_length=100)  # 3,4 行与列
    stack = models.CharField(max_length=1000)
    selector = models.CharField(max_length=1000)
