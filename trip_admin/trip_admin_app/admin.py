from django.contrib import admin

from .models import Chanel, Post, City, Destination, Country, Log


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('code',)


class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ["country"]
    list_display = ("name", "country", "code",)


class DestinationAdmin(admin.ModelAdmin):
    raw_id_fields = ("origin", "destination")
    list_filter = ["post"]


class DestinationsInline(admin.TabularInline):  # Только для отображения выплат внутри категории командировки
    model = Destination
    extra = 1  # Количество дополнительных форм для добавления прямо в интерфейсе
    raw_id_fields = ("origin", "destination",)


class PostAdmin(admin.ModelAdmin):
    inlines = [DestinationsInline]
    list_display = ("chanel", "text_before", "name",)
    list_filter = ("chanel",)


class LogAdmin(admin.ModelAdmin):
    search_fields = ('title', 'body')
    list_display = ("title", "body", "date",)
    list_filter = ("title", "date")

    def has_module_permission(self, request):
        return request.user.username in ['rauf', 'admin']


admin.site.register(Chanel)
admin.site.register(Post, PostAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Log, LogAdmin)
