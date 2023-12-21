from django.db import models


class Chanel(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название канала телеграм")
    chanel_chat_id = models.CharField(max_length=14, )

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


class Country(models.Model):
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return f"{self.code}"


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название')
    code = models.CharField(max_length=3, unique=True, verbose_name='IATA код города')


    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f"{self.name}"


class Destination(models.Model):
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='origin_trips', verbose_name='Откуда')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination_trips', verbose_name='Куда')

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f"Из {self.origin.name} в {self.destination.name}"


class TicketsList(models.Model):
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, verbose_name='Для канала')
    destinations = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name='Направления')

    class Meta:
        verbose_name = 'Подборка билетов'
        verbose_name_plural = 'Подборки билетов'

    def __str__(self):
        return f"Для {self.chanel.name}"





