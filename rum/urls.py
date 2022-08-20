"""rum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from distutils.log import error
from django.urls import path
from app.views import post, manage, errors, action, timing

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/post_err', post.post_data),
    # path('api/post_performance', post.post_performance),
    # path('api/get_all_err', get.get_all_err),
    # path('api/get_website_list', get.get_website_list),
    # path('api/get_errors', get.get_errors),
    # path('api/get_traffic', get.get_traffic),
    # path('api/get_performance', get.get_performance),
    path('manage/getAllWeb', manage.get_all_web),
    path('manage/changeWebName', manage.change_web_name),
    path('manage/changeWebTag', manage.change_web_tag),
    path('overview/webError', errors.web_error),
    path('overview/errorList', errors.error_list),
    # path('overview/userAction', action.get_user_action),
    path('overview/timing', timing.timing),
]
