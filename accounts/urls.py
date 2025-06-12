from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView, name='signup'),
    path('logout/', views.LogouView, name='logout'),
    
]