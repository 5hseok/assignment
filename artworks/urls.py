from django.urls import path
from . import views

app_name = 'artworks'

urlpatterns = [
    path('artworks/', views.artwork_list, name='artwork_list'),
    path('artwork/create/', views.create_artwork, name='create_artwork'),
]
