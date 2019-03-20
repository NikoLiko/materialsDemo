from django.urls import path
from . import views

urlpatterns = [
    path('', views.database, name='database'),
    path('select/', views.select, name='select'),
    path('query/',views.query, name="query"),
    path('upload/', views.upload, name='upload'),
    path('upload/uploaded/', views.uploaded, name='uploaded'),
]