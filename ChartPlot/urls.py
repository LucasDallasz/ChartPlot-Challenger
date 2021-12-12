from django.urls import path
from .views import (
    chartplot_create,
    chartplot_detail,
    chartplot_edit,
    chartplot_home,
    chartplot_tutorial, 
    )

app_name = 'ChartPlot'

urlpatterns = [
    path('home/', chartplot_home, name='home'),
    path('create/', chartplot_create, name='create'),
    path('tutorial/', chartplot_tutorial, name='tutorial'),
    path('<id>/detail/', chartplot_detail, name='detail'),
    path('<id>/edit/', chartplot_edit, name='edit'),
]