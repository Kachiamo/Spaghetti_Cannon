from django.urls import re_path

from . import views


urlpatterns = [
    re_path(f"/?$", views.Backtest.as_view(), name="backtest"),
]
