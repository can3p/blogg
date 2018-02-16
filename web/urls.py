from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('u/<username>/', views.BlogView.as_view(), name='blog'),
    path('u/<username>/<int:publication_id>',
         views.PublicationView.as_view(), name='publication'),
    path('edit/<username>/<int:publication_id>',  views.edit, name='edit'),
    path('update', views.update, name='update'),
]
