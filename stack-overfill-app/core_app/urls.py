from django.urls import path
from .views import AskQuestionView, QuestionDetailView

app_name = 'core_app'

urlpatterns = [
    path('ask', AskQuestionView.as_view(), name='ask_question'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
]