from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.user.managers import CustomUserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False)
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name='微信头像')

    email = models.CharField(max_length=255, unique=True, verbose_name='email')
    password = models.CharField(max_length=255, verbose_name='密码')

    is_superuser = models.BooleanField(default=False, verbose_name='超级管理员')
    is_staff = models.BooleanField(default=True, verbose_name="员工")
    is_active = models.IntegerField(default=1, verbose_name='状态 0-封禁 1-正常')

    created_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    updated_time = models.DateTimeField(default=datetime.now, verbose_name='活跃时间')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
