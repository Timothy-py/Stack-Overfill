from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.shortcuts import reverse


# Create your views here.

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('user_app:login')
