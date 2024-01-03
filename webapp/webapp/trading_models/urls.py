from django.urls import re_path

from . import views

UUID_RE = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

urlpatterns = [
    re_path(f"/?$", views.TradingModels.as_view(), name="trading models"),
    re_path(f"^/(?P<pk>{UUID_RE})/?$", views.TradingModel.as_view(), name="trading model"), # NOQA
    re_path(f"^/(?P<pk>{UUID_RE}):train/?$", views.TrainTradingModel.as_view(), name="train trading model"), # NOQA
]
