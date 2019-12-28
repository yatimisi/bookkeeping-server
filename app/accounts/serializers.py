from rest_framework import serializers

from .models import AccountBook, Authority, Category, Consume, Proportion


class AccountBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ConsumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consume
        fields = '__all__'


class ProportionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proportion
        fields = '__all__'
