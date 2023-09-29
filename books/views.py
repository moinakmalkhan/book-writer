from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from books.forms import BookForm, SectionForm, CollaboratorForm

get_books = lambda user: user.books.all() | user.contributed_books.all()

class BookCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()
            return redirect("books:detail", pk=book.pk)
        return render(request, "books/add_book.html", {"form": form})
    
    def get(self, request):
        form = BookForm()
        return render(request, "books/add_book.html", {"form": form})


class BookListView(LoginRequiredMixin, View):
    def get(self, request):
        books = get_books(self.request.user)
        return render(request, "books/books.html", {"books": books})


class BookDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(get_books(self.request.user), pk=pk)
        return render(request, "books/book.html", {"book": book})


class BookUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk=book.pk)
        return render(request, "books/update_book.html", {"form": form, "book": book})

    def get(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        form = BookForm(instance=book)
        return render(request, "books/update_book.html", {"form": form, "book": book})


class BookDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        book.delete()
        return redirect("books:home")
    

class SectionCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        form = SectionForm(book, request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.book = book
            section.author = request.user
            section.save()
            return redirect("books:detail", pk=book.pk)
        return render(request, "books/add_section.html", {"form": form})
    
    def get(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        form = SectionForm(book=book)
        return render(request, "books/add_section.html", {"form": form})


class SectionDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, section_pk):
        book = get_object_or_404((get_books(self.request.user)), pk=pk)
        section = get_object_or_404(book.sections, pk=section_pk)
        return render(request, "books/section.html", {"book": book, "section": section})


class SectionUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, section_pk):
        book = get_object_or_404((get_books(self.request.user)), pk=pk)
        section = get_object_or_404(book.sections, pk=section_pk)
        form = SectionForm(book, request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect("books:section-detail", pk=book.pk, section_pk=section.pk)
        return render(request, "books/update_section.html", {"form": form, "book": book, "section": section})
    
    def get(self, request, pk, section_pk):
        book = get_object_or_404((get_books(self.request.user)), pk=pk)
        section = get_object_or_404(book.sections, pk=section_pk)
        form = SectionForm(book, instance=section)
        return render(request, "books/update_section.html", {"form": form, "book": book, "section": section})


class SectionDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, section_pk):
        book = get_object_or_404(request.user.books, pk=pk)
        section = get_object_or_404(book.sections, pk=section_pk)
        section.delete()
        return redirect("books:detail", pk=book.pk)


class CollaboratorDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, collaborator_pk):
        book = get_object_or_404(request.user.books, pk=pk)
        collaborator = get_object_or_404(book.collaborators, pk=collaborator_pk)
        collaborator.delete()
        return redirect("books:detail", pk=book.pk)


class CollaboratorCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        form = CollaboratorForm(book, request)
        return render(request, "books/add_collaborator.html", {"book": book, "form": form})

    def post(self, request, pk):
        book = get_object_or_404(request.user.books, pk=pk)
        form = CollaboratorForm(book, request, request.POST)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk=book.pk)
        return render(request, "books/add_collaborator.html", {"book": book, "form": form})
