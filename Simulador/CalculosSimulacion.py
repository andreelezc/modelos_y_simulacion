class Util:
    @staticmethod
    def promedio(arr):
        return sum(arr) / len(arr)


class CalculosSimulacion:
    def __init__(self, simulacion):
        self.simulacion = simulacion
        self.calc_exp = []

        self.media_lleg = 0
        self.media_atencion = 0
        self.media_perm = 0
        self.media_esp_cola = 0
        self.media_ocio_sim = 0

        self.llegadas = []
        self.permanencias = []
        self.espera_prom_cola = []

    def calcular_sim(self):
        for e in self.simulacion.experimentos:
            c_e = CalculosExperimento(e)
            c_e.calcular_exp()
            self.calc_exp.append(c_e)

        self.llegadas = [experimento.media_lleg for experimento in self.calc_exp]
        self.media_lleg = Util.promedio(self.llegadas)

        self.media_atencion = Util.promedio([experimento.media_atencion for experimento in self.calc_exp])

        self.permanencias = [experimento.media_perm for experimento in self.calc_exp]
        self.media_perm = Util.promedio(self.permanencias)

        self.espera_prom_cola = [experimento.espera_prom_cola for experimento in self.calc_exp]
        self.media_esp_cola = Util.promedio(self.espera_prom_cola)

        self.media_ocio_sim = Util.promedio([experimento.ocio_exp for experimento in self.calc_exp])


class CalculosExperimento:
    def __init__(self, experimento):
        self.experimento = experimento
        self.calc_corr = []

        self.media_lleg = 0
        self.media_espera = 0
        self.media_perm = 0
        self.media_atencion = 0
        self.long_prom_cola = 0
        self.espera_prom_cola = 0
        self.utilizacion = 0
        self.ocio_exp = 0

        self.llegadas = []
        self.esperas = []
        self.permanencias = []
        self.atenciones = []

    def calcular_exp(self):
        for c in self.experimento.corridas:
            c_c = CalculosCorrida(c)
            c_c.calcular()
            self.calc_corr.append(c_c)

        self.llegadas = [corrida.media_lleg for corrida in self.calc_corr]
        self.media_lleg = Util.promedio(self.llegadas)

        self.esperas = [corrida.media_espera for corrida in self.calc_corr]
        self.media_espera = Util.promedio(self.esperas)

        self.permanencias = [corrida.media_perm for corrida in self.calc_corr]
        self.media_perm = Util.promedio(self.permanencias)

        self.atenciones = [corrida.media_atencion for corrida in self.calc_corr]
        self.media_atencion = Util.promedio(self.atenciones)

        self.long_prom_cola = Util.promedio([corrida.long_prom_cola for corrida in self.calc_corr])
        self.espera_prom_cola = Util.promedio([corrida.espera_prom_cola for corrida in self.calc_corr])
        self.utilizacion = Util.promedio([corrida.utilizacion for corrida in self.calc_corr])
        self.ocio_exp = Util.promedio([corrida.ocio for corrida in self.calc_corr])


class CalculosCorrida:
    def __init__(self, corrida):
        self.corrida = corrida
        self.media_lleg = 0
        self.media_espera = 0
        self.media_perm = 0
        self.long_prom_cola = 0
        self.espera_prom_cola = 0
        self.media_atencion = 0
        self.utilizacion = 0
        self.ocio = 0

        self.llegadas = []
        self.esperas = []
        self.permanencias = []
        self.atenciones = []
        self.usuarios = corrida.v_usuarios
        self.cola = corrida.cola
        self.entre_llegadas = corrida.entre_llegadas

    def calcular(self):
        self.llegadas = [usuario.llega for usuario in self.usuarios]
        self.media_lleg = Util.promedio(self.llegadas)

        self.esperas = [usuario.espera for usuario in self.usuarios]
        self.media_espera = Util.promedio(self.esperas)

        self.permanencias = [usuario.permanencia for usuario in self.usuarios]
        self.media_perm = Util.promedio(self.permanencias)

        self.atenciones = [usuario.atencion for usuario in self.usuarios]
        self.media_atencion = Util.promedio(self.atenciones)

        self.long_prom_cola = Util.promedio(self.cola)
        self.espera_prom_cola = self.corrida.tasa_lleg * self.media_espera
        self.utilizacion = self.corrida.tasa_lleg / (self.corrida.tasa_serv * self.corrida.experimento.num_serv)
        self.ocio = (1 - self.utilizacion)
