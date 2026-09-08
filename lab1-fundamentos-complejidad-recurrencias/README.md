# Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias

**Autor:** Juan Jose Rua David
**Curso:** Analisis de Algoritmos
**Caso:** Plataforma Tamiza — Secretaria de Salud departamental

## Instrucciones para reproducir el experimento

1. Desde la raiz del repositorio, active el entorno virtual y verifique que
   matplotlib esta instalado:

   ```bash
   # Windows
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Entre a la carpeta del laboratorio:

   ```bash
   cd lab1-fundamentos-complejidad-recurrencias
   ```

3. Ejecute la Parte 3 (insertion sort sobre los tres escenarios, genera
   `graficas/parte3_comparaciones.png` y `graficas/parte3_tiempo.png`):

   ```bash
   python parte3_casos.py
   ```

4. Ejecute la Parte 4 (comparacion temporal entre algoritmos, genera
   `graficas/parte4_tiempo.png`):

   ```bash
   python parte4_complejidad.py
   ```

Todo el codigo se ejecuta con el interpretador del entorno virtual
(`venv/`). Cada medicion se repite tres veces y se grafica el promedio
para reducir el ruido del sistema operativo.

---

## Parte 1 — Analizar el algoritmo antes de comprar hardware

> [!IMPORTANT]
> Esquema de trabajo. Redacta esta seccion con TUS palabras en un maximo
> de 500 palabras. Verifica cada punto antes de pasarla al informe final.

### Guia de respuesta

**Distinguir correccion de eficiencia** (requisito 1):
- [ ] Define con tus palabras lo que significa que un algoritmo sea *correcto*
      para Tamiza: producir la lista de llamadas ordenada por riesgo.
- [ ] Define con tus palabras lo que significa que sea *viable*: producirla
      dentro de la ventana de cuatro horas (2:00 a. m. – 6:00 a. m.).
- [ ] Explica por que correcto no implica viable, y nombra la restriccion
      concreta que incumple hoy: la ventana de cuatro horas. El proceso ha
      desbordado la ventana tres veces y el centro de contacto trabajo con
      listas parciales.

**Por que duplicar la velocidad del servidor no resuelve el problema de
fondo** (requisito 2):
- [ ] El costo del algoritmo no depende solo de la velocidad del reloj: con
      unos 1.200.000 registros, insertion sort ejecuta del orden de
      n²/2 comparaciones (ver medir en la Parte 3). Duplicar el reloj
      divide el tiempo por 2, pero la cantidad de trabajo sigue creciendo
      con el cuadrado de la entrada; basta que entren mas registros para volver
      a desbordar. Indica que la mejora es un factor constante, no un cambio
      de orden de crecimiento.
- [ ] Respeta la regla: no uses la palabra "eficiente" sin decir respecto a
      que recurso y a que restriccion.

**Segundo ejemplo propio** (requisito 3):
- [ ] Elige un sistema que conozcas o uses. Debe ser concreto: que se
      procesa, aproximadamente cuantos datos y que restriccion se incumple.
      Ejemplos tipo: busqueda lineal sobre N registros con latencia maxima,
      ordenamiento creciente de datos, reindexado de logs, etc.
- [ ] No repitas el caso de la empresa de energia ni el de Tamiza.

---

## Parte 2 — Responsabilidad ambiental y etica de la implementacion

> [!IMPORTANT]
> Esquema de trabajo. Redacta esta seccion con TUS palabras en un maximo
> de 600 palabras.

### Guia de respuesta

**Dimension ambiental**:
- [ ] Explica que el tiempo de ejecucion del proceso nocturno se traduce
      directamente en energia consumida por la CPU (y memoria) del servidor.
      Mas tiempo de CPU = mas energia.
- [ ] Explica la multiplicacion: el proceso corre *todas las madrugadas*,
      todo el ano, y por anos. Un algoritmo cuadratico en 1.200.000 registros
      gasta decenas de miles de veces mas energia que uno n log n, todos los
      dias, de forma acumulada. Haz la cuenta de las horas sobre la ventana y
      de los dias del ano.

**Dimension etica** (requisito 2) — identifica al menos dos perjuicios
concretos a una persona identificable y para cada uno responde quien asume
el costo:
- [ ] Perjuicio 1: un paciente de alto riesgo que no es llamado (la lista
      quedo incompleta y desordenada) deja de ser citado a valoracion y su
      enfermedad avanza sin control. Costo: el paciente. Quien mas: la
      Secretaria (por la prestacion de servicio).
- [ ] Perjuicio 2: el operador del centro de contacto debe llamar con una
      lista parcial y desordenada, sin prioridad real, perdiendo tiempo en
      llamadas de menor urgencia mientras pacientes criticos esperan. Costo:
      el operador y las personas no contactadas.
- [ ] Puedes agregar el costo del re-trabajo y de la confianza en el sistema.

**Tension del orden de la lista** (requisito 3):
- [ ] Discute: el orden decide a quien se llama primero, y quien se llama
      primero recibe atencion antes. Eso impone una obligacion adicional
      sobre la *correccion* del ordenamiento (no solo el tiempo): el orden
      debe estar bien hecho y ser estable/confiable, porque un error no es un
      dato estadistico sino una persona que deja de ser atendida.

---

## Parte 3 — Peor caso, mejor caso y caso promedio, demostrados en Python

Codigo de esta parte:
[algoritmos.py](algoritmos.py), [datos.py](datos.py),
[parte3_casos.py](parte3_casos.py).

### 3.1 — Explicacion

**Definicion de los tres casos** (redacta con tus palabras, pero sobre que se
toma cada extremo o promedio es el dato correcto a decir):

- Peor caso: el **maximo** del tiempo (o de comparaciones) sobre el conjunto
  de entradas de un mismo tamaño fijo n que produce el mayor trabajo. En
  insertion sort es la lista en el **orden inverso** al requerido.
- Mejor caso: el **minimo** sobre las entradas de tamaño fijo n. En insertion
  sort es la lista que **ya esta ordenada** en el sentido requerido.
- Caso promedio: el **promedio** sobre el conjunto de entradas de tamaño fijo
  n (o sobre todas las permutaciones del tamaño n).

**Que caso usar para decidir si el algoritmo entra en produccion:**

Responde a partir de la restriccion: la ventana de cuatro horas es estricta y
**no negociable**, y ademas el canal de entrada puede cambiar sin aviso. Por
eso hay que garantizar el **peor caso**: no basta con que el dia típico quepa.

**Prediccion previa (escrita antes de medir):**

> Con insertion sort ordenando de mayor a menor riesgo:
> - **Escenario A (aleatorio)** se aproxima al **caso promedio**: la lista
>   llega sin ningun orden, cada elemento se desplaza en promedio la mitad
>   de la parte ya ordenada.
> - **Escenario B (casi ordenado)** se aproxima al **mejor caso**: el 98 %
>   ya esta en su lugar, cada elemento requiere pocas comparaciones.
> - **Escenario C (orden inverso, de menor a mayor)** es el **peor caso**:
>   la lista llega exactamente en el orden contrario al que Tamiza necesita,
>   cada elemento debe atravesar todo lo ya ordenado.

### 3.2 — Demostracion experimental

Se midio `insertion_sort` sobre los tres escenarios para tamaños
100, 200, 400, 800, 1600, 3200 y 6400 registros, con `time.perf_counter()`
y contando las comparaciones entre elementos. Cada punto es el promedio de
tres corridas.

![Comparaciones vs. tamaño por escenario](graficas/parte3_comparaciones.png)

![Tiempo vs. tamaño por escenario](graficas/parte3_tiempo.png)

**Resultados (n = 6400, promedio de 3 corridas):**

| Escenario | Comparaciones | Tiempo |
|---|---|---|
| A — Aleatorio | 10.276.753 | 963 ms |
| B — Casi ordenado | 813.455 | 74 ms |
| C — Orden inverso | 20.476.800 | 1.871 ms |

**Analisis:** el escenario C resulto el **peor caso** (≈ n²/2 comparaciones,
tiempo cuadratico), el B el **mejor caso** (tiempo casi lineal) y el A se
aproxima al **caso promedio** (≈ n²/4). Esto **coincide con la prediccion**:
que C sea el peor caso es exactamente lo esperado (el lote llega en el orden
opuesto), y la consistencia se mantuvo gracias a que todos los experimentos
usan el mismo criterio de orden (mayor a menor riesgo).

---

## Parte 4 — Complejidad de merge sort e insertion sort: calculo y validacion

Codigo de esta parte: [parte4_complejidad.py](parte4_complejidad.py).

### 4.1 — Calculo teorico

#### Recurrencia de merge sort

Planteamiento:

```
T(n) = 2·T(n/2) + Θ(n)
```

De donde sale cada termino:
- **2 subproblemas** (a = 2): cada llamada divide el arreglo en dos mitades.
- **Tamanio n/2** (b = 2): cada mitad tiene la mitad de elementos.
- **Θ(n) de combinar**: la mezcla de dos mitades ordenadas recorre, en el
  peor caso, n elementos para unirlas (mas el costo constante de partir).

Resolucion por **metodo maestro**:

1. Identificar los tres ingredientes: a = 2, b = 2, f(n) = Θ(n).
2. Calcular n^(log_b a) = n^(log_2 2) = n^1 = n.
3. Comparar f(n) con n^(log_b a): f(n) = Θ(n) == Θ(n^1), por lo tanto
   f(n) = Θ(n^log_b a).
4. Aplica el **Caso 2** del metodo maestro (f(n) = Θ(n^log_b a)).
5. Conclusion: T(n) = Θ(n^log_b a · log n) = **Θ(n log n)**.

#### Analisis linea a linea de insertion sort

La implementacion (en [algoritmos.py](algoritmos.py)) con sus costos. Sea
t_i el numero de veces que se ejecuta el cuerpo del `while` para el elemento
i, y c_j el costo constante de cada linea:

```python
def insertion_sort(datos):                  # costo  veces
    copia = list(datos)                     #   c1    1
    comparaciones = 0                       #   c2    1
    n = len(copia)                          #   c3    1
    for i in range(1, n):                   #   c4    n
        clave = copia[i]                    #   c5    n-1
        j = i - 1                           #   c6    n-1
        while j >= 0:                       #   c7    Σ(t_i + 1)
            comparaciones += 1              #   c8    Σ t_i
            if copia[j] >= clave:           #   c9    Σ t_i
                break                       #   c10   Σ t_i' (los efectivos)
            copia[j + 1] = copia[j]         #   c11   Σ t_i - Σ t_i'
            j -= 1                          #   c12   Σ t_i - Σ t_i'
        copia[j + 1] = clave                #   c13   n-1
```

Peor caso (lista en orden **inverso** al requerido): para cada i, la clave
debe llegar hasta el inicio, t_i = i y el `break` nunca se ejecuta.

- Σ_{i=1}^{n-1} t_i = 1 + 2 + ... + (n-1) = n(n-1)/2.
- Σ_{i=1}^{n-1} (t_i + 1) = n(n-1)/2 + (n-1).

Sumando todas las lineas:

```
T(n) = c1 + c2 + c3 + c4·n             (lineas de 1 sola ejecucion o del for)
     + (c5 + c6 + c13 + c7)·(n-1)      (lineas que corren n-1 veces, con la
                                         carga del while que agrega n-1)
     + (c7 + c8 + c9 + c11 + c12)·n(n-1)/2
```

El termino dominante es n(n-1)/2 multiplicado por constantes: por lo tanto,
en el peor caso:

```
T(n) = Θ(n²)
```

#### Tabla de complejidades esperadas (por caso)

| Algoritmo | Mejor caso | Caso promedio | Peor caso |
|---|---|---|---|
| Insertion sort | Θ(n) | Θ(n²) | Θ(n²) |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |

### 4.2 — Validacion experimental

Se midio el tiempo de `insertion_sort` y `merge_sort` sobre el escenario A
(aleatorio) de Tamiza, con los mismos tamaños de entrada de la Parte 3,
promedio de tres corridas:

![Merge sort vs. insertion sort — escenario A](graficas/parte4_tiempo.png)

**Resultados destacados:**

| n | Insertion sort | Merge sort |
|---|---|---|
| 100 | 0,21 ms | 0,14 ms |
| 800 | 15,2 ms | 1,46 ms |
| 3200 | 219 ms | 6,31 ms |
| 6400 | 1.006 ms | 16,0 ms |

**Lectura de la grafica:** la curva de insertion sort crece de forma
cuadratica (al duplicar n el tiempo se cuadruplica: de 219 ms a 1.006 ms
al pasar de 3200 a 6400). La curva de merge sort crece de forma casi lineal
(6,31 ms → 16,0 ms) porque n log n crece poco a poco. En n = 100 la ventaja
de merge sort ya existe (0,14 ms frente a 0,21 ms) y se amplia sin parar:
en n = 6400 es unas 63 veces mas rapido.

**Contraste con la teoria:** coincide con lo calculado en 4.1. Aqui no se ve
el cruce clasico (insertion mas rapido para decenas de elementos) porque la
entrada es aleatoria y las constantes de Python de la implementacion recursiva
son bajas; el punto importante es que la tendencia asintotica cuadratica de
insertion se impone ni bien crece n. Para listas decenas de veces mas grandes
la brecha solo crece.

**Conclusion:** para Tamiza conviene **merge sort**, y se lee en la propia
grafica: su curva se mantiene practicamente horizontal respecto de la de
insertion sort a medida que crece el tamaño de entrada.

### 4.3 — Concepto tecnico a la Secretaria de Salud

> [!IMPORTANT]
> Esquema de trabajo. Redacta esta seccion con TUS palabras, en 400-600
> palabras, dirigida al equipo de ingenieria (no al docente). Usa los datos
> medidos abajo.

**Recomendacion de algoritmo** (requisito 1):
- [ ] Recomienda **merge sort** como unico algoritmo en produccion.
- [ ] Justifica el compromiso: el canal de entrada (A, B o C) puede cambiar
      sin aviso y Tamiza no quiere mantener tres implementaciones. Merge sort
      es el unico de los dos cuyo peor caso garantiza la ventana *para
      cualquier escenario*, mientras que insertion sort solo es rapido en B.

**Estimacion para 1.200.000 registros** (requisito 2) — declara que es una
estimacion, no una medicion, y usa la forma de las curvas (nunca regla de tres):
- [ ] Insertion sort actual, escenario A: en n = 6400 midió ~1,006 s. Si el
      tamaño crece k veces, un algoritmo cuadratico multiplica el tiempo por
      k². k = 1.200.000 / 6400 ≈ 187,5 → 1,006 s × 187,5² ≈ 9,8 horas.
      **Desborda las 4 horas.** En el escenario C (peor caso) seria aun peor
      (≈ 18 horas).
- [ ] Merge sort recomendado: tiempo ≈ t₀ × k × (log N / log n₀) con t₀ =
      0,016 s, k = 187,5, log₂(1.200.000) / log₂(6400) ≈ 1,6 → ≈ 5 segundos.
      **Cabe con margen enorme en las 4 horas.**
- [ ] Declara explícitamente que la extrapolacion supone que la relacion
      medida se mantiene y que es una estimacion (el dato mas solido es que
      incluso multiplicando el estimado por 100, merge sort sigue dentro de
      la ventana).

**Respuesta a la compra del servidor del doble de velocidad** (requisito 3),
con un dato medido por ti:
- [ ] Cita la grafica `parte3_tiempo.png` y el punto n = 6400 del escenario A
      (~1,006 s). Duplicar el reloj divide ese tiempo por 2, pero el costo
      sigue siendo cuadratico: en 1.200.000 registros seguiria tomando ~4,9
      horas — sobre la ventana, casi sin margen— y en el escenario C (peor
      caso) el tiempo se duplicaria y volveria a desbordar igual. El servidor
      nuevo es un factor constante; el problema es el orden de crecimiento.

**Consideracion distinta del tiempo** (requisito 4) — elige al menos una:
- [ ] **Memoria adicional de merge sort:** O(n) auxiliar frente a O(1) en
      insertion sort. Con 1.200.000 enteros es ~10 MB; manejable, pero hay
      que declararlo en la operacion.
- [ ] Estabilidad y orden: merge sort mezcla de forma estable; el orden final
      es deterministico entre pacientes con igual riesgo, lo que importa por
      el efecto sobre quien se llama primero.
- [ ] Riesgo de escenario B: si cambia el flujo de reproceso, el lote deja de
      ser casi ordenado y insertion sort pierde su unica ventaja; merge sort
      es inmune a ese cambio.
- [ ] Costo de mantenimiento: una sola implementacion, probada y con tests.

- [ ] No escribas "en este laboratorio aprendi": es un concepto tecnico.