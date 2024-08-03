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
        new_people = [
            ('Wilma Rudolph', 'Track and Field'), ('Carl Lewis', 'Track and Field'), ('Jesse Owens', 'Track and Field'), ('Allyson Felix', 'Track and Field'), ('Jackie Joyner-Kersee', 'Track and Field'), ('Kathie Lee Gifford', 'Skiing'), ('Edvin van der Meer', 'Speed Skating'), ('Paavo Nurmi', 'Track and Field'), ('Carl Spitz', 'Swimming'), ('Mark Spitz', 'Swimming'), ('Nadia Comăneci', 'Gymnastics'), ('Larisa Latynina', 'Gymnastics'), ('Věra Čáslavská', 'Gymnastics'), ('Abebe Bikila', 'Marathon'), ('Haile Gebrselassie', 'Marathon'), ('Emil Zátopek', 'Marathon'), ('Paula Radcliffe', 'Marathon'), ('Eliud Kipchoge', 'Marathon'), 
        ]
        for person_name, discipline in new_people:
            person, created = Person.objects.get_or_create(
                name=person_name,
                defaults={'discipline': discipline}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created person "{person_name}" from {discipline}'))
            else:
                self.stdout.write(self.style.WARNING(f'Person "{person_name}" already exists'))