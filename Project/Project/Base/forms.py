from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
# from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Video
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation







class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = [ 'username', 'email', 'password1', 'password2']




class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    

class videoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'