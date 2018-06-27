#!/usr/bin/env python
# encoding: utf-8

from .models import Comment
from django.forms import ModelForm
from django import forms


class CommentForm(ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    article_id = forms.IntegerField(widget=forms.HiddenInput, required=True)
    author_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body', 'parent_comment_id', 'article_id', 'author_id']
