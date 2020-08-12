from Simulador.SimulacionCantidad import *

simulacion = Simulacion()
e1 = simulacion.crear_exp(50, 1)
c1 = e1.crear_corrida(12356, 10, 12, 3)
simulacion.ejecutar()
pass
