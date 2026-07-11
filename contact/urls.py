from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('messages/', views.ContactMessagesListView.as_view(), name='messages_list'),
]
