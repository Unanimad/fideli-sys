from django import forms
from django.contrib.auth.models import User

from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'image', 'playStore', 'appStore')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'playStore': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'appStore': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'phone', 'password')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'id': 'phone'
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            )
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'reward')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'reward': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            )
        }


class CardConfigurationForm(forms.ModelForm):
    class Meta:
        model = CardConfiguration
        fields = ('expire', 'limit')
        widgets = {
            'expire': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'type': 'number'
                }
            ),
            'limit': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'type': 'number'
                }
            )
        }


class CardForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select-single',
                'required': True
            }
        ),
        label='Serviço'
    )
    configuration = forms.ModelChoiceField(
        queryset=CardConfiguration.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select-single',
                'required': True
            }
        ),
        label='Configuração'
    )
