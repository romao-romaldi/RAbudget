from django.urls import path
from . import account_view, core_views, contact_view, gestion_active_views

app_name = "lawyer"
urlpatterns = [
    #account urls
    path('account/login/', account_view.login_view, name='login'),
    path('account/register/', account_view.register_view, name='register'),

    # other paths can be added here
    # core views
    path('core/', core_views.index, name='index'),

    # contact views
    path('contact/list_personne/', contact_view.contact_personne, name='contact_personne'),
    path('contact/details_personne/', contact_view.details_contact_personne, name='detail_contact_personne'),


    #gestion des activites
    path('settings/gestion_active/', gestion_active_views.gestion_active_views, name='gestion_active'),
    path('settings/add_type_activiter/', gestion_active_views.add_type_activiter, name='add_type_activiter'),
    path('settings/details_type_active/<int:id>/', gestion_active_views.details_type_active,name='details_type_active'),
    path('settings/details_type_active/active_champs_types/<int:id>/<int:champs_id>',
         gestion_active_views.active_champs_types,name='active_champs_types'),

    path('settings/details_type_active/active_champs_types/categories/<int:id>/',
         gestion_active_views.add_categorie_activity,name='add_categorie_activity'),

]
