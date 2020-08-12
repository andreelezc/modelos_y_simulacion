"""
Simulación de Cola de Banco M/M/S.

Tiempos de Servicio: Dist. Exponencial
Tiempos Entre Llegadas: Dist. Exponencial
Cantidad de Servidores: 1 o más.
Disciplina de Cola: FIFO

Escenario:
  Un Banco tiene un número limitado de cajeros y define un proceso de
  atención cuya duración está determinada por un número pseudo aleatorio.

  Los procesos "Cliente" llegan al banco en un tiempo pseudo aleatorio.
  Si un cajero está disponible, la atención es inmediata.
  Si no, debe esperar a que uno se libere.

"""

# Módulos Importados ---------------------------------

from termcolor import cprint
from random import expovariate, seed
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
import simpy
import itertools

# Variables ------------------------------------------

# Por corrida
v_clientes = []
llegadas = []
entre_llegadas = []
atenciones = []
esperas = []
permanencias = []
salidas = []
en_cola = []

# Por experimento
media_lleg_exp = []
media_esp_exp = []
media_perm_exp = []
media_cola_exp = []
media_atenc_exp = []
espera_cola_exp = []
ocio_exp = []
trabajo_exp = []

# Por simulación
media_lleg_sim = []
media_atencion_sim = []
media_perm_sim = []
espera_cola_sim = []
ocio_sim = []


# Componentes del Modelo -----------------------------

class Banco(object):
    """Un banco tiene un numero limitado de cajeros (num_cajas) para
    atender a clientes en paralelo.

    El cliente saca turno. La atención está determinada por tiempo_serv.
    """

    def __init__(self, env, num_cajas):
        self.env = env
        self.mostrador = simpy.Resource(env, capacity=num_cajas)

    def atender(self, cliente):
        """Atiende un cliente."""

        global tiempo_serv
        tiempo_serv = expovariate(1 / MEDIA_SERV)  # Genera un numero pseudoaleatorio exp. para el tiempo de atencion
        yield self.env.timeout(tiempo_serv)


def cliente(env, name, bk):
    """El proceso 'cliente' llega al banco y solicita un turno.

    """
    llega = env.now
    llegadas.append(round(llega, 2))
    cprint("→ 🚶 ", "green", attrs=['bold'], end=" "), print("%s - %.2f" % (name, llega))
    with bk.mostrador.request() as request:
        yield request
        pasa = env.now
        espera = pasa - llega
        esperas.append(round(espera, 2))
        cprint("--- 🚶 ", "blue", attrs=['bold'], end=" "), print(
            "%s - %.2f. Esperó %.2f minutos" % (name, pasa, espera))
        yield env.process(bk.atender(name))
        deja = env.now
        salidas.append(round(deja, 2))
        atencion = tiempo_serv
        atenciones.append(round(atencion, 2))
        permanencia = espera + atencion
        permanencias.append(round(permanencia, 2))
        cprint("← 🚶 ", "red", attrs=['bold'], end=" "), print("%s - %.2f" % (name, deja))


def setup(env, num_cajas):
    """Crea un Banco, un número inicial de Clientes y continua creando clientes
    aproximadamente cada 'tiempo_lleg' minutos."""

    # Crea el Banco
    banco = Banco(env, num_cajas)

    # Crea los clientes iniciales (los que hacen cola antes de que el Banco abra)
    global no_atendidos, cola
    i = 0
    if C_INI > 0:
        for i in range(1, C_INI):
            env.process(cliente(env, 'C%d' % i, banco))
            v_clientes.append(i)
            entre_llegadas.append(0)
            cola = len(banco.mostrador.queue)
            en_cola.append(cola)

    # Crea mas clientes mientras la simulacion corre
    while True:
        tiempo_lleg = expovariate(1 / MEDIA_LLEG)  # Genera un numero pseudoaleatorio exp. para el tiempo entre llegadas
        yield env.timeout(tiempo_lleg)
        entre_llegadas.append(round(tiempo_lleg, 2))
        i += 1
        env.process(cliente(env, 'C%d' % i, banco))
        cola = len(banco.mostrador.queue)
        en_cola.append(cola)
        v_clientes.append(i)
        no_atendidos = cola


#  Tablas de Reportes --------------------------------

def resumen_corrida():
    t = PrettyTable()
    t.field_names = ['Cliente Nº', 'Llegada', 'T. Espera', 'Atencion', 'T. Salida', 'Permanencia', 'T.Entre Lleg',
                     'En cola']
    for lst in (itertools.zip_longest(v_clientes, llegadas, esperas, atenciones, salidas, permanencias, entre_llegadas,
                                      en_cola, fillvalue=" ")):
        t.add_row(lst)

    cprint('{:-^145}'.format(" RESUMEN CORRIDA ", end="\n"), "grey", end="\n")
    print(t)


def resumen_exp():
    v_corr = []
    for i in range(1, corr + 1):
        v_corr.append(i)

    t = PrettyTable()
    t.field_names = ['Corrida Nº', 'Llegada', 'Espera', 'Permanencia', 'Long. de Cola', 'Porc. Trabajo', 'Porc. Ocio']
    for lst in (itertools.zip_longest(v_corr, media_lleg_exp, media_esp_exp, media_perm_exp, media_cola_exp,
                                      trabajo_exp, ocio_exp, fillvalue=" ")):
        t.add_row(lst)

    cprint('{:-^145}'.format(" PROMEDIOS POR EXPERIMENTO ", end="\n"), "grey", end="\n")
    print(t)


def resumen_sim():
    v_exp = []
    for i in range(1, exp + 1):
        v_exp.append(i)

    t = PrettyTable()
    t.field_names = ['Experimento Nº', 'Llegada', 'Atención', 'Permanencia', 'Tiempo en Cola', 'Porc. Ocio']
    for lst in (itertools.zip_longest(v_exp, media_lleg_sim, media_atencion_sim, media_perm_sim, espera_cola_sim,
                                      ocio_sim, fillvalue=" ")):
        t.add_row(lst)

    cprint('{:-^145}'.format(" PROMEDIOS POR SIMULACIÓN ", end="\n"), "grey", end="\n")
    print(t)


# Gráficos--------------------------------------------

def graficar_corrida():
    x1 = range(len(llegadas))
    y1 = llegadas
    x2 = range(len(esperas))
    y2 = esperas
    x3 = range(len(atenciones))
    y3 = atenciones
    x4 = range(len(permanencias))
    y4 = permanencias

    fig = plt.figure()
    plt.style.use('seaborn-whitegrid')
    plt.suptitle("Resultados de Corrida (X: Clientes; Y: Tiempo)\n", fontweight='bold')

    f1 = fig.add_subplot(221)
    f1.plot(x1, y1, color='red')
    f1.title.set_text('\nLlegadas')

    f2 = fig.add_subplot(222)
    f2.plot(x2, y2, color='green')
    f2.title.set_text('\nEsperas')

    f3 = fig.add_subplot(223)
    f3.plot(x3, y3, color='orange')
    f3.title.set_text('\nDuración de la Atención')

    f4 = fig.add_subplot(224)
    f4.plot(x4, y4, label='Permanencia', color='blue')
    f4.title.set_text('\nPemanencia')
    plt.tight_layout()
    plt.minorticks_on()
    plt.show()


def graficar_exp():
    # definir estilo del grafico
    plt.style.use('seaborn-notebook')

    # definir ancho de barra
    barWidth = 0.15

    # definir alto de barra
    bars1 = media_lleg_exp
    bars2 = media_perm_exp
    bars3 = media_esp_exp

    # Establecer posicion de barra en el eje X
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    # Crear el grafico
    plt.bar(r1, bars1, color='red', width=barWidth, edgecolor='white', label='Llegada')
    plt.bar(r2, bars2, color='tomato', width=barWidth, edgecolor='white', label='Permanencia')
    plt.bar(r3, bars3, color='lightsalmon', width=barWidth, edgecolor='white', label='Espera')

    # Agregar marcas en la mitad del grupo de barras
    plt.xlabel('Corridas')
    plt.ylabel('Tiempo')
    plt.xticks([r + barWidth for r in range(len(bars1))], [str(i + 1) for i in range(len(bars1))])

    # Crear leyenda & mostrar grafico
    plt.legend()
    plt.title('Promedios por Experimento', fontweight='bold')
    plt.tight_layout()
    plt.show()


def graficar_sim():
    # definir estilo del grafico
    plt.style.use('seaborn-notebook')

    # definir ancho de barra
    barWidth = 0.15

    # definir alto de barra
    bars1 = media_lleg_sim
    bars2 = media_perm_sim
    bars3 = espera_cola_sim

    # Establecer posicion de barra en el eje X
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    # Crear el grafico
    plt.bar(r1, bars1, color='blue', width=barWidth, edgecolor='white', label='Llegada')
    plt.bar(r2, bars2, color='skyblue', width=barWidth, edgecolor='white', label='Permanencia')
    plt.bar(r3, bars3, color='seagreen', width=barWidth, edgecolor='white', label='Espera')

    # Agregar marcas en la mitad del grupo de barras
    plt.xlabel('Experimentos')
    plt.ylabel('Tiempo')
    plt.xticks([r + barWidth for r in range(len(bars1))], [str(i + 1) for i in range(len(bars1))])

    # Crear leyenda & mostrar grafico
    plt.legend()
    plt.title('Promedios por Simulación', fontweight='bold')
    plt.tight_layout()
    plt.show()


# Limpiar Vectores -----------------------------------

def eliminar_vectores_corrida():
    del v_clientes[:]
    del llegadas[:]
    del entre_llegadas[:]
    del atenciones[:]
    del esperas[:]
    del permanencias[:]
    del salidas[:]
    del en_cola[:]


def eliminar_vect_exp():
    del media_lleg_exp[:]
    del media_esp_exp[:]
    del media_perm_exp[:]
    del media_cola_exp[:]
    del media_atenc_exp[:]
    del espera_cola_exp[:]
    del ocio_exp[:]
    del trabajo_exp[:]


def eliminar_vect_sim():
    del media_lleg_sim[:]
    del media_atencion_sim[:]
    del media_perm_sim[:]
    del espera_cola_sim[:]
    del ocio_sim[:]


# Inicio de simulacion -------------------------------

cprint('{:-^145}'.format(" SEGUNDO PARCIAL - SIMULADOR DE BANCO "), 'green', attrs=['bold'])
print("REFERENCIAS:", end=" "), cprint('→ 🚶  LLEGADA', 'green', attrs=['bold'], end="\t"), \
    cprint('- 🚶  ATENCIÓN', 'blue', attrs=['bold'], end='\t'), \
    cprint('← 🚶  SALIDA', 'red', attrs=['bold'], end='\n')
print("\r")

sim = int(input("Cantidad de Simulaciones:"))
exp = int(input("Cantidad de Experimentos:"))
corr = int(input("Cantidad de Corridas:"))

simulaciones = 1
experimentos = 1
corridas = 1

while simulaciones <= sim:
    cprint('{:-^145}'.format(" SIMULACIÓN Nº: {} ".format(simulaciones)), "grey")
    while experimentos <= exp:
        print("\r")
        cprint('{:-^145}'.format(" EXPERIMENTO Nº: {} ".format(experimentos)), "grey")
        NUM_CAJAS = (int(input("Número de Servidores:")))
        TIEMPO_SIM = (int(input("Duración de la simulacion en horas:")))
        TIEMPO_SIM = TIEMPO_SIM * 60
        while corridas <= corr:
            cprint("\nCORRIDA Nº: {}".format(corridas), "green", attrs=['bold', 'underline'])
            SEMILLA = (int(input("Semilla:")))
            MEDIA_LLEG = (int(input("Media de Tiempo entre Llegadas (λ):")))
            MEDIA_SERV = (int(input("Media de Tiempo de Servicio (µ):")))
            C_INI = (int(input("Clientes iniciales:")))
            C_INI = C_INI + 1

            seed(SEMILLA)  # Ayuda a reproducir los resultados

            # Crea un entorno y llama al proc. Setup
            env = simpy.Environment()
            env.process(setup(env, NUM_CAJAS))

            # Ejecuta
            env.run(until=TIEMPO_SIM)

            resumen_corrida()
            print("\n Quedan sin atender:", no_atendidos)

            # Valores individuales de la corrida
            media_llegada = round(sum(llegadas) / len(llegadas), 2)
            media_espera = round(sum(esperas) / len(esperas), 2)  # (W)
            media_perm = round(sum(permanencias) / len(permanencias), 2)
            long_prom_cola = round(sum(en_cola) / len(en_cola), 2)
            espera_prom_cola = round(MEDIA_LLEG * media_espera, 2)  # (λ * W)
            media_atencion = round(sum(atenciones) / len(atenciones))
            utilizacion = round(MEDIA_LLEG / (MEDIA_SERV * NUM_CAJAS), 2)  # (λ / µ * s)
            ocio = round(1 - utilizacion, 2)

            # Calculos por Experimento (usando los valores individuales)
            media_lleg_exp.append(media_llegada)
            media_esp_exp.append(media_espera)
            media_perm_exp.append(media_perm)
            media_cola_exp.append(long_prom_cola)
            espera_cola_exp.append(espera_prom_cola)
            media_atenc_exp.append(media_atencion)
            trabajo_exp.append(utilizacion)
            ocio_exp.append(ocio)

            graficar_corrida()
            eliminar_vectores_corrida()
            corridas = corridas + 1

        # Calculos por Simulacion
        m_lleg = round(sum(media_lleg_exp) / len(media_lleg_exp))
        media_lleg_sim.append(m_lleg)
        m_aten = round(sum(media_atenc_exp) / len(media_atenc_exp))
        media_atencion_sim.append(m_aten)
        m_perm = round(sum(media_perm_exp) / len(media_perm_exp))
        media_perm_sim.append(m_perm)
        m_esp_cola = round(sum(espera_cola_exp) / len(espera_cola_exp))
        espera_cola_sim.append(m_esp_cola)
        m_ocio = sum(ocio_exp) / len(ocio_exp)
        ocio_sim.append(round(m_ocio, 2))

        resumen_exp()
        graficar_exp()
        eliminar_vect_exp()
        experimentos = experimentos + 1
        corridas = 1  # reinicia el contador de corridas

    resumen_sim()
    graficar_sim()
    eliminar_vect_sim()
    simulaciones = simulaciones + 1
    experimentos = 1  # reinicia el contador de experimentos

simulaciones = 1  # reinicia el contador de simulaciones

# ----------------------------------------------------
