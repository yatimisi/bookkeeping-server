from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
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
    ModifyAuthoritySerializer,
    CategorySerializer,
    ConsumeSerializer,
    ProportionSerializer,
)
from rest_framework.generics import get_object_or_404


class AccountBookViewSet(viewsets.ModelViewSet):
    queryset = AccountBook.objects.all()
    serializer_class = AccountBookSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            book__in=[Authority.book.id for Authority in Authority.objects
                      .filter(user=self.request.user)
                      .exclude(authority=Authority.LEAVE)]
        )

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return super().get_serializer_class()

        if self.action == 'create':
            return super().get_serializer_class()

        return ModifyAuthoritySerializer

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

    def perform_destroy(self, instance):
        me = Authority.objects\
            .filter(user=self.request.user)\
            .filter(book=instance.book).first()

        authority = Authority.objects.get(pk=instance.id)

        if instance.user != self.request.user and \
            me.authority <= instance.authority and \
            (Authority.objects.filter(book=authority.book).count() > 1 or
             instance.authority is not Authority.CREATOR):
            authority.authority = Authority.LEAVE
            authority.save()
            return

        raise PermissionDenied('Cannot delete.')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            book__in=[Authority.book.id for Authority in Authority.objects
                      .filter(user=self.request.user)
                      .exclude(authority=Authority.LEAVE)]
        )


class ConsumeViewSet(viewsets.ModelViewSet):
    queryset = Consume.objects.all()
    serializer_class = ConsumeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book', 'is_repay']

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            book__in=[Authority.book.id for Authority in Authority.objects
                      .filter(user=self.request.user)
                      .exclude(authority=Authority.LEAVE)]
        )

    def perform_create(self, serializer):
        consume = serializer.save()

        proportion = Proportion.objects.create(
            fee=0,
            username=consume.creator,
            consume=consume,
        )

        proportion.save()


class ProportionViewSet(viewsets.ModelViewSet):
    queryset = Proportion.objects.all()
    serializer_class = ProportionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consume']
