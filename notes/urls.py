from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path(
        'tasks/new/', views.TaskViewSet.as_view({
            'post': 'create',
        }), name='new_task'
    ),
    path(
        'tasks/<int:pk>/', views.TaskViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='edit_task'
    ),
    path(
        'tasks/<int:pk>/complete/', views.TaskViewSet.as_view({
            'post': 'complete',
        }), name='complete_task'
    ),
    path(
        'tasks/', views.TaskListViewSet.as_view({
            'get': 'list'
        }), name='tasks'
    ),
]
