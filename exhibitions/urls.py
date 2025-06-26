from django.urls import path
from . import views

app_name = 'exhibitions'

urlpatterns = [
    path('exhibitions/', views.exhibition_list, name='exhibition_list'),
    path('exhibition/create/', views.create_exhibition, name='create_exhibition'),
]
