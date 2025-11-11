from random import choice

from django.db import models
from django.db.models.signals import post_save
from pygments.lexer import default

from gestionbuget import utility

choise_status = (
        ("pending", "Pending"),
        ("accept", "Accept"),
        ("reject", "Reject")
    )

choise_role = (
    ("consultation", "Consultation"),
    ("gestionnaire", "Gestionnaire"),
    ("gerant", "Gérant"),
    ("superadmin", "SuperAdmin"),
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

    status = models.BooleanField(default=True)

    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_budget_sheets'
    )

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title




class SheetPartener(models.Model):
    pid = models.CharField(max_length=24, unique=True, help_text="Unique identifier partener")
    role = models.CharField(max_length=50, choices=choise_role, default=choise_role[0][0])
    sheet = models.ForeignKey(
        BudgetSheet,
        on_delete=models.CASCADE,
        related_name='type_sheet_partenaire'
    )
    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_partener_sheet'
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



class TypeBudget(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_due_date = models.BooleanField(default=False, help_text="Indicates if the budget has an expiration date")
    is_date_created = models.BooleanField(default=False, help_text="Indicates if the budget has a creation date")
    is_compte = models.BooleanField(default=False, help_text="Indicates if the budget is a compte type")
    is_income = models.BooleanField(default=False)
    is_spent = models.BooleanField(default=False)
    is_saving = models.BooleanField(default=False)
    is_transaction = models.BooleanField(default=False)
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
    amount_reel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    file = models.FileField(upload_to="doc/", null=True, blank=True)
    file_reel = models.FileField(upload_to="doc/", null=True, blank=True)
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
        'SheetPartener',
        on_delete=models.CASCADE,
        related_name='user_validate'
    )

    def __str__(self):
        return self.title


class CommentDemande(models.Model):
    description = models.TextField()
    status = models.CharField(choices=choise_status, max_length=15 ,default=choise_status[0][0])

    demande = models.ForeignKey('Demande', related_name='demande_comment', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'customuser.Profile',
        on_delete=models.CASCADE,
        related_name='user_comment_demande'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def create_partener_profile(sender, instance, created, **kwargs):
    if created:
        pid = utility.generpid(24)
        while len(SheetPartener.objects.filter(pid=pid)) > 0:
            pid = utility.generpid(35)

        SheetPartener.objects.create(sheet=instance, pid=pid, role=choise_status[0][0],
                                user=instance.user)


# def save_partainer_profile(sender, instance, **kwargs):
#     instance.SheetPartener.save()


post_save.connect(create_partener_profile, sender=BudgetSheet)
# post_save.connect(save_partainer_profile, sender=BudgetSheet)


class SheetInvitation(models.Model):
    INVITATION_STATUS = (
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
        ('expired', 'Expirée'),
    )
    
    pid = models.CharField(max_length=24, unique=True)
    sheet = models.ForeignKey(BudgetSheet, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey('customuser.Profile', on_delete=models.CASCADE, related_name='sent_invitations')
    email_or_username = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=choise_role, default='consultation')
    status = models.CharField(max_length=20, choices=INVITATION_STATUS, default='pending')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Invitation pour {self.email_or_username} - {self.sheet.title}"
