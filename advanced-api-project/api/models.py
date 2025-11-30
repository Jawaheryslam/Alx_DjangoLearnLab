from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255) # stores the name of the book

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255) # stores the book title
    publication_year = models.IntegerField() # stores publication year
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE) # links to author model

    def __str__(self):
        return self.title
