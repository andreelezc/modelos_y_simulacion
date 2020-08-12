import numpy as np
from otros import chicuadrado
from scipy.stats import poisson
from otros.generadorMixto import metodo_mixto
from prettytable import PrettyTable
from termcolor import colored, cprint
import matplotlib.pyplot as plt


demora_prov_a = [0, 1, 2, 3, 4, 5]
demoraPx_prov_a = [0.10, 0.02, 0.08, 0.15, 0.14, 0.01]
demoraFx_prov_a = []

demora_prov_b = [0, 1, 2, 3, 4, 5, 6, 7]
demoraPx_prov_b = [0.52, 0.16, 0.12, 0.05, 0.06, 0.03, 0.025, 0.035]
demoraFx_prov_b = []

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

v_total_prov_a = []
v_total_prov_b = []


def calcular_demoraFx(v_px, v_Fx):
    acum = 0
    for i in range(len(v_px)):
        v_Fx.append(acum + v_px[i])
        acum = v_Fx[i]
    np.asarray(v_Fx)


def calcular_demanda(dem, v_mu):
    for i in range(0, dias-1):
        dem.append(poisson.rvs(v_mu))
    np.asarray(dem)


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
    for i in range(len(v_Fx)):
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
    r.add_column("Proveedor A", v_total_prov_a)
    r.add_column("Proveedor B", v_total_prov_b)
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
    cprint('{:*^105}'.format(" DESEMPEÑO DEL NEGOCIO "), "cyan", attrs=['bold'])
    print('El 10% del total de ventas es: {0:.2f}'.format((10*tv)/100))
    print('El 5% del total de ventas es: {0:.2f}'.format((5*tv)/100))
    print("El porcentaje de pérdidas respecto al total de ventas es:", round((tp*100)/(tp + tv), 2), "%")
    cprint("\nCONCLUSIÓN:", "cyan", attrs=['bold'], end=" ")
    if tp > ((10*tv)/100):
        print("El stock inicial debería incrementarse, ya que las pérdidas fueron superiores al 10% de ventas")
    else:
        if tp < ((5*tv)/100):
            print("Podria reducirse la existencia inicial, ya que las pérdidas fueron menores al 5% de las ventas")
        else:
            print("El stock se puede mantener. Las pérdidas están entre el 5% y el 10% de las ventas.")
    cprint('\n{:*^105}'.format(""), "cyan", attrs=['bold'])


def diamax(vector):
    for i in range(0, len(vector)):
        if vector[i] == max(vector):
            return i


def graficar(x_range, **kwargs):  # sin usar vectores
    """
    Grafica ventas y perdidas.
    """
    x = x_range
    y1 = ventas
    y2 = dins
    plt.plot(x, y1, label='Ventas', color='green', **kwargs)
    plt.plot(x, y2, label='Pérdidas', color='red', **kwargs)

    plt.title('Ventas y Pérdidas Anuales')
    plt.xlabel('Días')
    plt.minorticks_on()

    x_vta_max = diamax(ventas)
    x_p_max = diamax(dins)
    plt.plot(v_dias[x_vta_max], max(ventas), marker='o', markersize=5, color="red", label='Venta Máx')
    plt.plot(v_dias[x_p_max], max(dins), marker='o', markersize=5, color="blue", label='Pérdida Máx')

    plt.legend()
    plt.show()


def graficar_total_prov(numcorridas):
    """
    Grafica el total de pedidos vendidos por cada proveedor
    por corrida.
    :param numcorridas: cantidad de simulaciones/corridas realizadas.
    """

    # data to plot
    n_groups = sim
    prov_a = v_total_prov_a
    prov_b = v_total_prov_b

    # create plot
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8

    nombres = []
    for i in range(1, numcorridas):
        nombres.append(i)

    plt.xlabel('Simulación')
    plt.ylabel('Cantidad de Pedidos')
    plt.title('Pedidos por Proveedores')
    plt.legend()
    plt.xticks()
    plt.tight_layout()
    plt.show()


def inicio(p_dias):
    corridas = 1

    for i in range(0, sim):
        v_total_per.append(0)
        v_total_vtas.append(0)
        v_mayorVenta.append(0)
        v_menorVenta.append(0)
        v_total_prov_a.append(0)
        v_total_prov_b.append(0)

    calcular_demoraFx(demoraPx_prov_a, demoraFx_prov_a)
    calcular_demoraFx(demoraPx_prov_b, demoraFx_prov_b)

    print('\nPROVEEDOR A')
    imprimir_demora(demora_prov_a, demoraPx_prov_a, demoraFx_prov_a)
    print('PROVEEDOR B')
    imprimir_demora(demora_prov_b, demoraPx_prov_b, demoraFx_prov_b)

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
        cont1, acum1 = 0, 0
        cont2, acum2 = 0, 0
        prov = []
        for i in range(0, dias - 1):
            dd = buscar_prob(demoraFx_prov_a, aleatorios[i])
            if dd is None:
                dd = buscar_prob(demoraFx_prov_b, aleatorios[i])
                cont2 = cont2 + 1
                prov.append('B')
            else:
                cont1 = cont1 + 1
                prov.append('A')
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
                stock_ini = stock_ini - ventas[i] + reposicion[i + 1] + 3

            stock_fin[i] = (stock[i] - ventas[i])

            if stock_fin[i] <= stock[i]:
                pedido.append(ventas[i])
                if diasdemo[i] + 1 < dias - 1:
                    dia_rep[i] = diasdemo[i] + 1
                if i + dia_rep[i] < dias - 1:
                    reposicion[i + dia_rep[i]] = pedido[i]
            else:
                pedido.append(0)

            if prov[i] == 'A':
                acum1 = acum1 + pedido[i]
            elif prov[i] == 'B':
                acum2 = acum2 + pedido[i]

        crear_tabla()
        print("Total Pérdidas:", total_perdidas)
        print("Total Ventas:", total_ventas)
        print("\nMayor Venta:", max(ventas))
        print("Menor Venta:", min(ventas))

        prom_a = round(acum1/sum(pedido), 2)
        prom_b = round(acum2/sum(pedido), 2)
        print("\nPedidos Proveedor A:", acum1, '{:>13}'.format("Promedio:"), prom_a)
        print("Pedidos Proveedor B:", acum2, '{:>13}'.format("Promedio:"), prom_b)

        informe(total_perdidas, total_ventas)

        x = np.linspace(min(v_dias), max(v_dias), dias - 1)
        graficar(x, lw=2)

        v_total_per[corridas-1] = total_perdidas
        v_total_vtas[corridas-1] = sum(ventas)
        v_mayorVenta[corridas-1] = max(ventas)
        v_menorVenta[corridas-1] = min(ventas)

        v_total_prov_a[corridas - 1] = acum1
        v_total_prov_b[corridas - 1] = acum2

        eliminar_vectores()
        corridas = corridas + 1

    tabla_resumen()
    graficar_total_prov(corridas)


###################################################################


cprint('{: ^105}'.format(" PRIMER PARCIAL MODELOS Y SIMULACIÓN "), 'blue', attrs=['bold', 'underline'], end="\n")
print('{: ^105}'.format(" SIMULADOR MODELO DE INVENTARIO "), end="\n")

sim = (int(input("Ingrese la cantidad de corridas: ")))
dias = (int(input("Ingrese la cantidad de días: ")))
dias = dias + 1
mu = (int(input("Valor de lambda (λ): ")))
v_dias = []
for i in range(1, dias):
    v_dias.append(i)
inicio(dias)
