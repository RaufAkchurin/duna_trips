from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Chanel(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название канала телеграм")
    chanel_chat_id = models.CharField(max_length=14, )

    class Meta:
        verbose_name = 'Телеграм канал'
        verbose_name_plural = 'Телеграм каналы'

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


class Post(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, verbose_name='Телеграм канал')
    text_before = models.TextField(max_length=255, blank=True, null=True, verbose_name='Текст вначале (необъязательно)')
    text_after = models.TextField(max_length=255, blank=True, null=True, verbose_name='Текст вконце (необъязательно)')
    picture = models.ImageField(upload_to='post_pictures/',
                                verbose_name='Изображение поста (отобразится если недоступна генерация через ИИ)')
    last_viewed_destination_index = models.IntegerField(default=-1,
                                                        verbose_name='Индекс последнего опубликованого направления')
    return_tickets = models.BooleanField(default=False, verbose_name='Билеты обратно')
    max_price_of_tickets = models.IntegerField(default=8000, verbose_name='Максимально допустимая цена билета')

    count_of_tickets_in_direction = models.PositiveIntegerField(
        default=5,
        verbose_name='Билетов для каждого направления'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f"{self.name}"


class Destination(models.Model):
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='origin_trips', verbose_name='Откуда')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination_trips',
                                    verbose_name='Куда')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='destination_post', verbose_name='К посту')

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f"Из {self.origin.name} в {self.destination.name}"


class Log(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст ошибки')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        return f"{self.title}"
