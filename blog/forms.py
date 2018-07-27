#!/usr/bin/env python
# encoding: utf-8

from .models import Comment
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets


class CommentForm(ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    article_id = forms.IntegerField(widget=forms.HiddenInput, required=True)
    author_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body', 'parent_comment_id', 'article_id', 'author_id']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
