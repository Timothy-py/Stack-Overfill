from django.core.management import BaseCommand

from core_app.service import elasticsearch
from core_app.models import Question


class Command(BaseCommand):
    help = "Load all questions in the database into Elasticsearch"

    def handle(self, *args, **options):
        # get the model objects from the database
        queryset = Question.objects.all()
        # load the queryset into elasticsearch
        load_all = elasticsearch.bulk_load(queryset)

        if load_all:
            self.stdout.write(self.style.SUCCESS('Successfully loaded all questions in the database into Elasticsearch.'))

        else:
            self.stdout.write(self.style.WARNING('Some questions not loaded successfully. See logged errors'))