# from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()
