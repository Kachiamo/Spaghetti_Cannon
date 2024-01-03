from django.urls import path

from . import views


urlpatterns = [
    path("", views.Backtest.as_view(), name='backtest')
]
