import email
from attr import field
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

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
        if commit:
            user.save()
        return user
