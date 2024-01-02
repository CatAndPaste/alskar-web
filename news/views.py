from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone

from .models import DiscordMessage

import markdown

def news(request):
    discord_messages = DiscordMessage.objects.all().order_by('-timestamp')  # Пример списка новостей

    current_date = timezone.now().date()
    for message in discord_messages:
        message.content = markdown.markdown(message.content)
        message.hot = message.timestamp.date() == current_date
        message.latest = False

    if discord_messages:
        discord_messages[0].latest = True

    paginator = Paginator(discord_messages, 5)  # Создаем объект Paginator с количеством новостей на странице (здесь 2)

    page_number = request.GET.get('page')  # Получаем номер страницы из параметра запроса
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы с соответствующими новостями

    context = {
        'title': 'Cats in Minecraft',
        'page_obj': page_obj,
    }

    if not page_obj.object_list:  # Проверка на наличие записей
        context['no_messages'] = True  # Добавляем флаг, если нет сообщений
    else:
        context['no_messages'] = False

    for m in page_obj:
        print(m)

    return render(request, 'news/news.html', context)