from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка додатку
    path('calculate/', views.main_view, name='main-view'),  # Сторінка для розрахунків
]

