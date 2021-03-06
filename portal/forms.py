from django import forms
from .models import *
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dni', 'birthdate', 'city', 'description', 'professions', 'picture']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Searchform(forms.Form):
    city = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LabourRequestForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    price = forms.IntegerField(min_value=0, max_value=9999)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = LabourImage
        fields = ('image',)


class RatingForm(forms.Form):
    punctuation = forms.IntegerField(min_value=0, max_value=10)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)


class ChatMessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols': 100,
            'rows': 3,
            'class': 'form-control'}), max_length=1000)


class OfferForm(forms.Form):
    price = forms.IntegerField(min_value=0)

    class Meta:
        model = LabourOffer
        fields = ('price',)
