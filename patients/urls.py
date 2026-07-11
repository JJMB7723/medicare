from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('register/', views.PatientRegisterView.as_view(), name='register'),
    path('', views.PatientListView.as_view(), name='list'),
    path('<int:pk>/edit/', views.PatientUpdateView.as_view(), name='edit'),
]
