"""Experimento de la Parte 3: los tres casos sobre los escenarios de Tamiza.

Ejecuta insertion sort sobre los escenarios A (aleatorio), B (casi
ordenado) y C (orden inverso) para siete tamanos de entrada, registra
el tiempo de ejecucion y el numero de comparaciones, y produce dos
graficas en la carpeta graficas/.

Uso:
    python parte3_casos.py
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

from algoritmos import insertion_sort  # noqa: E402
from datos import (  # noqa: E402
    generar_aleatorio,
    generar_casi_ordenado,
    generar_inverso,
)

TAMANOS: list[int] = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES: int = 3
GRAFICAS = "graficas"


def medir_escenario(generador: Callable[[int], list[int]],
                    n: int) -> tuple[float, int]:
    """Mide tiempo promedio y comparaciones de insertion sort en un escenario.

    El tiempo de generacion de los datos no se cronometra: la medicion
    cubre unicamente la llamada al algoritmo.

    Args:
        generador: funcion que produce un lote de n registros.
        n: tamanio de entrada del lote.

    Returns:
        Tupla con el tiempo promedio en segundos y el numero promedio
        de comparaciones.
    """
    tiempos: list[float] = []
    comparaciones_totales: int = 0

    for _ in range(REPETICIONES):
        datos = generador(n)
        inicio = time.perf_counter()
        _, comparaciones = insertion_sort(datos)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
        comparaciones_totales += comparaciones

    promedio_tiempo: float = sum(tiempos) / len(tiempos)
    promedio_comparaciones: int = comparaciones_totales // len(tiempos)
    return promedio_tiempo, promedio_comparaciones


def graficar(tamanos: list[int], series: dict[str, list], ylabel: str,
             nombre: str) -> None:
    """Grafica una serie por escenario y guarda la figura en graficas/.

    Args:
        tamanos: tamanos de entrada del eje x.
        series: diccionario nombre de escenario -> valores del eje y.
        ylabel: etiqueta del eje y.
        nombre: nombre del archivo de salida (PNG).
    """
    fig, ax = plt.subplots()
    for etiqueta, valores in series.items():
        ax.plot(tamanos, valores, marker="o", label=etiqueta)

    ax.set_title(f"Insertion sort - {ylabel}")
    ax.set_xlabel("Tamanio de entrada (registros)")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    carpeta = _DIR / GRAFICAS
    carpeta.mkdir(exist_ok=True)
    fig.savefig(carpeta / nombre, dpi=150)
    plt.close(fig)


def main() -> None:
    """Ejecuta el experimento y genera las dos graficas de la Parte 3."""
    escenarios: dict[str, Callable[[int], list[int]]] = {
        "A - Aleatorio": generar_aleatorio,
        "B - Casi ordenado": generar_casi_ordenado,
        "C - Orden inverso": generar_inverso,
    }

    tiempos: dict[str, list[float]] = {k: [] for k in escenarios}
    comparaciones: dict[str, list[int]] = {k: [] for k in escenarios}

    for n in TAMANOS:
        print(f"Midiendo insertion_sort para n = {n} ...")
        for nombre, generador in escenarios.items():
            tiempo, comp = medir_escenario(generador, n)
            tiempos[nombre].append(tiempo)
            comparaciones[nombre].append(comp)
            print(f"  {nombre}: tiempo = {tiempo * 1000:.2f} ms, "
                  f"comparaciones = {comp}")

    graficar(TAMANOS, comparaciones,
             "Comparaciones entre elementos", "parte3_comparaciones.png")
    graficar(TAMANOS, tiempos,
             "Tiempo de ejecucion (s)", "parte3_tiempo.png")
    print("Graficas guardadas en graficas/.")


if __name__ == "__main__":
    main()