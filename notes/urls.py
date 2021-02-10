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
            'get': 'retrieve',
        }), name='memo'
    ),
    path(
        'memo/<int:pk>/restore/', views.MemoTrashViewSet.as_view({
            'post': 'restore',
        }), name='restore_memo'
    ),
    path(
        'memos/', views.MemoListViewSet.as_view({
            'get': 'list',
        }), name='memos'
    ),
    path(
        'memos/trash/', views.MemoTrashListViewSet.as_view({
            'get': 'list',
        }), name='trash_memos'
    ),
    path(
        'memos/trash/empty/', views.MemoTrashViewSet.as_view({
            'post': 'empty',
        }), name='empty_trash_memos'
    ),
    path(
        'memos/shared/', views.SharedMemoListViewSet.as_view({
            'get': 'list',
        }), name='shared_memos'
    ),
    path(
        'memo/shared/<int:pk>/', views.SharedMemoViewSet.as_view({
            'get': 'retrieve',
        }), name='shared_memo'
    ),
]
