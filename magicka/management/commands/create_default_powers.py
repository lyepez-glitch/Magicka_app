from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.apps import apps
from magicka.models import PowerAbility, UserPower

class Command(BaseCommand):
    help = "Clear all tables except for User and reassign default powers to users"

    def handle(self, *args, **kwargs):
        # Step 1: Get the User model
        User = get_user_model()

        # Step 2: List all models in the magicka app except User
        all_models = apps.get_models()
        models_to_clear = [model for model in all_models if model != User and model._meta.app_label == 'magicka']

        # Step 3: Clear data from each model (except User)
        for model in models_to_clear:
            # Clear data
            model.objects.all().delete()
            self.stdout.write(f"Cleared all data from {model._meta.verbose_name_plural}.")

        # Step 4: Define default powers
        default_powers = [
            {
                "name": "Fireball",
                "damage": 50,
                "energy_cost": 30,
                "cooldown_time": 5,
                "description": "Launches a fiery projectile at the enemy, causing moderate damage.",
            },
            {
                "name": "Ice Shard",
                "damage": 40,
                "energy_cost": 20,
                "cooldown_time": 4,
                "description": "Hurls a sharp shard of ice, causing frost damage.",
            },
        ]

        # Step 5: Create powers
        for power in default_powers:
            power_obj, created = PowerAbility.objects.get_or_create(
                name=power["name"],
                defaults={
                    "damage": power["damage"],
                    "energy_cost": power["energy_cost"],
                    "cooldown_time": power["cooldown_time"],
                    "description": power["description"],
                },
            )
            if created:
                self.stdout.write(f"Power {power_obj.name} created.")
            else:
                self.stdout.write(f"Power {power_obj.name} already exists.")

        # Step 6: Assign powers to users
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING("No users found. Powers will not be assigned."))
            return

        for user in users:
            for power in PowerAbility.objects.all():
                user_power, created = UserPower.objects.get_or_create(
                    user=user,
                    power=power,
                    defaults={
                        "level": 1,
                        "energy_level": power.energy_cost * 2,  # Example starting energy
                        "energy_max": power.energy_cost * 3,    # Example max energy
                    },
                )
                if created:
                    self.stdout.write(f"Assigned {power.name} to {user.username}.")
                else:
                    self.stdout.write(f"{user.username} already has {power.name}.")

        self.stdout.write(self.style.SUCCESS("All tables cleared except 'User' and default attack powers created and assigned successfully!"))
