from django.urls import path
from girl_name import views

urlpatterns = [
    path('girls/', views.GirlsNameView.as_view(), name='girls'),
    path('boys/', views.BoysNameView.as_view(), name='boys'),
    path('reset-girls/', views.GirlsNameResetView.as_view(), name='reset_girls'),
    path('reset-boys/', views.BoysNameResetView.as_view(), name='reset_boys'),
    path('choose-girl/', views.GirlsNameChoose.as_view(), name='choose_girl'),
    path('choose-boy/', views.BoysNameChoose.as_view(), name='choose_boy'),
]
