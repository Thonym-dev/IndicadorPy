
class View:
    def exibir_resultados(self, saidi, saifi, maifi):
        print(f"SAIDI: {saidi:.2f} horas/consumidor")
        print(f"SAIFI: {saifi:.2f} interrupções/consumidor")
        print(f"MAIFI: {maifi:.2f} interrupções momentâneas/consumidor")
