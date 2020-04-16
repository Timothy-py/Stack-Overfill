from django.db import models
from django.conf import settings
from django.urls.base import reverse

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=140)
    question = models.TextField()
    # django recommends that that you never reference django.contrib.auth.models.User directly
    # but using either settings.AUTH_USER_MODEL or django.contrib.auth.get_user_mode()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)   # automatically set d field 2 now wen d obj is first created
                                                        # as opposed to auto_now which is for updates.

    def __str__(self):
        return self.title

    # a method to redirect to the detail page of a question immediately it's created
    def get_absolute_url(self):
        return reverse('core_app:question_detail', kwargs={'pk': self.id})

    def can_accept_answers(self, user):     # ***
        return user == self.user

    # turns each model object into a dictionary that is suitable for loading into Elasticsearch.
    def as_elasticsearch_dict(self):
        return {
            # custom fields required by elasticsearch.
            '_id': self.id,
            '_type': 'doc',
            'text': f"{self.title}\n{self.question}",

            'question_body': self.question,
            'title': self.title,
            'id': self.id,
            'created': self.created
        }


class Answer(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.title} - Answer"

    class Meta:
        ordering = ('-created',)     # descending order, to ensure that the newest answers be listed first
