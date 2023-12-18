from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=20)
    group_chat_id = models.CharField(max_length=14)

    class Meta:
        verbose_name = 'Телеграм группа'
        verbose_name_plural = 'Телеграм группы'

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    name = models.CharField(max_length=40)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f"{self.name}"



