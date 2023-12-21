from django.contrib import admin

from .models import Chanel, Post, City, Destination, Country


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('code',)


class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ["country"]
    list_display = ("name", "country", "code",)


class DestinationAdmin(admin.ModelAdmin):
    raw_id_fields = ("origin", "destination")
    list_filter = ["post"]


class DestinationsInline(admin.TabularInline):  # Только для отображения выплат внеутри категории командировки
    model = Destination
    extra = 1  # Количество дополнительных форм для добавления прямо в интерфейсе
    raw_id_fields = ("origin", "destination")


class PostAdmin(admin.ModelAdmin):
    inlines = [DestinationsInline]
    list_display = ("chanel", "text", "name",)
    list_filter = ("chanel",)


admin.site.register(Chanel)
admin.site.register(Post, PostAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
