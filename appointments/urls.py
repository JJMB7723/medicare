from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('book/', views.AppointmentBookView.as_view(), name='book'),
    path('history/', views.AppointmentHistoryView.as_view(), name='history'),
    path('<int:pk>/status/<str:status>/', views.AppointmentStatusUpdateView.as_view(), name='update_status'),
]
