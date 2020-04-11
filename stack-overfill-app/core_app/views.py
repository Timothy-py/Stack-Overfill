from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseBadRequest

from .models import Question
from .forms import QuestionForm, AnswerForm, AnswerAcceptanceForm

# Create your views here.


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