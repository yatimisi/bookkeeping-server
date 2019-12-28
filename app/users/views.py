import time

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .permissions import IsCurrentUser
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]

    @action(
        ['GET', 'PUT', 'PATCH'],
        False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=request.method == 'PATCH',
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        else:
            serializer = self.get_serializer(request.user)

        return Response(serializer.data)
