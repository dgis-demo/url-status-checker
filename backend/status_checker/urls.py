from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('load_urls/', views.load_urls),
    path('check_status/', views.check_status),
    path('change_status/', views.change_status),
]
