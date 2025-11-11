from django.urls import path
from .views import (
    index,
    budget_sheet_list,
    budget_sheet_detail,
    budget_sheet_create,
    created_budget,
    create_section,
    chart_budget,
    chart_budget_month,
    create_demande,
    budget_sheet_delete,
    manage_users, create_user_htmx, remove_partner_htmx, send_invitation_htmx,
    accept_invitation, demandes_list,
    create_demande_htmx, update_demande_status_htmx, demande_detail, add_comment_htmx

)

app_name="gestionbudget"

urlpatterns = [
    path('', budget_sheet_list, name='budget_sheet_list'),
    path('budget_sheet_detail/<str:pid>/', budget_sheet_detail, name='budget_sheet_detail'),
    path('budget_sheet_create/', budget_sheet_create, name='budget_sheet_create'),
    path('budget_sheet_delete/<str:pid>/', budget_sheet_delete, name='budget_sheet_delete'),

    path("created_budget/<str:pid>/", created_budget, name="created_budget"),
    path("chart_budget/<str:pid>/", chart_budget, name="chart_budget"),
    path("chart_budget_month/<str:pid>", chart_budget_month, name="chart_budget_month"),

    #section
    path("create-section/<str:pid>/", create_section, name="create_section"),

    #demande gestion partie
    path("create_demande/<str:pid_sheet>/", create_demande, name="create_demande"),
    
    # Gestion des utilisateurs
    path('manage_users/<str:pid>/', manage_users, name='manage_users'),
    path('create_user_htmx/<str:pid>/', create_user_htmx, name='create_user_htmx'),
    path('remove_partner_htmx/<str:pid>/', remove_partner_htmx, name='remove_partner_htmx'),
    path('send_invitation_htmx/<str:pid>/', send_invitation_htmx, name='send_invitation_htmx'),
    path('accept_invitation/<str:token>/', accept_invitation, name='accept_invitation'),
    
    # Gestion des demandes
    path('demandes/<str:pid>/',demandes_list, name='demandes_list'),
    path('create_demande_htmx/<str:pid>/',create_demande_htmx, name='create_demande_htmx'),
    path('update_demande_status_htmx/<str:pid>/',update_demande_status_htmx, name='update_demande_status_htmx'),
    path('demande_detail/<str:pid>/<str:demande_pid>/',demande_detail, name='demande_detail'),
    path('add_comment_htmx/<str:pid>/<str:demande_pid>/',add_comment_htmx, name='add_comment_htmx'),
]
