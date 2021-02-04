from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path(
        'task/new/', views.TaskViewSet.as_view({
            'post': 'create',
        }), name='new_task'
    ),
    path(
        'task/<int:pk>/', views.TaskViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'delete',
        }), name='edit_task'
    ),
    path(
        'task/<int:pk>/complete/', views.TaskViewSet.as_view({
            'post': 'complete',
        }), name='complete_task'
    ),
    path(
        'tasks/', views.TaskListViewSet.as_view({
            'get': 'list'
        }), name='tasks'
    ),
    path(
        'memo/new/', views.MemoViewSet.as_view({
            'post': 'create',
        }), name='new_memo'
    ),
    path(
        'memo/<int:pk>/', views.MemoViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'delete',
        }), name='edit_memo'
    ),
    path(
        'memos/', views.MemoListViewSet.as_view({
            'get': 'list'
        }), name='memos'
    ),
]
