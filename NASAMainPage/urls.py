from django.urls import path
from . import views

urlpatterns = [
    path("models/", views.models, name="models"),
    path("models/<str:id>/", views.model_detail, name="model_detail"),
    path("models/<str:id>/test_model/", views.test_model, name="test_model"),
    path('datasets/', views.datasets, name='datasets'),
    path('datasets/<str:dataset_name>/', views.dataset_detail, name='dataset_detail'),
    path("game/", views.main_game_screen, name="game"),
    path("game/game_selection/", views.game_selection, name="game_selection"),
    path("game/loading", views.model_prepping, name="model_prepping"),
    path("game/gameplay", views.game, name="gameplay"),
    path("game/leaderboard/", views.leaderboard, name="leaderboard"),
    path("about-us/", views.about_us, name="about-us"),
    path("index/", views.index, name='index'),
    path("game/save_predictions/", views.save_predictions, name="save_predictions"),
    path("game/round_results", views.round_results, name="round_results"),
    path("game/game_results", views.game_results, name="game_results"),
    path("game/guess_number/", views.guess_number, name="guess_number"),
]
