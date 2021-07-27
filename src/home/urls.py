from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path("", views.home_page, name="home"),
    path("quizes/", views.quizes, name="quizes"),
]
