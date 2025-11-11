from django import forms
from . models import GestionTimer


class GestionTimerForm(forms.ModelForm):
    class Meta:
        model = GestionTimer
        fields = ['name', 'affaire']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 bg-white \
                rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm '}),
            'affaire': forms.TextInput(attrs={'class': 'px-2 py-1 hidden'}),
        }