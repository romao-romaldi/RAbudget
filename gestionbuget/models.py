from random import choice

from django.db import models
from pygments.lexer import default

choise_status = (
        ("pending", "Pending"),
        ("accept", "Accept"),
        ("reject", "Reject")
    )

# Create your models here.

class BudgetSheet(models.Model):
    type_currency = (
        ("FCFA", "FCFA"),
        ("USD", "$"),
        ("EUR", "€"),
        ("GBP", "GBP"),
        ("JPY", "JPY"),
        ("CNY", "CNY"),
        ("INR", "INR"),
        ("AUD", "AUD"),
        ("CAD", "CAD"),
        ("CHF", "CHF"),
    )
    pid = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the budget sheet")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    currency = models.CharField(choices=type_currency, default=type_currency[0][0], max_length=10,
                             help_text="Currency type for the budget sheet")

    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_budget_sheets'
    )

    def __str__(self):
        return self.title

class TypeBudget(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_due_date = models.BooleanField(default=False, help_text="Indicates if the budget has an expiration date")
    is_date_created = models.BooleanField(default=False, help_text="Indicates if the budget has a creation date")
    is_compte = models.BooleanField(default=False, help_text="Indicates if the budget is a compte type")
    is_salary = models.BooleanField(default=False, help_text="Indicates if the budget is a salary type")
    is_income = models.BooleanField(default=False)
    is_spent = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    budget_sheet = models.ForeignKey(
        BudgetSheet,
        on_delete=models.CASCADE,
        related_name='type_budgets_sheet'
    )
    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_type_budgets'
    )

    def __str__(self):
        return self.name

class Budget(models.Model):
    pid = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the budget sheet")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    amount_reel = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True, null=True, help_text="Expiration date of the budget")
    is_date_created = models.DateField(blank=True, null=True, help_text="Creation date of the budget")
    account = models.CharField(blank=True, null=True, max_length=100, help_text="Account associated with the budget")

    type_budget = models.ForeignKey(TypeBudget, on_delete=models.CASCADE, related_name='budgets')
    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_budgets'
    )

    def __str__(self):
        return self.title


class Demande(models.Model):

    pid = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the budget sheet")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    amount_reel = models.DecimalField(max_digits=10, decimal_places=2)
    file = models.FileField(upload_to="doc/", null=True, blank=True)
    status = models.CharField(choices=choise_status, max_length=15 ,default=choise_status[0][0])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    type_budget = models.ForeignKey(TypeBudget, on_delete=models.CASCADE, related_name='demandes')
    budget_sheet = models.ForeignKey(
        BudgetSheet,
        on_delete=models.CASCADE,
        related_name='demanse_budgets_sheet'
    )
    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_demande'
    )

    user_validete = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_validate'
    )

    def __str__(self):
        return self.title


