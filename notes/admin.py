from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'color',
        'content',
        'date_from',
        'date_until',
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
        '-id',
    )
    list_display_links = (
        'id',
        'content',
    )


@admin.register(models.Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'title',
        'doctype',
        'updated_at',
        'is_pinned',
        'is_shared',
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
    )
    list_display_links = (
        'id',
        'title',
    )
