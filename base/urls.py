from django.urls import path

from . import views


main_view = views.Staticpage.as_view

urlpatterns = [
    path("", main_view(), name="landingpage"),
    path("new", main_view(), name="newdocumentpage", kwargs={"mode": "new"}),
    path("doc/<slug:slug>/<slug:doc_key>", main_view(), name="reviewpage", kwargs={"mode": "review"}),
    path("doc/<slug:slug>/<slug:doc_key>/o/<slug:owner_key>", main_view(), name="documentpage", kwargs={"mode": "owner"}),
]
