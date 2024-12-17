from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

# # Custom user model
# class User(AbstractUser):
#     # Add related_name to resolve the conflict
#     groups = models.ManyToManyField(
#         Group,
#         related_name='magicka_user_set',  # This will resolve the conflict
#         blank=True,
#     )

#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='magicka_user_permissions_set',  # This will resolve the conflict
#         blank=True,
#     )

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    energy_level = models.IntegerField(default=100)
    last_updated = models.DateTimeField(auto_now=True)# When the power was last used
    energy_max = models.IntegerField(default=100)  # Max energy limit

    def regenerate_energy(self):
        """
        This method checks how much energy should be regenerated based on the time
        passed since the last update.
        """
        time_diff = timezone.now() - self.last_updated
        regeneration_rate = 5  # energy points regenerated per minute
        regenerated_energy = int(time_diff.total_seconds() / 60) * regeneration_rate

        # Limit the energy to the max allowed value
        new_energy = min(self.energy_level + regenerated_energy, self.energy_max)
        self.energy_level = new_energy

        self.save()


    def __str__(self):
        return f'{self.user.username} Profile'

class PowerAbility(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Kamehameha"
    damage = models.IntegerField()  # Damage caused by the attack
    energy_cost = models.IntegerField()  # Energy required to perform the attack
    cooldown_time = models.IntegerField()  # Cooldown time in seconds
    description = models.TextField()  # Description of the power

    def __str__(self):
        return self.name

class UserPower(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    power = models.ForeignKey(PowerAbility, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)  # User's power level (could affect damage)
    energy_level = models.IntegerField(default=100)  #  StartingEnergy level to launch the attack
    energy_max = models.IntegerField(default=100)  # Max energy limit
    last_updated = models.DateTimeField(auto_now=True)  # When the power was last used

    def regenerate_energy(self):
        """
        This method checks how much energy should be regenerated based on the time
        passed since the last update.
        """
        time_diff = timezone.now() - self.last_updated
        regeneration_rate = 5  # energy points regenerated per minute
        regenerated_energy = int(time_diff.total_seconds() / 60) * regeneration_rate

        # Limit the energy to the max allowed value
        new_energy = min(self.energy_level + regenerated_energy, self.energy_max)
        self.energy_level = new_energy

        self.save()

    def __str__(self):
        return f"{self.user.username}'s {self.power.name} Level {self.level}"



# models.py
class UserAttackHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    power = models.ForeignKey(PowerAbility, on_delete=models.CASCADE)
    energy_spent = models.IntegerField()  # Energy used for the attack
    damage_done = models.IntegerField()  # Damage dealt by the attack
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of attack

    def __str__(self):
        return f"{self.user.username} used {self.power.name} at {self.timestamp}"

