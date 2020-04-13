from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView


# Create your views here.

class RegisterView(CreateView):
    template_name = 'user_app/register.html'
    form_class = UserCreationForm