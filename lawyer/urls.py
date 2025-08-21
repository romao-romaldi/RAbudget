from django.urls import path
from . import account_view, core_views, contact_view

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
]
