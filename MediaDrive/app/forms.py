from django import forms
from app.models import *
from django.contrib.auth.forms import *


class AccountCreationForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(
		attrs={'class':'myinput_form','placeholder':'Enter your full name'}
	))
	email = forms.CharField(widget=forms.EmailInput(
		attrs={'class':'myinput_form','placeholder':'Enter your email'}
	))
	phone = forms.CharField(widget=forms.NumberInput(
		attrs={'class':'myinput_form','placeholder':'Enter your number'}
	))
	password1 = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'myinput_form','placeholder':'Enter your password'}
	))
	password2 = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'myinput_form','placeholder':'Enter your confirm password'}
	))
	class Meta:
		model = UsersAccounts
		fields = ['first_name','email','phone']

	def __init__(self, *args, **kwargs):
		super(AccountCreationForm, self).__init__(*args, **kwargs)
		self.fields['phone'].widget.attrs.pop('autofocus',None)



class AuthenticationUserForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(
		attrs={'class':'myinput_form','placeholder':'Enter your number'}
	))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'myinput_form','placeholder':'Enter your password'}
	))

	def __init__(self, *args, **kwargs):
		super(AuthenticationUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.pop('autofocus',None)



class UserUpdateForm(UserChangeForm):
	password = None
	image = forms.ImageField(required=False,widget=forms.FileInput(
		attrs={'class':'folderinput border','id':'chooseyourimg'}
	))
	class Meta:
		model = UsersAccounts
		fields = ['image','first_name','email','phone']
		widgets = {
			'first_name':forms.TextInput(attrs={'class':'folderinput border','id':'inputyourname'}),
			'email':forms.TextInput(attrs={'class':'folderinput border','id':'inputyouremail'}),
			'phone':forms.TextInput(attrs={'class':'folderinput border','id':'inputyourphone'}),
		}


class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'folderinput border','id':'inputyouroldpassword'}
	))
	new_password1 = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'folderinput border','id':'inputyourpassword'}
	))
	new_password2 = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'folderinput border','id':'inputyourconfirmpassword'}
	))


class FilesCreateForm(forms.ModelForm):
	class Meta:
		model = FilesModel
		fields = ['file']
		widgets = {
			'file':forms.FileInput(attrs={'type':'file','class':'folderinput fileInput p-3', 'id':'inputfile'}),
		}