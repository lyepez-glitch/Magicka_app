from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, PowerAbility, UserPower, UserAttackHistory
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

User = get_user_model()

def home(request):
    return HttpResponse("Welcome to Home")

# User Registration
class RegisterUserView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create and save the user
                user = User.objects.create_user(username=username, password=password)
                user.save()  # Ensures the user instance is fully committed to the database

                # Create a profile for the user
                Profile.objects.create(user=user)  # Ensure `user` is not null
                return JsonResponse({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Login and JWT Token
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print('uname ' + str(username))
        print('password ' + str(password))

        if not username or not password:

            return JsonResponse({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(access_token),
                'username': user.username,
                'id':user.id
            })

        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Profile Update
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        profile = user.profile
        avatar = request.data.get("avatar")
        energy_level = request.data.get("energy_level")

        try:
            if avatar:
                profile.avatar = avatar
            if energy_level:
                profile.energy_level = energy_level

            profile.save()
            return JsonResponse({"message": "Profile updated successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Launch Attack
class LaunchAttackView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        power_id = request.data.get("power_id")
        print("power id " + str(power_id))

        if not power_id:
            return JsonResponse({"error": "Power ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            power = PowerAbility.objects.get(id=power_id)
            name = power.name
            profile = Profile.objects.get(user=user)

            og_level = profile.energy_level
            # Regenerate user's energy
            profile.regenerate_energy()
            print('power cost ' + str(power.energy_cost) + 'og energy level ' + str(og_level) + 'recharged energy level ' + str(profile.energy_level))
            if profile.energy_level < power.energy_cost:

                return JsonResponse({"error": "Not enough energy"}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct energy and save attack history
            profile.energy_level -= power.energy_cost
            profile.last_updated = timezone.now()
            profile.save()

            attack_history = UserAttackHistory.objects.create(
                user=user,
                power=power,
                energy_spent=power.energy_cost,
                damage_done=power.damage
            )

            return JsonResponse({
                "message": "Attack launched!",
                "damage_done": attack_history.damage_done,
                "remaining_energy": profile.energy_level,
                "timestamp": attack_history.timestamp,
                'name':name,
                "energy_cost":power.energy_cost
            })

        except PowerAbility.DoesNotExist:
            return JsonResponse({"error": "Power not found"}, status=status.HTTP_404_NOT_FOUND)
        except UserPower.DoesNotExist:
            return JsonResponse({"error": "UserPower not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPowers(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        # Fetch all powers from the database
        powers = PowerAbility.objects.all().values(
            "id","name", "damage", "energy_cost", "cooldown_time", "description"
        )
        return Response({"powers": list(powers)}, status=status.HTTP_200_OK)

class GetAttacks(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        # Fetch all powers from the database
        attacks = UserAttackHistory.objects.all().values(
            "id","user", "power", "energy_spent", "damage_done", "timestamp"
        )
        return Response({"attacks": list(attacks)}, status=status.HTTP_200_OK)


class GetAllUsersView(APIView):
    permission_classes = [AllowAny]  # Set appropriate permissions if required

    def get(self, request):
        users = User.objects.all().values('id', 'username', 'email', 'date_joined')
        return Response({"users": list(users)}, status=status.HTTP_200_OK)

class GetAllUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all().values('id', 'username', 'email', 'date_joined')
        return Response({"users": list(users)}, status=status.HTTP_200_OK)

class AttackUser(APIView):
    def post(self,request):
        data = request.data
        attacker_id = data.get('attacker_id')
        target_id = data.get('target_id')
        power_id = data.get('power_id')
        target_user = User.objects.filter(id=id)
        profile = Profile.objects.get(user=target_user)
        power = PowerAbility.objects.filter(id=power_id)

        if not attacker_id or not target_id or not power_id:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        og_level = profile.energy_level

        profile.regenerate_energy()
        print('power cost ' + str(power.energy_cost) + 'og energy level ' + str(og_level) + 'recharged energy level ' + str(profile.energy_level))

        if profile.energy_level < power.energy_cost:
            return JsonResponse({"error": "Not enough energy"}, status=status.HTTP_400_BAD_REQUEST)


        profile.energy_level -= power.energy_cost
        profile.last_updated = timezone.now()
        profile.save()
        attack_history = UserAttackHistory.objects.create(
            user=request.user,
            power=power,
            energy_spent=power.energy_cost,
            damage_done=power.damage
            )

        return JsonResponse({
            "message": "Attack launched!",
            "damage_done": attack_history.damage_done,
            "remaining_energy": profile.energy_level,
            "timestamp": attack_history.timestamp,
            'name':power.name,
            "energy_cost":power.energy_cost
        })

class GetProfile(APIView):
    def get(self,request,id):
        user = User.objects.get(id=id)

        profile = Profile.objects.get(user=user)
        avatar_url = profile.avatar.url if profile.avatar else None
        profile_data = {
                "id": user.id,
                "avatar": avatar_url,
                "energy_level": profile.energy_level,
            }

        return Response({"user":{"username":user.username,"id":user.id},"avatar": avatar_url,"energy_level":profile.energy_level}, status=status.HTTP_200_OK)


