import os
import django

# python manage.py runserver

# Указать путь к файлу settings.py вашего Django проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alskar.settings')
django.setup()

import discord
from asgiref.sync import sync_to_async
from news.models import DiscordMessage

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

CHANNEL_ID = int(os.environ.get('NEWS_CHANNEL_ID'))
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Получение последней записи из базы данных
    last_message = await sync_to_async(DiscordMessage.objects.last)()
    if last_message:
        last_timestamp = last_message.timestamp
    else:
        last_timestamp = None

    # Получение канала для сбора сообщений (замените на свой ID канала)
    channel = client.get_channel(CHANNEL_ID)

    count = 0

    async for message in channel.history(after=last_timestamp, oldest_first=True):
        await sync_to_async(DiscordMessage.objects.create)(
            content=message.content,
            author=str(message.author),
            avatar_url=str(message.author.display_avatar.url),
            channel_id=message.channel.id,
            timestamp=message.created_at
        )
        count += 1

    print(f'Collected {count} messages!')


@client.event
async def on_message(message):
    if not message.channel.id == CHANNEL_ID:
        return

    if message.author == client.user:
        return

    channel = client.get_channel(CHANNEL_ID)
    msg = await channel.fetch_message(message.id)

    await sync_to_async(DiscordMessage.objects.create)(
        content=msg.content,
        author=str(msg.author),
        avatar_url=str(msg.author.display_avatar.url),
        channel_id=msg.channel.id,
        timestamp=msg.created_at
    )
    print("Got new message!")

# Запуск бота (замените на свой токен)
client.run(BOT_TOKEN)