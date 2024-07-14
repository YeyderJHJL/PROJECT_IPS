from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/list/', views.personal_list, name='personal_list'),
    path('personal/add/', views.personal_add, name='personal_add'),
    path('personal/edit/<int:pk>/', views.personal_edit, name='personal_edit'),
    path('personal/delete/<int:pk>/', views.personal_delete, name='personal_delete'),
    path('personal/toggle_status/<int:pk>/', views.toggle_personal_status, name='toggle_personal_status'),
    path('estado_personal/', views.estado_personal_list, name='estado_personal_list'),
    path('estado_personal/add/', views.estado_personal_add, name='estado_personal_add'),
    path('estado_personal/edit/<str:pk>/', views.estado_personal_edit, name='estado_personal_edit'),
    path('estado_personal/delete/<str:pk>/', views.estado_personal_delete, name='estado_personal_delete'),
    path('tipo_personal/', views.tipo_personal_list, name='tipo_personal_list'),
    path('tipo_personal/add/', views.tipo_personal_add, name='tipo_personal_add'),
    path('tipo_personal/edit/<str:pk>/', views.tipo_personal_edit, name='tipo_personal_edit'),
    path('tipo_personal/delete/<str:pk>/', views.tipo_personal_delete, name='tipo_personal_delete'),
]