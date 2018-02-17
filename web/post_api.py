from django.utils import timezone
from .models import Publication, PublicationContent, User


def create_publication(username, subject, post):
    author = User.objects.get(username=username)
    publication = Publication()
    publication.author = author
    publication.pub_date = timezone.now()
    publication.effective_pub_date = timezone.now()
    publication.save()

    content = PublicationContent()
    content.publication = publication
    content.title = subject
    content.post = post
    content.inserted_at = timezone.now()
    content.save()

    return publication


def update_publication(username, publication_id, subject, post):
    publication = Publication.objects.filter(author__username=username, effective_pub_date__isnull=False).get(id=publication_id)
    publication.effective_pub_date = timezone.now()
    publication.save()

    content = PublicationContent()
    content.publication = publication
    content.title = subject
    content.post = post
    content.inserted_at = timezone.now()
    content.save()

    return publication
