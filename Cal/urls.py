
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("trigo", views.trigo, name="trigo"),
    path("logln", views.logln, name="logln"),
    path("strigo", views.strigo, name="strigo"),
    path("slogln", views.slogln, name="slogln"),
    path("hcflcm", views.hcflcm, name="hcflcm"),
    path("shcflcm", views.shcflcm, name="shcflcm"),
    path("qe", views.qe, name="qe"),
    path("sqe", views.sqe, name="sqe"),
    path("stats", views.stats, name="stats"),
    path("sstats", views.sstats, name="sstats")
]