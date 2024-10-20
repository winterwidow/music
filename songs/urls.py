from django.urls import path
from . import views

urlpatterns = [
    path('classify/', views.classify_song, name='classify_song'),
]
