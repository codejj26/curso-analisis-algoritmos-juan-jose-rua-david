# Retroalimentación — Laboratorio 1: Fundamentos, complejidad y recurrencias

**Estudiante:** Juan José Rúa David · **Laboratorio:** Laboratorio evaluativo 01 — Plataforma Tamiza
**Fecha límite:** 2026-10-04 23:59 · **Versión revisada:** commit `901055d`

Muy buen trabajo: un informe completo, ordenado y apoyado en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 23 / 25 |
| Calidad de la explicación teórica | 23 / 25 |
| Corrección de la implementación | 17 / 20 |
| Calidad del análisis de las gráficas | 18 / 20 |
| Documentación y organización del informe | 9 / 10 |
| **Total** | **90 / 100** |
| **Nota (0–5)** | **4.50** |

## 1. Corrección conceptual (23 / 25)
**Lo que hizo bien:**
- Distingue con claridad entre algoritmo correcto y algoritmo viable, y nombra la restricción que se incumple: la ventana de cuatro horas.
- Explica bien que un servidor el doble de rápido solo divide el tiempo por dos, mientras el algoritmo crece con el cuadrado.
- El segundo ejemplo (el buscador de ~30.000 registros que congelaba la interfaz) es propio, con datos y con la restricción de tiempo de respuesta.
- En la parte ética identifica dos perjuicios (el paciente y el operador del centro de contacto) y dice quién asume el costo de cada uno. También discute la obligación que impone que el orden decida a quién se llama primero.

**Lo que puede mejorar:**
- La parte ambiental queda en lo cualitativo: se echa de menos una cifra aproximada de horas de servidor al año para ver el tamaño real del consumo.
- El ejemplo del buscador queda sin cifras de tiempo concretas ("varios segundos").

## 2. Calidad de la explicación teórica (23 /25)
**Lo que hizo bien:**
- Define los tres casos indicando sobre qué se toma el máximo, el mínimo y el promedio, y justifica por qué usaría el peor caso.
- Escribe la predicción antes de medir y la contrasta después con honestidad, explicando el matiz del escenario B.
- Plantea la recurrencia de merge sort explicando cada término y la resuelve con el método maestro, verificando la condición del caso 2.
- El análisis línea a línea de insertion sort y la tabla de complejidades están completos.

**Lo que puede mejorar:**
- En el análisis línea a línea, el mejor caso y el caso promedio se resumen en pocas frases; faltó escribir también esas sumas.
- Faltó explicar que la tabla muestra la complejidad "esperada" y que merge sort en su implementación hace entre (n log n)/2 y n log n comparaciones.

## 3. Corrección de la implementación (17 / 20)
**Lo que hizo bien:**
- Ambos algoritmos ordenan bien (de mayor a menor), no modifican la lista recibida, cuentan solo comparaciones entre elementos y no usan `sorted()` ni `list.sort()`.
- `merge_sort` tiene su propia mezcla recursiva.
- Los generadores producen valores distintos, del tamaño pedido y con semilla.

**Lo que puede mejorar:**
- Estilo PEP 8: falta una línea en blanco antes de `insertion_sort` y los archivos no terminan con salto de línea.
- La función interna `_merge_sort` no tiene su descripción (docstring).
- En el escenario B el 2 % final son los valores más grandes del lote, así que no es un "casi ordenado" típico; usted lo explica bien, pero conviene escoger esos valores al azar.

## 4. Calidad del análisis de las gráficas (18 /20)
**Lo que hizo bien:**
- Las tres gráficas existen, con título, ejes rotulados, unidades y leyenda, y las curvas están en los mismos ejes.
- Identifica con datos el peor caso (C), el mejor (B) y el promedio (A).
- La lectura de la gráfica de la Parte 4 es concreta (el tiempo se multiplica por casi 8 frente a 3,5) y la compara con lo calculado.
- El concepto técnico recomienda merge sort, extrapola a 1.200.000 registros declarándolo estimación y responde con un dato medido a la propuesta del servidor.

**Lo que puede mejorar:**
- En la gráfica de la Parte 4, merge sort queda casi pegada al eje; una escala logarítmica o un recuadro ampliado permitiría ver su forma.
- Los tiempos de insertion sort en n = 6400 difieren entre la Parte 3 y la Parte 4 (2,97 s y 2,57 s) y no lo comenta.

## 5. Documentación y organización del informe (9 / 10)
**Lo que hizo bien:**
- Carpeta y archivos con los nombres pedidos, gráficas incrustadas con ruta correcta, enlaces al código en cada parte y 12 commits con mensajes descriptivos.

**Lo que puede mejorar:**
- Las instrucciones de reproducción solo muestran los comandos de Windows; agregue los de Linux/macOS.

## ¿El código funciona?
Sí. Los scripts corren sin errores, ordenan correctamente los tres escenarios y generan las tres gráficas.

## Para el próximo laboratorio
- Revise el estilo con una herramienta de PEP 8 antes de entregar y ponga docstring a todas las funciones, incluidas las internas.
- Acompañe los argumentos ambientales con una cifra estimada.
- Use escala logarítmica cuando una curva quede aplastada por otra.
- Explique las pequeñas diferencias entre mediciones repetidas del mismo caso.
- Incluya instrucciones para todos los sistemas operativos.
