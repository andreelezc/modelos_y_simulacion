import numpy as np
from otros import chicuadrado
from scipy.stats import poisson
from otros.generadorMixto import metodo_mixto
from prettytable import PrettyTable
from termcolor import colored, cprint

demoraX = [1, 2, 3, 4, 5]
demoraPx = [0.26, 0.32, 0.22, 0.14, 0.06]
demoraFx = []

demanda = []
aleatorios = []

ventas = []
dins = []
pedido = []
stock = []
stock_fin = []
reposicion = []
diasdemo = []
dia_rep = []

v_total_per = []
v_total_vtas = []
v_mayorVenta = []
v_menorVenta = []


def calcular_demoraFx(v_px, v_Fx):
    acum = 0
    for i in range(len(v_px)):
        v_Fx.append(acum + v_px[i])
        acum = v_Fx[i]
    np.asarray(v_Fx)


def calcular_demanda(dem, v_mu):
    for i in range(1, dias):
        dem.append(poisson.rvs(v_mu))
    np.asarray(demanda)


def imprimir_demora(vector_demora, vector_px, vector_Fx):
    print("\rDemora", end="")
    for item in vector_demora:
        print('{:5}'.format(np.round(item, 2)), end=" ")
    print("\np(x)", end="\t")
    for item in vector_px:
        print('{:5}'.format(np.round(item, 4)), end=" ")
    print("\nF(x)", end="\t")
    for item in vector_Fx:
        print('{:5}'.format(np.round(item, 4)), end=" ")
    print("\n")


def buscar_prob(v_Fx, num):
    for i in range(1, len(v_Fx)):
        if v_Fx[i] > num:
            return i
    return None


def iniciar_repo(v_repo, cant_dias):
    for i in range(0, cant_dias - 1):
        v_repo.append(0)


def iniciar_dia_rep(v_dia_rep, cant_dias):
    for i in range(0, cant_dias - 1):
        v_dia_rep.append(0)


def crear_tabla():
    t = PrettyTable()
    t.add_column('Días', v_dias)
    t.add_column('Stock Inicial', stock)
    t.add_column('Demanda', demanda)
    t.add_column('Venta', ventas)
    t.add_column('Insatisfecho', dins)
    t.add_column('Pedido', pedido)
    t.add_column('Demora + 1', dia_rep)
    t.add_column('Reposicion', reposicion)
    t.add_column('Stock Final', stock_fin)
    print(t)


def tabla_resumen():
    r = PrettyTable()
    cant_sim = []
    for i in range(1, sim+1):
        cant_sim.append(i)
    r.add_column("Ejecución", cant_sim)
    r.add_column("Total Perdidas", v_total_per)
    r.add_column("Total Ventas", v_total_vtas)
    r.add_column("Mayor Venta", v_mayorVenta)
    r.add_column("Menor Venta", v_menorVenta)
    print(colored('{:_^105}'.format(" TABLA DE RESÚMENES ", end="\n"), "blue", attrs=['bold']))
    print(r)


def eliminar_vectores():
    del stock[:]
    del stock_fin[:]
    del ventas[:]
    del pedido[:]
    del aleatorios[:]
    del dins[:]
    del diasdemo[:]
    del dia_rep[:]
    del demanda[:]
    del reposicion[:]


def informe(tp, tv):
    print('El 8% del total de ventas es: {0:.2f}'.format((8*tv)/100))
    print('El 2% del total de ventas es: {0:.2f}'.format((2*tv)/100))
    if tp > ((10*tv)/100):
        print("La Existencia inicial deberia incrementarse, ya que la perdida por agotamiento de existencia fue superior al 8% de ventas")
    else:
        if tp < ((2*tv)/100):
            print("Podria reducirse la existencia inicial, ya que la perdida por agotamiento de existencias es menor al 2%")
        else:
            print("La perdida con respecto a las ventas se encuentra entre el 2% y 8%. El experimento pudo haberse detenido")


def inicio(p_dias):
    corridas = 1

    for i in range(0, sim):
        v_total_per.append(0)
        v_total_vtas.append(0)
        v_mayorVenta.append(0)
        v_menorVenta.append(0)

    calcular_demoraFx(demoraPx, demoraFx)

    print('\nTABLA DE DEMORA')
    imprimir_demora(demoraX, demoraPx, demoraFx)

    while corridas <= sim:
        print('{: ^34}'.format(""))
        cprint("ITERACIÓN NÚMERO:", 'blue', attrs=['bold', 'underline'], end=""), cprint(corridas, 'blue', attrs=['bold', 'underline'])
        print("\nMÉTODO MIXTO DE CONGRUENCIAS")
        semilla = (int(input("Semilla: ")))
        p1 = (int(input("a:")))
        p2 = (int(input("c:")))
        modulo = (int(input("Módulo:")))
        print("")
        stock_ini = (int(input("STOCK INICIAL:")))
        metodo_mixto(p_dias, semilla, p1, p2, modulo, aleatorios)
        chicuadrado.test_chi(aleatorios)
        for item in aleatorios:
            dd = buscar_prob(demoraFx, item)
            diasdemo.append(dd)

        calcular_demanda(demanda, mu)
        iniciar_repo(reposicion, dias)
        iniciar_dia_rep(dia_rep, dias)

        # calculos
        total_perdidas = 0
        total_ventas = 0

        for i in range(0, dias - 1):
            stock.append(stock_ini)
            stock_fin.append(0)

            if demanda[i] <= stock_ini:
                ventas.append(demanda[i])
                dins.append(0)
            else:
                ventas.append(stock_ini)
                dins.append(demanda[i] - stock_ini)

            total_perdidas = total_perdidas + dins[i]
            total_ventas = total_ventas + ventas[i]

            if i + 1 < dias - 1:
                stock_ini = stock_ini - ventas[i] + reposicion[i + 1]
                stock_fin[i] = (stock[i] - ventas[i])
            if stock_fin[i] <= stock[i]:
                pedido.append(ventas[i])
                if diasdemo[i] + 1 < dias - 1:
                    dia_rep[i] = diasdemo[i] + 1
                if i + dia_rep[i] < dias - 1:
                    reposicion[i + dia_rep[i]] = pedido[i]
            else:
                pedido.append(0)

        crear_tabla()
        print("Total Pérdidas:", total_perdidas)
        print("Total Ventas:", total_ventas)
        print("Mayor Venta:", max(ventas))
        print("Menor Venta:", min(ventas))

        v_total_per[corridas-1] = total_perdidas
        v_total_vtas[corridas-1] = sum(ventas)
        v_mayorVenta[corridas-1] = max(ventas)
        v_menorVenta[corridas-1] = min(ventas)
        eliminar_vectores()
        corridas = corridas + 1

    tabla_resumen()
1

###################################################################

cprint('{:_^105}'.format(" SIMULADOR MODELO DE INVENTARIO "), 'blue', attrs=['bold'], end="\n")

sim = (int(input("Ingrese la cantidad de simulaciones: ")))
dias = (int(input("Ingrese la cantidad de días de simulación: ")))
dias = dias + 1
mu = (int(input("Valor de lambda (λ): ")))
v_dias = []
for i in range(1, dias):
    v_dias.append(i)
inicio(dias)

