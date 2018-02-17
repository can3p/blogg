from django_xmlrpc.decorators import xmlrpc_func
from django.contrib.auth.hashers import UnsaltedMD5PasswordHasher
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from django.urls import reverse
from django.conf import settings

from .post_api import create_publication, update_publication

TEMPORARY_CHALLENGE = 'test'  # just joking


def xmlrpc_auth(func):
    pass

    def _wrapper(struct):
        # check auth there and scream in case of troubles
        required = ('username', 'auth_method', 'auth_challenge',
                    'auth_response', 'event', 'subject')
        if not(all(name in struct for name in required)):
            raise Exception("Required fields missing")

        try:
            author = User.objects.get(username=struct['username'])
        except ObjectDoesNotExist:
            raise Exception("Blog not found")

        hasher = UnsaltedMD5PasswordHasher()

        verify_hash = hasher.encode(struct['auth_challenge'] + author.password, salt='')

        if verify_hash != struct['auth_response']:
            raise Exception("Auth failed")

        return func(struct)

    return _wrapper


@xmlrpc_func(returns='struct', args=[])
def getchallenge():
    """Returns a cookie for subsequent calls"""
    return {
            'auth_scheme': 'c1',
            'challenge': TEMPORARY_CHALLENGE,
            'expire_time': 13425345,  # all those stubs should be replaced with somewhing real
            'server_time': 13425345
            }


@xmlrpc_func(returns='struct', args=['struct'])
@xmlrpc_auth
def postevent(struct):
    """Post a new publication in a blog. We support bare minimum
       to be compatible with cl-journal client.

       Livejournal api supports a very reach input:
       Struct {
        :username *service-login*
        :auth_method "challenge"
        :auth_challenge challenge
        :auth_response auth-response
        :event
        :subject
        :props {
            :music
            :mood
            :location
            :tags
        }
        :security (public|allowmask|private)
        :allowmask 1 (in case of :security allowmask)
        :usejournal
        :year year
        :mon month
        :day date
        :hour hour
        :min minute
       }

       But we don't. The only thing we care about is auth + event and subject
       Hence the minimal input in our case is like this:

       Struct {
        :username *service-login*
        :auth_method "challenge"
        :auth_challenge challenge
        :auth_response auth-response
        :event
        :subject
       }

       Output: {
        :itemid
        :anum - random crap, don't rely on it
        :url
       }
    """

    publication = create_publication(struct['username'],
                                     struct['subject'],
                                     struct['event'])
    return {
            'itemid': publication.id,
            'anum': 42,  # perfectly random
            'url': settings.BASE_URL + reverse('publication', args=[struct['username'], publication.id])
            }


@xmlrpc_func(returns='struct', args=['struct'])
@xmlrpc_auth
def editevent(struct):
    """Update existing publication in a blog.

       At the moment post deletion is not supported.

       Expected input (can be more, but that won't be saved)

       Struct {
        :itemid
        :username
        :auth_method "challenge"
        :auth_challenge challenge
        :auth_response auth-response
        :event
        :subject
       }

       Output: {
        :itemid
        :anum - random crap, don't rely on it
        :url
       }
    """

    publication = update_publication(struct['username'],
                                     struct['itemid'],
                                     struct['subject'],
                                     struct['event'])
    return {
            'itemid': publication.id,
            'anum': 42,  # perfectly random
            'url': settings.BASE_URL + reverse('publication', args=[struct['username'], publication.id])
            }
