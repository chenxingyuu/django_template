from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions.permission import IsAdmin, IsSuperuser
from utils.permissions.views import MyModelViewSet
# Create your views here.
from .filter import UserFilter
from .models import User
from .serializers import UserInfoSerializer


class UserModelViewSet(MyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = (IsAdmin,)
        else:
            self.permission_classes = (IsSuperuser,)
        return [permission() for permission in self.permission_classes]
