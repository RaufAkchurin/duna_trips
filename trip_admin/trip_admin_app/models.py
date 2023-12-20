from django.db import models


class Chanel(models.Model):
    name = models.CharField(max_length=20)
    chanel_chat_id = models.CharField(max_length=14)

    class Meta:
        verbose_name = 'Телеграм канал'
        verbose_name_plural = 'Телеграм каналы'

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    name = models.CharField(max_length=40)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f"{self.name}"


# class Direction(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=3)
#
#     class Meta:
#         verbose_name = 'Направление'
#         verbose_name_plural = 'Направления'
#
#     def __str__(self):
#         return f"{self.name}"


