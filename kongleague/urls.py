"""
URL configuration for kongleague project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from tournament import views

urlpatterns = [
    # Public pages
    path('', views.standings_view, name='standings'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('teams/', views.teams_view, name='teams'),

    # Admin authentication
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),

    # Admin pages
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/teams/', views.manage_teams_view, name='manage_teams'),
    path('dashboard/matches/', views.manage_matches_view, name='manage_matches'),
    path('dashboard/settings/', views.tournament_settings_view, name='tournament_settings'),

    # Django admin (optional, for superuser access)
    path("admin/", admin.site.urls),
]
