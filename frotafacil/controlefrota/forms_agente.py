from django import forms
from .models_agente import Agente

class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['matricula', 'nome', 'email']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'id': 'matricula'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'id': 'nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'readonly': 'readonly'}),
        }

    class Media:
        js = ('js/buscar_ldap.js',) 