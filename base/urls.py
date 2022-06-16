from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('subject/<str:pk>/', views.subject, name='subject'),

    path('create-subject/', views.createSubject, name='create-subject'),
    path('create-assignment/<str:pk>', views.createAssignment, name='create-assignment'),

]