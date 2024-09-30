class Dispositivo:
    def __init__(self, nome, taxa_falha, tempo_reparo, interrupcoes_momentaneas=0):
        self.nome = nome
        self.taxa_falha = taxa_falha
        self.tempo_reparo = tempo_reparo
        self.interrupcoes_momentaneas = interrupcoes_momentaneas

class Linha:
    def __init__(self, nome, comprimento, dispositivos=[]):
        self.nome = nome
        self.comprimento = comprimento
        self.dispositivos = dispositivos

class Rede:
    def __init__(self):
        self.linhas = []

    def adicionar_linha(self, linha):
        self.linhas.append(linha)

    def calcular_saidi(self):
        saidi_total = 0
        for linha in self.linhas:
            for dispositivo in linha.dispositivos:
                saidi_total += dispositivo.taxa_falha * dispositivo.tempo_reparo
        return saidi_total

    def calcular_saifi(self):
        saifi_total = 0
        for linha in self.linhas:
            for dispositivo in linha.dispositivos:
                saifi_total += dispositivo.taxa_falha
        return saifi_total

    def calcular_maifi(self):
        maifi_total = 0
        for linha in self.linhas:
            for dispositivo in linha.dispositivos:
                maifi_total += dispositivo.interrupcoes_momentaneas
        return maifi_total