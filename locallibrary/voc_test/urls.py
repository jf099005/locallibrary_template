from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='main')),
    path('MCQ/answering/', views.MCQ_answering, name='MCQ_answering'),
    path('MCQ/update_vocabulary/', views.MCQ_update_vocabulary, name='MCQ_update'),
    path('MCQ/', views.MCQ_view, name='MCQ'),
    path('MCQ/', views.MCQ_view, name='MCQ'),
    path('<str:username>/', views.main, name='user-main'),
    path('main', views.main, name='main'),

    path('main/<str:table_name>', views.table_detail_page, name = 'table-detail')

]