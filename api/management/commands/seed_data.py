from django.core.management.base import BaseCommand
from api.models import Person

class Command(BaseCommand):
    # Person.objects.all().delete()
    help = 'Seeds the database with a predefined list of people'

    def handle(self, *args, **options):
        # Predefined list of people to seed
        people_to_seed = [
            "Simone Biles",
            "Michael Phelps", "Ato Boldon", "Teddy Riner", "Ma Long", "Andy Murray"
        ]

        for person_name in people_to_seed:
            person, created = Person.objects.get_or_create(name=person_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created person "{person_name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Person "{person_name}" already exists'))
        
        new_people = [
            ("Usain Bolt", "Jamaica"),
            ("Serena Williams", "United States"),
            ("Lionel Messi", "Argentina"),
            ("Naomi Osaka", "Japan"),
            ("Roger Federer", "Switzerland"),
            ("Eliud Kipchoge", "Kenya")
        ]
        # Seed new people with country information
        for person_name, country in new_people:
            person, created = Person.objects.get_or_create(
                name=person_name,
                defaults={'country': country}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created person "{person_name}" from {country}'))
            else:
                self.stdout.write(self.style.WARNING(f'Person "{person_name}" already exists'))