"""Pruebas de verificacion de las dos soluciones del subarreglo maximo.

Comprueba casos de resultado conocido y contrasta las dos funciones
sobre listas aleatorias. Las pruebas comparan la suma, no los indices,
porque ante empates cualquiera de los tramos es valido.

Uso:
    python pruebas.py
"""

import random
import sys
from pathlib import Path

_DIR = Path(__file__).resolve().parent
if str(_DIR) not in sys.path:
    sys.path.insert(0, str(_DIR))

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo  # noqa: E402


def mejor_suma(valores: list[float]) -> float:
    """Devuelve la suma del mejor tramo segun divide y venceras."""
    return subarreglo_maximo(valores, 0, len(valores) - 1)[2]


def verificar_indices(valores: list[float],
                      resultado: tuple[int, int, float]) -> None:
    """Comprueba que el tramo devuelto suma el valor reportado."""
    inicio, fin, suma = resultado
    assert 0 <= inicio <= fin < len(valores)
    assert sum(valores[inicio:fin + 1]) == suma


def main() -> None:
    """Ejecuta todos los casos de prueba sobre ambas soluciones."""
    # Serie de ocho dias de la situacion problema: mejor racha suma 17.
    serie = [-3, 5, -2, 8, -6, 3, 9, -4]
    assert subarreglo_fuerza_bruta(serie)[2] == 17
    assert subarreglo_maximo(serie, 0, len(serie) - 1)[2] == 17
    verificar_indices(serie, subarreglo_fuerza_bruta(serie))
    verificar_indices(serie, subarreglo_maximo(serie, 0, len(serie) - 1))

    # Un solo elemento: el unico tramo posible es ese elemento.
    assert subarreglo_fuerza_bruta([7])[2] == 7
    assert subarreglo_maximo([7], 0, 0)[2] == 7
    assert subarreglo_fuerza_bruta([-4])[2] == -4
    assert subarreglo_maximo([-4], 0, 0)[2] == -4

    # Todos negativos: conviene el menos negativo.
    negativos = [-5, -2, -9, -1, -7]
    assert subarreglo_fuerza_bruta(negativos)[2] == -1
    assert mejor_suma(negativos) == -1

    # Todos positivos: conviene la serie completa.
    positivos = [3, 1, 4, 1, 5, 9, 2, 6]
    assert subarreglo_fuerza_bruta(positivos)[2] == sum(positivos)
    assert mejor_suma(positivos) == sum(positivos)

    # Caso cuyo mejor tramo cruza el punto medio (indices 1 y 2).
    cruzado = [-5, 4, 3, -5]
    assert subarreglo_fuerza_bruta(cruzado)[2] == 7
    assert subarreglo_maximo(cruzado, 0, len(cruzado) - 1)[2] == 7

    # Al menos veinte listas aleatorias: ambas funciones coinciden.
    generador = random.Random(2026)
    for _ in range(20):
        n = generador.randint(1, 60)
        valores = [generador.randint(-100, 100) for _ in range(n)]
        assert (subarreglo_fuerza_bruta(valores)[2]
                == subarreglo_maximo(valores, 0, n - 1)[2])

    print("Todas las pruebas pasaron.")


if __name__ == "__main__":
    main()
