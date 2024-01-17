from django.urls import re_path

from . import views

TEXT_RE = "[a-zA-Z]*"

urlpatterns = [
    re_path(f"/?$", views.Stocks.as_view(), name="stocks"),
    re_path(f":update/?$", views.UpdateStocks.as_view(), name="update stocks"),
    re_path(f"^/(?P<pk>{TEXT_RE})/?$", views.Stock.as_view(), name="stock"),
    re_path(f"^/(?P<pk>{TEXT_RE}):update/?$", views.UpdateStock.as_view(), name="update stock"),
]
