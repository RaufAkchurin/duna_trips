from django.contrib import admin

from .models import Chanel, Post, City, Destination, TicketsList, Country

admin.site.register(Chanel)
admin.site.register(Post)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Destination)
admin.site.register(TicketsList)
