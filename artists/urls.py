from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/apply/', views.apply_artist, name='apply_artist'),
    path('artist/dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/applications/', views.admin_applications, name='admin_applications'),
    path('admin/applications/download-csv/', views.download_applications_csv, name='download_applications_csv'),
    path('admin/statistics/', views.admin_statistics, name='admin_statistics'),
    path('admin/process-applications/', views.process_applications, name='process_applications'),
]
