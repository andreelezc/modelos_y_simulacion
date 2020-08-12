import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
from otros import chicuadrado
from otros.generadorMixto import metodo_mixto

marcas = []
Fx = []
fx = []
periodo = []
aleatorios = []


def calcular_marcas(cant_marcas, vector_marcas):
    """Calcula la amplitud de los intervalos

    de acuerdo a la cantidad de marcas de clase deseadas."""
    amplitud_int = 8 / cant_marcas
    inf = -4
    while inf <= 4:
        vector_marcas.append(inf)
        inf = inf + amplitud_int
    np.asarray(vector_marcas)
    #print("Cantidad de Marcas:", cant_marcas)
    print("Amplitud del Intervalo", round(amplitud_int, 2), "\n")


def calcular_fx(vector_marcas, vector_fx):
    """Calcula la funcion de densidad de probabilidad

    segun la distribución Normal (0,1) por defecto"""
    for item in vector_marcas:
        vector_fx.append(norm.pdf(item))  # para cambiar mu y sigma agregar parametros loc=mu, scale=sigma
    np.asarray(vector_fx)


def calcular_Fx(vector_fx, vector_Fx):
    """Calcula la funcion de probabilidad acumulada

    segun la distribución Normal (0,1) por defecto"""
    # for item in vector_marcas:
    #     vector_Fx.append(norm.cdf(item))  # para cambiar mu y sigma agregar parametros loc=mu, scale=sigma
    acum = 0
    for item in vector_fx:
        acum = acum + item
        vector_Fx.append(round(acum, 4))
    np.asarray(vector_Fx)


def generar_random(v_semilla, cant_dias, vector_random):
    """
    Genera un número aleatorio partiendo desde la semilla.
    :param v_semilla: valor desde donde parte el algoritmo.
    :param cant_dias: longitud del vector de numeros aleatorios (debe ser igual a la cantidad de dias simulados)
    :param vector_random: vector donde guarda los numeros aleatorios
    :return: numero aleatorio entre 0 y 1
    """
    random.seed(v_semilla)
    for i in range(cant_dias):
        vector_random.append(round(random.random(), 4))


def buscar_intervalo(valor_semilla, cant_dias, vector_marcas, vector_Fx):
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

        valor_semilla = valor_semilla + vector_marcas[c]  # Obtener nuevo valor inicial

        print("\tmarca", "{0:.2f}".format(vector_marcas[c]))
        print("\tsemilla", "{0:.2f}".format(valor_semilla))
        periodo.append(round(valor_semilla, 2))  # Agregar nuevo valor al vector de muestra aleatoria
        print("\tincremento: {0:.2f}".format(marcas[c]))
        a = a + 1

    np.asarray(periodo)


def imprimir(vector_marcas, vector_fx, vector_Fx):
    print("Marcas", end="")
    for i in range(len(vector_marcas)):
        print('\t{:5}'.format(np.round((vector_marcas[i]), 2)), end=" ")
    print("\n f(x)", end="")
    for i in range(len(vector_fx)):
        print('\t{:5}'.format(np.round((vector_fx[i]), 4)), end=" ")
    print("\n F(x)", end="")
    for i in range(len(vector_Fx)):
        print('\t{:5}'.format(np.round((vector_Fx[i]), 4)), end=" ")
    print("\n")


def graficar_funciones(vector_marcas, vector_fx, vector_Fx):  #  usando vectores
    plt.title('Distribución Normal')

    x = np.linspace(min(vector_marcas), max(vector_marcas), len(vector_marcas))
    y_pdf = vector_fx
    y_cdf = vector_Fx

    plt.plot(x, y_pdf, label='f (x)', color='orange', lw=2)
    plt.plot(x, y_cdf, label='F (x)', color='blue', lw=2)

    plt.minorticks_on()

    plt.xlabel('x')
    plt.ylabel('y')

    plt.legend()
    plt.show()


def graficar_normal(x_range, mu=0, sigma=1, **kwargs): #sin usar vectores
    """
    Grafica la función de distribución normal para un rango de x dado.
    Si mu y sigma no se especifican, grafica la distribución normal estandar.
    Se le pueden pasar otros kwargs como grosor de linea, transparencia, etc.
    """
    x = x_range
    y1 = norm.pdf(x, mu, sigma)
    y2 = norm.cdf(x, mu, sigma)
    plt.plot(x, y1, label='f (x)', color='orange', **kwargs)
    plt.plot(x, y2, label='F (x)', color='green', **kwargs)

    plt.title('Distribución Normal')
    plt.xlabel('Variable Aleatoria X')
    plt.minorticks_on()
    plt.legend()
    plt.show()


def main():
    print('{:_^78}'.format(" DISTRIBUCIÓN NORMAL "))
    num_marcas = (int(input("Cantidad de marcas:")))

    calcular_marcas(num_marcas, marcas)
    calcular_fx(marcas, fx)
    calcular_Fx(fx, Fx)
    imprimir(marcas, fx, Fx)

    dias = (int(input("Cantidad de días a simular:")))
    semilla = (int(input("Valor de la semilla:")))
    metodo_mixto(dias, semilla, 11, 13, 64, aleatorios)
    print("\nVALORES ALEATORIOS", aleatorios)
    chicuadrado.test_chi(aleatorios)

    # generar_random(semilla,dias, aleatorios)
    # metodo_mult(cant_dias, valor_semilla, 11, 64, aleatorios)
    # metodo_mixto(cant_dias, valor_semilla, 11, 13, 64, aleatorios)

    buscar_intervalo(semilla, dias, marcas, Fx)

    print('{:_^78}'.format(""))
    print("CANTIDAD DE DÍAS", dias, "\n"
                                    "VALORES DIARIOS ", periodo)

    x = np.linspace(-4, 4, 50)
    graficar_normal(x, lw=2)


if __name__ == "__main__":  # solo se ejecuta cuando no es llamado via 'import'
    main()
