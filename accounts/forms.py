from django import forms
from django.contrib.auth import authenticate, get_user_model, login

User = get_user_model()


class BaseForm(forms.Form):
    """Base form."""
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        # add form-control class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(BaseForm):
    """Login form."""
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid username or password')
        cleaned_data['user'] = user
        return cleaned_data


class SignUpForm(BaseForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Confirm Password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(self.request, user)
        return user
