from django.urls import path
from . import views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('inputs', views.inputs, name='inputs'),
    path('indicators/', views.indicators_view, name='indicators'),
    path('show_graph/', views.show_graph, name='show_graph'),
]+ debug_toolbar_urls()
'''path('graph/', views.graph, name='graph'),
    path('table/', views.table, name='table'),
    path('inputs/', views.inputs, name='inputs'),'''