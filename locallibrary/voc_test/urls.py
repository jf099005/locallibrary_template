from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('call/', views.button_view, name='call'),
    path('MCQ_answering/', views.MCQ_answering, name='MCQ_answering'),
    path('MCQ/', views.MCQ_view, name='MCQ'),
]