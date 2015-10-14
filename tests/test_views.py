from datetime import datetime, timedelta
import pytest
from django.core.urlresolvers import reverse
from .models import Author, Book


@pytest.fixture()
@pytest.mark.django_db
def create_books():
    author_data = {'name': 'Angel Velasquez', 'nickname': 'angvp'}
    author = Author.objects.create(**author_data)

    for i in range(0, 3):
        book_data = {
            'title': 'The book #{}'.format(i),
            'description': 'This is a long long book',
            'publication_date': datetime.today() - timedelta(days=365 * i),
            'isbn': '978-3-16-148410-{}'.format(i),
            'author': author,
        }
        Book.objects.create(**book_data)


@pytest.fixture()
@pytest.mark.django_db
def delete_books():
    Author.objects.all().delete()
    Book.objects.all().delete()


@pytest.mark.usefixtures('create_books')
@pytest.mark.django_db
def test_list_without_filters(client):
    """
    This test checks the view ```BookView``` is working and status_code == 200
    and list the 3 books that we previously created on our fixture
    """
    url = reverse('api-book-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.usefixtures('create_books')
@pytest.mark.django_db
def test_book_filter_nickname(client):
    """
    This test check the filter by author nickname
    """
    url = reverse('api-book-list')
    request = client.get(url, {'author__nickname': 'angvp'})
    assert request.status_code == 200
    assert len(request.data) == 3


@pytest.mark.usefixtures('create_books')
@pytest.mark.django_db
def test_book_filter_isbn(client):
    """
    This test check the filter by isbn
    """
    url = reverse('api-book-list')
    request = client.get(url, {'isbn': '978-3-16-148410-1'})
    assert request.status_code == 200
    assert len(request.data) == 1


@pytest.mark.usefixtures('create_books')
@pytest.mark.django_db
def test_book_filter_new(client):
    """
    This test checks the custom filter ```filter_new``` part of the
    BookView.
    """
    url = reverse('api-book-list')
    request = client.get(url, {'new': ''})
    assert request.status_code == 200
    assert len(request.data) == 1
