from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('add/<int:patient_id>/', views.record_add, name='record_add'),
    path('<int:pk>/', views.record_detail, name='record_detail'),
]
