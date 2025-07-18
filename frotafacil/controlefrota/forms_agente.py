from django import forms
from .models_agente import Agente

class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['matricula', 'nome', 'email', 'ferias_inicio', 'ferias_fim', 'data_inicio_escala', 'ativo']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'id': 'matricula'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'id': 'nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'readonly': 'readonly'}),
            'ferias_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id': 'ferias_inicio', 'type': 'date'}),
            'ferias_fim': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id': 'ferias_fim', 'type': 'date'}),
            'data_inicio_escala': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id': 'data_inicio_escala', 'type': 'date'}),
        }
        input_formats = {'ferias_inicio': ['%Y-%m-%d'], 'ferias_fim': ['%Y-%m-%d'], 'data_inicio_escala': ['%Y-%m-%d']}

    class Media:
        js = ('js/buscar_ldap.js',)

    def clean(self):
        cleaned_data = super().clean()
        matricula = cleaned_data.get('matricula')
        email = cleaned_data.get('email')
        # Verifica duplicidade de matrícula
        if matricula and Agente.objects.filter(matricula=matricula).exclude(pk=self.instance.pk).exists():
            self.add_error('matricula', 'Já existe um agente com esta matrícula.')
        # Verifica duplicidade de e-mail
        if email and Agente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error('email', 'Já existe um agente com este e-mail.')
        return cleaned_data 