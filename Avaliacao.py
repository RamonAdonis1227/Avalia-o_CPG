import pandas as pd
import matplotlib.pyplot as plt
import random

# Função para gerar uma cor aleatória em formato hexadecimal
def cor_aleatoria():
    return '#{:02x}{:02x}{:02x}'.format(*random.sample(range(256), 3))

# Função para gerar uma cor aleatória mais forte em formato hexadecimal
def cor_aleatoria_forte():
    min_value = 50  # Valor mínimo para os componentes RGB
    max_value = 180  # Valor máximo para os componentes RGB
    return '#{0:02x}{1:02x}{2:02x}'.format(random.randint(min_value, max_value), random.randint(min_value, max_value), random.randint(min_value, max_value))


# Ler o arquivo Excel
df = pd.read_excel("Avaliação CPG(1-19).xlsx", engine="openpyxl")

# Excluir as colunas que não serão utilizadas
colunas_descartadas = [
    "ID", "Hora de início", "Hora de conclusão", 
    "Email", "Nome", "Total de Pontos", "Comentários do teste", 
    "Hora da última modificação", "Total de pontos",
]
df = df.drop(columns=colunas_descartadas, errors='ignore')
colunas_descartadas = [coluna for coluna in df.columns if "Pontos" in coluna or "Comentários" in coluna]
df = df.drop(columns=colunas_descartadas, errors='ignore')

# Dicionário para armazenar as médias de cada equipe
medias_por_equipe = {}

# Selecionar apenas as colunas relacionadas às equipes
equipe_columns = [coluna for coluna in df.columns if pd.api.types.is_numeric_dtype(df[coluna])]
# print("Colunas selecionadas para cálculo das médias:", equipe_columns)  # Adicionei esta linha para verificar as colunas selecionadas
for coluna in equipe_columns:
    # Extrair o número da equipe do nome da coluna
    numero_equipe = coluna.split(' -')[0].split(' ')[-1]
    try:
        numero_equipe = int(numero_equipe)
    except ValueError:
        print("Número de equipe inválido na coluna:", coluna) # Aviso para ciência de que o nome ou numero da coluna se encontra incorreto
        continue  # Ignorar colunas que não contêm um número de equipe válido
    
    dados_equipe = df[coluna].dropna()  # Selecionar coluna de valor e remover valores nulos
    # Calcular a média
    media = dados_equipe.mean()
    # Adicionar a média ao dicionário de médias por equipe
    if numero_equipe in medias_por_equipe:
        medias_por_equipe[numero_equipe].append(media)
    else:
        medias_por_equipe[numero_equipe] = [media]

# Calcular a média das médias por equipe
media_das_medias_por_equipe = {equipe: sum(medias) / len(medias) for equipe, medias in medias_por_equipe.items()}

# Ordenar as médias das médias por equipe em ordem decrescente
media_das_medias_por_equipe_sorted = dict(sorted(media_das_medias_por_equipe.items(), key=lambda item: item[1], reverse=True))

# Selecionar apenas as 5 primeiras equipes
top10_equipes = dict(list(media_das_medias_por_equipe_sorted.items())[:10])

# Definir as cores das barras
# cores = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightblue']  # Exemplo de cores

# Definir as cores das barras de forma aleatória
# cores = [cor_aleatoria() for _ in range(len(top10_equipes))]

# Definir as cores das barras de forma aleatória, mas mais fortes
# cores = [cor_aleatoria_forte() for _ in range(len(top10_equipes))]

# Definir as cores das barras de forma aleatória, mas mais fracas
cores = [cor_aleatoria_forte() for _ in range(len(top10_equipes))]

# cores = ['black', 'darkred', 'darkblue', 'violet', 'darkgreen', 'yellow', 'orange', 'purple', 'brown', 'pink']  # Exemplo de cores


# Definir os limites do eixo y de 0 a 10
plt.ylim(0, 10)

# Plotar o gráfico de barras com os valores das médias das médias em formato de ranking
plt.bar(range(1, len(top10_equipes) + 1), top10_equipes.values(), color=cores)
for i, media in enumerate(top10_equipes.values(), start=1):
    plt.text(i, media, f'{media:.2f}', ha='center', va='bottom')
plt.xlabel('Equipe (Ranking)')
plt.ylabel('Média Final das Equipes')
plt.title('Média Final por Equipe (Ranking)')
plt.xticks(range(1, len(top10_equipes) + 1), [f'Equipe {equipe}' for equipe in top10_equipes.keys()], rotation=45, ha='right')
plt.tight_layout()
plt.show()
