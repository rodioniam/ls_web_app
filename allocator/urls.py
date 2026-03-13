from django.urls import path
from . import views

urlpatterns = [
    path('session/<int:session_id>/', views.index, name='index')
]
