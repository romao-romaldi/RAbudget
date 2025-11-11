from django import forms
from .models import Logo


class LogoForm(forms.ModelForm):
    """Formulaire pour créer et modifier les logos"""

    class Meta:
        model = Logo
        fields = ['nom', 'image', 'est_actif', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Logo principal, Logo secondaire...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*'
            }),
            'est_actif': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Description optionnelle du logo...'
            })
        }
        help_texts = {
            'nom': 'Donnez un nom descriptif à votre logo',
            'image': 'Formats acceptés : PNG, JPG, SVG. Taille recommandée : 100x100px maximum',
            'est_actif': 'Cochez cette case pour utiliser ce logo dans la navbar',
            'description': 'Décrivez l\'usage ou le style de ce logo'
        }
