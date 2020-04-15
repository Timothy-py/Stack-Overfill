from django.contrib import admin
from .models import Question, Answer

# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    fields = ['title', 'question', 'user', 'created']
    search_fields = ('title',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer,)
