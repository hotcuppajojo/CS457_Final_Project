# botmanager.py
import discord
from discord.ext import commands
from datamanager import DataManager  # Import the DataManager class
from alertmanager import AlertManager  # Import the AlertManager class

class BotManager(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.data_manager = DataManager()  # Create an instance of DataManager
        self.alert_manager = AlertManager()  # Create an instance of AlertManager

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!subscribe'):
            await self.handle_subscribe_command(message)

        if message.content.startswith('!set'):
            await self.handle_set_command(message)

        if message.content.startswith('!alerts'):
            await self.handle_alerts_command(message)

    async def handle_subscribe_command(self, message):
        # Extract the NEO id from the message
        neo_id = message.content.split(' ')[1]
        # Use the DataManager to subscribe the user to the NEO
        self.data_manager.subscribe_user_to_neo(message.author.id, neo_id)
        await message.channel.send('You have been subscribed to updates for NEO ' + neo_id)

    async def handle_set_command(self, message):
        # Extract the alert threshold from the message
        alert_threshold = float(message.content.split(' ')[1])
        # Use the DataManager to update the user's alert threshold
        self.data_manager.set_user_alert_threshold(message.author.id, alert_threshold)
        await message.channel.send('Your alert threshold has been set to ' + str(alert_threshold))

    async def handle_alerts_command(self, message):
        # Use the AlertManager to fetch and display the latest alerts
        alerts = self.alert_manager.get_latest_alerts_for_user(message.author.id)
        for alert in alerts:
            await message.channel.send(alert)

    def send_alerts(self, message):
        # Use the AlertManager to send alerts to the user
        self.alert_manager.send_alert(message)

# Create an instance of the BotManager class
bot = BotManager(command_prefix='!')

# Start the bot
bot.run('discord-bot-token')