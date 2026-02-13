import pandas as pd
import random
import numpy as np

print("🔧 Iniciando ajuste de distribuição de contratos...")
print("📊 Meta: 50%+ Anual | ~30% 5 anos | ~20% 10 anos\n")

# ========================================
# CARREGAR O EXCEL EXISTENTE
# ========================================

try:
    # Carregar todas as abas
    df_clientes = pd.read_excel('alpha_club_database.xlsx', sheet_name='Clientes')
    df_vendas = pd.read_excel('alpha_club_database.xlsx', sheet_name='Vendas')
    df_entradas = pd.read_excel('alpha_club_database.xlsx', sheet_name='Entradas')
    df_restaurante = pd.read_excel('alpha_club_database.xlsx', sheet_name='Restaurante')

    print("✅ Arquivo carregado com sucesso!")
    print(f"   • Clientes: {len(df_clientes)}")
    print(f"   • Vendas: {len(df_vendas)}")
    print(f"   • Entradas: {len(df_entradas)}")
    print(f"   • Restaurante: {len(df_restaurante)}\n")

except FileNotFoundError:
    print("❌ ERRO: Arquivo 'alpha_club_database.xlsx' não encontrado!")
    print("   Execute primeiro o script de geração do banco de dados.")
    exit()

# ========================================
# ANALISAR DISTRIBUIÇÃO ATUAL
# ========================================

print("📊 Distribuição ATUAL de contratos:")
print("-" * 50)

# Filtrar apenas clientes principais (não dependentes e não sem contrato)
clientes_principais = df_clientes[
    ~df_clientes['Contrato'].str.contains('Dependente', na=False) &
    (df_clientes['Contrato'] != 'Sem Contrato')
    ]

contratos_atuais = clientes_principais['Contrato'].value_counts()
total_contratos = len(clientes_principais)

for contrato, qtd in contratos_atuais.items():
    percentual = (qtd / total_contratos) * 100
    print(f"   {contrato}: {qtd} ({percentual:.1f}%)")

print("\n")

# ========================================
# REDISTRIBUIR CONTRATOS
# ========================================

print("🔄 Redistribuindo contratos conforme especificação...")


# ===== NOVA DISTRIBUIÇÃO DESEJADA =====
# 50%+ Plano Anual | ~30% Plano de 5 anos | ~20% Plano de 10 anos

def escolher_novo_contrato():
    """
    Escolhe um novo tipo de contrato seguindo a distribuição desejada:
    - 50%+ Plano Anual
    - ~30% Plano de 5 anos
    - ~20% Plano de 10 anos
    """
    rand = random.random()

    if rand < 0.50:  # 50% Plano Anual
        return 'Plano Anual'
    elif rand < 0.80:  # 30% Plano de 5 anos (50% + 30% = 80%)
        return 'Plano de 5 anos'
    else:  # 20% Plano de 10 anos
        return 'Plano de 10 anos'


# Redistribuir contratos dos clientes principais
for idx, cliente in clientes_principais.iterrows():
    novo_contrato = escolher_novo_contrato()
    df_clientes.at[idx, 'Contrato'] = novo_contrato

# ========================================
# AJUSTAR DEPENDENTES (limites por plano)
# ========================================

print("👨‍👩‍👧 Ajustando número de dependentes por plano...")

# Verificar e ajustar dependentes que excedem o limite
for idx, cliente in df_clientes.iterrows():
    if 'Dependente' in str(cliente['Contrato']):
        # Extrair ID do cliente principal
        try:
            id_principal = int(cliente['Contrato'].split('(')[1].split(')')[0])
            principal = df_clientes[df_clientes['ID'] == id_principal]

            if len(principal) > 0:
                contrato_principal = principal.iloc[0]['Contrato']

                # Contar quantos dependentes o principal tem
                dependentes = df_clientes[
                    df_clientes['Contrato'].str.contains(f'Dependente ({id_principal})', na=False, regex=False)
                ]

                # Definir limite baseado no novo plano
                if contrato_principal == 'Plano Anual':
                    limite = 6
                elif contrato_principal == 'Plano de 5 anos':
                    limite = 10
                elif contrato_principal == 'Plano de 10 anos':
                    limite = 13
                else:
                    continue

                # Se exceder o limite, remover os excedentes
                if len(dependentes) > limite:
                    # Manter apenas os primeiros 'limite' dependentes
                    dependentes_remover = dependentes.iloc[limite:]
                    df_clientes = df_clientes[~df_clientes['ID'].isin(dependentes_remover['ID'])]
        except:
            continue

# ========================================
# AJUSTAR TABELA DE VENDAS
# ========================================

print("💰 Ajustando tabela de vendas...")

# Atualizar contratos vendidos com a nova distribuição
for idx, venda in df_vendas.iterrows():
    novo_contrato = escolher_novo_contrato()
    df_vendas.at[idx, 'Contrato'] = novo_contrato

# ========================================
# VERIFICAR NOVA DISTRIBUIÇÃO
# ========================================

print("\n📊 Distribuição NOVA de contratos:")
print("-" * 50)

# Filtrar novamente clientes principais
clientes_principais_novo = df_clientes[
    ~df_clientes['Contrato'].str.contains('Dependente', na=False) &
    (df_clientes['Contrato'] != 'Sem Contrato')
    ]

contratos_novos = clientes_principais_novo['Contrato'].value_counts()
total_contratos_novo = len(clientes_principais_novo)

for contrato, qtd in contratos_novos.items():
    percentual = (qtd / total_contratos_novo) * 100
    print(f"   {contrato}: {qtd} ({percentual:.1f}%)")

print("\n")

# ========================================
# SALVAR ARQUIVO AJUSTADO
# ========================================

print("💾 Salvando arquivo ajustado...")

# Salvar com novo nome para não sobrescrever o original
nome_arquivo_saida = 'alpha_club_database_ajustado.xlsx'

with pd.ExcelWriter(nome_arquivo_saida, engine='openpyxl') as writer:
    df_clientes.to_excel(writer, sheet_name='Clientes', index=False)
    df_vendas.to_excel(writer, sheet_name='Vendas', index=False)
    df_entradas.to_excel(writer, sheet_name='Entradas', index=False)
    df_restaurante.to_excel(writer, sheet_name='Restaurante', index=False)

print(f"\n✅ CONCLUÍDO! Arquivo '{nome_arquivo_saida}' gerado com sucesso!")

# ========================================
# ESTATÍSTICAS FINAIS
# ========================================

print("\n📈 ESTATÍSTICAS FINAIS:")
print("-" * 50)
print(f"   • Total de Clientes: {len(df_clientes):,}")
print(f"   • Clientes Principais: {len(clientes_principais_novo):,}")
print(f"   • Dependentes: {len(df_clientes) - len(clientes_principais_novo):,}")
print(f"   • Total de Vendas: {len(df_vendas):,}")
print(f"   • Total de Entradas: {len(df_entradas):,}")
print(f"   • Total de Refeições: {len(df_restaurante):,}")

print("\n🎯 Distribuição de contratos ajustada:")
print(
    f"   • Plano Anual: {contratos_novos.get('Plano Anual', 0)} ({(contratos_novos.get('Plano Anual', 0) / total_contratos_novo * 100):.1f}%)")
print(
    f"   • Plano de 5 anos: {contratos_novos.get('Plano de 5 anos', 0)} ({(contratos_novos.get('Plano de 5 anos', 0) / total_contratos_novo * 100):.1f}%)")
print(
    f"   • Plano de 10 anos: {contratos_novos.get('Plano de 10 anos', 0)} ({(contratos_novos.get('Plano de 10 anos', 0) / total_contratos_novo * 100):.1f}%)")

print("\n🏊‍♂️ Alpha Club - Ajuste Concluído!")