import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt
from otros import chicuadrado
from otros.generadorMixto import metodo_mixto

X = []
fx = []
Fx = []
aleatorios = []
periodo = []


def var_al(cant, v_mu):
    """

    Genera una muestra de n números aleatorios que provienen de una
    distribución de poisson con parámetros mu
    """

    for i in range(cant+1):
        #X.append(poisson.rvs(v_mu))
        X.append(i)
    np.asarray(X)
    # X.sort()


def calcular_fx(vector_x, vector_fx, v_mu):
    for item in vector_x:
        vector_fx.append(round(poisson.pmf(item, v_mu), 4))


def calcular_Fx(vector_fx, vector_Fx):
    # for item in vector_x:
    #     vector_Fx.append(round(poisson.cdf(item, v_mu), 3))
    acum = 0
    for item in vector_fx:
        acum = acum + item
        vector_Fx.append(acum)


def graficar_poi(x, v_mu):
    plt.ylabel('Probabilidad de que X ocurra')
    plt.xlabel('Variable Aleatoria X')
    plt.title('Distribución de Poisson')
    y1 = []
    y2 = []
    poi = poisson(v_mu)
    for num in range(0, x):
        y1.append(poi.pmf(num))  # Función de Masa de Probabilidad
    for num in range(0, x):
        y2.append(poi.cdf(num))  # Función de Probabilidad Acumulada

    # prob = poi.pmf(20)  # ejemplo de probabilidad puntual
    plt.grid(True)
    plt.minorticks_on()
    plt.plot(y1, lw=2.0, label="f (x)", color="blue")
    plt.plot(y2, lw=2.0, label="F (x)", color="orange")
    # plt.plot([20], [prob], marker='o', markersize=6, color="red")
    plt.legend()
    plt.show()


def imprimir(vector_x, vector_fx, vector_Fx):
    print("\r X", end="\t")
    for i in range(len(vector_x)):
        print('\t{:5}'.format(np.round((vector_x[i]), 2)), end=" ")
    print("\n f(x)", end="")
    for i in range(len(vector_fx)):
        print('\t{:5}'.format(np.round((vector_fx[i]), 4)), end=" ")
    print("\n F(x)", end="")
    for i in range(len(vector_Fx)):
        print('\t{:5}'.format(np.round((vector_Fx[i]), 4)), end=" ")
    print("\n")


def buscar_intervalo(valor_semilla, cant_dias, vector_x, vector_Fx):
    a = 0
    for i in range(0, cant_dias):
        c = 0

        print('{:_^30}'.format(""))
        print("Dia", i+1)
        print("Semilla:", "{0:.2f}".format(valor_semilla))
        print("Valor aleatorio: ", aleatorios[a])

        while c < len(vector_Fx) and aleatorios[a] > vector_Fx[c]:  # Buscar intervalo al que pertenece el numero aleatorio
            c = c + 1  # Avanzar en el vector

        if c == len(vector_Fx):
            c = c - 1

        valor_semilla = valor_semilla + vector_x[c]  # Obtener nuevo valor inicial

        print("\tX:", "{0:.2f}".format(vector_x[c]))
        print("\tsemilla:", "{0:.2f}".format(valor_semilla))
        periodo.append(round(valor_semilla, 2))  # Agregar nuevo valor al vector de muestra aleatoria
        print("\tincremento: {0:.2f}".format(vector_x[c]))
        a = a + 1

    np.asarray(periodo)


def main():
    print('{:_^78}'.format(" DISTRIBUCIÓN DE POISSON "))
    n = (int(input("Cantidad de variables aleatorias deseadas:")))
    mu = (float(input("Valor de mu:")))
    var_al(n, mu)
    calcular_fx(X, fx, mu)
    calcular_Fx(fx, Fx)
    imprimir(X, fx, Fx)

    dias = (int(input("Cantidad de días a simular:")))
    semilla = (int(input("Valor de la semilla:")))

    metodo_mixto(dias, semilla, 11, 13, 64, aleatorios)
    print("VALORES ALEATORIOS:", aleatorios)
    chicuadrado.test_chi(aleatorios)

    buscar_intervalo(semilla, dias, X, Fx)

    print('{:_^78}'.format(""), "\n")
    print("CANTIDAD DE DÍAS EVALUADOS:", dias, "\n"
                                    "VALORES DIARIOS OBTENIDOS: ", periodo)

    graficar_poi(50, mu)


if __name__ == "__main__":  # solo se ejecuta cuando no es llamado via 'import'
    main()
