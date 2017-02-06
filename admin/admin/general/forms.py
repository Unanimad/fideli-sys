from django import forms

from .models import *


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'phone')
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
