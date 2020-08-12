import matplotlib.pyplot as plt
import numpy as np


class GraficarSim:
    def __init__(self, calculo_simulacion, figura):
        self.llegadas = calculo_simulacion.llegadas
        self.permanencias = calculo_simulacion.permanencias
        self.espera_prom_cola = calculo_simulacion.espera_prom_cola
        self.figura = figura

    def graficar_sim(self):
        plt.style.use('seaborn-whitegrid')
        f1 = self.figura.add_subplot(111)

        # definir ancho de barra
        barWidth = 0.15

        # definir alto de barra
        bars1 = self.llegadas
        bars2 = self.permanencias
        bars3 = self.espera_prom_cola

        # Establecer posicion de barra en el eje X
        r1 = np.arange(len(bars1))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        # Crear el grafico
        f1.bar(r1, bars1, color='blue', width=barWidth, edgecolor='white', label='Media de Llegadas')
        f1.bar(r2, bars2, color='skyblue', width=barWidth, edgecolor='white', label='Media de Permanencia')
        f1.bar(r3, bars3, color='seagreen', width=barWidth, edgecolor='white', label='Media de Espera')

        # Agregar marcas en la mitad del grupo de barras
        f1.set_xlabel('Experimentos')
        f1.set_ylabel('Tiempo')
        f1.set_xticks([r + barWidth for r in range(len(bars1))])
        f1.set_xticklabels([str(i + 1) for i in range(len(bars1))])

        f1.legend()


class GraficosExp:
    def __init__(self, calculo_experimento, figura):
        self.llegadas_exp = calculo_experimento.llegadas
        self.esperas_exp = calculo_experimento.esperas
        self.perm_exp = calculo_experimento.permanencias
        self.figura = figura

    def graficar_exp(self):
        plt.style.use('seaborn-whitegrid')
        f1 = self.figura.add_subplot(111)

        # definir ancho de barra
        barWidth = 0.15

        # definir alto de barra
        bars1 = self.llegadas_exp
        bars2 = self.perm_exp
        bars3 = self.esperas_exp

        # Establecer posicion de barra en el eje X
        r1 = np.arange(len(bars1))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        # Crear el grafico
        f1.bar(r1, bars1, color='red', width=barWidth, edgecolor='white', label='Media de Llegada')
        f1.bar(r2, bars2, color='tomato', width=barWidth, edgecolor='white', label='Media de Permanencia')
        f1.bar(r3, bars3, color='lightsalmon', width=barWidth, edgecolor='white', label='Media de Espera')

        # Agregar marcas en la mitad del grupo de barras
        f1.set_xlabel('Corridas')
        f1.set_ylabel('Tiempo')
        f1.set_xticks([r + barWidth for r in range(len(bars1))])
        f1.set_xticklabels([str(i + 1) for i in range(len(bars1))])

        f1.legend()


class GraficosCorrida:
    def __init__(self, calculo_corrida, figura):
        self.llegadas = calculo_corrida.llegadas
        self.esperas = calculo_corrida.esperas
        self.atenciones = calculo_corrida.atenciones
        self.permanencias = calculo_corrida.permanencias
        self.figura = figura
        self.figura.suptitle('X: Usuarios; Y: Tiempo', fontweight='bold')

    def graficar_corrida(self):
        x1 = range(len(self.llegadas))
        y1 = self.llegadas

        x2 = range(len(self.esperas))
        y2 = self.esperas

        x3 = range(len(self.atenciones))
        y3 = self.atenciones

        x4 = range(len(self.permanencias))
        y4 = self.permanencias

        plt.style.use('seaborn-whitegrid')

        f1 = self.figura.add_subplot(221)
        f1.plot(x1, y1, color='red')
        f1.title.set_text('\nLlegadas')

        f2 = self.figura.add_subplot(222)
        f2.plot(x2, y2, color='green')
        f2.title.set_text('\nEsperas')

        f3 = self.figura.add_subplot(223)
        f3.plot(x3, y3, color='orange')
        f3.title.set_text('\nDuración de la Atención')

        f4 = self.figura.add_subplot(224)
        f4.plot(x4, y4, label='Permanencia', color='blue')
        f4.title.set_text('\nPemanencia')
