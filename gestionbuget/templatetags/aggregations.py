from django import template
from django.db.models import Avg, Sum, Count
from datetime import datetime


register = template.Library()

@register.filter(name="aggregate_sum")
def aggregate_sum(queryset, arg):
    """
    Calcule la moyenne du champ 'price' dans un queryset.
    """
    return queryset.aggregate(total_prix=Sum(arg))['total_prix']

@register.filter(name="aggregate_difference")
def aggregate_difference(queryset):
    return queryset.amount_reel - queryset.amount_spent


@register.filter(name="aggregate_differnces")
def aggregate_diffences(queryset):
    """
    Calcule la moyenne du champ 'price' dans un queryset.
    """
    amount_spent= queryset.aggregate(total_prix=Sum("amount_spent"))['total_prix']
    amount_reel = queryset.aggregate(total_prix=Sum("amount_reel"))['total_prix']
    return amount_reel - amount_spent

def aggregate_total_global(queryset):
    """
    Calcule la somme totale du champ 'price' dans un queryset.
    """

    return queryset.aggregate(total_prix=Sum("amount_reel"))['total_prix']

@register.filter(name="current_month")
def current_month(queryset):
    """
    Calcule la somme totale du champ 'price' dans un queryset.
    """
    month = datetime.now().month
    year = datetime.now().year

    return queryset.filter(date_created__month=month, date_created__year=year)