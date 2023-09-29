from django.db import models
from django.conf import settings


class BookCollaborator(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books")
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="contributed_books", through=BookCollaborator)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sections", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="subsections")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sections")
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

