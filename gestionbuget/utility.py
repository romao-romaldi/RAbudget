import random
from django.db.models import  Count, Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, date, timedelta

from .models import TypeBudget


def generpid(number_caracter:int):
    pid = "".join(random.choices("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             k=number_caracter))
    return pid


def default_create_init(request, budgetSheet):
    """
    Function to create initial budget types for a new budget sheet.
    """
    types = [
        {
            "name": "Revenus", "description": "Budget pour les revenus",
            "is_due_date": False, "is_date_created": True, "is_compte": False,
            "is_salary": True,"is_revenu":True
        },
        {
            "name": "Dépenses", "description": "Budget pour les dépenses",
            "is_due_date": True, "is_date_created": True, "is_compte": False,
            "is_salary": False,"is_revenu":False
         },
        {
            "name": "Epargne", "description": "Budget pour d'épargne",
            "is_due_date": False, "is_date_created": True, "is_compte": True,
            "is_salary": False,"is_revenu":False
        }
    ]

    for type_data in types:
        type_budget = TypeBudget.objects.create(
            name=type_data["name"],
            description=type_data["description"],
            is_due_date=type_data["is_due_date"],
            is_date_created=type_data["is_date_created"],
            is_compte=type_data["is_compte"],
            is_salary=type_data["is_salary"],
            is_income = type_data["is_revenu"],
            budget_sheet=budgetSheet,
            user=request.user.profile
        )
        type_budget.save()

    return True


def get_monthly_data_by_type(YourModel):
    monthly_data = (YourModel.values('amount_reel', 'date_created', "type_budget__is_income", "type_budget__is_spent"))

    # # Convertir les résultats en dictionnaire pour faciliter l'accès
    result_spent = {}
    result_icome = {}

    for entry in monthly_data:
        month = int(entry['date_created'].strftime('%m'))  # Formater la date
        type_field = entry['type_budget__is_income']
        type_field_spent = entry["type_budget__is_spent"]

        if month not in result_spent and month not in result_icome:
            result_spent[month] = 0
            result_icome[month] = 0
        if type_field:
            result_icome[month] = result_icome[month] + entry['amount_reel']
        elif type_field_spent:
            result_spent[month] = result_spent[month] + entry['amount_reel']

    spent = [ result_spent.get(c, 0) for c in range(1, 13)]
    icome = [ result_icome.get(c, 0) for c in range(1, 13)]

    return {
        "spent": spent,
        "icome": icome,

    }

def recuper_le_mois_en_francais(mois=1):
    """
    Fonction pour récupérer le nom du mois en français à partir de son numéro.
    """
    mois_en_francais = {
        1: "Janvier",
        2: "Février",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin",
        7: "Juillet",
        8: "Août",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Décembre"
    }
    return mois_en_francais.get(mois, "")

def statistiques_par_jours(Budget, aujourdhui=date.today()):
    """
    Fonction pour récupérer et afficher les statistiques par jour du mois actuel.
    """
    premier_jour_mois = aujourdhui.replace(day=1)
    dernier_jour_mois = (premier_jour_mois.replace(month=premier_jour_mois.month + 1) - timedelta(
        days=1)) if premier_jour_mois.month < 12 else (
                premier_jour_mois.replace(year=premier_jour_mois.year + 1, month=1) - timedelta(days=1))

    statistiques_par_jour = {
        "spent": [],
        "income": [],
        "x_data" : [],
        'mois_actuel': recuper_le_mois_en_francais(aujourdhui.month) + " " + aujourdhui.strftime("%Y")
    }

    for jour in range((dernier_jour_mois - premier_jour_mois).days + 1):
        date_actuelle = premier_jour_mois + timedelta(days=jour)
        statistiques_par_jour["x_data"].append(date_actuelle.day)
        budget = Budget.filter(date_created__date=date_actuelle).values('amount_reel', 'date_created',
        'type_budget__is_income', "type_budget__is_spent")

        if budget.exists():
            total_spent = budget.filter(type_budget__is_spent=True).aggregate(total=Sum('amount_reel'))['total'] or 0
            total_income = budget.filter(type_budget__is_income=True).aggregate(total=Sum('amount_reel'))['total'] or 0

            statistiques_par_jour["spent"].append(total_spent)
            statistiques_par_jour["income"].append(total_income)
        else:
            statistiques_par_jour["spent"].append(0)
            statistiques_par_jour["income"].append(0)
    return statistiques_par_jour

