from django.urls import re_path

from . import views

TEXT_RE = "[a-zA-Z0-9]*"

urlpatterns = [
    re_path(f"/?$", views.Strategies.as_view(), name="strategies"),
]
