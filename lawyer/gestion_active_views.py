from django.contrib.postgres.functions import TransactionNow
from django.db import transaction
from django.shortcuts import render
from .models import Champs
from .models import TypeActivity
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

    if type_activity_id:
        try:
            type_activity = TypeActivity.objects.get(id=type_activity_id)
            used_champs = list(type_activity.champs.all())
            all_champs = list(Champs.objects.all())
            unused_champs = [champ for champ in all_champs if champ not in used_champs]
        except TypeActivity.DoesNotExist:
            type_activity = None

    context = {
        "type_activity": type_activity if type_activity_id else None,
        "used_champs": used_champs,
        "unused_champs": unused_champs
    }
    return render(request, "lawyer/activiter/htmx/details_type_activiter.html", context)
