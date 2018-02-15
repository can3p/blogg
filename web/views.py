from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


from .models import Publication, PublicationContent, User


class IndexView(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'publications'

    def get_queryset(self):
        """Return the last five published questions."""
        return Publication.objects.order_by('-effective_pub_date')[:5]


class BlogView(generic.ListView):
    template_name = 'web/blog.html'
    context_object_name = 'publications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_username'] = self.kwargs['username']

        return context

    def get_queryset(self):
        """Return the last five published questions."""

        try:
            author = User.get(username=self.kwargs['username'])
        except ObjectDoesNotExist:
            raise Http404("Blog not found")

        return Publication.objects.filter(author=author).order_by('-effective_pub_date')[:5]


class PublicationView(generic.DetailView):
    template_name = 'web/publication.html'
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_username'] = self.kwargs['username']

        return context

    def get_object(self):
        """Return the last five published questions."""

        username = self.kwargs['username']
        publication_id = self.kwargs['publication_id']

        try:
            publication = Publication.objects.filter(author__username=username, effective_pub_date__isnull=False).get(id=publication_id)
        except ObjectDoesNotExist:
            raise Http404("Post not found")

        return publication


@login_required
def update(request):
    if request.method == 'POST':
        publication = Publication()
        publication.author = request.user
        publication.pub_date = timezone.now()
        publication.effective_pub_date = timezone.now()
        publication.save()

        content = PublicationContent()
        content.publication = publication
        content.title = request.POST['title']
        content.post = request.POST['post']
        content.inserted_at = timezone.now()
        content.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        template = loader.get_template('web/update.html')
        context = {}

        return HttpResponse(template.render(context, request))
