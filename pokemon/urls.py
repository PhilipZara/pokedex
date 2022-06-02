from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('pokemon/', views.pokemon, name="pokemon")
]
