from django.urls import path

from .views import ChanelListView, PostViewSet, PostLastViewChanger

urlpatterns = [
    path("chanels", ChanelListView.as_view({'get': 'list', }), name="chanels", ),
    path("posts", PostViewSet.as_view({'get': 'list', }), name="posts", ),
    path("post_last_view_changer/<int:pk>", PostLastViewChanger.as_view({'put': 'update'}), name="last_view_changer", ),
]
