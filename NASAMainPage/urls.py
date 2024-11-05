from django.urls import path
from . import views

urlpatterns = [
    path("", views.current_datetime, name="index"),
    path("models/", views.models, name="models"),
    path("datasets/", views.datasets, name="datasets"),
    path("game/", views.game, name="game"),
    path("about-us/", views.about_us, name="about-us"),
    path("run-script/", views.run_script, name='run_script')
]