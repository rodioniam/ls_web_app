from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('session/<int:session_id>/', views.index, name='index'),
    path('card/<int:card_id>/<str:action>/',
         views.change_points, name='change_points'),
    path('session/<int:session_id>/reset/',
         views.reset_points, name='reset_points'),
    path('session/<int:session_id>/multipliers/',
         views.assign_multiplier, name='assign_multiplier')
]
