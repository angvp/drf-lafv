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
