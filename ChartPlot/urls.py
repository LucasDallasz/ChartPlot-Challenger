from django.urls import path
from .views import (
    chartplot_home, 
    chartplot_create,
    chartplot_detail,
    chartplot_edit,
    )

app_name = 'ChartPlot'

urlpatterns = [
    path('home/', chartplot_home, name='home'),
    path('create/', chartplot_create, name='create'),
    path('<id>/detail/', chartplot_detail, name='detail'),
    path('<id>/edit/', chartplot_edit, name='edit'),
]