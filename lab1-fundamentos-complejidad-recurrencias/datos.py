"""Generadores de lotes de registros para los escenarios de Tamiza.

Todos los generadores producen indices de riesgo enteros distintos
entre si. Los escenarios A y B aceptan una semilla para que las
mediciones sean reproducibles.
"""

import random


def generar_aleatorio(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote de n registros en orden aleatorio (escenario A).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio, para que el
            experimento sea reproducible.

    Returns:
        Lista de n indices de riesgo enteros distintos, desordenada.
    """
    generador = random.Random(semilla)
    indices: list[int] = list(range(n))
    generador.shuffle(indices)
    return indices


def generar_casi_ordenado(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote casi ordenado: 98% ordenado y 2% al final (escenario B).

    El 98% inicial queda en el orden correcto (de mayor a menor indice
    de riesgo). El 2% restante se anexa al final desordenado.

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio.

    Returns:
        Lista de n indices de riesgo enteros distintos, con el primer
        98% en el orden que el algoritmo produce y el 2% restante
        desordenado al final.
    """
    generador = random.Random(semilla)
    corte: int = n * 98 // 100

    ordenado: list[int] = list(range(corte - 1, -1, -1))
    cola: list[int] = list(range(corte, n))
    generador.shuffle(cola)

    return ordenado + cola


def generar_inverso(n: int) -> list[int]:
    """Genera un lote en el orden exactamente contrario (escenario C).

    Args:
        n: cantidad de registros del lote.

    Returns:
        Lista de n indices de riesgo enteros distintos, en el orden
        inverso al que el algoritmo debe producir.
    """
    return list(range(n))