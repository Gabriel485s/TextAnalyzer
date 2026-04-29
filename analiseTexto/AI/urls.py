from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analise/', views.analise, name='analise'),
    path('5_dias/', views.analise_5_dias, name='5_dias')
]
