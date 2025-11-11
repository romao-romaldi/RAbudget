from django.urls import path

from .views import (todo_list, todo_detail, todo_create, todo_update, todo_validate, todo_complete)

app_name = 'todo'

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:todo_id>/', todo_detail, name='todo_detail'),
    path('<int:todo_id>/update/', todo_update, name='todo_update'),
    path('<int:todo_id>/validate/', todo_validate, name='todo_validate'),
    path('<int:todo_id>/complete/', todo_complete, name='todo_complete'),
    path('create/', todo_create, name='todo_create'),
]