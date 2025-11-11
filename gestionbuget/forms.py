from django import forms

from .models import BudgetSheet, Budget, TypeBudget, Demande, CommentDemande

class FormBudgetSheet(forms.ModelForm):
    class Meta:
        model = BudgetSheet
        fields = ["title", "description", "currency"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "mt-1 block w-full border \
                                  border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le nom du budget", "required": True}),
            "description": forms.Textarea(attrs={"class": "mt-1 block w-full border \
                                  border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500", }),
            "currency": forms.Select(attrs={"class": "mt-1 block w-full border \
                                  border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500", })
        },


class FormBudget(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["title", "description", "amount_spent", "amount_reel", "due_date", "account"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "mt-1 block w-full border \
                                    border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le nom du budget", "required": True}),
            "description": forms.Textarea(attrs={"class": "mt-1 block w-full border \
                                border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                            "placeholder": "Decriver pourquoi vous avez fait cette operation,"
                                           "cela vous permetra de vous souvenir au momant de faire le billan"}),
            "amount_spent": forms.NumberInput(attrs={"class": "mt-1 block w-full border \
                                    border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le montant estimer obtenir ou dépenser", "required": True}),
            "amount_reel": forms.NumberInput(attrs={"class": "mt-1 block w-full border \
                                    border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le Montant reel obtenu ou dépenser", "required": True}),
            "due_date": forms.DateInput(attrs={"type":"date","class": "mt-1 block w-full border \
                                    border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                            "placeholder": "Entrez le nom du compte au quelle vous avez deposer", "required": True}),
            "account": forms.TextInput(attrs={"class": "mt-1 block w-full border \
                                     border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le nom du budget", "required": True}),

        }


class FormSection(forms.ModelForm):
    class Meta:
        model = TypeBudget
        fields = ["name", "description", "is_spent", "is_transaction", "is_saving"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "mt-1 block w-full border \
                                        border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le nom du budget", "required": True}),
            "description": forms.Textarea(attrs={"class": "mt-1 block w-full border \
                            border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500", }),
            "is_spent": forms.CheckboxInput(attrs={"class": "hidden", ":checked": "is_spent"}),
            "is_transaction": forms.CheckboxInput(attrs={"class": "hidden", ":checked": "is_transaction"}),
            "is_saving": forms.CheckboxInput(attrs={"class": "hidden", ":checked": "is_saving"})

        }



class FormDemande(forms.ModelForm):
    class Meta:
        model = Demande

        fields = ["title", "description", "amount_spent","file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "mt-1 block w-full border \
                                    border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500",
                                            "placeholder": "Entrez le nom du budget", "required": True}),
            "description": forms.Textarea(attrs={"class": "mt-1 block w-full border \
                                   border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500", }),

            "amount_spent": forms.NumberInput(attrs={
                "class":"mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 \
                      focus:border-blue-500" , "required": True
            }),
            # "amount_reel": forms.NumberInput(attrs={
            #     "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 \
            #                   focus:border-blue-500", "required": True
            # }),
        }


class FormComment(forms.ModelForm):
    class Meta:
        model = CommentDemande
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "mt-1 block w-full border \
            border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500", })
        }

