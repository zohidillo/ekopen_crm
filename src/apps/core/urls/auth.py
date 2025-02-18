from django.urls import path

import src.apps.core.views.auth as views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.custom_login_view, name='login'),
    path('logout', views.custom_logout_view, name='logout'),
]
