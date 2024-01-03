from django.urls import path, re_path

from . import views

TEXT_RE = "[a-zA-Z0-9]*"

urlpatterns = [
    path("", views.Strategies.as_view(), name='strategies'),
]
