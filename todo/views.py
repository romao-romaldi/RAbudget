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

# Create your views here.
@login_required
def todo_list(request):
    # This is a placeholder for the actual implementation
    # In a real application, you would fetch todos from the database and pass them to the template
    # For now, we will just render the template without any context

    todos = Todo.objects.all()
    users = Profile.objects.all()

    context = {
        "todos": todos,
        "users": users,
    }


    return render(request, 'todo/todo_list.html', context)

@login_required
def todo_detail(request, todo_id):
    # Fetch the todo item by its ID
    todo = Todo.objects.get(id=todo_id)

    # Fetch related data if needed, e.g., comments, collaborators, validations
    comments = todo.comments.all()
    responsible = todo.TodoResponsible.all()
    validations = todo.validations.all()

    context = {
        'todo': todo,
        'comments': comments,
        'responsible': responsible,
        'validations': validations,
    }

    return render(request, 'todo/todo_detail.html', context)

@login_required
def todo_create(request):
    # This is a placeholder for the actual implementation
    # In a real application, you would handle form submission to create a new todo item
    # For now, we will just render the template without any context
    if request.method == 'POST':
        # Handle form submission here
        # return redirect('todo_detail', todo_id=todo.id)
        forms = TodoForm(request.POST)
        responsible = (request.POST.get('isResponsible', "")).split(",")
        print("responsible :", responsible)
        validators = (request.POST.get('validators', "")).split(",")
        print("je suis :", validators)

        if forms.is_valid() and responsible and validators:
            try:
                with transaction.atomic():
                    todo = forms.save(commit=False)
                    todo.user = request.user.profile
                    todo.save()


                    if len(responsible) < 0:
                        TodoResponsible.objects.create(todo=todo, user=request.user)
                    else:
                        for i in responsible:
                            responsible_user = Profile.objects.get_or_None(id=int(i))
                            if responsible_user:
                                TodoResponsible.objects.create(todo=todo, user=responsible_user.user)


                    if len(validators) < 0:
                        TodoValidation.objects.create(todo=todo, user=request.user)
                    else :
                        for i in validators:
                            validators_user = Profile.objects.get_or_None(id=i)
                            if validators_user:
                                TodoValidation.objects.create(todo=todo, user=validators_user.user)


            except Exception as e:
                # Handle exceptions, the transaction will be rolled back automatically
                print(f"Transaction failed: {e}")

        if request.htmx:
            return render(request, "todo/create_todo.html", context={"users": Profile.objects.all()})



    context = {
        "form": TodoForm(),  # Initialize the form for creating a new todo
        "users": Profile.objects.all()
    }

    return render(request, 'todo/create_todo.html', context)

@login_required
def todo_update(request, todo_id):
    # Fetch the todo item by its ID
    todo = get_object_or_404(Todo, id=todo_id, user=request.user.profile)

    if request.method == 'POST':
        # Handle form submission to update the todo item
        # For example, update the title and description
        forms = TodoForm(request.POST, instance=todo)
        if forms.is_valid():
            forms.save()
            # Redirect to the todo detail page after updating
            return redirect('todo_detail', todo_id=todo.id)
        else:
            # Handle form errors
            pass

        pass  # Replace with actual form handling logic

    context = {
        'todo': todo,
    }

    return render(request, 'todo/todo_update.html', context)

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
    # Fetch the todo item by its ID
    # todo = get_object_or_404(Todo, id=todo_id, user=request.user.profile)
    todo = get_object_or_404(Todo, id=todo_id, todo_colaborators__user=request.user.profile)
    todo_collaborators = get_object_or_404(TodoResponsible, todo=todo, user=request.user.profile)

    if request.method == 'POST':
        # Mark the todo as completed
        is_completed = request.POST.get('is_completed', 'false')

        try:
            with transaction.atomic():
                todo.mark_completed()
                todo_completes = TodoCompleted.objects.create(todo=todo, user=request.user.profile,is_completed='true')

        except Exception as e:
            print("Transaction failed: ", e)


        # Redirect to the todo detail page after completion
        return redirect('todo_detail', todo_id=todo.id)

    context = {
        'todo': todo,
    }

    return render(request, 'todo/todo_complete.html', context)

@login_required
def todo_validate(request, todo_id):
    # Fetch the todo item by its ID
    # todo = get_object_or_404(Todo, id=todo_id, todo_validations__user=request.user.profile)
    todo_validations = get_object_or_404(TodoValidation, user=request.user.profile)

    if request.method == 'POST':
        # Mark the todo as validated
        todo_validations.is_validated = True
        todo_validations.save()
        todo_validations.todo.mark_validated()
        # Redirect to the todo detail page after validation
        return redirect('todo_detail', todo_id=todo.id)

    context = {
        'todo': todo,
    }

    return render(request, 'todo/todo_validate.html', context)



