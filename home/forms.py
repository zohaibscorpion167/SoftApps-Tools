from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.validators import validate_email

class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),required=True,max_length=50)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email ID'}),required=True,max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),required=True,max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),required=True,max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}),required=True,max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}),required=True,max_length=50)

    class Meta():
        model = User
        fields = ['username','email','first_name','last_name','password','confirm_password']


    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            match = User.objects.get(username=user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError("Username already exist")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            match_email = User.objects.get(email=email)
        except:
            return self.cleaned_data['email']
        raise forms.ValidationError("Account on this Email ID already exist")

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')

        # check for min length
        min_length = 8
        if len(password) <= min_length:
            msg = "Password must be at least %s characters long" %(min_length)
            self.add_error('password', msg)


        password_confirm = cleaned_data.get('confirm_password')


        if password and password_confirm:
            if password != password_confirm:
                msg = "The two password fields must match"
                self.add_error('confirm_password', msg)
        return cleaned_data
        
        