from django import forms
from django.contrib.auth.models import User

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class Create_accountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']