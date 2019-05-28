from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Post, UserProfile

class UserNameField(forms.CharField):
    def to_python(self, value):
        return value.lower()

# Form to create a user
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'password1', 'password2')

#Form to log a user in
class CustomAuthForm(AuthenticationForm):
    username = UserNameField(max_length=50)

    class Meta(AuthenticationForm):
        model = User
        fields = ('username', 'password')

    def clean_email(self):
        return self.cleaned_data['username'].lower()

# From to post a message
class PostForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class':'materialize-textarea', 'data-length':'120'}), max_length=200)

    class Meta(forms.ModelForm):
        model = Post
        fields = ('message',)


class ProfileImageForm(forms.ModelForm):
    
    class Meta(forms.ModelForm):
        model = UserProfile
        fields = ('profile_image',)

