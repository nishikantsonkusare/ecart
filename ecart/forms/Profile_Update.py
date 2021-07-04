from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from ecart.models import UserProfile
import re

class UpdateUser(ModelForm):

    class Meta:
        model = User
        
        fields = ['first_name', 'last_name', 'username']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'First Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'Last Name', 'class': 'form-control', 'autocomplete': 'off'}),
            'username' : forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control', 'autocomplete': 'off', 'readonly':''}),
        }

    def clean(self):
        super(UpdateUser, self).clean()

        fname = self.cleaned_data.get('first_name')
        lname = self.cleaned_data.get('last_name')

        if not fname:
            self.add_error('first_name', 'Please enter first name.')
        
        if not lname:
            self.add_error('last_name', 'Please enter last name')
        
        return self.cleaned_data

def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)

class UpdateProfile(ModelForm):
    class Meta:
        model = UserProfile

        fields = ['mobile', 'address', 'profile_image']

        widgets = {
            'mobile' : forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control', 'autocomplete': 'off'}),
            'address' : forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control', 'autocomplete': 'off'}),
            'profile_image' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        super(UpdateProfile, self).clean()

        mob = self.cleaned_data.get('mobile')
        add = self.cleaned_data.get('address')
        pic = self.cleaned_data.get('profile_image')

        if not add:
            self.add_error('address', 'Please must not blank.')
        
        if pic:
            if pic.size >= 5242880:
                self.add_error('profile_image', 'Profile Pic must be less than 5MB.') 

        if not mob:
            self.add_error('mobile', 'Please enter valid mobile number.')

        if mob:
            if (not isValid(mob)):
                self.add_error('mobile', 'Please entered valid mobile number.')

        return self.cleaned_data
    