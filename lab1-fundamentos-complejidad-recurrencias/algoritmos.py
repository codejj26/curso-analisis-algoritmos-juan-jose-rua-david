"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1.

Ambos algoritmos ordenan de mayor a menor indice de riesgo y cuentan
las comparaciones entre elementos de la lista. Ninguno modifica la
lista recibida: trabajan sobre una copia.
"""

from collections.abc import Sequence


def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    copia: list[int] = list(datos)
    comparaciones: int = 0
    n: int = len(copia)

    for i in range(1, n):
        clave: int = copia[i]
        j: int = i - 1
        while j >= 0:
            comparaciones += 1
            if copia[j] >= clave:
                break
            copia[j + 1] = copia[j]
            j -= 1
        copia[j + 1] = clave

    return copia, comparaciones


def merge_sort(datos: Sequence[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    def _merge_sort(arr: list[int]) -> tuple[list[int], int]:
        n: int = len(arr)
        if n <= 1:
            return arr[:], 0

        medio: int = n // 2
        izquierda, comp_izq = _merge_sort(arr[:medio])
        derecha, comp_der = _merge_sort(arr[medio:])
        mezclada, comp_mezcla = _merge(izquierda, derecha)

        return mezclada, comp_izq + comp_der + comp_mezcla

    return _merge_sort(list(datos))


def _merge(izquierda: list[int], derecha: list[int]) -> tuple[list[int], int]:
    """Mezcla dos listas ya ordenadas de mayor a menor.

    Args:
        izquierda: primera lista ordenada.
        derecha: segunda lista ordenada.

    Returns:
        Tupla con la lista mezclada (mayor a menor) y la cantidad de
        comparaciones entre elementos realizadas.
    """
    resultado: list[int] = []
    i: int = 0
    j: int = 0
    comparaciones: int = 0

    while i < len(izquierda) and j < len(derecha):
        comparaciones += 1
        if izquierda[i] >= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado, comparaciones