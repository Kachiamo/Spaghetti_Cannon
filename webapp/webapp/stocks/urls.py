from django.urls import re_path

from . import views


urlpatterns = [
    re_path(f"/?$", views.Stocks.as_view(), name="stocks"),
]
