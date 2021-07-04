from django.contrib.auth.forms import PasswordChangeForm
from django import forms

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label = 'Old Password',
        strip = False,
        widget = forms.PasswordInput(attrs={ 'placeholder': 'Enter Old Password', 'class' : 'form-control', 'autocomplete': 'off'})
    )

    new_password1 = forms.CharField(
        label = 'New Password',
        strip = False,
        widget = forms.PasswordInput(attrs={ 'placeholder': 'Enter New Password', 'class' : 'form-control', 'autocomplete': 'off'})
    )

    new_password2 = forms.CharField(
        label = 'New Password Again',
        strip = False,
        widget = forms.PasswordInput(attrs={ 'placeholder': 'Enter New Password Again', 'class' : 'form-control', 'autocomplete': 'off'})
    )