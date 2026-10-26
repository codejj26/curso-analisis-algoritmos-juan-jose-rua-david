"""Pruebas assert para las estructuras del lab 3 (exento de PEP 8 estricto)."""

import random

from estructuras import ListaEnlazada, TablaHash


def probar_lista():
    lista = ListaEnlazada()
    assert lista.buscar(123) is None
    lista.insertar(123, "en bodega")
    lista.insertar(456, "en reparto")
    assert lista.buscar(123) == "en bodega"
    assert lista.buscar(456) == "en reparto"
    assert lista.buscar(789) is None
    assert lista.tamano == 2
    print("OK: lista enlazada, busqueda exitosa e infructuosa")


def probar_colision_forzada():
    tabla = TablaHash(7)
    # 10 % 7 = 3, 24 % 7 = 3, 17 % 7 = 3: las tres caen en la casilla 3.
    for guia in (10, 24, 17):
        assert tabla.hash(guia) == 3
        tabla.insertar(guia, "en bodega")
    assert tabla.buscar(10) == "en bodega"
    assert tabla.buscar(24) == "en bodega"
    assert tabla.buscar(17) == "en bodega"
    assert tabla.buscar(99) is None
    assert tabla.casillas[3].tamano == 3
    assert tabla.factor_carga() == 3 / 7
    assert tabla.tamano == 3
    print("OK: colision forzada con m=7 y factor de carga 3/7")


def probar_colecciones_aleatorias(cantidad_colecciones=20):
    azar = random.Random(42)
    for i in range(cantidad_colecciones):
        numero_guias = azar.randint(5, 80)
        m = azar.choice([3, 7, 11, 13, 17, 31])
        guias = azar.sample(range(10**9, 10**10), numero_guias)
        estados = ["en bodega", "en reparto", "entregado", "en ruta"]

        datos = {guia: azar.choice(estados) for guia in guias}

        lista = ListaEnlazada()
        tabla = TablaHash(m)
        for guia, estado in datos.items():
            lista.insertar(guia, estado)
            tabla.insertar(guia, estado)

        # Todas las guias existentes deben dar lo mismo.
        for guia in guias:
            assert lista.buscar(guia) == tabla.buscar(guia) == datos[guia]

        # Guias inexistentes deben dar lo mismo (None).
        for _ in range(numero_guias):
            inexistente = azar.randint(10**9, 10**10 - 1)
            while inexistente in datos:
                inexistente = azar.randint(10**9, 10**10 - 1)
            assert lista.buscar(inexistente) is None
            assert tabla.buscar(inexistente) is None
    print(f"OK: {cantidad_colecciones} colecciones aleatorias, lista == tabla")


if __name__ == "__main__":
    probar_lista()
    probar_colision_forzada()
    probar_colecciones_aleatorias()
    print("Todas las pruebas pasaron.")
