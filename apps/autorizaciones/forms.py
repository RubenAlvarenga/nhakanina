from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
from django.core.files.images import get_image_dimensions
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget

class UserForm(UserCreationForm):
    avatar = forms.ImageField(required = False)
    class Meta:
        model = User
        fields = ['username',]
        widgets = {
			'username' : forms.TextInput(attrs = {'class':'form-control'}),
        	'password': forms.PasswordInput(attrs = {'class':'form-control'}),
        }



class updUserForm(ModelForm):
    email = forms.EmailField(required = True, widget=forms.TextInput(attrs = {'class':'form-control'}))
    avatar = forms.ImageField(required = False)
    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)
    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'date_joined', 'is_staff', 'password']
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'user_permissions', 'is_active')
        widgets = {
            'username' : forms.TextInput(attrs = {'class':'form-control'}),
            'first_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'last_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'groups' : FilteredSelectMultiple("groups", is_stacked=False, attrs = {'class':'form-control'}),
            'user_permissions' : FilteredSelectMultiple("user_permissions", is_stacked=False, attrs = {'class':'form-control'}),
        }
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()


class updPerfilForm(ModelForm):
    email = forms.EmailField(required = True, widget=forms.TextInput(attrs = {'class':'form-control'}))
    avatar = forms.ImageField(required = False)
    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'date_joined', 'is_staff', 'password', 'groups', 'user_permissions', 'is_active', 'username']
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            # 'username' : forms.TextInput(attrs = {'class':'form-control'}),
            'first_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'last_name' : forms.TextInput(attrs = {'class':'form-control'}),
        }
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()


class GroupForm(ModelForm):
    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)
    class Meta:
        exclude=[]
        model = Group
        widgets = {
            'name' : forms.TextInput(attrs = {'class':'form-control'}),
            'permissions' : FilteredSelectMultiple("permissions", is_stacked=False, attrs = {'class':'form-control'}),
        }


class chgPasswordForm(ModelForm):
    class Meta:
        fields = ['password',]
        model = User
        widgets = {
            'password': forms.PasswordInput(attrs = {'class':'form-control'}),
        }

class PasswordChangeForm(ModelForm):
    class Meta:
        fields = ['password',]
        model = User
        widgets = {
            'password': forms.PasswordInput(attrs = {'class':'form-control'}),
        }        