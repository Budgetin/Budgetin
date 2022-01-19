import json
from django.core.management.base import BaseCommand
from api.models import Action,ProjectType,Strategy,Table

class Command(BaseCommand):

    def seed_action(self):
        with open('api/json/action.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            Action.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Action seeded")

    def seed_project_type(self):
        with open('api/json/project_type.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            ProjectType.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Project Type seeded")

    def seed_strategy(self):
        with open('api/json/strategy.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            Strategy.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Strategy seeded")

    def seed_table(self):
        with open('api/json/table.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            Table.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Table seeded")

    def comment(self, comment):
        self.stdout.write(self.style.HTTP_SUCCESS('%s' % comment))

    def handle(self, *args, **options):
        self.seed_action()
        self.seed_project_type()
        self.seed_strategy()
        self.seed_table()
