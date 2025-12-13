from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class profileForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')

class PostForm(forms.ModelForm):
    tags = forms.CharField(
            required=False,
            help_text='Add tags separated by commas (e.g. django, python, tutorial).',
            widget=forms.TextInput(attrs={'placeholder': 'tag1', 'tag2', 'tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'published', 'tags']
        widgets = {'content': forms.Textarea(attrs={'rows': 8})}

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['tags'].initial = ','.join([t.name for t in instance.tags.all()])

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        names = []
        for part in raw.split(','):
            name = part.strip()
            if name:
                if name.lower() not in [n.lower() for n in names]:
                    names.append(name)
            return names

    def save(self, commit=True):
        tags = self.cleaned_date.pop('tags', [])
        post = super().save(commit=commit)
        post.tags.clear()
        for name in tags:
            tag_obj, _= Tag.objects.get_or_create(name=name)
            post.tags.add(tag_obj)
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'})}

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content
