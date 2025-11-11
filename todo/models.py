from django.db import models
from customuser.models import Profile

# Create your models here.
TodoStatusChoices = (
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('archived', 'Archived'),
)

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    status = models.CharField(choices=TodoStatusChoices, default='pending')
    priority = models.CharField(max_length=20, null=True, blank=True)
    date_execution = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='todos'
    )

    def mark_completed(self):
        self.completed = True
        self.status = 'completed'
        self.save()

    def mark_incomplete(self):
        self.completed = False
        self.save()

    def mark_validated(self):
        self.is_validated = True
        self.save()

    def __str__(self):
        return self.title


class TodoResponsible(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='todo_colaborators')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='todo_colaborators_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'

class TodoValidation(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='todo_validations')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='todo_validations_user')
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Todo Validation'
        verbose_name_plural = 'Todo Validations'


class TodoComment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='todo_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Todo Comment'
        verbose_name_plural = 'Todo Comments'

    def __str__(self):
        return f'Comment by {self.user.last_name} on {self.todo.title}'


class TodoCompleted(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='completed_todos')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='completed_todos_user')
    completed_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = 'Todo Completed'
        verbose_name_plural = 'Todos Completed'

    def __str__(self):
        return f'{self.todo.title} completed by {self.user.last_name}'
