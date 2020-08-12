import random
import math
import simpy
import matplotlib.pyplot as plt
import numpy as np
from termcolor import colored, cprint
from prettytable import PrettyTable


te = 0.0  # tiempo de espera total
dt = 0.0  # duracion de servicio total
fin = 0.0  # minuto en el que finaliza
upi = 0.0  # uso promedio de la instalacion

NUM_PELUQUEROS = 1

# acumuladores por corrida
v_clientes = []
v_llegadas = []
v_tiempo_corte = []
v_salidas = []
v_tiempo_esp = []
v_tiempo_perm = []
v_ocio = []
v_tiempo_entre = []

# acumuladores por experimento
lpc_exp = []
tep_exp = []
upi_exp = []
ocio_exp = []
v_tot_serv = []
v_tot_perm = []
media_llegada = []
media_perm = []


# acumuladores por simulacion
total_serv = []
lpc_sim = []
perm_sim = []
ocio_sim = []
media_serv_sim = []
media_llegada_sim = []
media_perm_sim = []
media_ocio_sim = []


def cortar(cliente):
    global dt  # Para poder acceder a la variable dt declarada anteriormente
    r = random.random()  # Obtiene un numero aleatorio y lo guarda en r
    tiempo_corte = -T_SERVICIO * math.log(r)  # Distribucion exponencial
    v_tiempo_corte.append(round(tiempo_corte, 2))
    yield env.timeout(tiempo_corte)  # deja correr el tiempo n minutos
    print(r' \o/ Corte listo a %s en %.2f minutos' % (cliente, tiempo_corte))
    dt = dt + tiempo_corte  # Acumula los tiempos de uso de la instalacion


def cliente(env, name, personal):
    global te
    global fin
    llega = env.now  # Guarda el minuto de llegada del cliente
    v_llegadas.append(round(llega, 2))
    cprint("\n→", "green", attrs=['bold'], end=" "), print("%s llego a peluqueria en minuto %.2f" % (name, llega))
    with personal.request() as request:  # Espera su turno
        yield request  # Obtiene turno
        pasa = env.now  # Guarda el minuto cuado comienza a ser atendido
        espera = pasa - llega  # Calcula el tiempo que espero
        v_tiempo_esp.append(round(espera, 2))  # Guarda los tiempos de espera
        te = te + espera  # Acumula los tiempos de espera
        cprint("---", "red", attrs=['bold'], end=" "), print(
            "%s pasa con peluquero en minuto %.2f habiendo esperado %.2f minutos" % (name, pasa, espera))
        yield env.process(cortar(name))  # Invoca al proceso cortar
        deja = env.now  # Guarda el minuto en que termina el proceso cortar
        servicio = deja - pasa  # Calcula la duracion del servicio
        v_tiempo_perm.append(round(espera + servicio, 2))  # Guarda el tiempo de permanencia
        v_salidas.append(round(deja, 2))  # Guarda el min en que sale
        cprint("←", "blue", attrs=['bold'], end=" "), print("%s deja peluqueria en minuto %.2f" % (name, deja))
        fin = deja  # Conserva globalmente el ultimo minuto de la simulacion


def principal(env, personal):
    for i in range(TOT_CLIENTES):  # Para n clientes
        r = random.random()
        llegada = -T_LLEGADAS * math.log(r)  # Distribucion exponencial
        yield env.timeout(llegada)  # Deja transcurrir un tiempo entre uno y otro
        if i == 0:
            v_tiempo_entre.append(0)  # Guarda el tiempo entre llegadas (0 si es el primero)
            v_ocio.append(0)  # Guarda el tiempo de ocio del peluquero (0 si es el primero)
        else:
            v_tiempo_entre.append(round(llegada, 2))  # Guarda el tiempo entre llegadas
            v_ocio.append(0)  # CORREGIR! (averiguar como se calcula el ocio)
        i += 1
        env.process(cliente(env, 'Cliente %d' % i, personal))


def graficar_exp():
    # set width of bar
    barWidth = 0.25

    # set height of bar
    bars1 = media_llegada
    bars2 = media_perm
    bars3 = tep_exp

    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    # Make the plot
    plt.bar(r1, bars1, color='orange', width=barWidth, edgecolor='white', label='Llegada')
    plt.bar(r2, bars2, color='red', width=barWidth, edgecolor='white', label='Permanencia')
    plt.bar(r3, bars3, color='green', width=barWidth, edgecolor='white', label='Espera')

    # Add xticks on the middle of the group bars
    plt.xlabel('Corridas', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars1))], [str(i+1) for i in range(len(bars1))])

    # Create legend & Show graphic
    plt.legend()
    plt.title('Medias por Experimento')
    plt.tight_layout()
    plt.show()


def tabla_resumen_corrida():
    r = PrettyTable()
    for i in range(1, TOT_CLIENTES + 1):
        v_clientes.append(i)
    r.add_column("Cliente Nº", v_clientes)
    r.add_column("Llegada", v_llegadas)
    r.add_column("Duración del Servicio", v_tiempo_corte)
    r.add_column("Tiempo de Espera", v_tiempo_esp)
    r.add_column("Salida", v_salidas)
    r.add_column("Permanencia", v_tiempo_perm)
    r.add_column("Tiempo Entre Llegadas", v_tiempo_entre)
    print(colored('{:_^145}'.format(" RESUMEN CORRIDA ", end="\n"), "blue", attrs=['bold']))
    print(r)


def tabla_resumen_exp():
    r = PrettyTable()
    cant_corr = []
    for i in range(1, corr + 1):
        cant_corr.append(i)
    r.add_column("Corrida Nº", cant_corr)
    r.add_column("Clientes en Cola", lpc_exp)
    r.add_column("Tiempo de Espera", tep_exp)
    r.add_column("Tiempo de Llegadas", media_llegada)
    r.add_column("Tiempo de Permanencia", media_perm)
    r.add_column("Porc. de Uso de la Instalacion", upi_exp)
    r.add_column("Porc. de Ocio", ocio_exp)
    print(colored('{:_^145}'.format(" PROMEDIOS POR EXPERIMENTO ", end="\n"), "blue", attrs=['bold']))
    print(r)


def tabla_resumen_sim():
    r = PrettyTable()
    cant_exp = []
    for i in range(1, exp + 1):
        cant_exp.append(i)
    r.add_column("Exp. Nº", cant_exp)
    r.add_column("Tiempo de Servicio", media_serv_sim)
    r.add_column("Tiempo de Llegadas", media_llegada_sim)
    # r.add_column("Tiempo en cola", lpc_sim)
    r.add_column("Permanencia en el Sistema", media_perm_sim)
    r.add_column("Tiempo de Ocio", media_ocio_sim)
    print(colored('{:_^145}'.format(" PROMEDIOS DE SIMULACIÓN ", end="\n"), "blue", attrs=['bold']))
    print(r)


def eliminar_vectores_corrida():
    del v_clientes[:]
    del v_llegadas[:]
    del v_tiempo_corte[:]
    del v_salidas[:]
    del v_tiempo_esp[:]
    del v_tiempo_perm[:]
    del v_tiempo_entre[:]
    del v_ocio[:]


def eliminar_vectores_exp():
    del lpc_exp[:]
    del tep_exp[:]
    del upi_exp[:]
    del media_llegada[:]
    del media_perm[:]
    del ocio_exp[:]


def eliminar_vectores_sim():
    del lpc_exp[:]
    del tep_exp[:]
    del upi_exp[:]
    del media_llegada[:]


def calcular_media(vector, res):
    acum = sum(vector)
    res.append(round(acum / len(vector), 2))


cprint('{: ^145}'.format(" ✂ SIMULADOR DE PELUQUERÍA ✂ "), 'blue', attrs=['bold'], end="\n")
sim = int(input("Cantidad de Simulaciones:"))
exp = int(input("Cantidad de Experimentos:"))
corr = int(input("Cantidad de Corridas:"))

simulaciones = 1
experimentos = 1
corridas = 1


while simulaciones <= sim:
    cprint('{: ^145}'.format("SIMULACIÓN Nº: {}".format(simulaciones)), "green", attrs=['bold', 'underline'])
    while experimentos <= exp:
        print("\r")
        cprint('{: ^145}'.format("EXPERIMENTO Nº: {}".format(experimentos)), "green", attrs=['bold'])
        T_LLEGADAS = (int(input("Tiempo Promedio entre Llegadas:")))  # varía por experimento (segun la consigna)
        print("\r")
        while corridas <= corr:
            cprint("CORRIDA Nº: {}".format(corridas), "green", attrs=['bold', 'underline'])
            SEMILLA = (int(input("Semilla:")))
            T_SERVICIO = (int(input("Tiempo Promedio de Servicio:")))
            # TIEMPO_SIMULACION = (int(input("Horas simuladas:")))  (se usa para trabajar por tiempo en vez de clientes)
            # TIEMPO_SIMULACION = TIEMPO_SIMULACION * 60
            TOT_CLIENTES = (int(input("Total de Clientes:")))

            random.seed(SEMILLA)  # Cualquier valor
            env = simpy.Environment()  # Crea el objeto entorno de simulacion
            personal = simpy.Resource(env, NUM_PELUQUEROS)  # Crea los recursos (peluqueros)
            env.process(principal(env, personal))  # Invoca el proceso principal
            env.run()  # Inicia la simulacion
            print("\r")
            tabla_resumen_corrida()

            # CALCULOS PARA TABLA CORRIDA
            lpc = te / fin  # longitud promedio de la cola
            tep = te / TOT_CLIENTES  # tiempo de espera promedio
            upi = (dt * 100) / fin  # porcentaje de uso de la instalacion
            media_lleg_corr = (sum(v_llegadas))/len(v_llegadas)
            media_perm_corr = (sum(v_tiempo_perm))/(len(v_tiempo_perm))
            media_esp_corr = (sum(v_tiempo_esp))/(len(v_tiempo_esp))

            # CALCULOS PARA TABLA EXPERIMENTO
            calcular_media(v_llegadas, media_llegada)  # calcula el promedio de llegadas
            calcular_media(v_tiempo_perm, media_perm)  # calcula el tiempo promedio de permanencia
            lpc_exp.append(round(lpc, 2))  # vector que guarda las longitudes promedio de cada corrida
            tep_exp.append(round(tep, 2))  # vector que guarda las esperas promedio de cada corrida
            upi_exp.append(round(upi*100/fin, 2))  # vector que guarda el PORCENTAJE de uso de la inst. de cada corrida
            ocio = 100 - (upi*100/fin)  # calcula el ocio para poder calcular el porcentaje que representa
            ocio_exp.append(round(ocio, 2))  # vector que guarda el PORCENTAJE de ocio de cada corrida
            v_tot_serv.append(sum(v_tiempo_corte))  # calcula los tiempos totales de corte de cada corrida
            v_tot_perm.append(sum(v_tiempo_perm))  # calcula los tiempos totales de permanencia de cada corrida

            eliminar_vectores_corrida()  # para que se vuelvan a crear vacíos en la proxima iteración
            corridas = corridas + 1
            ocio = 0
            upi = 0

        print("\r")

        tabla_resumen_exp()
        graficar_exp()

        # CALCULOS PARA TABLA SIMULACION
        calcular_media(v_tot_serv, media_serv_sim)
        calcular_media(media_llegada, media_llegada_sim)
        calcular_media(media_perm, media_perm_sim)
        calcular_media(ocio_exp, media_ocio_sim)

        eliminar_vectores_exp()  # para que se vuelvan a crear vacíos en la proxima iteración
        experimentos = experimentos + 1

        # graficos por exp
        corridas = 1  # reinicia el contador de corridas

    print("\r")
    tabla_resumen_sim()
    eliminar_vectores_sim()
    simulaciones = simulaciones + 1
    experimentos = 1  # reinicia el contador de experimentos
    # graficos por simulacion
