from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.user.auth import MyJWTAuthentication
from utils.permissions.permission import IsAdmin


class MyReadOnlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyJWTAuthentication,)

    def list(self, request, *args, **kwargs):
        return super(MyReadOnlyModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(MyReadOnlyModelViewSet, self).retrieve(request, *args, **kwargs)


class MyBaseModelViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = (IsAdmin,)
    authentication_classes = (MyJWTAuthentication,)

    def create(self, request, *args, **kwargs):
        return super(MyBaseModelViewSet, self).create(request)

    def update(self, request, *args, **kwargs):
        return super(MyBaseModelViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(MyBaseModelViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(MyBaseModelViewSet, self).destroy(request, *args, **kwargs)


class MyModelViewSet(MyBaseModelViewSet, MyReadOnlyModelViewSet):
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdmin,)
        return [permission() for permission in self.permission_classes]
