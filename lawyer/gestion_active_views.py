from django.contrib.postgres.functions import TransactionNow
from django.db import transaction
from django.shortcuts import render
from .models import TypeActivity, Champs, CategoryActivity, SubCategory
# Create your views here.




def gestion_active_views(request):

    champs = Champs.objects.all()
    type_activity = TypeActivity.objects.all()
    # print("je suis dans gestion active views", data)

    context = {
        "champs": champs,
        "type_activity": type_activity,
    }
    return render(request, 'lawyer/activiter/gestion_activiter.html', context)


def add_type_activiter(request):
    context = {
        "initialChamps": None,
        "success": False
    }
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        champs_ids = request.POST.get("champs")

        if champs_ids:
            champs_ids = [int(id) for id in champs_ids.split(",") if id.isdigit()]
            context["initialChamps"] = champs_ids

        if isinstance(champs_ids, list) and len(champs_ids) > 0:

            with transaction.atomic():
                type_activity = TypeActivity.objects.create(
                    name=name,
                    description=description,
                )
                print(type_activity, type(type_activity))
                type_activity.champs.set(champs_ids)
                type_activity.save()
                context = {
                    "type_activity": type_activity,
                    "initialChamps": [],
                    "success": True
                }
                return render(request, "lawyer/activiter/htmx/add_activity.html", context)
        else:
            context["error"] = "Veuillez sélectionner au moins un champ."

    return render(request, "lawyer/activiter/htmx/add_activity.html", context)

def details_type_active(request, id):
    type_activity_id = id
    used_champs = []
    unused_champs = []
    categorie = False
    if type_activity_id:
        try:
            type_activity = TypeActivity.objects.get(id=type_activity_id)
            # subCategorie = type_activity.
            type_champs = type_activity.champs.all()
            if type_champs.filter(name="categorie").first():
                categorie = True
            used_champs = list(type_champs)
            all_champs = list(Champs.objects.all())
            unused_champs = [champ for champ in all_champs if champ not in used_champs]
        except TypeActivity.DoesNotExist:
            type_activity = None

    context = {
        "type_activity": type_activity if type_activity_id else None,
        "used_champs": used_champs,
        "unused_champs": unused_champs,
        "categorie" : categorie

    }
    return render(request, "lawyer/activiter/htmx/details_type_activiter.html", context)

def active_champs_types(request, id, champs_id):
    type_activity = TypeActivity.objects.filter(id=id).first()
    champs = Champs.objects.filter(id=champs_id).first()
    if request.method == "POST":
        status = request.POST.get("status", False)
        print("je uis le status", status)
        if status:
            type_activity.champs.add(champs)

        else:
            type_activity.champs.remove(champs)

        context = {
            "status": status,
            "success": True,
            "type_activity": type_activity,
            "champs": champs
        }
        return render(request, "lawyer/activiter/htmx/champs.html", context)

    context = {

    }
    return render(request, "lawyer/activiter/htmx/champs.html", context)


def add_categorie_activity(request, id):
    type_activity = TypeActivity.objects.filter(id=id).first()
    if request.method == "POST" and type_activity:
        name = request.POST.get("name", None)
        description = request.POST.get("description", None)

        if not CategoryActivity.objects.filter(type_activity=type_activity).first():
            CategoryActivity.objects.create(type_activity=type_activity)

        if name:
            categorie_activity = type_activity.categoryactivity

            sub = SubCategory.objects.create(name=name, description=description, category=categorie_activity)
            context = {
                "sub_categorie": sub,
                "categorie": categorie_activity
            }
            return render(request, "lawyer/activiter/htmx/subcategorie.html", context)

    context = {
        "type_activity":type_activity
    }
    return render(request, "lawyer/activiter/htmx/subcategorie.html", context)
