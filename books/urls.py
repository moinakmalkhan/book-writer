from django.urls import path
from books.views import (
    BookListView,
    BookCreateView,
    BookDetailView,
    BookUpdateView,
    BookDeleteView,
    SectionCreateView,
    SectionDetailView,
    SectionUpdateView,
    SectionDeleteView,
    CollaboratorCreateView,
    CollaboratorDeleteView,
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="home"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/add/", BookCreateView.as_view(), name="add"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="detail"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="delete"),
    path(
        "books/<int:pk>/collaborators/add/",
        CollaboratorCreateView.as_view(),
        name="add-collaborator",
    ),
    path(
        "books/<int:pk>/collaborators/<int:collaborator_pk>/delete/",
        CollaboratorDeleteView.as_view(),
        name="delete-collaborator",
    ),
    path(
        "books/<int:pk>/sections/<int:section_pk>/",
        SectionDetailView.as_view(),
        name="section-detail",
    ),
    path(
        "books/<int:pk>/sections/add/",
        SectionCreateView.as_view(),
        name="add-section",
    ),
    path(
        "books/<int:pk>/sections/<int:section_pk>/update/",
        SectionUpdateView.as_view(),
        name="update-section",
    ),
    path(
        "books/<int:pk>/sections/<int:section_pk>/delete/",
        SectionDeleteView.as_view(),
        name="delete-section",
    ),
]
