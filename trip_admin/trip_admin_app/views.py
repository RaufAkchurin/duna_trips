from rest_framework import viewsets

from .models import Chanel
from .serializers import ChanelSerializer


class ChanelListView(viewsets.ModelViewSet):
    serializer_class = ChanelSerializer
    queryset = Chanel.objects.all()


