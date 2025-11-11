from django import template
from ..models import Logo

register = template.Library()


@register.simple_tag
def get_logo_actif():
    """Template tag pour récupérer le logo actif"""
    return Logo.get_logo_actif()
