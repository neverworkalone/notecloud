from django.urls import path

from . import views

app_name = 'forums'

urlpatterns = [
    path(
        'question/new/', views.QuestionViewSet.as_view({
            'post': 'create',
        }), name='new_question'
    ),
    path(
        'question/<int:pk>/answer/', views.QuestionAnswerViewSet.as_view({
            'post': 'partial_update',
        }), name='answer_question'
    ),
    path(
        'questions/', views.QuestionListViewSet.as_view({
            'get': 'list'
        }), name='questions'
    ),
    path(
        'question/<int:pk>/', views.QuestionRetrieveViewSet.as_view({
            'get': 'retrieve',
        }), name='question'
    ),
]
