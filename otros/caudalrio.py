from random import random
import matplotlib.pyplot as plt
import numpy as np


marcas = [-30, -20, -10, 0, 10, 20, 30]  # Marcas de Clase
Fx = [0.0543, 0.2067, 0.5189, 0.6433, 0.6758, 0.8580, 1]  # Valores de F(X)
QDI = []  # valores diarios del caudal


def caudalmedio(qdi):  # Calcular caudal medio del rio durante un año
    sum = 0.0
    for item in qdi:
        sum = sum + item
    return sum / len(qdi)


def contar_csu(qdi, limite_sup):  # Contar cuantos dias el caudal fue mayor al limite superior
    c2 = 0  # contador para buscar CSU
    for item in qdi:
        if item > limite_sup:
            c2 = c2 + 1
    return c2


def buscar_csu(qdi, limite_sup):  # Buscar cuales fueron los dias en los que el caudal fue mayor al limite CSU
    for i in range(len(qdi)):
        if qdi[i] > limite_sup:
            print(" *  Caudal del dia ", i + 1, ": ", qdi[i])


def contar_cin(qdi, limite_sup):  # Contar cuantos dias el caudal fue menor al limite inferior
    c3 = 0  # contador para buscar CIN
    for item in qdi:
        if item < limite_sup:
            c3 = c3 + 1
    return c3


def buscar_cin(qdi, limite_sup):  # Buscar cuales fueron los dias en los que el caudal fue menor al limite CIN
    for i in range(0, len(QDI)):
        if (qdi[i] < limite_sup):
            print(" *  Caudal del dia ", i + 1, ": ", qdi[i])


def buscar_intervalo(valor_semilla, cant_dias, vector_Fx, vector_marcas):
    for i in range(0, cant_dias):
        c = 0
        valor_aleatorio = round(aleatorio(), 4)  # Generar valor aleatorio
        # aca aplicar test_chi_2

        print('{:_^30}'.format(""))
        print("Dia", i+1)
        print("Semilla: {0:.2f}".format(valor_semilla))
        print("Valor aleatorio: ", valor_aleatorio)

        while valor_aleatorio > vector_Fx[c]:  # Buscar intervalo al que pertenece el numero aleatorio
            c = c + 1  # Avanzar en el vector

        valor_semilla = valor_semilla + vector_marcas[c]  # Obtener nuevo valor inicial

        print("\tmarca", "{0:.2f}".format(vector_marcas[c]))
        print("\tsemilla", "{0:.2f}".format(valor_semilla))
        QDI.append(round(valor_semilla, 2))  # Agregar nuevo valor al vector de muestra aleatoria
        print("\tincremento del día: {0:.2f}".format(vector_marcas[c]))

def imprimir(vector_marcas, vector_Fx):
    print("\nMarcas", end="")
    for i in range(len(vector_marcas)):
        print('\t{:5}'.format(vector_marcas[i]), end=" ")
    print("\n F(x)", end="")
    for i in range(len(vector_Fx)):
        print('\t{:5}'.format(vector_Fx[i]), end=" ")
    print("\n")


def graficar_caudal(x_range, vector_qdi, **kwargs):
    x = x_range
    y = vector_qdi

    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, label='F (x)', color='orange', **kwargs)

    plt.title('Valores diarios del caudal')
    plt.xlabel('Dias')
    plt.ylabel('F (x)')
    plt.minorticks_on()
    plt.legend()
    plt.show()




if __name__ == '__main__':
    print("********** EVALUACIÓN DEL CAUDAL DE UN RIO DURANTE EL PERIODO DE UN AÑO (365 DÍAS) **********\n")
    semilla = (int(input('Ingrese valor inicial: ')))  # Valor inicial
    dias = 15
    QDI.append(semilla)  # Agregar valor inicial al vector QDI
    caudal_sup = (int(input('Ingrese límite superior de caudal (CSU): ')))
    caudal_inf = (int(input('Ingrese límite inferior de caudal (CIN): ')))

    imprimir(marcas, Fx)
    buscar_intervalo(semilla, dias, Fx, marcas)

    print("\n--- QDI: Valores diarios del caudal ---", QDI)
    print("--- QSA: caudal máximo alcanzado ---", max(QDI))  # Buscar valor maximo en el vector QDI
    print("--- QIA: caudal mínimo alcanzado ---", min(QDI))  # Buscar valor minimo en el vector QDI
    print("--- TSQ: tiempo en el que el caudal fue superior a un determinado volumen dado CSU ---",
          contar_csu(QDI, caudal_sup), "dias")
    buscar_csu(QDI, caudal_sup)
    print("--- TIQ: tiempo en el que el caudal fue inferior a un determinado volumen dado CIN ---",
          contar_cin(QDI, caudal_inf), "dia(s)")
    buscar_cin(QDI, caudal_inf)

    prom = caudalmedio(QDI)
    print("--- QMS: caudal medio durante el periodo de simulación ---", prom)

    x = np.linspace(1, dias, dias+1)
    graficar_caudal(x, QDI, lw=2)
