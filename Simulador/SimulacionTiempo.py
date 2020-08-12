"""
Simulación de Cola M/M/S.

Tiempos de Servicio: Dist. Exponencial
Tiempos Entre Llegadas: Dist. Exponencial
Cantidad de Servidores: 1 o más.
Disciplina de Cola: FIFO

Escenario:
  Un Sistema tiene un número limitado de servidores y define un proceso de
  atención cuya duración está determinada por un número pseudo aleatorio.

  Los usuarios llegan al banco en un tiempo pseudo aleatorio.
  Si un servidor está disponible, la atención es inmediata.
  Si no, debe esperar a que uno se libere.

"""

# Módulos Importados ---------------------------------

from random import expovariate, seed
import simpy


# Componentes del Modelo -----------------------------

class Usuario(object):
    """
    El usuario llega al sistema y solicita un turno
    """

    def __init__(self, env, mostrador, temporizador):
        self.mostrador = mostrador
        self.temporizador = temporizador
        self.env = env
        self.llega = 0
        self.pasa = 0
        self.espera = 0
        self.deja = 0
        self.atencion = 0
        self.permanencia = 0
        self.servidor = None

    def usar_sistema(self):
        self.llega = self.env.now
        with self.mostrador.request() as request:
            yield request
            self.pasa = self.env.now
            self.espera = self.pasa - self.llega
            self.servidor = self.mostrador.users.index(request)
            yield self.env.process(self.temporizador())
            self.deja = self.env.now
            self.atencion = self.deja - self.pasa
            self.permanencia = self.espera + self.atencion


class Simulacion:
    def __init__(self):
        self.experimentos = []
        self.env = simpy.Environment()

    def ejecutar(self):
        for e in self.experimentos:
            e.ejecutar()
        self.env.run(until=sum([exp.duracion for exp in self.experimentos]))

    def crear_exp(self, duracion, num_serv=1):
        exp = Experimento(self, duracion, num_serv)
        self.experimentos.append(exp)
        return exp


class Experimento:
    def __init__(self, simulacion, duracion, num_serv=1):
        self.env = simulacion.env
        self.mostrador = None
        self.num_serv = num_serv
        self.duracion = duracion
        self.corridas = []

    def crear_corrida(self, semilla, tasa_lleg, tasa_serv, u_ini=0):
        corrida = Corrida(self, semilla, tasa_lleg, tasa_serv, u_ini)
        self.corridas.append(corrida)
        return corrida

    def ejecutar(self):
        self.mostrador = simpy.Resource(self.env, capacity=self.num_serv)
        for c in self.corridas:
            c.ejecutar()


class Corrida:
    def __init__(self, experimento, semilla, tasa_lleg, tasa_serv, u_ini=0):
        self.experimento = experimento
        self.semilla = semilla
        self.tasa_lleg = tasa_lleg
        self.tasa_serv = tasa_serv
        self.u_ini = u_ini

        self.entre_llegadas = []
        self.v_usuarios = []
        self.en_cola = 0
        self.cola = []

    def tiempo_atencion(self):
        """Atiende un usuario."""

        tiempo_serv = expovariate(1 / self.tasa_serv)  # Genera un numero pseudoaleatorio exp. para el tiempo de atencion
        yield self.experimento.env.timeout(tiempo_serv)

    def setup(self):
        """Crea un Sistema, un número inicial de Usuarios y continua creando usuarios
        aproximadamente cada 'tiempo_lleg' minutos."""

        # Crea los usuarios iniciales
        for i in range(self.u_ini):
            self.encolar_usuario(0)

        # Crea mas usuarios mientras la simulacion corre
        while True:
            tiempo_lleg = expovariate(1 / self.tasa_lleg)  # Genera un numero pseudoaleatorio exp. para el tiempo entre llegadas
            yield self.experimento.env.timeout(tiempo_lleg)

            self.encolar_usuario(tiempo_lleg)

    def encolar_usuario(self, t_entre_lleg):
        self.entre_llegadas.append(t_entre_lleg)

        usuario = Usuario(self.experimento.env, self.experimento.mostrador, self.tiempo_atencion)
        self.experimento.env.process(usuario.usar_sistema())

        self.v_usuarios.append(usuario)
        self.en_cola = len(self.experimento.mostrador.queue)
        self.cola.append(self.en_cola)

    def ejecutar(self):
        seed(self.semilla)
        self.experimento.env.process(self.setup())
        # self.experimento.env.run(until=self.experimento.env.timeout(self.experimento.duracion))
