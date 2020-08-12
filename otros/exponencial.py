import numpy as np
from scipy.stats import expon
import matplotlib.pyplot as plt
from otros import chicuadrado
from otros.generadorMixto import metodo_mixto

X = []
fx = []
Fx = []
aleatorios = []
periodo = []


def var_al(ini, n, a):
    """

    Genera una muestra de n números aleatorios que provienen de una
    distribución exponencial con parámetros mu = 0 y sigma = 1
    """

    for i in np.arange(ini, n+a, a):
        X.append(i)
    #X.sort()


def calcular_fx(vector_x, vector_fx):
    for item in vector_x:
        vector_fx.append(round(expon.pdf(item), 5))


def calcular_Fx(vector_fx, vector_Fx):
    # for item in vector_x:
    #     vector_Fx.append(round(expon.cdf(item), 3))
    acum = 0
    for item in vector_fx:
        acum = acum + item
        vector_Fx.append(round(acum, 4))

def graficar_exp(x_range, mu=0, sigma=1, **kwargs):  # sin usar vectores
    """
    Grafica la función de distribución exponencial para un rango de x dado.
    Si mu y sigma no se especifican, son 0 y 1.
    Se le pueden pasar otros kwargs como grosor de linea, transparencia, etc.
    """
    x = x_range
    y1 = expon.pdf(x, mu, sigma)
    y2 = expon.cdf(x, mu, sigma)
    plt.plot(x, y1, label='f (x)', color='orange', **kwargs)
    plt.plot(x, y2, label='F (x)', color='green', **kwargs)

    plt.title('Distribución Exponencial')
    plt.xlabel('Variable Aleatoria X')
    plt.ylabel('Probabilidad')
    plt.minorticks_on()
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
    print('{:_^78}'.format(" DISTRIBUCIÓN EXPONENCIAL "))
    n = (int(input("Cantidad de eventos a evaluar:")))
    a = (float(input("Amplitud del intervalo:")))
    ini = (float(input("Valor inicial:")))
    var_al(ini, n, a)
    calcular_fx(X, fx)
    calcular_Fx(fx, Fx)
    imprimir(X, fx, Fx)

    dias = (int(input("Cantidad de días a simular:")))
    semilla = (int(input("Valor de la semilla:")))
    metodo_mixto(dias, semilla, 11, 13, 1024, aleatorios)
    print("\nVALORES ALEATORIOS:", aleatorios)
    chicuadrado.test_chi(aleatorios)

    buscar_intervalo(semilla, dias, X, Fx)

    print('{:_^78}'.format(""), "\n")
    print("CANTIDAD DE DÍAS EVALUADOS:", dias, "\n"
                                    "VALORES DIARIOS OBTENIDOS: ", periodo)

    x = np.linspace(0, 10, 50)
    graficar_exp(x, lw=2)


if __name__ == "__main__":
    main()
