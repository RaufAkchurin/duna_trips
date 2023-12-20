from django.contrib import admin

from .models import Chanel, Post, City, Destination, TicketsList, Country


class CityAdmin(admin.ModelAdmin):
    search_fields = ('name__icontains',)
    list_filter = ["country__code"]
    list_display = ("name", "country", "code",)

    def get_search_results(self, request, queryset, search_term):  # чтобы при поиске не учитывался регистр введенного
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(name__icontains=search_term.capitalize())
        return queryset, use_distinct


class DestinationAdmin(admin.ModelAdmin):
    raw_id_fields = ("origin", "destination",)
    search_fields = ("name",)


class TicketsListAdmin(admin.ModelAdmin):
    list_filter = ("chanel",)


admin.site.register(Chanel)
admin.site.register(Post)
admin.site.register(Country)
admin.site.register(City, CityAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(TicketsList, )
