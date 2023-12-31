from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<token>/', views.Activate.as_view(), name='activate'),
]
