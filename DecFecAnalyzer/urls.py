from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inputs', views.inputs, name='inputs'),
    path('save_device', views.save_device, name='save_device'),
]
'''path('graph/', views.graph, name='graph'),
    path('table/', views.table, name='table'),
    path('inputs/', views.inputs, name='inputs'),'''