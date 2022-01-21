import json
from sre_constants import SUCCESS
from turtle import st
from django.core.management.base import BaseCommand
from api.models import Action, ProjectType, Strategy, Table, MonitoringStatus, User, Coa


class Command(BaseCommand):

    def seed_action(self):
        with open('api/json/action.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            Action.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding Action")

    def seed_project_type(self):
        with open('api/json/project_type.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            ProjectType.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding Project Type")

    def seed_strategy(self):
        with open('api/json/strategy.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            Strategy.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding Strategy")

    def seed_table(self):
        with open('api/json/table.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            Table.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding Table")

    def seed_monitoring_status(self):
        with open('api/json/monitoring_status.json') as f:
            data_list = json.load(f)

        for data in data_list:
            data['pk'] = data.pop('id')
            MonitoringStatus.objects.get_or_create(
                pk=data['pk'], defaults=data)
        self.comment("Seeding Monitoring Status")

    def seed_user_dev(self):
        with open('api/json/user.json') as f:
            data_list = json.load(f)
            
        for data in data_list:
            data['pk'] = data.pop('id')
            User.objects.get_or_create(
                pk=data['pk'], defaults=data)
        self.comment("Seeding User")

    def seed_coa(self):
        with open('api/json/coa.json') as f:
            data_list = json.load(f)
        for data in data_list:
            data['pk'] = data.pop('id')
            Coa.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding COA")

    def comment(self, comment):
        self.stdout.write(self.style.HTTP_SUCCESS('%s... ' %
                          comment)+self.style.SUCCESS('OK'))

    def handle(self, *args, **options):
        self.seed_action()
        self.seed_project_type()
        self.seed_strategy()
        self.seed_table()
        self.seed_monitoring_status()
        self.seed_user_dev()
        self.seed_coa()
