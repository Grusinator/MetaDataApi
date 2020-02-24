from django.core.management.base import BaseCommand, CommandError

from dataproviders.models import DataProvider
from dataproviders.services import InitializeDataProviders


class Command(BaseCommand):
    help = 'load data providers from json or aws'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        InitializeDataProviders.load()
        dps = [dp.provider_name for dp in DataProvider.objects.all()]
        if not len(dps):
            raise CommandError("load data providers failed")
        self.stdout.write(self.style.SUCCESS(f'Successfully added dataproviders: {dps}'))
