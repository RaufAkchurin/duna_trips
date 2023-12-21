from django.contrib import admin

from .models import Chanel, Post, City, Destination, TicketsList, Country


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('code',)


class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ["country"]
    list_display = ("name", "country", "code",)


class DestinationAdmin(admin.ModelAdmin):
    raw_id_fields = ("origin", "destination", "chanel")
    list_filter = ["chanel"]


class TicketsListAdmin(admin.ModelAdmin):
    list_filter = ("chanel",)


admin.site.register(Chanel)
admin.site.register(Post)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(TicketsList, )
