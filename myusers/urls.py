from django.conf.urls import path
from .views import *
from django.contrib.auth import auth_views

urlpatterns = [
    path('logout/', logout_view, name="logout"),
    path('', overview, name='dashboard'),
    path('users/', users_view, name="users"),
    path('user_detail/<int:pk>/', user_detail_view, name="user_detail"),
    path('user_detail/<int:pk>/disable/',
         disable_user_view, name="disable_user_detail"),
    path('user_detail/<int:pk>/enable/$',
         enable_user_view, name="enable_user_detail"),
    path('user_activity/', user_activity_view, name="user_activity"),
    path('clients/', clients_view, name="clients"),
    path('client_detail/<int:pk>/', client_detail_view, name="client_detail"),
    path('client_ova_edit/<int:pk>/',
         client_ova_edit_view, name="client_ova_edit"),
    path('client_user_activity/', client_user_activity_view,
         name="client_user_activity"),
]
