from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.http import HttpResponseBadRequest

from .models import Question
from .forms import QuestionForm

# Create your views here.


# The CreateView render the template for GET requests and validate the form on POST requests.
class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'core_app/ask.html'

    # this method ensures the user field is pre-filled with the current user that makes the request.
    def get_initial(self):
        return {'user': self.request.user.id}

    def form_valid(self, form):
        action = self.request.POST.get('action')    # *******
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            preview = Question(
                    question=form.cleaned_data['question'],
                    title=form.cleaned_data(['title']),
                )
            context = self.get_context_data(preview=preview)
            return self.render_to_response(context=context)
        else:
            return HttpResponseBadRequest
