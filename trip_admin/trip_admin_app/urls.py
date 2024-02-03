from django.urls import path

from .views import ChanelListView, PostsListViewSet, PostLastViewChanger, LogCreate, PostDetailView

urlpatterns = [
    path("chanels", ChanelListView.as_view({'get': 'list', }), name="chanels", ),
    path("posts", PostsListViewSet.as_view({'get': 'list', }), name="posts", ),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path("post_last_view_changer/<int:pk>", PostLastViewChanger.as_view({'put': 'update'}), name="last_view_changer", ),
    path("log_create", LogCreate.as_view({'post': 'create'}), name="log_create", ),
]
