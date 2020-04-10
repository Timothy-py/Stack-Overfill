from django.urls import path
from .views import AskQuestionView

app_name = 'core_app'

urlpatterns = [
    path('ask', AskQuestionView.as_view(), name='ask_question')
]