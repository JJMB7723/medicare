from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('book/', views.appointment_book, name='appointment_book'),
    path('<int:pk>/status/<str:status>/', views.appointment_update_status, name='appointment_update_status'),
    path('history/', views.appointment_history, name='appointment_history'),
]
