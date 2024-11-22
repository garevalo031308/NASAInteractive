from django.urls import path
from . import views

urlpatterns = [
    path("models/", views.models, name="models"),
    path("models/<str:model_name>/", views.model_detail, name="model_detail"),
    path('datasets/', views.datasets, name='datasets'),
    path('datasets/<str:dataset_name>/', views.dataset_detail, name='dataset_detail'),
    path("game/", views.game, name="game"),
    path("about-us/", views.about_us, name="about-us"),
    path("run-script/", views.run_script, name='run_script'),
    path("index/", views.index, name='index')
]