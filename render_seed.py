from django.core.management import call_command
from django.db import connections

def seed_production():
    print("Seeding database...")
    call_command('seed_data')
    print("Seeding complete!")

if __name__ == "__main__":
    seed_production()