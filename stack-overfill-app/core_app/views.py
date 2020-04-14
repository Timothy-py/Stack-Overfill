from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DayArchiveView, RedirectView, TemplateView
from django.http import HttpResponseBadRequest
from django.utils.timezone import timezone
from django.shortcuts import reverse

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm, AnswerAcceptanceForm

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home_page.html'


# The CreateView render the template for GET requests and validate the form on POST requests.
class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'core_app/ask.html'

    # this method ensures the user field is pre-filled with the current user that makes the request.
    def get_initial(self):
        return {'user': self.request.user.id}

    def form_valid(self, form):
        action = self.request.POST.get('action')    # get the value returned by the form<button> in the template
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            preview = Question(
                    question=form.cleaned_data['question'],
                    title=form.cleaned_data(['title']),
                )
            context = self.get_context_data(preview=preview)
            return self.render_to_response(context=context)     # *****
        else:
            return HttpResponseBadRequest


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'

    ACCEPT_FORM = AnswerAcceptanceForm(initial={'accepted': True})
    REJECT_FORM = AnswerAcceptanceForm(initial={'accepted': False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add answer form to the context and pre-filled the user and question field
        context.update(
            {'answer_form': AnswerForm(initial={'user': self.request.user.id, 'question': self.object.id})}
        )

        # if the current user is same as the user that created the question being displayed;
        # load the accept and reject form.
        if self.object.can_accept_answers(self.request.user):
            # if self.model.can_accept_answers(user=self.request.user):
            context.update(
                {'accept_form': self.ACCEPT_FORM, 'reject_form': self.REJECT_FORM}
            )
        else:
            return context


class CreateAnswerView(LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    template_name = 'core_app/create_answer.html'

    def get_initial(self):
        return {
            'question': self.get_question().id,
            'user': self.request.user.id
        }

    def get_context_data(self, **kwargs):
        return super(CreateAnswerView, self).get_context_data(question=self.get_question(), **kwargs)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super(CreateAnswerView, self).form_valid(form)
        elif action == 'PREVIEW':
            preview_context = self.get_context_data(preview=form.cleaned_data['answer'])
            return self.render_to_response(context=preview_context)
        else:
            return HttpResponseBadRequest()

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])


class UpdateAnswerAcceptance(LoginRequiredMixin, UpdateView):
    form_class = AnswerAcceptanceForm
    queryset = Answer.objects.all()

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_invalid(self, form):
        return HttpResponseBadRequest(
            redirect_to=self.object.question.get_absolute_url()
        )


# The DayArchiveView is used to Listing all of objects published on a given day.
class DailyQuestionList(DayArchiveView):
    queryset = Question.objects.all()
    date_field = 'created'
    month_format = '%m'
    allow_empty = True      # *****


class TodaysQuestionList(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse(
            'core_app:daily_questions',
            kwargs={
                'day': today.day,
                'month': today.month,
                'year': today.year,
            }
        )
