from django import forms
from .models import Todo, TodoResponsible, TodoValidation, TodoComment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description']
        widgets = {

        }