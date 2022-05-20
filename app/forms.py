from cProfile import label
from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from app.models import Question, Tag, Profile, Answer


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "mb-3"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "mb-3"}))


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "mb-3"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "mb-3"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

        labels = {
            'first_name': 'Nick name'
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "mb-3"}),
            "first_name": forms.TextInput(attrs={"class": "mb-3"}),
            "email": forms.TextInput(attrs={"class": "mb-3"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data['password']
        pass2 = cleaned_data['password_repeat']

        if pass1 != pass2:
            self.add_error('password_repeat', "Passwords do not match")

        count_usrs_email = User.objects.filter(email=self.cleaned_data['email']).count()

        if count_usrs_email > 0:
            self.add_error('email', "User with this email is already registered")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user.save()
        profile = Profile.objects.create(user=user)

        if commit:
            profile.save()

        return profile


class SettingsForm(forms.ModelForm):
    avatar = forms.FileField(label="Avatar image", required=False, widget=forms.FileInput(
        attrs={"class": "col-md-9 pe-5 mb-3"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        labels = {
            'first_name': 'Nick name'
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "mb-3"}),
            "first_name": forms.TextInput(attrs={"class": "mb-3"}),
            "email": forms.TextInput(attrs={"class": "mb-3"}),
        }


class QuestionForm(forms.ModelForm):

    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "mb-3",
                                                         "placeholder": "Input one or few tags"}), label="Tags")

    def save(self, user):
        question = super().save(commit=False)
        question.profile = user
        question.save()
        tags_list = self.cleaned_data["tags"].split()
        for tag in tags_list:
            new = Tag.objects.get_or_create(name=tag)
            question.tags.add(new[0].id)
        question.save()

        return question

    class Meta:
        model = Question
        fields = ['title', 'text']
        labels = {
            'title': 'Question title',
            'text': 'Question',
        }

        widgets = {
            "title": forms.TextInput(attrs={"class": "mb-3"}),
            "text": forms.TextInput(attrs={"class": "mb-3"}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = {
            'text': 'Your answer'
        }

        widgets = {
            "text": forms.TextInput(attrs={"class": "mb-3"}),
        }
