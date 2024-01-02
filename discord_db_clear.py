import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcnews.settings')
django.setup()

from news.models import DiscordMessage


# Функция для удаления сообщений из базы данных
def delete_messages_from_channel(channel_id):
    deleted_count, _ = DiscordMessage.objects.filter(channel_id=channel_id).delete()
    return deleted_count


# Пример удаления сообщений из определенного канала
def delete_messages_command(channel_id):
    deleted_count = delete_messages_from_channel(channel_id)
    print(f"Deleted {deleted_count} messages from channel {channel_id}")


if __name__ == "__main__":
    import argparse

    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Delete messages from a channel in the database.')
    parser.add_argument('channel_id', type=int, help='ID of the channel to delete messages from')

    # Получение аргументов из командной строки
    args = parser.parse_args()

    # Вызов функции для удаления сообщений из определенного канала (замените на нужный ID канала)
    delete_messages_command(args.channel_id)
