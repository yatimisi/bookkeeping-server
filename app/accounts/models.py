from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


class AccountBook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField('詳細資訊', blank=True)
    create_at = models.DateTimeField('建立時間', auto_now_add=True)
    update_at = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return self.title


class Authority(models.Model):
    CREATOR, WRITER, READER, LEAVE = range(4)
    STATUS_CHOICES = (
        (CREATOR, 'creator'),
        (WRITER, 'writer'),
        (READER, 'reader'),
        (LEAVE, 'leave'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='使用者', related_name='share')
    book = models.ForeignKey(
        AccountBook, on_delete=models.CASCADE, verbose_name='帳本', related_name='book')
    authority = models.PositiveIntegerField(
        choices=STATUS_CHOICES, default=CREATOR)

    class Meta:
        unique_together = (
            ('user', 'book'),
        )  # 合在一起為pk

    def __str__(self):
        return f'{self.user} has {self.authority} on {self.book}.'


class Category(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(AccountBook, on_delete=models.CASCADE,
                             verbose_name='所屬帳簿', related_name='category')

    class Meta:
        unique_together = (
            ('name', 'book'),
        )  # 合在一起為pk

    def __str__(self):
        return self.name


class Consume(models.Model):
    name = models.CharField(max_length=255)
    note = models.TextField('備註', blank=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='付款人', related_name='paid')
    category = models.ForeignKey(
        Category, models.SET_DEFAULT, null=True, blank=True, default=None, verbose_name='分類')
    book = models.ForeignKey(
        AccountBook, on_delete=models.CASCADE, verbose_name='所屬帳簿', related_name='consume')
    image = models.ImageField(blank=True)
    is_repay = models.BooleanField(default=False)
    description = models.TextField('詳細資訊', blank=True)
    consume_at = models.DateField('消費日', default=datetime.date.today)
    create_at = models.DateTimeField('建立時間', auto_now_add=True)
    update_at = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return self.name


class Proportion(models.Model):
    username = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='付款人', related_name='percent')
    fee = models.PositiveIntegerField('費用')
    consume = models.ForeignKey(
        Consume, on_delete=models.CASCADE, verbose_name='消費明細', related_name='list')

    class Meta:
        unique_together = (
            ('username', 'consume'),
        )  # 合在一起為pk

    def __str__(self):
        return f'{self.username} spent {self.fee}.'
