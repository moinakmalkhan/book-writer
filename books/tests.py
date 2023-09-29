from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from books.forms import BookForm, SectionForm, CollaboratorForm
from books.models import Book, Section

User = get_user_model()


class TestLoginRequired:
    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")


class TestBookCreateView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.url = reverse("books:add")
        self.user = User.objects.create_user(username="test", password="test")

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookForm)
        self.assertTemplateUsed(response, "books/add_book.html")

    def test_post(self):
        self.client.force_login(self.user)
        self.assertEqual(Book.objects.count(), 0)
        response = self.client.post(self.url, {"name": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().name, "test")
        self.assertEqual(Book.objects.first().author, self.user)
        self.assertRedirects(response, reverse("books:detail", kwargs={"pk": Book.objects.first().pk}))

    def test_post_invalid(self):
        self.client.force_login(self.user)
        self.assertEqual(Book.objects.count(), 0)
        response = self.client.post(self.url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)
        self.assertTemplateUsed(response, "books/add_book.html")
        self.assertIsInstance(response.context["form"], BookForm)
        self.assertFormError(response, "form", "name", "This field is required.")
        

class TestBookListView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.url = reverse("books:home")
        self.user = User.objects.create_user(username="test", password="test")

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/books.html")
        self.assertQuerysetEqual(response.context["books"], [])

    def test_get_with_books(self):
        self.client.force_login(self.user)
        book = Book.objects.create(name="test", author=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/books.html")
        self.assertQuerysetEqual(response.context["books"], [book])


class TestBookDetailView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.url = reverse("books:detail", kwargs={"pk": self.book.pk})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book.html")
        self.assertEqual(response.context["book"], self.book)


class TestBookUpdateView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.url = reverse("books:update", kwargs={"pk": self.book.pk})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookForm)
        self.assertTemplateUsed(response, "books/update_book.html")
        self.assertEqual(response.context["book"], self.book)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"name": "new name"})
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.name, "new name")
        self.assertRedirects(response, reverse("books:detail", kwargs={"pk": self.book.pk}))

    def test_post_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/update_book.html")
        self.assertIsInstance(response.context["form"], BookForm)
        self.assertFormError(response, "form", "name", "This field is required.")

    def test_post_invalid_user(self):
        user2 = User.objects.create_user(username="test2", password="test")
        self.client.force_login(user2)
        response = self.client.post(self.url, {"name": "new name"})
        self.assertEqual(response.status_code, 404)

    

class TestBookDeleteView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.url = reverse("books:delete", kwargs={"pk": self.book.pk})

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)
        self.assertRedirects(response, reverse("books:home"))

    def test_post_invalid_user(self):
        user2 = User.objects.create_user(username="test2", password="test")
        self.client.force_login(user2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Book.objects.count(), 1)


class TestSectionCreateView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.url = reverse("books:add-section", kwargs={"pk": self.book.pk})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], SectionForm)
        self.assertTemplateUsed(response, "books/add_section.html")

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"title": "test", "content": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Section.objects.count(), 1)
        self.assertRedirects(response, reverse("books:detail", kwargs={"pk": self.book.pk}))
        self.assertEqual(Section.objects.first().title, "test")
        self.assertEqual(Section.objects.first().content, "test")
        self.assertEqual(Section.objects.first().book, self.book)
        self.assertEqual(Section.objects.first().author, self.user)

    def test_post_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"content": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Section.objects.count(), 0)
        self.assertTemplateUsed(response, "books/add_section.html")
        self.assertIsInstance(response.context["form"], SectionForm)
        self.assertFormError(response, "form", "title", "This field is required.")

    def test_post_invalid_user(self):
        user2 = User.objects.create_user(username="test2", password="test")
        self.client.force_login(user2)
        response = self.client.post(self.url, {"title": "test", "content": "test"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Section.objects.count(), 0)
    

class TestSectionUpdateView(TestCase, TestLoginRequired):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.section = Section.objects.create(title="test", content="test", book=self.book, author=self.user)
        self.url = reverse("books:update-section", kwargs={"pk": self.book.pk, "section_pk": self.section.pk})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], SectionForm)
        self.assertTemplateUsed(response, "books/update_section.html")
        self.assertEqual(response.context["book"], self.book)
        self.assertEqual(response.context["section"], self.section)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"title": "new title", "content": "new content"})
        self.assertEqual(response.status_code, 302)
        self.section.refresh_from_db()
        self.assertEqual(self.section.title, "new title")
        self.assertEqual(self.section.content, "new content")
        self.assertRedirects(response, reverse("books:section-detail", kwargs={"pk": self.book.pk, "section_pk": self.section.pk}))

    def test_post_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"title": "", "content": "new content"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/update_section.html")
        self.assertIsInstance(response.context["form"], SectionForm)
        self.assertFormError(response, "form", "title", "This field is required.")

    def test_post_invalid_user(self):
        user2 = User.objects.create_user(username="test2", password="test")
        self.client.force_login(user2)
        response = self.client.post(self.url, {"title": "new title", "content": "new content"})
        self.assertEqual(response.status_code, 404)
        self.section.refresh_from_db()
        self.assertEqual(self.section.title, "test")
        self.assertEqual(self.section.content, "test")

    def test_collaborator_can_update_section(self):
        user2 = User.objects.create_user(username="test2", password="test")
        self.book.collaborators.add(user2)
        self.client.force_login(user2)
        response = self.client.post(self.url, {"title": "new title", "content": "new content"})
        self.assertEqual(response.status_code, 302)
        self.section.refresh_from_db()
        self.assertEqual(self.section.title, "new title")
        self.assertEqual(self.section.content, "new content")
        self.assertRedirects(response, reverse("books:section-detail", kwargs={"pk": self.book.pk, "section_pk": self.section.pk}))


class TestSectionDetailView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.section = Section.objects.create(title="test", content="test", book=self.book, author=self.user)
        self.url = reverse("books:section-detail", kwargs={"pk": self.book.pk, "section_pk": self.section.pk})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/section.html")
        self.assertEqual(response.context["book"], self.book)
        self.assertEqual(response.context["section"], self.section)


class TestSectionDeleteView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test")
        self.book = Book.objects.create(name="test", author=self.user)
        self.section = Section.objects.create(title="test", content="test", book=self.book, author=self.user)
        self.url = reverse("books:delete-section", kwargs={"pk": self.book.pk, "section_pk": self.section.pk})

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Section.objects.count(), 0)
        self.assertRedirects(response, reverse("books:detail", kwargs={"pk": self.book.pk}))

    def test_post_invalid_user(self):
        user2 = User.objects.create_user(username="test2", password="test")
        self.client.force_login(user2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Section.objects.count(), 1)


class TestCollaboratorCreateView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test", email="test1@gmail.com")
        self.user2 = User.objects.create_user(username="test2", password="test", email="test2@gmail.com")
        self.book = Book.objects.create(name="test", author=self.user)
        self.url = reverse("books:add-collaborator", kwargs={"pk": self.book.pk})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], CollaboratorForm)
        self.assertTemplateUsed(response, "books/add_collaborator.html")
        self.assertEqual(response.context["book"], self.book)

    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"email": self.user2.email})
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.collaborators.count(), 1)
        self.assertEqual(self.book.collaborators.first(), self.user2)
        self.assertRedirects(response, reverse("books:detail", kwargs={"pk": self.book.pk}))

    def test_post_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"email": "wrong@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/add_collaborator.html")
        self.assertIsInstance(response.context["form"], CollaboratorForm)
        self.assertFormError(response, "form", "email", "User with this email does not exist.")


class TestCollaboratorDeleteView(TestCase, TestLoginRequired):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="test", email="test1@gmail.com")
        self.user2 = User.objects.create_user(username="test2", password="test", email="test2@gmail.com")
        self.book = Book.objects.create(name="test", author=self.user)
        self.book.collaborators.add(self.user2)
        self.url = reverse("books:delete-collaborator", kwargs={"pk": self.book.pk, "collaborator_pk": self.user2.pk})
    
    def test_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.collaborators.count(), 0)
        self.assertRedirects(response, reverse("books:detail", kwargs={"pk": self.book.pk}))

    def test_post_invalid_user(self):
        user3 = User.objects.create_user(username="test3", password="test")
        self.client.force_login(user3)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.book.refresh_from_db()
        self.assertEqual(self.book.collaborators.count(), 1)
        self.assertEqual(self.book.collaborators.first(), self.user2)
