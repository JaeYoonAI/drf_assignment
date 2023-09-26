from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, fullname, nickname, birthday, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        elif not username:
            raise ValueError("Users must have an username")
        elif not fullname:
            raise ValueError("Users must have an fullname")
        elif not nickname:
            raise ValueError("Users must have an nickname")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            fullname=fullname,
            nickname=nickname,
            birthday=birthday,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, fullname, nickname, birthday, password=None
    ):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            fullname=fullname,
            nickname=nickname,
            birthday=birthday,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(null=True, max_length=50, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(null=True, max_length=50)
    nickname = models.CharField(null=True, max_length=30, unique=True)
    birthday = models.DateField()
    join_date = models.DateTimeField(null=True, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "fullname", "nickname", "birthday"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
