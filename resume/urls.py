from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    # Liste des résumés
    path('<str:pid_sheet>/', views.resume_list, name='resume_list'),
    
    # Créer un résumé
    path('<str:pid_sheet>/create/', views.resume_create, name='resume_create'),
    
    # Détails d'un résumé
    path('<str:pid_sheet>/<str:pid_resume>/', views.resume_detail, name='resume_detail'),
    
    # Modifier un résumé
    path('<str:pid_sheet>/<str:pid_resume>/edit/', views.resume_edit, name='resume_edit'),
    
    # Actions sur un résumé
    path('<str:pid_sheet>/<str:pid_resume>/submit/', views.resume_submit, name='resume_submit'),
    path('<str:pid_sheet>/<str:pid_resume>/validate/', views.resume_validate, name='resume_validate'),
    path('<str:pid_sheet>/<str:pid_resume>/reject/', views.resume_reject, name='resume_reject'),
    
    # Commentaires
    path('<str:pid_sheet>/<str:pid_resume>/comment/', views.comment_create, name='comment_create'),
    
    # Gestion de la hiérarchie
    path('<str:pid_sheet>/hierarchie/manage/', views.hierarchie_manage, name='hierarchie_manage'),
]
