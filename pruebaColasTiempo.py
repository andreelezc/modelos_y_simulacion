from SimulacionTiempo import *
from CalculosSimulacion import *
from GraficosSimulacion import *

sim = Simulacion()
e1 = sim.crear_exp(120, 3)
c1 = e1.crear_corrida(12345, 10, 12, 0)
c2 = e1.crear_corrida(65423, 15, 20, 0)
c3 = e1.crear_corrida(65321, 20, 10, 5)
sim.ejecutar()

calculo_sim = CalculosSimulacion(sim)
calculo_sim.calcular_sim()

# g_s = GraficarSim(calculo_sim)
# g_s.graficar_sim()
#
# for exp in calculo_sim.calc_exp:
#     g_e = GraficosExp(exp)
#     g_e.graficar_exp()
#     for corr in exp.calc_corr:
#         g_c = GraficosCorrida(corr)
#         g_c.graficar_corrida()
