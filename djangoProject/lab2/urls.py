from django.urls import path
from . import views

urlpatterns = [
    path('university/', views.university_list, name='university_list'),
    path('university/new/', views.university_new, name='university_new'),
    path('university/<int:pk>/edit/', views.university_edit, name='university_edit'),
    path('university/<int:pk>/delete/', views.university_delete, name='university_delete'),
    path('students/new/', views.student_new, name='student_new'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/', views.student_list, name='students_list')
]
