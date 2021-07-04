from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'username' : forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean(self):
        super(UserForm, self).clean()

        first = self.cleaned_data.get('first_name')
        last = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not first:
            self.add_error('first_name', 'Please enter first name.')
        
        if not last:
            self.add_error('last_name', 'Please enter last name.')

        if len(password) < 6:
            self.add_error('password', 'Password length should be at least 6.')
        
        if len(password) > 20:
            self.add_error('password', 'Password length should not be greater than 20.')
            
        if (not any(char.isdigit() for char in password)) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)):
            self.add_error('password', 'Password should have at least one lower, upper and digit letters.')

        return self.cleaned_data


# class LoginForm(forms):
    
