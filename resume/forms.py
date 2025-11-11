from django import forms
from .models import Resume, CommentResume, Hierarchie


class ResumeForm(forms.ModelForm):
    """Formulaire pour créer/modifier un rapport"""
    
    class Meta:
        model = Resume
        fields = ['title', 'content', 'date_resume']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Titre du rapport'
            }),
            'date_resume': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
        }
        labels = {
            'title': 'Titre',
            'content': 'Contenu du rapport',
            'date_resume': 'Date',
        }


class CommentResumeForm(forms.ModelForm):
    """Formulaire pour ajouter un commentaire sur un rapport"""
    
    class Meta:
        model = CommentResume
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Votre commentaire...'
            }),
        }
        labels = {
            'content': 'Commentaire',
        }


class HierarchieForm(forms.ModelForm):
    """Formulaire pour définir la hiérarchie"""
    
    def __init__(self, *args, **kwargs):
        budget_sheet = kwargs.pop('budget_sheet', None)
        super().__init__(*args, **kwargs)
        
        if budget_sheet:
            # Récupérer tous les utilisateurs liés à cette feuille
            from customuser.models import Profile
            user_ids = [budget_sheet.user.id]
            
            # Ajouter les partenaires
            partenaires = budget_sheet.type_sheet_partenaire.all()
            for partenaire in partenaires:
                user_ids.append(partenaire.user.id)
            
            # Filtrer les choix
            self.fields['user'].queryset = Profile.objects.filter(id__in=user_ids)
            self.fields['superieur'].queryset = Profile.objects.filter(id__in=user_ids)
    
    class Meta:
        model = Hierarchie
        fields = ['user', 'superieur']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'superieur': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
        }
        labels = {
            'user': 'Utilisateur',
            'superieur': 'Supérieur hiérarchique',
        }
