from django.urls import path
from . import views

app_name = 'auth_management'

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
]
