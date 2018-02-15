from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.views import generic


from .models import Publication, PublicationContent


class IndexView(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'publications'

    def get_queryset(self):
        """Return the last five published questions."""
        return Publication.objects.order_by('-effective_pub_date')[:5]


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
