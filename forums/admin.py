from django.contrib import admin

from . import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'address',
        'title',
        'state',
        'assignee',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'id',
        'user',
        'address',
        'title',
        'content',
        'answer',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'title',
    )
