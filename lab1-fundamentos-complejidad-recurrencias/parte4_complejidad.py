"""Validacion experimental de la Parte 4: merge sort vs. insertion sort.

Compara el tiempo de ejecucion de ambos algoritmos sobre el escenario
A (aleatorio) de Tamiza para los mismos tamanos de entrada de la Parte
3, y produce la grafica parte4_tiempo.png en la carpeta graficas/.

Uso:
    python parte4_complejidad.py
"""

import sys
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

_DIR = Path(__file__).resolve().parent
if str(_DIR) not in sys.path:
    sys.path.insert(0, str(_DIR))

from algoritmos import insertion_sort, merge_sort  # noqa: E402
from datos import generar_aleatorio  # noqa: E402

TAMANOS: list[int] = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES: int = 3


def medir_tiempo(ordenar: Callable[[list[int]], tuple[list[int], int]],
                 n: int) -> float:
    """Mide el tiempo promedio de un algoritmo sobre el escenario A.

    El tiempo de generacion de los datos no se cronometra: la medicion
    cubre unicamente la llamada al algoritmo.

    Args:
        ordenar: funcion de ordenamiento a medir.
        n: tamanio de entrada del lote.

    Returns:
        Tiempo promedio en segundos sobre REPETICIONES corridas.
    """
    tiempos: list[float] = []

    for _ in range(REPETICIONES):
        datos = generar_aleatorio(n)
        inicio = time.perf_counter()
        ordenar(datos)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    return sum(tiempos) / len(tiempos)


def main() -> None:
    """Mide ambos algoritmos y genera la grafica de la Parte 4."""
    tiempos_insertion: list[float] = []
    tiempos_merge: list[float] = []

    for n in TAMANOS:
        print(f"Midiendo para n = {n} ...")
        tiempo_insertion = medir_tiempo(insertion_sort, n)
        tiempo_merge = medir_tiempo(merge_sort, n)
        tiempos_insertion.append(tiempo_insertion)
        tiempos_merge.append(tiempo_merge)
        print(f"  insertion sort: {tiempo_insertion * 1000:.2f} ms")
        print(f"  merge sort:     {tiempo_merge * 1000:.2f} ms")

    fig, ax = plt.subplots()
    ax.plot(TAMANOS, tiempos_insertion, marker="o",
            label="Insertion sort")
    ax.plot(TAMANOS, tiempos_merge, marker="s",
            label="Merge sort")

    ax.set_title("Merge sort vs. insertion sort - escenario A (aleatorio)")
    ax.set_xlabel("Tamanio de entrada (registros)")
    ax.set_ylabel("Tiempo de ejecucion promedio (s)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    carpeta = _DIR / "graficas"
    carpeta.mkdir(exist_ok=True)
    fig.savefig(carpeta / "parte4_tiempo.png", dpi=150)
    plt.close(fig)
    print("Grafica guardada en graficas/parte4_tiempo.png.")


if __name__ == "__main__":
    main()