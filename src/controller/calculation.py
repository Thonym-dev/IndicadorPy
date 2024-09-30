from ..model.devices import Dispositivo
from src.view.main_view import View

class Controller:
    def __init__(self):
        self.rede = Rede()
        self.view = View()

    def adicionar_dispositivos_e_linhas(self):
        # Exemplo de adição de dispositivos e linhas
        dispositivo_1 = Dispositivo("Transformador", taxa_falha=0.1, tempo_reparo=2, interrupcoes_momentaneas=1)
        dispositivo_2 = Dispositivo("Chave Seccionadora", taxa_falha=0.05, tempo_reparo=1, interrupcoes_momentaneas=0.5)
        
        linha_1 = Linha("Linha 1", comprimento=5, dispositivos=[dispositivo_1, dispositivo_2])
        
        self.rede.adicionar_linha(linha_1)

    def calcular_e_exibir_indicadores(self):
        # Realizar os cálculos
        saidi = self.rede.calcular_saidi()
        saifi = self.rede.calcular_saifi()
        maifi = self.rede.calcular_maifi()

        # Atualizar a view com os resultados
        self.view.exibir_resultados(saidi, saifi, maifi)
k
# Executar o fluxo
if __name__ == "__main__":
    controller = Controller()
    controller.adicionar_dispositivos_e_linhas()
    controller.calcular_e_exibir_indicadores()