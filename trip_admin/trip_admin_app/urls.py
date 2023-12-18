from django.urls import path

from .views import ChanelListView

urlpatterns = [
    path("chanels", ChanelListView.as_view({'get': 'list', }), name="chanels", ),
]
