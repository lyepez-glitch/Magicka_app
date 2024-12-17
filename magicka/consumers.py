from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
import json

class AttackNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection attempt started")

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(f'Connected to room: {self.room_name}')
        self.room_group_name = f'battle_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("WebSocket connection established")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        attacker_id = data.get('attacker_id')
        target_id = data.get('target_id')
        power_id = data.get('power_id')

        if not all([attacker_id, target_id, power_id]):
            return await self.send(text_data=json.dumps({"error": "Missing required fields."}))

        print('received data ' + str(data))

        try:
            # Ensure to use sync_to_async for all database interactions
            target_user = await sync_to_async(self.get_target_user)(target_id)
            profile = await sync_to_async(self.get_profile)(target_user)
            power = await sync_to_async(self.get_power)(power_id)
        except Exception as e:
            return await self.send(text_data=json.dumps({"error": f"Error fetching data: {str(e)}"}))

        if profile.energy_level < power.energy_cost:
            return await self.send(text_data=json.dumps({"error": "Not enough energy"}))

        og_level = profile.energy_level
        await sync_to_async(profile.regenerate_energy)()
        print(f'Power cost: {power.energy_cost}, Original energy level: {og_level}, Recharged energy level: {profile.energy_level}')

        profile.energy_level -= power.energy_cost
        profile.last_updated = timezone.now()
        await sync_to_async(profile.save)()

        # Log the attack in history
        await sync_to_async(self.create_attack_history)(target_user, power)

        # Send updated avatar and energy level to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_attack_data',
                # 'avatar': profile.avatar if profile else '',  # Access avatar after loading profile
                'energy_level': profile.energy_level,
            }
        )

    def get_target_user(self, target_id):
        from django.contrib.auth.models import User
        return User.objects.get(id=target_id)

    def get_profile(self, target_user):
        from .models import Profile
        return target_user.profile  # Access the related profile directly

    def get_power(self, power_id):
        from .models import PowerAbility
        return PowerAbility.objects.get(id=power_id)

    def create_attack_history(self, target_user, power):
        from .models import UserAttackHistory
        return UserAttackHistory.objects.create(
            user=target_user,
            power=power,
            energy_spent=power.energy_cost,
            damage_done=power.damage
        )

    async def send_attack_data(self, event):
        # Send the message to WebSocket clients in the group
        await self.send(text_data=json.dumps({
            # 'avatar': event['avatar'],
            'energy_level': event['energy_level'],
        }))
