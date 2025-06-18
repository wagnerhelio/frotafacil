from django import forms
from .models_veiculo import Veiculo

class CadastrarVeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={'placeholder': 'AAA0A00'}),
            'ano_fabricacao': forms.NumberInput(attrs={'min': 1990}),
            'potencia_cv': forms.NumberInput(attrs={'step': '0.01'}),
            'valor_atual_mercado': forms.NumberInput(attrs={'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

class EditarVeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={'readonly': 'readonly'}),
            'ano_fabricacao': forms.NumberInput(attrs={'min': 1990}),
            'potencia_cv': forms.NumberInput(attrs={'step': '0.01'}),
            'valor_atual_mercado': forms.NumberInput(attrs={'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

class ListarVeiculoForm(forms.Form):
    placa = forms.CharField(
        max_length=10,
        required=False,
        label='Placa (contém)'
    )
    marca = forms.CharField(
        max_length=50,
        required=False,
        label='Marca'
    )
    modelo = forms.CharField(
        max_length=50,
        required=False,
        label='Modelo'
    )
    ano_fabricacao = forms.IntegerField(
        required=False,
        label='Ano de Fabricação',
        min_value=1990
    )

class ExcluirVeiculoForm(forms.Form):
    confirmar = forms.BooleanField(
        label="Confirmo que desejo excluir este veículo",
        required=True
    )
