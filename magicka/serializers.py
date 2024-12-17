from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile,PowerAbility

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        # Create the user instance but do not save it yet
        user = super().create(validated_data)

        # Hash the password before saving the user
        user.set_password(password)
        user.save()  # Save the user instance

        # Create the profile after the user is saved
        Profile.objects.create(user=user)

        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'energy_level']

class PowerAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerAbility
        fields = '__all__'  # Include all fields from the PowerAbility model