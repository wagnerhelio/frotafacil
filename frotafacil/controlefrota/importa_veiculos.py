import pandas as pd
from controlefrota.models_veiculo import Veiculo
from django.db import IntegrityError

# Caminho do arquivo Excel
excel_path = 'static/Planilha Customizada Veiculos.xlsx'

# Dicionário para converter nome do mês para número
meses = {
    'JANEIRO': 1, 'FEVEREIRO': 2, 'MARÇO': 3, 'ABRIL': 4, 'MAIO': 5, 'JUNHO': 6,
    'JULHO': 7, 'AGOSTO': 8, 'SETEMBRO': 9, 'OUTUBRO': 10, 'NOVEMBRO': 11, 'DEZEMBRO': 12
}

# Mapeamento das colunas da planilha para os campos do modelo
col_map = {
    'ANO_REFERENCIA': 'ano_referencia',
    'MES_REFERENCIA': 'mes_referencia',
    'TRIBUNAL': 'localizacao_tribunal',
    'SECAO': 'localizacao_secao',
    'SUBSECAO': 'localizacao_subsecao',
    'TOMBAMENTO': 'registro_patrimonial',
    'CLASSIFICACAO_GRUPO': 'classificacao_grupo',
    'MARCA': 'marca',
    'MODELO': 'modelo',
    'PLACA': 'placa',
    'ANO_FABRICACAO': 'ano_fabricacao',
    'POTENCIA': 'potencia_cv',
    'AC': 'complemento_ac',
    'DH': 'complemento_dh',
    'VE': 'complemento_ve',
    'TE': 'complemento_te',
    'BAG': 'complemento_bag',
    'ABS': 'complemento_abs',
    'TIPO_COMBUSTIVEL': 'tipo_combustivel',
    'CONSERVACAO': 'estado_conservacao',
    'VALOR_ATUAL_MERCADO': 'valor_atual_mercado',
    'OBSERVACOES': 'observacoes',
}

# Lê a planilha
print('Lendo planilha...')
df = pd.read_excel(excel_path)

# Renomeia as colunas para bater com o modelo
df = df.rename(columns=col_map)

# Converte os campos de SIM/NÃO para booleano
for col in ['complemento_ac', 'complemento_dh', 'complemento_ve', 'complemento_te', 'complemento_bag', 'complemento_abs']:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: True if str(x).strip().upper() in ['SIM', '1', 'TRUE'] else False)

# Preenche valores faltantes com None
df = df.where(pd.notnull(df), None)

# Cria os objetos Veiculo
print('Importando veículos...')
for idx, row in df.iterrows():
    placa = row.get('placa')
    modelo = row.get('modelo')
    if not placa or not modelo:
        print(f"Registro ignorado (placa ou modelo vazio): {row.to_dict()}")
        continue

    # Verifica se já existe veículo com a mesma placa
    if Veiculo.objects.filter(placa=placa).exists():
        print(f"Veículo com placa {placa} já existe. Registro ignorado.")
        continue

    # Conversão do mês para número
    mes_ref = row.get('mes_referencia')
    if isinstance(mes_ref, str):
        mes_ref_num = meses.get(mes_ref.strip().upper(), None)
    else:
        mes_ref_num = mes_ref

    try:
        Veiculo.objects.create(
            ano_referencia=row.get('ano_referencia'),
            mes_referencia=mes_ref_num,
            localizacao_tribunal=row.get('localizacao_tribunal'),
            localizacao_secao=row.get('localizacao_secao'),
            localizacao_subsecao=row.get('localizacao_subsecao'),
            registro_patrimonial=row.get('registro_patrimonial'),
            classificacao_grupo=row.get('classificacao_grupo'),
            marca=row.get('marca'),
            modelo=row.get('modelo'),
            placa=placa,
            ano_fabricacao=row.get('ano_fabricacao'),
            potencia_cv=row.get('potencia_cv'),
            complemento_ac=row.get('complemento_ac'),
            complemento_dh=row.get('complemento_dh'),
            complemento_ve=row.get('complemento_ve'),
            complemento_te=row.get('complemento_te'),
            complemento_bag=row.get('complemento_bag'),
            complemento_abs=row.get('complemento_abs'),
            tipo_combustivel=row.get('tipo_combustivel'),
            estado_conservacao=row.get('estado_conservacao'),
            valor_atual_mercado=row.get('valor_atual_mercado'),
            observacoes=row.get('observacoes'),
        )
    except IntegrityError as e:
        print(f"Erro de integridade ao importar placa {placa}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao importar placa {placa}: {e}")

print('Importação concluída!') 