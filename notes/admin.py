from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'color',
        'content',
        'date',
        'is_completed',
        'is_deleted',
        'created_at',
    )
    search_fields = (
        'id',
        'owner',
        'content',
    )
    ordering = (
        '-date',
        '-id',
        'created_at',
    )
    list_display_links = (
        'id',
        'owner',
        'content',
    )


@admin.register(models.Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'title',
        'content',
        'updated_at',
        'is_deleted',
    )
    search_fields = (
        'id',
        'owner',
        'title',
        'content',
    )
    ordering = (
        '-id',
        'updated_at',
    )
    list_display_links = (
        'id',
        'owner',
        'title',
    )
