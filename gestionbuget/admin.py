from django.contrib import admin
from .models import BudgetSheet, TypeBudget, Budget
# Register your models here.

admin.site.register(BudgetSheet)
admin.site.register(TypeBudget)
admin.site.register(Budget)