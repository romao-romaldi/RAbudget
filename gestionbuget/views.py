from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch, Sum
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime

from . import utility
from .models import (BudgetSheet, TypeBudget, Budget)
from  customuser.models import Profile
from .forms import (FormBudgetSheet, FormBudget, FormSection
                    )
from .utility import get_monthly_data_by_type, statistiques_par_jours


# Create your views here.

def index(request):
    pass

@login_required
def budget_sheet_create(request):
    """
    View to create a new budget sheet.
    """
    if request.method == 'POST':
        form = FormBudgetSheet(request.POST)
        if form.is_valid():
            while transaction.atomic():
                pid = utility.generpid(20)
                budget_sheet = form.save(commit=False)
                budget_sheet.user = request.user.profile
                budget_sheet.pid = pid
                budget_sheet.save()
            # After saving the budget sheet, redirect to a success page or render a template
                if budget_sheet:
                    r = utility.default_create_init(request, budget_sheet)
                    if request.htmx and r:
                        return render(request, 'gestionbuget/htmx/budgetsheet_created.html',
                                      {'budget_sheet': budget_sheet, 'htmx': True, "is_success": True,
                                       "form": FormBudgetSheet()
                                       }, status=201)
                    return render(request, 'gestionbuget/htmx/budgetsheet_created.html',
                                  {'budget_sheet': budget_sheet}, status=201)
                else :
                    return render(request, 'gestionbuget/htmx/budgetsheet_created.html',
                                  {'budget_sheet': budget_sheet, "form": FormBudgetSheet()})

    else:
        form = FormBudgetSheet()

    return render(request, 'gestionbuget/htmx/budget_sheet_create.html', {'form': form})

@login_required
def budget_sheet_list(request):
    """
    View to list all budget sheets.
    """

    budget_sheets = request.user.profile.user_budget_sheets.all()
    print("je ben", budget_sheets)

    context = {
        'budget_sheets': budget_sheets,
        "form": FormBudgetSheet()
        }
    return render(request, 'gestionbuget/budget_sheet_list.html', context)

@login_required
def budget_sheet_detail(request, pid):
    """
    View to display details of a specific budget sheet.
    """
    month = datetime.now().month
    year = datetime.now().year
    month_filter = request.GET.get('month_filter', None)
    print("je suis dans budget_sheet_detail", month_filter)
    Month_current = datetime.now()
    print("mois courant : ",Month_current)
    filter = ""


    if month_filter:
        month = int(month_filter.split("-")[1])
        year = int(month_filter.split("-")[0])
        print(month_filter, "type", type(month_filter))
        Month_current = datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d")
        filter = month_filter
    try:
        print("je suis pid", pid)
        budget_sheet = request.user.profile.user_budget_sheets.get(pid=pid)
        type_budgets = budget_sheet.type_budgets_sheet.all().prefetch_related(
            Prefetch('budgets',
                    queryset=Budget.objects.filter(date_created__month=month, date_created__year=year)
                     .order_by('-date_created'),
                    )
        )

        # buggets = type_budgets.budgets.all().filter(date_created__month=datetime.now().month)
    except:
        print("je suis dans erreurs")
        return render(request, 'gestionbuget/budget_sheet_not_found.html', {'pid': pid})

    date = datetime.strptime("2023-07-01", "%Y-%m-%d")



    context = {
        'budget_sheet': budget_sheet,
        "Month_current": Month_current,
        "form": FormBudget(),
        "type_budgets": type_budgets,
        "filter" : filter
    }

    return render(request, 'gestionbuget/budget_sheet_details.html', context)

@login_required
def chart_budget(request, pid):
    """
    View to display a chart of budgets for a specific budget sheet.
    """


    try:
        budget_sheet = request.user.profile.user_budget_sheets.get(pid=pid)

        data = get_monthly_data_by_type(Budget.objects.filter(type_budget__budget_sheet__pid=pid))

    except:
        return JsonResponse({}, safe=False, status=404)
    return JsonResponse(data, safe=False, status=200)

@login_required
def chart_budget_month(request, pid):
    """
    View to display a chart of budgets for a specific budget sheet.
    """
    month_filter = request.GET.get('month_filter', None)
    budget_sheet = request.user.profile.user_budget_sheets.get(pid=pid)

    try:
        budget_sheet = request.user.profile.user_budget_sheets.get(pid=pid)
        print(budget_sheet.pid, )
        buget = Budget.objects.filter(type_budget__budget_sheet__pid=budget_sheet.pid)
        if month_filter:
            data = statistiques_par_jours(buget,
                            datetime.strptime(f"{month_filter}-01", "%Y-%m-%d"))
        else:
            data =statistiques_par_jours(buget)
    except:
        print("je suis erreur ", month_filter)
        return JsonResponse({}, safe=False, status=404)
    return JsonResponse(data, safe=False, status=200)

@login_required
def created_budget(request, pid):
    # try:
    budget_sheet = request.user.profile.user_budget_sheets.get(pid=pid)
    month = datetime.now().month
    year = datetime.now().year
    if request.method == "POST":
        type_budget = request.POST.get("type_budget", None)
        type_budget = budget_sheet.type_budgets_sheet.get(id=type_budget)

        form = FormBudget(request.POST)
        print("je print form", form)
        if form.is_valid():
            print("je suis pid", budget_sheet)
            f = form.save(commit=False)
            f.type_budget = type_budget
            f.user = request.user.profile
            f.pid = utility.generpid(21)
            f.save()

            if request.htmx:
                return render(request, 'gestionbuget/htmx/create_budgets.html',
                              {"type_budget":type_budget, "budget":f,
                               'htmx': True, "is_success": True, "form": FormBudget(),
                               "budget_sheet":budget_sheet
                               }, status=201)
            return render(request, 'gestionbuget/htmx/create_budgets.html',
                              {"type_budget":type_budget, "budget":f, "budget_sheet":budget_sheet}, status=201)
        return render(request, 'gestionbuget/htmx/create_budgets.html',
                      {"type_budget": type_budget, "form":form, "budget_sheet":budget_sheet})



    # except:
    #     print("je suis dans erreurs")
    #     return render(request, 'gestionbuget/budget_sheet_not_found.html', {'pid': pid})
    #
    return render(request, 'gestionbuget/htmx/create_budgets.html',
                  {"form":FormBudget(), "type_budget":budget_sheet.type_budgets_sheet.last(),
                   "form_section": FormSection()})


@login_required
def create_section(request, pid):
    context = {
        "form": FormSection()
    }
    return render(request, "", )


@login_required
def create_demande(request, pid):



    context = {

    }
    return render(request, "", context)





