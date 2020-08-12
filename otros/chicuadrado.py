from scipy.stats import chisquare
from termcolor import colored


def test_chi(v_aleatorios):
    print('{:*^105}'.format(" Test Chi Cuadrado "))
    alpha = (float(input("Nivel de significancia "
                         "(0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90:")))
    chi2, p_val = chisquare(v_aleatorios)
    print("χ²:", round(chi2, 4))
    print("p:", round(p_val, 4))
    if p_val > alpha:
        print(colored(" - LA SERIE DE NÚMEROS ALEATORIOS PASO EL TEST DE χ² CON ÉXITO", "green", attrs=['bold']))
    elif p_val <= alpha:
        print(colored(" - LA SERIE DE NÚMEROS ALEATORIOS NO PASO EL TEST DE χ²", "red", attrs=['bold']))
    print("Vector de numeros aleatorios")
    print(v_aleatorios)
    print('{:*^105}'.format(""))
