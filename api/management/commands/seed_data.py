from django.core.management.base import BaseCommand
from api.models import Person

class Command(BaseCommand):
    help = 'Seeds the database with a predefined list of people'

    def handle(self, *args, **options):
        # Predefined list of people to seed
        people_to_seed = [
            "John Doe",
            "Jane Smith",
            "Alice Johnson",
            "Bob Williams",
            "Emma Brown"
        ]

        for person_name in people_to_seed:
            person, created = Person.objects.get_or_create(name=person_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created person "{person_name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Person "{person_name}" already exists'))