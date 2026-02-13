import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Configuração de seed para reprodutibilidade (opcional)
random.seed(42)
np.random.seed(42)

print("🏊‍♂️ Iniciando geração do banco de dados Alpha Club...")

# ========================================
# DADOS BASE
# ========================================

nomes_brasileiros = [
    'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Souza',
    'Juliana Lima', 'Fernando Alves', 'Patricia Rocha', 'Roberto Martins', 'Lucia Ferreira',
    'Marcos Pereira', 'Fernanda Gomes', 'Ricardo Barbosa', 'Camila Rodrigues', 'José Carvalho',
    'Amanda Dias', 'Paulo Nascimento', 'Tatiana Moreira', 'Gabriel Ramos', 'Isabela Castro',
    'Rafael Mendes', 'Beatriz Cardoso', 'Thiago Monteiro', 'Carolina Freitas', 'Diego Pinto',
    'Vanessa Correia', 'Lucas Teixeira', 'Bruna Ribeiro', 'Gustavo Azevedo', 'Leticia Cunha',
    'Rodrigo Neves', 'Mariana Duarte', 'Eduardo Moura', 'Renata Campos', 'Felipe Barros',
    'Adriana Farias', 'Bruno Castro', 'Daniela Sousa', 'Henrique Lopes', 'Raquel Pires',
    'Leonardo Vieira', 'Cristina Machado', 'Alexandre Araújo', 'Monica Batista', 'Vinicius Torres',
    'Silvia Cavalcanti', 'Marcelo Rezende', 'Paula Melo', 'Anderson Coelho', 'Simone Fonseca'
]

sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Costa', 'Souza', 'Lima', 'Alves',
              'Rocha', 'Martins', 'Ferreira', 'Pereira', 'Cardoso', 'Ribeiro']


# ========================================
# FUNÇÕES AUXILIARES
# ========================================

# ===== CUMPRIMENTO: DIAS DE FUNCIONAMENTO (TERÇA A DOMINGO) =====
def gerar_data_aleatoria(inicio, fim):
    """
    Gera uma data aleatória entre inicio e fim.
    IMPORTANTE: Ajusta para funcionar apenas de TERÇA a DOMINGO (segunda-feira fechado).
    """
    data_inicio = datetime.strptime(inicio, '%Y-%m-%d')
    data_fim = datetime.strptime(fim, '%Y-%m-%d')

    delta = data_fim - data_inicio
    dias_aleatorios = random.randint(0, delta.days)
    data_aleatoria = data_inicio + timedelta(days=dias_aleatorios)

    # Verificar dia da semana: 0=Segunda, 1=Terça, ..., 6=Domingo
    dia_semana = data_aleatoria.weekday()

    # Se for SEGUNDA-FEIRA (0), mover para TERÇA-FEIRA (1)
    if dia_semana == 0:
        data_aleatoria += timedelta(days=1)

    return data_aleatoria


# ===== CUMPRIMENTO: SAZONALIDADE =====
def calcular_sazonalidade(data):
    """
    Calcula multiplicador de sazonalidade baseado no mês.

    VERÃO (Nov-Mar): ALTA temporada - 1.5x
    OUTONO (Abr-Mai): Começa a cair - 0.8x
    INVERNO (Jun-Ago): BAIXA temporada - 0.4x (mínima)
    PRIMAVERA (Set-Out): Recuperação - 1.0x
    """
    mes = data.month

    if mes in [11, 12, 1, 2, 3]:  # Verão
        return 1.5
    elif mes in [4, 5]:  # Outono
        return 0.8
    elif mes in [6, 7, 8]:  # Inverno
        return 0.4
    else:  # Primavera (9, 10)
        return 1.0


# ===== CUMPRIMENTO: OUTLIERS CLIMÁTICOS/EVENTOS =====
def gerar_outlier_climatico():
    """
    Simula dias atípicos (outliers):
    - 10% de chance: dia ruim (chuva forte) -> visitação muito baixa
    - 5% de chance: dia excepcional (evento, feriado) -> visitação muito alta
    - 85%: dia normal
    """
    rand = random.random()

    if rand < 0.10:  # 10% - Dia ruim (chuva)
        return 0.2  # Reduz para 20% da capacidade
    elif rand < 0.15:  # 5% - Dia excepcional
        return 1.8  # Aumenta para 180% da capacidade
    else:
        return 1.0  # Dia normal


# ========================================
# TABELA 1: CLIENTES
# ========================================

print("\n📋 Gerando tabela de CLIENTES...")

clientes_data = []
id_counter = 1
contratos = ['Plano Anual', 'Plano de 5 anos', 'Plano de 10 anos']
regioes = ['Oeste', 'Sul', 'Norte']

# ===== CUMPRIMENTO: CRESCIMENTO/DECLÍNIO AO LONGO DOS ANOS =====
# Simula diferentes fases do negócio
for ano in range(2001, 2026):

    # FASE 1: Crescimento (2001-2010) - Empresa em expansão
    if ano <= 2010:
        num_clientes_ano = int(300 + random.random() * 200)  # 300-500 clientes/ano

    # FASE 2: Declínio (2010-2022) - Crise, concorrência, pandemia (CHURN ALTO)
    elif ano <= 2022:
        num_clientes_ano = int(100 + random.random() * 150)  # 100-250 clientes/ano

    # FASE 3: Recuperação inicial (2023) - Pós-pandemia
    elif ano == 2023:
        num_clientes_ano = int(250 + random.random() * 150)  # 250-400 clientes/ano

    # FASE 4: Forte crescimento (2024-2025) - Novos investimentos (CHURN BAIXO)
    else:
        num_clientes_ano = int(400 + random.random() * 200)  # 400-600 clientes/ano

    for i in range(num_clientes_ano):
        primeiro_contrato = gerar_data_aleatoria(f'{ano}-01-01', f'{ano}-12-31')
        contrato_tipo = random.choice(contratos)

        # Calcular anos de contrato
        anos_contrato = 1 if contrato_tipo == 'Plano Anual' else (5 if contrato_tipo == 'Plano de 5 anos' else 10)
        ultimo_contrato = primeiro_contrato + timedelta(days=365 * anos_contrato)

        idade = random.randint(18, 68)

        # ===== CUMPRIMENTO: 70%+ DA ZONA OESTE =====
        regiao = 'Oeste' if random.random() < 0.70 else random.choice(regioes)

        # Determinar se o contrato ainda está ativo
        contrato_status = contrato_tipo if ultimo_contrato > datetime.now() else 'Sem Contrato'

        # ===== CUMPRIMENTO: 60% CARTEIRINHA ATIVA E INSPEÇÃO EM DIA =====
        cliente = {
            'ID': id_counter,
            'Nome': random.choice(nomes_brasileiros),
            'Idade': idade,
            'Regiao': regiao,
            'Contrato': contrato_status,
            'Carteirinha': 'Ativada' if random.random() < 0.6 else 'Desativada',
            'Inspecao_Medica': 'Dentro da validade' if random.random() < 0.6 else 'Fora da validade',
            'Primeiro_Contrato': primeiro_contrato.strftime('%Y-%m-%d'),
            'Ultimo_Contrato': ultimo_contrato.strftime('%Y-%m-%d'),
            'Recomendacao': 'Sim' if random.random() > 0.6 else 'Não'
        }

        clientes_data.append(cliente)
        id_cliente_principal = id_counter
        id_counter += 1

        # ===== CUMPRIMENTO: DEPENDENTES POR TIPO DE PLANO =====
        max_dependentes = 6 if contrato_tipo == 'Plano Anual' else (10 if contrato_tipo == 'Plano de 5 anos' else 13)
        num_dependentes = random.randint(0, max_dependentes // 2)

        for d in range(num_dependentes):
            sobrenome_principal = cliente['Nome'].split()[-1]

            # ===== CUMPRIMENTO: DEPENDENTES COM HISTÓRICO =====
            tem_historico = random.random() > 0.8

            dependente = {
                'ID': id_counter,
                'Nome': f"{random.choice(nomes_brasileiros)} {sobrenome_principal}",
                'Idade': random.randint(5, 65),
                'Regiao': regiao,
                'Contrato': f'Dependente ({id_cliente_principal})',
                'Carteirinha': 'Ativada' if random.random() < 0.6 else 'Desativada',
                'Inspecao_Medica': 'Dentro da validade' if random.random() < 0.6 else 'Fora da validade',
                'Primeiro_Contrato': primeiro_contrato.strftime('%Y-%m-%d') if tem_historico else '',
                'Ultimo_Contrato': ultimo_contrato.strftime('%Y-%m-%d') if tem_historico else '',
                'Recomendacao': 'Sim'
            }

            clientes_data.append(dependente)
            id_counter += 1

df_clientes = pd.DataFrame(clientes_data)
print(f"✅ {len(df_clientes)} clientes gerados (incluindo dependentes)")

# ========================================
# TABELA 2: VENDAS
# ========================================

print("\n💰 Gerando tabela de VENDAS...")

# ===== CUMPRIMENTO: VENDEDORES ESPECIFICADOS =====
vendedores = [
    'Ricardo', 'Anchieta', 'Cássia', 'Mario',
    'Juliana', 'Fernando', 'Beatriz', 'Carlos', 'Mariana',
    'Pedro', 'Amanda', 'Lucas', 'Fernanda', 'Gabriel',
    'Patricia', 'Rodrigo', 'Camila', 'Thiago', 'Daniela'
]

vendas_data = []
id_venda = 1

clientes_principais = df_clientes[~df_clientes['Contrato'].str.contains('Dependente', na=False)]

for _, cliente in clientes_principais.iterrows():
    data_contrato = cliente['Primeiro_Contrato']

    # ===== CUMPRIMENTO: OUTLIERS DE VENDEDORES =====
    rand = random.random()
    if rand < 0.35:
        vendedor = 'Ricardo'
    elif rand < 0.60:
        vendedor = 'Anchieta'
    else:
        vendedor = random.choice(vendedores)

    venda = {
        'ID_Vendedor': id_venda,
        'Data': data_contrato,
        'ID_Cliente': cliente['ID'],
        'Cliente': cliente['Nome'],
        'Contrato': random.choice(contratos),
        'Vendedor': vendedor
    }

    vendas_data.append(venda)
    id_venda += 1

df_vendas = pd.DataFrame(vendas_data)
print(f"✅ {len(df_vendas)} vendas geradas")

# ========================================
# TABELA 3: ENTRADAS
# ========================================

print("\n🎫 Gerando tabela de ENTRADAS...")

entradas_data = []
id_entrada = 1

for ano in range(2001, 2026):

    if ano <= 2010:
        entradas_ano = int(15000 + random.random() * 5000)
    elif ano <= 2022:
        entradas_ano = int(5000 + random.random() * 3000)
    elif ano == 2023:
        entradas_ano = int(12000 + random.random() * 3000)
    else:
        entradas_ano = int(20000 + random.random() * 5000)

    for i in range(entradas_ano // 5):

        data_entrada = gerar_data_aleatoria(f'{ano}-01-01', f'{ano}-12-31')
        sazonalidade = calcular_sazonalidade(data_entrada)
        outlier_climatico = gerar_outlier_climatico()
        fator_final = sazonalidade * outlier_climatico

        if random.random() > fator_final * 0.7:
            continue

        cliente = df_clientes.sample(1).iloc[0]
        hora_entrada = random.randint(8, 14)
        hora_saida = hora_entrada + random.randint(2, 8)

        # ===== CUMPRIMENTO: ACOMPANHANTES POR TIPO DE PLANO =====
        if 'Dependente' in str(cliente['Contrato']):
            try:
                id_principal = int(cliente['Contrato'].split('(')[1].split(')')[0])
                principal = df_clientes[df_clientes['ID'] == id_principal].iloc[0]
                contrato_ref = principal['Contrato']
            except:
                contrato_ref = 'Plano Anual'
        else:
            contrato_ref = cliente['Contrato']

        if contrato_ref == 'Plano Anual':
            max_acompanhantes = 6
        elif contrato_ref == 'Plano de 5 anos':
            max_acompanhantes = 10
        elif contrato_ref == 'Plano de 10 anos':
            max_acompanhantes = 13
        else:
            max_acompanhantes = 2

        acompanhantes = random.randint(0, max_acompanhantes)
        visitante = 'Sim' if random.random() > 0.85 else 'Não'

        entrada = {
            'ID': id_entrada,
            'Data': data_entrada.strftime('%Y-%m-%d'),
            'Hora_Entrada': f"{hora_entrada:02d}:{random.randint(0, 59):02d}",
            'Hora_Saida': f"{hora_saida:02d}:{random.randint(0, 59):02d}",
            'ID_Cliente': cliente['ID'],
            'Cliente': cliente['Nome'],
            'Acompanhantes': acompanhantes,
            'Visitante': visitante
        }

        entradas_data.append(entrada)
        id_entrada += 1

df_entradas = pd.DataFrame(entradas_data)
print(f"✅ {len(df_entradas)} entradas geradas")

# ========================================
# TABELA 4: RESTAURANTE
# ========================================

print("\n🍽️ Gerando tabela de RESTAURANTE...")

bebidas_tipos = ['Alcóolicas', 'Refrigerantes', 'Sucos', 'Água']
precos_bebidas = {'Alcóolicas': 7, 'Refrigerantes': 8, 'Sucos': 8, 'Água': 4}

restaurante_data = []

# ===== CUMPRIMENTO: PADRÃO DE CLIENTES QUE ALMOÇAM =====
clientes_que_almocam = set(df_clientes.sample(frac=0.6)['ID'].tolist())

# ===== CUMPRIMENTO: PADRÃO DE CLIENTES QUE COMEM MÚLTIPLAS VEZES =====
clientes_come_multiplas_vezes = set(df_clientes.sample(frac=0.15)['ID'].tolist())

for idx, entrada in df_entradas.iterrows():
    ano = int(entrada['Data'].split('-')[0])

    # ===== CUMPRIMENTO: PREÇO HISTÓRICO DO QUILO =====
    preco_quilo = 59.90 if ano < 2015 else 79.90

    id_cliente = entrada['ID_Cliente']

    # ===== CUMPRIMENTO: 60% DOS CLIENTES ALMOÇAM =====
    cliente_almoca = id_cliente in clientes_que_almocam

    # ===== CUMPRIMENTO: 30% DOS VISITANTES ALMOÇAM =====
    visitante_almoca = entrada['Visitante'] == 'Sim' and random.random() < 0.3

    if not cliente_almoca and not visitante_almoca:
        if random.random() > 0.6:
            continue

    # ===== CUMPRIMENTO: CLIENTES QUE COMEM MÚLTIPLAS VEZES =====
    if id_cliente in clientes_come_multiplas_vezes:
        vezes_que_comeu = 2 if random.random() < 0.4 else 1
    else:
        vezes_que_comeu = 1

    almoco_total = 0
    for vez in range(vezes_que_comeu):
        peso_prato = random.uniform(0.3, 1.0)
        almoco_total += peso_prato * preco_quilo

    num_bebidas = random.randint(1, 3)
    bebidas_selecionadas = random.sample(bebidas_tipos, num_bebidas)

    total_bebidas = 0
    for bebida in bebidas_selecionadas:
        quantidade = random.randint(1, 3)
        total_bebidas += precos_bebidas[bebida] * quantidade

    registro = {
        'Data': entrada['Data'],
        'ID_Cliente': id_cliente,
        'Cliente': entrada['Cliente'],
        'Almoco': round(almoco_total, 2),
        'Bebidas': ', '.join(bebidas_selecionadas),
        'Total_Gasto': round(almoco_total + total_bebidas, 2)
    }

    restaurante_data.append(registro)

df_restaurante = pd.DataFrame(restaurante_data)
print(f"✅ {len(df_restaurante)} registros de restaurante gerados")

# ========================================
# EXPORTAR PARA EXCEL
# ========================================

print("\n📊 Exportando para Excel...")

with pd.ExcelWriter('alpha_club_database.xlsx', engine='openpyxl') as writer:
    df_clientes.to_excel(writer, sheet_name='Clientes', index=False)
    df_vendas.to_excel(writer, sheet_name='Vendas', index=False)
    df_entradas.to_excel(writer, sheet_name='Entradas', index=False)
    df_restaurante.to_excel(writer, sheet_name='Restaurante', index=False)

print("\n✅ CONCLUÍDO! Arquivo 'alpha_club_database.xlsx' gerado com sucesso!")
print("\n📈 ESTATÍSTICAS FINAIS:")
print(f"   • Total de Clientes: {len(df_clientes):,}")
print(f"   • Total de Vendas: {len(df_vendas):,}")
print(f"   • Total de Entradas: {len(df_entradas):,}")
print(f"   • Total de Refeições: {len(df_restaurante):,}")
print(f"   • Receita Restaurante: R$ {df_restaurante['Total_Gasto'].sum():,.2f}")
print("\n🏊‍♂️ Alpha Club - Simulação Completa!")