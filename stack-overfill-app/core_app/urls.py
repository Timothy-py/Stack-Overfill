from django.urls import path
from .views import AskQuestionView, QuestionDetailView, CreateAnswerView, UpdateAnswerAcceptance

app_name = 'core_app'

urlpatterns = [
    path('ask', AskQuestionView.as_view(), name='ask_question'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:pk>/answer', CreateAnswerView.as_view(), name='answer_question'),
    path('answer/<int:pk>/accept', UpdateAnswerAcceptance.as_view(), name='update_answer_acceptance'),
]