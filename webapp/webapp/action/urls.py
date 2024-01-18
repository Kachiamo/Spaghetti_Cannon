from django.urls import re_path

from . import views


urlpatterns = [
    re_path(f"/?$", views.Action.as_view(), name="action"),
]
