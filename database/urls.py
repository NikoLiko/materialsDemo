from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    path('', views.database, name='database'),
    path('select/', views.select, name='select'),
    path('query/',views.query, name="query"),
    path('upload/', views.upload, name='upload'),
    path('upload/uploaded/', views.uploaded, name='uploaded'),
    # path('detail/', views.struct,name="detail"),
    path('sites/', views.sites, name='sites'),
    path('get_GeometryOptimization/',views.get_GeometryOptimization, name="get_GeometryOptimization"),
]