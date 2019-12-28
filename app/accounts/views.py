from django.shortcuts import render
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    AccountBook,
    Authority,
    Category,
    Consume,
    Proportion,
)
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


class AuthorityViewSet(viewsets.ModelViewSet):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ConsumeViewSet(viewsets.ModelViewSet):
    queryset = Consume.objects.all()
    serializer_class = ConsumeSerializer


class ProportionViewSet(viewsets.ModelViewSet):
    queryset = Proportion.objects.all()
    serializer_class = ProportionSerializer
