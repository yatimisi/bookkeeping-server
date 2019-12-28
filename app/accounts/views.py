from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import (
    AccountBook,
    Authority,
    Category,
    Consume,
    Proportion,
)
from .permissions import IsCurrentUser
from .serializers import (
    AccountBookSerializer,
    AuthoritySerializer,
    CategorySerializer,
    ConsumeSerializer,
    ProportionSerializer,
)
from rest_framework.generics import get_object_or_404


class AccountBookViewSet(viewsets.ModelViewSet):
    queryset = AccountBook.objects.all()
    serializer_class = AccountBookSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            id__in=[Authority.book.id for Authority in Authority.objects
                    .filter(user=self.request.user)
                    .exclude(authority=Authority.LEAVE)]
        )

    def perform_create(self, serializer):
        account_book = serializer.save()

        authority = Authority.objects.create(
            user=self.request.user,
            book=account_book,
        )

        authority.save()

    def perform_destroy(self, instance):
        authority = Authority.objects.filter(
            user=self.request.user).filter(book=instance).first().authority

        if authority is Authority.CREATOR:
            super().perform_destroy(instance)
            return

        self.leave(self.request.user, book=instance.id)

    @action(
        ['POST'],
        False,
        'leave/(?P<book>[^/.]+)',
        permission_classes=[IsAuthenticated]
    )
    def leave(self, request, book):
        account_book = get_object_or_404(AccountBook, pk=book)
        authority = get_object_or_404(Authority,
                                      user=self.request.user,
                                      book=account_book)

        authority.authority = Authority.LEAVE
        authority.save()

        return Response({
            'success': True,
        })


class AuthorityViewSet(viewsets.ModelViewSet):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            book__in=[Authority.book.id for Authority in Authority.objects
                      .filter(user=self.request.user)
                      .exclude(authority=Authority.LEAVE)]
        )

    def perform_create(self, serializer):
        book = get_object_or_404(AccountBook,
                                 pk=serializer.validated_data['book'].id)
        authorities = Authority.objects\
            .filter(user=self.request.user)\
            .filter(book=book)

        if not authorities or authorities.first().authority in [Authority.CREATOR, Authority.WRITER]:
            super().perform_create(serializer)
            return

        raise PermissionDenied('Cannot post.')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ConsumeViewSet(viewsets.ModelViewSet):
    queryset = Consume.objects.all()
    serializer_class = ConsumeSerializer


class ProportionViewSet(viewsets.ModelViewSet):
    queryset = Proportion.objects.all()
    serializer_class = ProportionSerializer
