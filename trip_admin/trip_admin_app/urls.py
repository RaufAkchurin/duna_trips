from django.urls import path

from .views import ChanelListView, PostViewSet

urlpatterns = [
    path("chanels", ChanelListView.as_view({'get': 'list', }), name="chanels", ),
    path("posts", PostViewSet.as_view({'get': 'list', }), name="posts", ),
]
