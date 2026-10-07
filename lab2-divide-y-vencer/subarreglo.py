"""Subarreglo maximo: fuerza bruta y divide y venceras.

Ambas funciones encuentran el tramo de dias consecutivos cuya variacion
de caja acumulada es la mayor. Ninguna modifica la lista recibida y, si
hay varios tramos con la misma suma maxima, cualquiera de ellos es
valido: las pruebas comparan la suma, no los indices.
"""


def subarreglo_fuerza_bruta(valores: list[float]) -> tuple[int, int, float]:
    """Encuentra la mejor racha probando todos los pares de dias (i, j).

    Acumula la suma dentro del ciclo interno en lugar de recalcularla
    desde cero para cada par, de modo que el algoritmo es Θ(n²).

    Args:
        valores: variacion diaria de caja, una por dia. Tiene al menos
            un elemento.

    Returns:
        Una tupla (inicio, fin, suma) con los indices inclusivos del
        tramo de mayor suma y el valor de esa suma.
    """
    n: int = len(valores)
    mejor_inicio: int = 0
    mejor_fin: int = 0
    mejor_suma: float = valores[0]

    for i in range(n):
        suma: float = 0.0
        for j in range(i, n):
            suma += valores[j]
            if suma > mejor_suma:
                mejor_suma = suma
                mejor_inicio = i
                mejor_fin = j

    return mejor_inicio, mejor_fin, mejor_suma


def suma_cruzada(
    valores: list[float], inicio: int, medio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra el mejor tramo que cruza el punto medio.

    Barre de forma lineal desde el punto medio hacia la izquierda y
    desde medio + 1 hacia la derecha, eligiendo en cada lado el tramo de
    mayor suma. El resultado incluye al menos un elemento de cada mitad.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango considerado (inclusive).
        medio: indice del ultimo elemento de la mitad izquierda.
        fin: indice final del rango considerado (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo que incluye al
        menos un elemento de cada mitad.
    """
    suma_izquierda: float = float("-inf")
    acumulada: float = 0.0
    mejor_inicio: int = medio

    for i in range(medio, inicio - 1, -1):
        acumulada += valores[i]
        if acumulada > suma_izquierda:
            suma_izquierda = acumulada
            mejor_inicio = i

    suma_derecha: float = float("-inf")
    acumulada = 0.0
    mejor_fin: int = medio + 1

    for j in range(medio + 1, fin + 1):
        acumulada += valores[j]
        if acumulada > suma_derecha:
            suma_derecha = acumulada
            mejor_fin = j

    return mejor_inicio, mejor_fin, suma_izquierda + suma_derecha


def subarreglo_maximo(
    valores: list[float], inicio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra la mejor racha por divide y venceras.

    Divide el rango en dos mitades, resuelve cada mitad de forma
    recursiva, calcula el mejor tramo que cruza el punto medio y
    devuelve el mejor de los tres casos.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango a considerar (inclusive).
        fin: indice final del rango a considerar (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo dentro de
        valores[inicio..fin].
    """
    if inicio == fin:
        return inicio, fin, valores[inicio]

    medio: int = (inicio + fin) // 2
    izq_inicio, izq_fin, izq_suma = subarreglo_maximo(valores, inicio, medio)
    der_inicio, der_fin, der_suma = subarreglo_maximo(
        valores, medio + 1, fin
    )
    cru_inicio, cru_fin, cru_suma = suma_cruzada(
        valores, inicio, medio, fin
    )

    if izq_suma >= der_suma and izq_suma >= cru_suma:
        return izq_inicio, izq_fin, izq_suma
    if der_suma >= izq_suma and der_suma >= cru_suma:
        return der_inicio, der_fin, der_suma
    return cru_inicio, cru_fin, cru_suma
