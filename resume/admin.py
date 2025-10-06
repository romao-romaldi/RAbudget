from django.contrib import admin
from .models import Hierarchie, Resume, CommentResume


@admin.register(Hierarchie)
class HierarchieAdmin(admin.ModelAdmin):
    list_display = ['user', 'superieur', 'budget_sheet', 'created_at']
    list_filter = ['budget_sheet', 'created_at']
    search_fields = ['user__user__username', 'superieur__user__username']
    raw_id_fields = ['user', 'superieur', 'budget_sheet']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'budget_sheet', 'date_resume', 'status', 'destinataire', 'created_at']
    list_filter = ['status', 'budget_sheet', 'date_resume', 'created_at']
    search_fields = ['title', 'content', 'author__user__username']
    raw_id_fields = ['author', 'destinataire', 'budget_sheet']
    readonly_fields = ['pid', 'created_at', 'updated_at', 'submitted_at', 'validated_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('pid', 'title', 'content', 'date_resume', 'status')
        }),
        ('Relations', {
            'fields': ('budget_sheet', 'author', 'destinataire')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'submitted_at', 'validated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CommentResume)
class CommentResumeAdmin(admin.ModelAdmin):
    list_display = ['resume', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__user__username', 'resume__title']
    raw_id_fields = ['resume', 'author']
