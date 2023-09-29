from typing import Any, Dict
from django import forms
from django.contrib.auth import get_user_model

from books.models import Book, Section

User = get_user_model()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class SectionForm(forms.ModelForm):
    def __init__(self, book, *args, **kwargs):
        self.book = book
        super().__init__(*args, **kwargs)

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        parent = cleaned_data.get("parent")
        if parent and parent.book != self.book:
            raise forms.ValidationError("Parent section is not from this book.")
        return cleaned_data

    class Meta:
        model = Section
        fields = ["title", "parent", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "parent": forms.Select(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class BaseCollaboratorForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    def __init__(self, book, request, *args, **kwargs):
        self.book = book
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        self.user = User.objects.filter(email=email).first()
        if not self.user:
            raise forms.ValidationError("User with this email does not exist.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if self.request.user.id != self.book.author_id:
            raise forms.ValidationError("You are not the author of this book.")

        if self.book.collaborators.filter(email=email).exists():
            raise forms.ValidationError("User with this email is already a collaborator.")



class CollaboratorForm(BaseCollaboratorForm):
    def save(self):
        self.book.collaborators.add(self.user)
        self.book.save()
        return self.user
