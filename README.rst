drf-lafv
======================================

|build-status-image| |pypi-version|

Overview
--------

A better way than DRF proposed for do some basic filters

Requirements
------------

-  Python (2.7, <3.5)
-  Django (1.8)
-  Django REST Framework (3.0, 3.1, 3.2)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install drf-lafv

Example
-------

Imagine that you have the following models.py

.. code:: python

    from django.db import models


    class Author(models.Model):
        name = models.CharField(max_length=250)
        nickname = models.CharField(max_length=100)


    class Book(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField()
        publication_date = models.DateField()
        isbn = models.CharField(max_length=17)
        author = models.ForeignKey(Author)


And you want to filter your list of books by author's nickname, isbn and create
a custom filter which will allow to get you books that were published less than
30 days ago. Well, DRF per se, ask you to install django-filter and write a
bunch of stuff that maybe hard. With ``lafv`` you can accomplish this doing this:


.. code:: python 

    from lafv.views import ListAPIFilteredView
    from serializers import BookSerializer


    class BookView(ListAPIFilteredView):
        queryset = Book.objects.all()
        serializer_class = BookSerializer
        filter_fields = ('author__nickname', 'isbn')
        custom_filters = ('new', )

        def filter_new(self, queryset):
            """
            get books that publication date is no longer than 1 month
            """
            last_month = datetime.today() - timedelta(days=30)
            queryset = queryset.filter(publication_date__gte=last_month)
            return queryset


And that's it!, please check the examples on the test app

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/angvp/drf-lafv.svg?branch=master
   :target: http://travis-ci.org/angvp/drf-lafv?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-lafv.svg
   :target: https://pypi.python.org/pypi/drf-lafv
