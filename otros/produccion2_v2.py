import random
import numpy as np


def calcular_aleatorios(cant):
    num_aleatorios = []
    for i in range(cant):
        r = round(random.uniform(0.5, 3.5), 2)
        num_aleatorios.append(r)
    num_aleatorios.sort()
    return num_aleatorios


# def calcular_aleatorios(cant):
#     num_aleatorios = np.around(np.random.uniform(low=0.5, high=3.5, size=cant), 2)
#     num_aleatorios.sort()
#     return num_aleatorios


def contar_menores(v_aleatorios):
    cont = 0
    for item in v_aleatorios:
        if item < 1.5:
            cont = cont + 1
    return cont


def imprimir_vectores(v_aleatorios):
    print("\nComputadora", end="")
    for i in range(1, n+1):
        print('{:5}'.format(i), end=" ")
    print("\nDuración", end="\t")
    for item in v_aleatorios:
        print('{:5}'.format(item), end=" ")
    print("\n")


n = (int(input("Cantidad de computadoras:")))
comp = []
if n > 0:
    aleatorios = calcular_aleatorios(n)
    imprimir_vectores(aleatorios)
    menores = contar_menores(aleatorios)
    porc = menores * 100 / n
    print("\nCantidad de computadoras con duracion menor a 1.5 hs: ", menores)
    print("\nPorcentaje que representa: ", round(porc, 2), "%")
    if porc > (15*n)/100:
        print("\nMás del 15% de las baterias actuales dura menos de 1,5 hs. La investigacion puede continuar.")
    elif porc < (15*n)/100:
        print("\nMenos del 15% de las baterias actuales dura menos de 1,5 hs. La investigacion no puede continuar.")
    else:
        print("\nLa cantidad de baterias actuales no supera el 15%. La investigacion no puede continuar")
else:
    print("Introduzca un número correcto")
