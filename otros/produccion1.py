import numpy as np
from scipy.stats import norm
from termcolor import colored, cprint
import matplotlib.pyplot as plt

g1 = {'Watts': 1000, 'Arranque': 15000, '$/KW': 23}
g2 = {'Watts': 1000, 'Arranque': 15000, '$/KW': 23}
g3 = {'Watts': 2000, 'Arranque': 21000, '$/KW': 18}
g4 = {'Watts': 2000, 'Arranque': 21000, '$/KW': 18}
g5 = {'Watts': 3000, 'Arranque': 26000, '$/KW': 14}

generadores = [g1, g2, g3, g4, g5]
costo_gral = []


def calcular_consumo(media, desvio, cant):
    cons = np.round(norm.rvs(loc=media, scale=desvio, size=cant), 2)
    cons.sort()
    np.asarray(cons)
    return cons


def buscar_mayor(v_gen, num):
    for i in range(len(v_gen)):
        if v_gen[i]['Watts'] > num:
            return i
    return len(v_gen)-1


def buscar(v_gen, num):
    gens = v_gen.copy()
    r_gens = []
    x = num
    while x >= 0 and len(gens) > 0:
        gi = buscar_mayor(gens, x)
        x = x - gens[gi]['Watts']
        r_gens.append(gens[gi])
        del gens[gi]
    return r_gens


def graficar(x_range, **kwargs):  # sin usar vectores
    """
    Grafica costos totales por corrida.
    """
    x = x_range
    y1 = costo_gral
    plt.plot(x, y1, label='Costos Totales', color='red', **kwargs)

    plt.title('Costos Anuales')
    plt.xlabel('Días')
    plt.minorticks_on()

    plt.legend()
    plt.show()


def inicio(media, desviacion, dias):
    corridas = 1
    while corridas <= sim:
        print('{: ^34}'.format(""))
        cprint("ITERACIÓN NÚMERO:", 'blue', attrs=['bold', 'underline'], end=""), cprint(corridas, 'blue', attrs=['bold', 'underline'])
        consumo = calcular_consumo(media, desviacion, dias)

        for i in range(1, n):
            costo_unit_total = 0
            costo_arr_total = 0
            costo_total = 0
            cprint("\nDía:", 'green', attrs=['bold'], end=''), cprint(i, 'green', attrs=['bold'])
            print("Consumo:", consumo[i])
            encender = buscar(generadores, consumo[i])
            print("Generadores:", encender)
            for gen in encender:
                costo_arr_total = costo_arr_total + gen['Arranque']
                costo_unit_total = costo_unit_total + gen['Watts'] * gen['$/KW']
                costo_total = costo_arr_total + costo_unit_total
            print(" - Costo de Arranque Total: $", costo_arr_total)
            print(" - Costo Unitario Total: $", costo_unit_total)
            print(" - Costo Total: $", costo_total)
            costo_gral.append(costo_total)

        x = np.linspace(0, n, n-1)
        graficar(x, lw=2)
        del costo_gral[:]
        corridas = corridas + 1


####################################################################################################################

print(colored('{:_^105}'.format(" SIMULADOR DE SISTEMA DE PRODUCCIÓN ", end="\n"), "blue", attrs=['bold', 'underline']))

sim = (int(input("Ingrese la cantidad de corridas: ")))
n = (int(input("Cantidad de días:")))
n = n + 1

mu = (int(input("Media:")))
sigma = (int(input("Desviación:")))
inicio(mu, sigma, n)
