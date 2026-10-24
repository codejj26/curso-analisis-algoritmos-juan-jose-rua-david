# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Juan José Rúa David · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-21 23:59 · **Versión revisada:** commit `1423edc`

Excelente trabajo: un informe completo, ordenado y apoyado en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 19 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 24 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **98 / 100** |
| **Nota (0–5)** | **4.90** |

## 1. Corrección conceptual (19 / 20)
**Lo que hizo bien:**
- Identificó que el cruce entre los dos algoritmos ocurre entre 10 y 50 registros y explicó que se debe al costo fijo de las llamadas recursivas.
- Comparó con el máximo de un arreglo: combinar cuesta solo Θ(1), así que dividir no cambia el orden Θ(n).
- Recomendó divide y vencerás y declaró la cifra a 1.000.000 de registros como estimación, escalando con n log n y n² en vez de una regla de tres lineal.

**Lo que puede mejorar:**
- La estimación parte de una sola medición (n = 4000); sería más sólida si mencionara que las constantes pueden cambiar con tamaños tan grandes (memoria, profundidad de la recursión).

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Planteó `T(n) = 2T(n/2) + Θ(n)` explicando de dónde sale cada término y la resolvió con el método maestro, verificando la condición del Caso 2.
- Justificó el Θ(n²) de la fuerza bruta contando las iteraciones: n(n+1)/2.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan la suma correcta en todos los casos pedidos (ocho días, un elemento, todos negativos, todos positivos, caso cruzado) y coinciden en las veinte listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos sin usar la fuerza bruta y no modifica la lista recibida.
- Tiene *type hints* y *docstrings* en todas las funciones.

## 4. Calidad del análisis de las gráficas (24 / 25)
**Lo que hizo bien:**
- La gráfica tiene título, ejes rotulados y leyenda, con ambas curvas en los mismos ejes y seis tamaños. En ella se lee unos 0,7 s para la fuerza bruta en n = 4000, coherente con su tabla.
- Calculó los factores de crecimiento al duplicar n (×4,12 y ×2,16; ×4,50 y ×2,79) y los contrastó con Θ(n²) y Θ(n log n).
- Incluyó una tabla con los valores medidos para ver los tamaños pequeños.

**Lo que puede mejorar:**
- El eje dice "promedio" pero usted calculó la mediana.
- Al comparar con Θ(n log n), conviene explicar por qué ×2,79 queda por encima de lo esperado (ruido de medición).

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Siguió la estructura de carpetas acordada, el informe respeta el orden pedido, la gráfica se ve y cada parte enlaza su código.
- Incluyó instrucciones de reproducción y cinco commits descriptivos del laboratorio.

## ¿El código funciona?
Sí. Las pruebas pasan, probé sus funciones con listas aleatorias adicionales y coinciden con el resultado de referencia, y la medición corre y genera la gráfica.

## Para el próximo laboratorio
- Mantenga el rótulo de los ejes consistente con lo que calcula (mediana o promedio).
- Explique las diferencias entre lo medido y lo teórico, por ejemplo cuando un factor sale más alto de lo esperado.
- Verifique que todas las funciones tengan docstring con Args y Returns, type hints y dos líneas en blanco entre ellas.
