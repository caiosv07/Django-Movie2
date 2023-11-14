from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView, name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout', views.LogouView, name='logout'),
    
]