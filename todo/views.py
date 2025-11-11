from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.utils.translation.trans_real import translation
from pygments.lexer import using

from customuser.models import Profile
from .models import (Todo, TodoResponsible, TodoValidation, TodoComment, TodoCompleted
                     )
from .forms import TodoForm

def assign_default_roles(todo, creator_user):
    """
    Assigne automatiquement le créateur comme responsable et validateur
    s'il n'y en a pas déjà d'assignés
    """
    # Vérifier et assigner responsable par défaut
    if not todo.todo_colaborators.exists():
        TodoResponsible.objects.get_or_create(
            todo=todo,
            user=creator_user,
            defaults={'user': creator_user}
        )

    # Vérifier et assigner validateur par défaut
    if not todo.todo_validations.exists():
        TodoValidation.objects.get_or_create(
            todo=todo,
            user=creator_user,
            defaults={'user': creator_user}
        )
@login_required
def todo_list(request):
    """
    Affiche la liste des todos avec filtrage par statut
    """
    # Récupérer le filtre depuis les paramètres GET
    status_filter = request.GET.get('status', '')

    # Filtrer les todos selon le statut
    if status_filter:
        todos = Todo.objects.filter(status=status_filter)
    else:
        todos = Todo.objects.all()

    # Trier par date de création (plus récentes d'abord)
    todos = todos.order_by('-created_at')

    # Assigner automatiquement les rôles par défaut pour toutes les todos
    for todo in todos:
        assign_default_roles(todo, todo.user.user if todo.user else request.user)

    users = Profile.objects.all()

    context = {
        "todos": todos,
        "users": users,
        "current_filter": status_filter,
    }

    return render(request, 'todo/todo_list.html', context)

@login_required
def todo_detail(request, todo_id):
    # Fetch the todo item by its ID
    todo = Todo.objects.get(id=todo_id)

    # Assigner automatiquement les rôles par défaut si nécessaire
    assign_default_roles(todo, todo.user.user if todo.user else request.user)

    # Fetch related data if needed, e.g., comments, collaborators, validations
    comments = todo.comments.all()
    responsible = todo.todo_colaborators.all()
    validations = todo.todo_validations.all()

    context = {
        'todo': todo,
        'responsible': responsible,
        'validations': validations,
        'user': request.user,
    }

    return render(request, 'todo/details_todo.html', context)

@login_required
def todo_create(request):
    # This is a placeholder for the actual implementation
    # In a real application, you would handle form submission to create a new todo item
    # For now, we will just render the template without any context
    if request.method == 'POST':
        # Handle form submission here
        # return redirect('todo_detail', todo_id=todo.id)
        forms = TodoForm(request.POST)
        responsible = (request.POST.get('isResponsible', [])).split(",")
        print("responsible :", responsible)
        validators = (request.POST.get('validators', [])).split(",")
        print("je suis :", validators)

        if forms.is_valid() and responsible and validators:
            try:
                with transaction.atomic():
                    todo = forms.save(commit=False)
                    todo.user = request.user.profile
                    todo.save()

                    # Créer les responsables assignés
                    responsables_crees = 0
                    for i in responsible:
                        if i.strip().isdigit():
                            responsable_id = int(i.strip())
                            responsable_user = Profile.objects.filter(id=responsable_id).first()
                            if responsable_user:
                                TodoResponsible.objects.get_or_create(
                                    todo=todo,
                                    user=responsable_user.user
                                )
                                responsables_crees += 1

                    # Créer les validateurs assignés
                    validateurs_crees = 0
                    for i in validators:
                        if i.strip().isdigit():
                            validateur_id = int(i.strip())
                            validateur_user = Profile.objects.filter(id=validateur_id).first()
                            if validateur_user:
                                TodoValidation.objects.get_or_create(
                                    todo=todo,
                                    user=validateur_user.user
                                )
                                validateurs_crees += 1

                    # Assigner automatiquement le créateur comme responsable/validateur par défaut
                    assign_default_roles(todo, request.user)

                # Redirection après succès
                if request.htmx:
                    return render(request, "todo/create_todo.html", {
                        "users": Profile.objects.all(),
                        "success": True,
                        "message": f"Todo créée avec succès ! {responsables_crees} responsables et {validateurs_crees} validateurs assignés."
                    })
                else:
                    return redirect('todo_detail', todo_id=todo.id)

            except Exception as e:
                print(f"Erreur lors de la création: {e}")
                if request.htmx:
                    return render(request, "todo/create_todo.html", {
                        "users": Profile.objects.all(),
                        "form": forms,
                        "error": f"Erreur lors de la création: {str(e)}"
                    })

        elif request.method == 'POST':
            # Formulaire invalide ou données manquantes
            error_msg = "Veuillez remplir tous les champs correctement"
            if not responsible:
                error_msg += " (Sélectionnez au moins un responsable)"
            if not validators:
                error_msg += " (Sélectionnez au moins un validateur)"

            if request.htmx:
                return render(request, "todo/create_todo.html", {
                    "users": Profile.objects.all(),
                    "form": forms,
                    "error": error_msg
                })



    context = {
        "form": TodoForm(),  # Initialize the form for creating a new todo
        "users": Profile.objects.all()
    }

    return render(request, 'todo/create_todo.html', context)

@login_required
def todo_update(request, todo_id):
    """
    Modifie une todo existante avec gestion des responsables et validateurs
    """
    # Récupérer la todo ou 404 si elle n'existe pas ou n'appartient pas à l'utilisateur
    todo = get_object_or_404(Todo, id=todo_id, user=request.user.profile)

    if request.method == 'POST':
        forms = TodoForm(request.POST, instance=todo)

        if forms.is_valid():
            try:
                with transaction.atomic():
                    # Sauvegarder les modifications de base
                    forms.save()

                    # Note: Les responsables et validateurs ne sont modifiés que lors de la création
                    # Pour la modification, on pourrait ajouter cette logique si nécessaire

                # Réponse HTMX pour mise à jour dynamique
                if request.htmx:
                    return render(request, "todo/edit_todo.html", {
                        "todo": todo,
                        "form": forms,
                        "success": True,
                        "message": "Todo mise à jour avec succès !"
                    })
                else:
                    return redirect('todo_list')

            except Exception as e:
                print(f"Erreur lors de la mise à jour: {e}")
                if request.htmx:
                    return render(request, "todo/edit_todo.html", {
                        "todo": todo,
                        "form": forms,
                        "error": f"Erreur lors de la mise à jour: {str(e)}"
                    })

        elif request.htmx:
            return render(request, "todo/edit_todo.html", {
                "todo": todo,
                "form": forms,
                "error": "Veuillez corriger les erreurs dans le formulaire"
            })

    # Affichage initial du formulaire
    context = {
        'todo': todo,
        'form': TodoForm(instance=todo),
    }

    return render(request, 'todo/edit_todo.html', context)

@login_required
def todo_delete(request, todo_id):
    # Fetch the todo item by its ID
    todo = get_object_or_404(Todo, id=todo_id, user=request.user.profile)

    if request.method == 'POST' and todo.is_validated and todo.is_completed and todo.status == 'completed':
        # Handle form submission to delete the todo item
        todo.delete()
        # Redirect to the todo list after deletion
        return redirect('todo_list')

    context = {
        'todo': todo,
    }

    return render(request, 'todo/todo_delete.html', context)

@login_required
def todo_complete(request, todo_id):
    """
    Termine une todo - nécessite que la todo soit validée et que l'utilisateur soit responsable
    """
    # Vérifier que l'utilisateur est responsable de cette todo
    todo = get_object_or_404(Todo, id=todo_id, todo_colaborators__user=request.user)

    # Vérifier que la todo est validée avant de permettre la completion
    if not todo.is_validated:
        if request.htmx:
            return render(request, "todo/details_todo.html", {
                "todo": todo,
                "responsible": todo.todo_colaborators.all(),
                "validations": todo.todo_validations.all(),
                "user": request.user,
                "error": "La tâche doit être validée avant d'être terminée."
            })
        else:
            return redirect('todo_detail', todo_id=todo_id)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Marquer la todo comme terminée
                todo.mark_completed()
                print("todo", todo.status)
                TodoCompleted.objects.create(
                    todo=todo,
                    user=request.user.profile,
                    is_completed=True
                )

            # Réponse HTMX pour mise à jour dynamique
            if request.htmx:
                return render(request, "todo/details_todo.html", {
                    "todo": todo,
                    "responsible": todo.todo_colaborators.all(),
                    "validations": todo.todo_validations.all(),
                    "success": True,
                    "message": "Todo terminée avec succès !",
                    "user": request.user,
                })
            else:
                return redirect('todo_detail', todo_id=todo_id)

        except Exception as e:
            print(f"Erreur lors de la completion: {e}")
            if request.htmx:
                return render(request, "todo/details_todo.html", {
                    "todo": todo,
                    "responsible": todo.todo_colaborators.all(),
                    "validations": todo.todo_validations.all(),
                    "error": f"Erreur lors de la completion: {str(e)}",
                    "user": request.user,
                })

    # Affichage de la page de completion (si nécessaire)
    context = {
        'todo': todo,
        'responsible': todo.todo_colaborators.all(),
        'validations': todo.todo_validations.all(),
        'user': request.user,
    }

    return render(request, 'todo/details_todo.html', context)

@login_required
def todo_validate(request, todo_id):
    """
    Valide une todo - l'utilisateur doit être assigné comme validateur pour cette todo
    """
    # Vérifier que l'utilisateur est bien assigné comme validateur pour cette todo
    todo_validation = get_object_or_404(
        TodoValidation,
        todo_id=todo_id,
        user=request.user.profile
    )

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Marquer la validation comme faite
                todo_validation.is_validated = True
                todo_validation.save()

                # Mettre à jour le statut de la todo si elle est complétée
                todo_validation.todo.mark_validated()

            # Réponse HTMX pour mise à jour dynamique
            if request.htmx:
                return render(request, "todo/details_todo.html", {
                    "todo": todo_validation.todo,
                    "responsible": todo_validation.todo.todo_colaborators.all(),
                    "validations": todo_validation.todo.todo_validations.all(),
                    "success": True,
                    "message": "Todo validée avec succès !",
                    "user": request.user,
                })
            else:
                return redirect('todo_detail', todo_id=todo_id)

        except Exception as e:
            print(f"Erreur lors de la validation: {e}")
            if request.htmx:
                return render(request, "todo/details_todo.html", {
                    "todo": todo_validation.todo,
                    "responsible": todo_validation.todo.todo_colaborators.all(),
                    "validations": todo_validation.todo.todo_validations.all(),
                    "error": f"Erreur lors de la validation: {str(e)}",
                    "user": request.user,
                })

    # Affichage de la page de validation (si nécessaire)
    context = {
        'todo': todo_validation.todo,
        'responsible': todo_validation.todo.todo_colaborators.all(),
        'validations': todo_validation.todo.todo_validations.all(),
        'user': request.user,
    }

    return render(request, 'todo/details_todo.html', context)



