import pandas as pd
from collections import defaultdict
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# E aí, Professor Zanin! Aqui começamos com o básico: classe pra pegar os dados
class Concessionaria:
    def __init__(self, node_a, node_b, falhas_ano, horas_falha, consumidores):
        # Sabe como é, a gente precisa guardar direitinho essas falhas né, professor? Senão o sistema cai!
        self.node_a = node_a
        self.node_b = node_b
        self.falhas_ano = falhas_ano
        self.horas_falha = horas_falha
        self.consumidores = consumidores

# Essa função aqui vai organizar a bagunça da rede, tipo arrumar o quarto antes da visita chegar (FAÇO MUITO KKK)
def organizar_dados(dados):
    rede = defaultdict(list)
    falhas_por_no = defaultdict(float)
    horas_por_no = defaultdict(float)
    consumidores_por_no = defaultdict(int)

    # Olha só, professor, já estamos populando os dicionários, porque organização é tudo, né? 
    for linha in dados:
        rede[linha.node_a].append(linha.node_b)
        falhas_por_no[linha.node_b] = linha.falhas_ano
        horas_por_no[linha.node_b] = linha.horas_falha
        consumidores_por_no[linha.node_b] = linha.consumidores

    return rede, falhas_por_no, horas_por_no, consumidores_por_no

# Zanin, a gente precisa acumular as falhas, né? Tipo quando acumula trabalho no final de semestre!
def calcular_fec_acumulado(no, falhas_por_no, rede, fec_cache):
    if no in fec_cache:
        return fec_cache[no]

    fec_acumulado = falhas_por_no[no]

    for node_pai in rede:
        if no in rede[node_pai]:
            fec_acumulado += calcular_fec_acumulado(node_pai, falhas_por_no, rede, fec_cache)

    fec_cache[no] = fec_acumulado
    return fec_acumulado

# Agora o DIC, porque né, quem nunca acumulou horas de interrupção quando caiu a luz na aula do Zanin?
def calcular_dic_acumulado(no, horas_por_no, falhas_por_no, rede, dic_cache):
    if no in dic_cache:
        return dic_cache[no]

    dic_acumulado = horas_por_no[no] * falhas_por_no[no]

    for node_pai in rede:
        if no in rede[node_pai]:
            dic_acumulado += calcular_dic_acumulado(node_pai, horas_por_no, falhas_por_no, rede, dic_cache)

    dic_cache[no] = dic_acumulado
    return dic_acumulado

# Agora sim, vamos pro DEC e FEC da linha toda, ACHO QUE FALTOU ISSO NA MINHA PROVA KKK!
def calcular_dec_fec_total(dados):
    total_falhas = 0
    total_duracao_falhas = 0
    total_consumidores = 0

    # Olha aí, somando tudo igual quando junta a nota da turma inteira depois de uma prova suaaa!
    for dado in dados:
        total_falhas += dado.falhas_ano * dado.consumidores
        total_duracao_falhas += dado.horas_falha * dado.falhas_ano * dado.consumidores
        total_consumidores += dado.consumidores

    if total_consumidores == 0:
        return 0, 0  # Se não tiver consumidor, já era, né professor? Tudo zero!

    # Aqui o cálculo final, ou como o Zanin diz, "TEM QUE SABER"!
    dec_total = total_duracao_falhas / total_consumidores
    fec_total = total_falhas / total_consumidores

    return dec_total, fec_total

# Professor, o aluno aqui vai escolher o arquivo que tem os dados da rede, mas sem enrolar, direto ao ponto!
def calcular_indicadores_de_arquivo():
    Tk().withdraw()  # Esconde aquela janela do Tkinter que ninguém quer ver
    arquivo_excel = askopenfilename(title="Escolhe logo o arquivo, Zanin", filetypes=[("Arquivo Excel", "*.xlsx")])

    if not arquivo_excel:
        print("Nenhum arquivo selecionado, professor. Não dá pra calcular sem os dados!")
        return

    df = pd.read_excel(arquivo_excel)

    # Transformando os dados da planilha em algo que faça sentido, tipo a aula quando cai na prova
    dados = [Concessionaria(row['Node A'], row['Node B'], row['Falhas por Ano'], row['Horas por Falha'], row['Consumidores Node B']) for index, row in df.iterrows()]

    # Organizando a bagunça da rede de novo, porque organização é o que mantém a calma nas aulas do Zanin!
    rede, falhas_por_no, horas_por_no, consumidores_por_no = organizar_dados(dados)

    # Agora, a mágica: acumulando FEC e DIC, igual a ansiedade antes da entrega de um projeto!
    fec_cache = {}
    dic_cache = {}
    fec_por_no = {}
    dic_por_no = {}

    for dado in dados:
        fec_por_no[dado.node_b] = calcular_fec_acumulado(dado.node_b, falhas_por_no, rede, fec_cache)
        dic_por_no[dado.node_b] = calcular_dic_acumulado(dado.node_b, horas_por_no, falhas_por_no, rede, dic_cache)

    # Vamos pro show final: DEC e FEC da linha inteira, ou como chamam, a média da turma, 0!
    dec_total, fec_total = calcular_dec_fec_total(dados)

    # Resultado, professor! Olha só como ficou bonito!
    print("FEC Acumulado por Nó (Node B):")
    for no, fec in fec_por_no.items():
        print(f"Nó {no}: {fec:.2f} falhas/ano")
    
    print("\nDIC Acumulado por Nó (Node B):")
    for no, dic in dic_por_no.items():
        print(f"Nó {no}: {dic:.2f} horas/ano")

    print(f"\nDEC Total da Linha: {dec_total:.2f} horas/ano por consumidor")
    print(f"FEC Total da Linha: {fec_total:.2f} falhas/ano por consumidor")

# Agora executa aí, Zanin, antes que o meu processador queime e o sistema caia e eu REPROVEEEEE! :)
if '__main__' == __name__:
    calcular_indicadores_de_arquivo()
