import json
from django.core.management.base import BaseCommand
from api.models import ProjectType, Strategy, MonitoringStatus, User, Coa, Product, Planning


class Command(BaseCommand):

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

    def seed_product(self):
        with open('api/json/product.json') as f:
            data_list = json.load(f)
        for data in data_list:
            data['pk'] = data.pop('id')
            Product.all_object.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding Product")

    def seed_planning(self):
        with open('api/json/planning.json') as f:
            data_list = json.load(f)
        for data in data_list:
            data['pk'] = data.pop('id')
            Planning.objects.get_or_create(pk=data['pk'], defaults=data)
        self.comment("Seeding Planning")

    def comment(self, comment):
        self.stdout.write(self.style.HTTP_SUCCESS('%s... ' %
                          comment)+self.style.SUCCESS('OK'))

    def handle(self, *args, **options):
        self.seed_project_type()
        self.seed_strategy()
        self.seed_monitoring_status()
        self.seed_user_dev()
        self.seed_coa()
        self.seed_product()
        self.seed_planning()
