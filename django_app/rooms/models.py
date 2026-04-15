from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', blank=True, null=True, default='default/shell.jpg', upload_to='uploads/room/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_owners', verbose_name='Создатель')
    tags = models.ManyToManyField(Tag, blank=True, related_name='room_tags', verbose_name='Тэги')
    members = models.ManyToManyField(User, blank=True, related_name='room_members', verbose_name='Участники')

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'Комната {self.name}'