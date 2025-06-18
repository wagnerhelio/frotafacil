from django import forms
from .models_requisicao import Requisicao
from .models_veiculo import Veiculo
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Requisicao
        fields = [
            'unidade', 'usuario', 'data_utilizacao', 'itinerario',
            'natureza_servico', 'veiculo', 'nome_motorista'
        ]
        widgets = {
            'data_utilizacao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'usuario': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        veiculos_ocupados = [r.veiculo_id for r in Requisicao.objects.filter(status='ativa')]
        self.fields['veiculo'].queryset = Veiculo.objects.exclude(id__in=veiculos_ocupados)
        now = timezone.localtime()
        self.fields['data_utilizacao'].initial = now.strftime('%Y-%m-%dT%H:%M')
        self.fields['data_utilizacao'].widget.attrs['value'] = now.strftime('%Y-%m-%dT%H:%M')
        if user:
            self.fields['usuario'].initial = user.pk

class FiltrarRequisicaoForm(forms.Form):
    veiculo = forms.ModelChoiceField(queryset=Veiculo.objects.all(), required=False, label='Veículo')
    usuario = forms.ModelChoiceField(queryset=None, required=False, label='Motorista')
    data_inicial = forms.DateField(required=False, label='Data Inicial', widget=forms.DateInput(attrs={'type': 'date'}))
    data_final = forms.DateField(required=False, label='Data Final', widget=forms.DateInput(attrs={'type': 'date'}))
    data_especifica = forms.DateField(required=False, label='Dia Específico', widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.all() 

class FinalizarRequisicaoForm(forms.ModelForm):
    motivo_km_saida_divergente = forms.CharField(label='Motivo da Divergência do KM de Saída', required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Descreva o motivo da divergência do KM de saída, se houver.'}))

    class Meta:
        model = Requisicao
        fields = [
            'data_saida', 'data_chegada', 'km_saida', 'motivo_km_saida_divergente',
            'km_chegada', 'ocorrencias', 'nome_motorista', 'assinatura_usuario'
        ]
        widgets = {
            'data_saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_chegada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        veiculo = kwargs.pop('veiculo', None)
        super().__init__(*args, **kwargs)
        from .models_requisicao import Requisicao
        now = timezone.localtime()
        # Sempre usar o valor salvo na instância
        if hasattr(self.instance, 'data_utilizacao') and self.instance.data_utilizacao:
            local_dt = localtime(self.instance.data_utilizacao)
            value_str = local_dt.strftime('%Y-%m-%dT%H:%M')
            self.fields['data_saida'].initial = value_str
            self.fields['data_saida'].widget.attrs['value'] = value_str
        else:
            value_str = now.strftime('%Y-%m-%dT%H:%M')
            self.fields['data_saida'].initial = value_str
            self.fields['data_saida'].widget.attrs['value'] = value_str
        self.fields['data_chegada'].initial = now.strftime('%Y-%m-%dT%H:%M')
        # Sugerir km_saida anterior
        km_sugerido = ''
        if veiculo:
            qs = Requisicao.objects.filter(veiculo=veiculo, status='finalizada')
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            req = qs.order_by('-data_chegada').first()
            km_sugerido = req.km_chegada if req and req.km_chegada else ''
        self.km_saida_sugerido = km_sugerido
        self.fields['km_saida'].initial = km_sugerido
        self.fields['km_saida'].widget.attrs['value'] = km_sugerido

    def clean(self):
        cleaned = super().clean()
        km_saida = cleaned.get('km_saida')
        km_chegada = cleaned.get('km_chegada')
        km_saida_sugerido = self.km_saida_sugerido
        motivo = cleaned.get('motivo_km_saida_divergente')
        # Validação de divergência
        if km_saida and km_saida_sugerido and str(km_saida) != str(km_saida_sugerido):
            if not motivo:
                self.add_error('motivo_km_saida_divergente', 'Informe o motivo da divergência do KM de saída.')
        # Validação: KM de chegada não pode ser menor que KM de saída
        try:
            if km_saida is not None and km_chegada is not None:
                if float(km_chegada) < float(km_saida):
                    self.add_error('km_chegada', 'O KM de chegada não pode ser menor que o KM de saída.')
        except Exception:
            pass
        data_saida = cleaned.get('data_saida')
        data_chegada = cleaned.get('data_chegada')
        # Validação: Data de chegada não pode ser menor que data de saída
        if data_saida and data_chegada:
            if data_chegada < data_saida:
                self.add_error('data_chegada', 'A data de chegada não pode ser menor que a data de saída.')
        return cleaned 