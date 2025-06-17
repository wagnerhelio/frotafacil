from django import forms
from models_veiculo import Veiculo

class CadastrarVeiculoForm (forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={'placeholder': 'AAA0A00'}),
            'valor_aquisicao': forms.NumberInput(attrs={'step': '0.01'}),
            'ano_fabricacao': forms.NumberInput(attrs={'min': 1990}),
        }

class EditarVeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={'readonly': 'readonly'}),
            'valor_aquisicao': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ListarVeiculoForm(forms.Form):
    placa = forms.CharField(
        max_length=10,
        required=False,
        label='Placa (contém)'
    )
    
class ExcluirVeiculoForm(forms.Form):
    confirmar = forms.BooleanField(label="Confirmo que desejo excluir este veículo")
