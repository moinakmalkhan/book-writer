from django.contrib import admin
from books.models import Book, Section,  BookCollaborator


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "created_at", "updated_at"]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["title", "book", "parent", "author", "created_at", "updated_at"]


@admin.register(BookCollaborator)
class BookCollaboratorAdmin(admin.ModelAdmin):
    list_display = ["book", "collaborator", "created_at", "updated_at"]
