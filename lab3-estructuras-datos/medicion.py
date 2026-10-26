"""Experimentos de medicion del lab 3 y generacion de las graficas."""

import math
import random
import time

import matplotlib.pyplot as plt

from estructuras import ListaEnlazada, TablaHash


def es_primo(k: int) -> bool:
    """Indica si k es primo.

    Args:
        k: numero entero a verificar.

    Returns:
        True si k es primo, False en caso contrario.
    """
    if k < 2:
        return False
    for divisor in range(2, int(math.isqrt(k)) + 1):
        if k % divisor == 0:
            return False
    return True


def primo_cercano(k: int) -> int:
    """Devuelve el primo mas cercano a k (busca hacia arriba).

    Args:
        k: numero de referencia.

    Returns:
        El primo mas pequeno mayor o igual que k.
    """
    candidato = max(2, k)
    while not es_primo(candidato):
        candidato += 1
    return candidato


def generar_guias(n: int, semilla: int = 7) -> list[int]:
    """Genera n guias de diez digitos distintas con semilla fija.

    Args:
        n: cantidad de guias a generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con n guias distintas.
    """
    azar = random.Random(semilla)
    return azar.sample(range(10**9, 10**10), n)


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def tiempo_promedio_busquedas(
    estructura, guias_buscar: list[int], repeticiones: int = 3
) -> float:
    """Mide el tiempo medio por busqueda, repitiendo la tanda varias veces.

    Args:
        estructura: estructura con metodo buscar (ListaEnlazada o TablaHash).
        guias_buscar: guias a buscar en cada tanda.
        repeticiones: numero de tandas de medicion a promediar.

    Returns:
        El tiempo medio por busqueda en segundos.
    """
    total_medido = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        for guia in guias_buscar:
            estructura.buscar(guia)
        fin = time.perf_counter()
        total_medido.append(fin - inicio)
    return min(total_medido) / len(guias_buscar)


def experimento_a() -> list[tuple[int, int, float, float]]:
    """Mide lista vs tabla para varios n y genera lista_vs_tabla.png.

    Returns:
        Una lista de tuplas (n, m, tiempo_lista, tiempo_tabla).
    """
    valores_n = [100, 500, 1000, 5000, 20000, 50000]
    resultados = []
    for n in valores_n:
        m = primo_cercano(max(2, n // 2))
        guias = generar_guias(n)
        existentes = set(guias)
        inexistentes = generar_guias_inexistentes(existentes, 200)

        lista = ListaEnlazada()
        for guia, estado in zip(guias, ["en bodega"] * n):
            lista.insertar(guia, estado)
        tabla = TablaHash(m)
        for guia, estado in zip(guias, ["en bodega"] * n):
            tabla.insertar(guia, estado)

        # Verificacion de consistencia en una muestra.
        muestra = guias[: min(20, n)]
        for guia in muestra:
            assert lista.buscar(guia) == tabla.buscar(guia)

        t_lista = tiempo_promedio_busquedas(lista, inexistentes)
        t_tabla = tiempo_promedio_busquedas(tabla, inexistentes)
        resultados.append((n, m, t_lista, t_tabla))
        print(f"n={n}, m={m}: lista={t_lista*1e6:.1f} us, tabla={t_tabla*1e6:.1f} us")

    ns = [r[0] for r in resultados]
    t_lista = [r[2] * 1e3 for r in resultados]
    t_tabla = [r[3] * 1e3 for r in resultados]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, t_lista, "o-", label="Lista enlazada")
    ax.plot(ns, t_tabla, "s-", label="Tabla hash")
    ax.set_title("Tiempo medio de busqueda de guias inexistentes vs n")
    ax.set_xlabel("Numero de guias n (guias)")
    ax.set_ylabel("Tiempo medio por busqueda (ms)")
    ax.legend()
    ax.grid(True)
    fig.savefig("graficas/lista_vs_tabla.png", dpi=150)
    print("Grafica guardada: graficas/lista_vs_tabla.png")
    return resultados


def experimento_b() -> list[tuple[float, int, float]]:
    """Mide el efecto del factor de carga y genera tiempo_vs_alfa.png.

    Returns:
        Una lista de tuplas (alfa, m, tiempo_medio_por_busqueda).
    """
    n = 20000
    factores_alfa = [0.5, 1, 4, 10]
    guias = generar_guias(n)
    existentes = set(guias)
    inexistentes = generar_guias_inexistentes(existentes, 200)
    resultados = []
    for alfa in factores_alfa:
        m = primo_cercano(max(2, round(n / alfa)))
        tabla = TablaHash(m)
        for guia in guias:
            tabla.insertar(guia, "en bodega")
        assert abs(tabla.factor_carga() - n / m) < 0.01
        t = tiempo_promedio_busquedas(tabla, inexistentes)
        resultados.append((n / m, m, t))
        print(f"alfa~{alfa}, m={m}: {t*1e6:.1f} us por busqueda")

    als = [r[0] for r in resultados]
    tiempos = [r[2] * 1e6 for r in resultados]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(als, tiempos, "o-", label="Tabla hash (20000 guias)")
    ax.set_title("Tiempo medio de busqueda de guias inexistentes vs factor de carga")
    ax.set_xlabel("Factor de carga alfa (guias por casilla)")
    ax.set_ylabel("Tiempo medio por busqueda (microsegundos)")
    ax.legend()
    ax.grid(True)
    fig.savefig("graficas/tiempo_vs_alfa.png", dpi=150)
    print("Grafica guardada: graficas/tiempo_vs_alfa.png")
    return resultados


if __name__ == "__main__":
    experimento_a()
    experimento_b()
