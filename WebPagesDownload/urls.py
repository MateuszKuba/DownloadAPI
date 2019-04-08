from django.urls import path

from . import views
from . import api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/status/<str:pk>/', api_views.StatusDetail.as_view()),
]