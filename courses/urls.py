from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_management, name='course_management'),
    path('<str:course_code>/', views.course_management, name='course_management_with_code'),
]