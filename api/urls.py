from django.urls import path, re_path
from . import views

urlpatterns = [

    # re_path("^get/o/(?P<owner_key>.+)$", views.get_data, name="api_get_ok", kwargs={"foo": "bar"}),
    path("get/o/<slug:owner_key>", views.get_data, name="api_get_ok"),
    re_path("get/?", views.get_data, name="api_get"),
    re_path("add/?", views.add_data, name="api_add"),

]
