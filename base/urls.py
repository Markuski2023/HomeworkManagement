from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('subject/<str:pk>/', views.subject, name='subject'),
    path('grades/', views.grades, name='grades'),

    path('create-subject/', views.createSubject, name='create-subject'),
    path('create-assignment/<str:pk>', views.createAssignment, name='create-assignment'),

    path('delete-subject/<str:pk>/', views.deleteSubject, name='delete-subject'),
    path('delete-note/<str:pk>/', views.deleteNote, name='delete-note'),
    path('delete-assignment/<str:pk>/', views.deleteAssignment, name='delete-assignment'),

    path('update-subject/<str:pk>/', views.updateSubject, name='update-subject'),
    path('update-assignment/<str:pk>/', views.updateAssignment, name='update-assignment'),

    path('group/', views.group, name='group'),
]