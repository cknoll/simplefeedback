from django.urls import path

from . import views

urlpatterns = [
    path("", views.Staticpage.as_view(), name="landingpage")
]
