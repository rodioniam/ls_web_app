from django.urls import path
from . import views

urlpatterns = [
    path('session/<int:session_id>/', views.index, name='index'),
    path('card/<int:card_id>/<str:action>/',
         views.change_points, name='change_points')
]
