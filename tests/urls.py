from django.conf.urls import patterns, url
from .views import BookView

urlpatterns = patterns(
    '',
    url(r'^api/book$', BookView.as_view(), name='api-book-list'),
)
