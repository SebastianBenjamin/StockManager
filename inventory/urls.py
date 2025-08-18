from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_product, name='add_product'),
    path('edit/', views.edit_product, name='edit_product'),
    path('delete/', views.delete_product, name='delete_product'),
    
]
