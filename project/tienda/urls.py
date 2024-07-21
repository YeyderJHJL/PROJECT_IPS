from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_form, name='contact_form'),
    path('empresa/', views.empresa, name='empresa'),
    path('login/', views.login, name='login'),
    path('contact/success/', views.contact_success, name='contact_success'),
]
