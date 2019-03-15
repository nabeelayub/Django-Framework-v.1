from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

from .models import User
import re



class CustomUserCreationForm(forms.Form):
    username=forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'username'}), max_length=50)
    email=forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        if not (re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$",password1)):
            raise ValidationError("Password should have atleast one digit,one uppercase letter,one lowercase letter"
                                  " and one special character")


        return password2

    def save(self, commit=True):
        user1 = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user1

class UserForm(forms.Form):
    username=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'username'}),max_length=50)
    password=forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    model=User
    fields=['username', 'password']

class editprofile(forms.ModelForm):

    images=forms.ImageField(label='',widget=forms.FileInput,required=False)
    first_name=forms.CharField(label='', max_length=20,widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name=forms.CharField(label='', max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': ' old password'}),
                                   required=False)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password'}),required=False)
    email=forms.CharField(label='',max_length=30)
    password_confirm = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': ' Confirm Password'}),required=False)
    check_password=0

    class Meta:
        model=User
        fields=('images','first_name','last_name','email','old_password','password','password_confirm')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole

        super(editprofile, self).__init__(*args, **kwargs)
        self.check_password=self.user.password
        print(self.user.password)

    def clean(self):
        #cleaned_data = super(editprofile, self).clean()
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')
        password3=self.cleaned_data.get('old_password')

        if not (check_password(password3,self.check_password)):
            raise forms.ValidationError("Old Password not matched!")


        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password don't match")




    def save(self, commit=True):
            user = super(editprofile, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user





class MyClearableFileInput(ClearableFileInput):
    initial_text = ''
    input_text = ''
    clear_checkbox_label = 'clear'
