from django.urls import path
from . import views

app_name = 'customuser'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Gestion des logos
    path('logos/', views.logo_list, name='logo_list'),
    path('logos/creer/', views.logo_create, name='logo_create'),
    path('logos/<int:pk>/modifier/', views.logo_edit, name='logo_edit'),
    path('logos/<int:pk>/activer/', views.logo_activate, name='logo_activate'),
    path('logos/<int:pk>/supprimer/', views.logo_delete, name='logo_delete'),
]
