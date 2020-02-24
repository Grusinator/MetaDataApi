from django.core.management.base import BaseCommand

from dataproviders.services import InitializeDataProviders


class Command(BaseCommand):
    help = 'load data providers from json or aws'

    def handle(self, *args, **options):
        filename = InitializeDataProviders.dump_all_providers_to_providers_file()
        self.stdout.write(self.style.SUCCESS(f'Successfully dumped dataproviders to: {filename}'))
