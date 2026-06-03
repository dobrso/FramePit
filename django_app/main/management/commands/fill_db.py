from random import choice

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

from users.models import Profile
from rooms.models import Tag, Room

class Command(BaseCommand):
    def handle(self, *args, **options):
        self._create_site()
        users = self._create_users()
        tags = self._create_tags()
        self._create_rooms(users, tags)
        self._create_providers()

        self.stdout.write('БД заполнена данными')

    def _create_site(self):
        Site.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'localhost:8000',
                'name': 'localhost',
            }
        )

    def _create_users(self):
        User = get_user_model()
        users = []

        if not User.objects.filter(username='framepitadmin').exists():
            admin = User.objects.create_superuser(username='framepitadmin', email='framepit@example.com', password='framepitadmin')
            Profile.objects.get_or_create(user=admin)
            self.stdout.write('Создан админ')

        for i in range(5):
            name = f'pituser_{i+1}'
            user, created = User.objects.get_or_create(username=name, defaults={'email': f'{name}@example.com'})

            if created:
                user.set_password(name)
                user.save()
                Profile.objects.get_or_create(user=user)
                self.stdout.write(f'Создан пользователь {name}')
            users.append(user)

        return users

    def _create_tags(self):
        names = ['Фильмы', 'Игры', 'Мультики']
        tags = []

        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        self.stdout.write('Созданы теги')
        return tags

    def _create_rooms(self, users, tags):
        for i in range(10):
            user = choice(users)
            name = f'Комната {user.username}_{i+1}'

            room, _ = Room.objects.get_or_create(name=name, owner=user)
            room.tags.add(choice(tags))
            room.members.add(user)

        self.stdout.write('Созданы комнаты')

    def _create_providers(self):
        site = Site.objects.get_current()

        github_app, created = SocialApp.objects.get_or_create(
            provider='github',
            defaults={
                'name': 'GitHub',
                'client_id': settings.GITHUB_CLIENT_ID,
                'secret': settings.GITHUB_CLIENT_SECRET,
            }
        )

        if created:
            github_app.sites.add(site)
            github_app.save()

        yandex_app, created = SocialApp.objects.get_or_create(
            provider='yandex',
            defaults={
                'name': 'Yandex',
                'client_id': settings.YANDEX_CLIENT_ID,
                'secret': settings.YANDEX_CLIENT_SECRET,
            }
        )

        if created:
            yandex_app.sites.add(site)
            yandex_app.save()