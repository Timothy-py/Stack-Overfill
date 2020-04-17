from django.urls import path
from .views import AskQuestionView, QuestionDetailView, CreateAnswerView, \
    UpdateAnswerAcceptance, DailyQuestionList, HomePageView, \
    TodaysQuestionList, SearchView

app_name = 'core_app'

urlpatterns = [
    path('home', HomePageView.as_view(), name='home_page'),
    path('ask', AskQuestionView.as_view(), name='ask_question'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:pk>/answer', CreateAnswerView.as_view(), name='answer_question'),
    path('answer/<int:pk>/accept', UpdateAnswerAcceptance.as_view(), name='update_answer_acceptance'),
    path('daily/<int:year>/<int:month>/<int:day>/', DailyQuestionList.as_view(), name='daily_questions'),
    path('today', TodaysQuestionList.as_view(), name='today_questions'),
    path('q/search', SearchView.as_view(), name='question_search')
]