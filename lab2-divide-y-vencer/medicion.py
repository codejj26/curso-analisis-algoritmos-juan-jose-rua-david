"""Experimento de la Parte 2: fuerza bruta vs. divide y venceras.

Mide el tiempo de ambas soluciones del subarreglo maximo sobre la misma
serie aleatoria para varios tamanos de entrada, verifica que las dos
devuelven la misma suma y produce la grafica graficas/tiempo_vs_n.png.

Uso:
    python medicion.py
"""

import random
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

from subarreglo import (  # noqa: E402
    subarreglo_fuerza_bruta,
    subarreglo_maximo,
)

TAMANOS: list[int] = [10, 50, 100, 500, 1000, 4000]
REPETICIONES: int = 3
SEMILLA: int = 2026


def generar_serie(n: int, semilla: int = SEMILLA) -> list[int]:
    """Genera una serie de n variaciones diarias reproducibles.

    Args:
        n: cantidad de dias de la serie.
        semilla: semilla del generador aleatorio, para que el
            experimento sea reproducible.

    Returns:
        Lista de n enteros entre -100 y 100.
    """
    generador = random.Random(semilla)
    return [generador.randint(-100, 100) for _ in range(n)]


def medir_mediana(
    calcular: Callable[[], tuple[int, int, float]], repeticiones: int
) -> float:
    """Mide la mediana del tiempo de una llamada al algoritmo.

    Se usa la mediana para reducir el efecto de los picos de ruido del
    sistema operativo. El tiempo de generacion de los datos no se
    cronometra: la medicion cubre unicamente la llamada al algoritmo.

    Args:
        calcular: llamada a cronometrar.
        repeticiones: numero de corridas a considerar.

    Returns:
        Mediana del tiempo en segundos.
    """
    tiempos: list[float] = []

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        calcular()
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    tiempos.sort()
    return tiempos[len(tiempos) // 2]


def main() -> None:
    """Ejecuta el experimento y genera la grafica de la Parte 2."""
    tiempos_fuerza: list[float] = []
    tiempos_divide: list[float] = []

    for n in TAMANOS:
        datos = generar_serie(n)
        tiempo_fuerza = medir_mediana(
            lambda: subarreglo_fuerza_bruta(datos), REPETICIONES
        )
        tiempo_divide = medir_mediana(
            lambda: subarreglo_maximo(datos, 0, n - 1), REPETICIONES
        )

        suma_fuerza = subarreglo_fuerza_bruta(datos)[2]
        suma_divide = subarreglo_maximo(datos, 0, n - 1)[2]
        assert suma_fuerza == suma_divide, (
            f"Las sumas difieren en n = {n}: "
            f"{suma_fuerza} != {suma_divide}"
        )

        tiempos_fuerza.append(tiempo_fuerza)
        tiempos_divide.append(tiempo_divide)
        print(f"n = {n}: fuerza bruta = {tiempo_fuerza * 1000:.4f} ms, "
              f"divide y venceras = {tiempo_divide * 1000:.4f} ms, "
              f"suma = {suma_divide}")

    fig, ax = plt.subplots()
    ax.plot(TAMANOS, tiempos_fuerza, marker="o",
            label="Fuerza bruta")
    ax.plot(TAMANOS, tiempos_divide, marker="s",
            label="Divide y venceras")

    ax.set_title("Subarreglo maximo: fuerza bruta vs. divide y venceras")
    ax.set_xlabel("Tamano de entrada (registros)")
    ax.set_ylabel("Tiempo de ejecucion promedio (s)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    carpeta = _DIR / "graficas"
    carpeta.mkdir(exist_ok=True)
    fig.savefig(carpeta / "tiempo_vs_n.png", dpi=150)
    plt.close(fig)
    print("Grafica guardada en graficas/tiempo_vs_n.png.")


if __name__ == "__main__":
    main()
