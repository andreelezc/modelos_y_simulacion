from otros import chicuadrado

res = []


def metodo_mult(n, x, a, mod, v_res):
    """
    Genera números aleatorios utilizando el método de congruencia multiplicativo.
    La fórmula es: Xn+1 = (a.Xn) mod m

    :param x: semilla (>0, impar)
    :param a: multiplicador (>0); a=3+8k o a=5+8k; K = 0,1,2,3,…
    :param mod: modulo (x, a <  m); mod =2^g; g debe ser entero
    :param v_res: vector resultado

    Si se siguen estas condiciones se puede lograr que el algoritmo tenga un período de vida
    (iteraciones sin encontrar repetición) de mod/4.

    """

    for i in range(n):
        x1 = (a * x) % mod
        x2 = x1 / (mod-1)  # para que el valor esté entre 0 y 1
        # print (i+1, x2)
        x = x1
        v_res.append(round(x2, 4))

    #print(v_res)


def main():
    n = int(input("Cantidad de números deseados:"))
    x = int(input("Introduce el valor de la semilla: "))
    a = int(input("Introduce el valor del multiplicador: "))
    m = int(input("Introduce el valor del modulo: "))
    metodo_mult(n, x, a, m, res)


if __name__ == "__main__": # solo se ejecuta cuando no es llamado via 'import'
    main()
    print("\nValores Aleatorios:", res)
    chicuadrado.test_chi(res)
