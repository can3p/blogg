from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()


class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    effective_pub_date = models.DateTimeField('date of the post on the site')

    def content(self):
        return PublicationContent.objects.order_by('-inserted_at').filter(publication=self)[:1][0]


class PublicationContent(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    inserted_at = models.DateTimeField('draft saved at')
    post = models.TextField(null=True)
