from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classify/', views.classify_song, name='classify_song'),
]
