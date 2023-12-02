from django.urls import path

from . import views


main_view = views.Staticpage.as_view

urlpatterns = [
    path("", views.Staticpage.as_view(), name="landingpage"),
    path("new", views.Staticpage.as_view(), name="newdocumentpage", kwargs={"mode": "new"}),
    path("doc/<slug:slug>/<slug:doc_key>", views.Staticpage.as_view(), name="reviewpage"),
    path("doc/<slug:slug>/<slug:doc_key>/o/<slug:owner_key>", views.Staticpage.as_view(), name="documentpage"),
]
