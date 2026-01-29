import os
import winsound
import pytest

fichas= ['o','x']
def mostrar_tablero(n, movimientos_jugadores):
    for i in range(n):
        for j in range(n):
            casilla_vacia = True
            for k in range(len(movimientos_jugadores)):
                movimientos_jugador= movimientos_jugadores[k]
                if i in movimientos_jugador:
                    if j in movimientos_jugador[i]:
                        print(fichas[k],end='')
                        casilla_vacia= False
            if casilla_vacia:
                print('_ ',end='')
        print()

@pytest.fixture
def tablero_dimension():
    return 3

@pytest.fixture
def movimientos_ambos_jugadores():
    return [{},{}]

@pytest.fixture
def movimientos_vacios():
    return {}, {}

@pytest.fixture
def movimientos_ocupados():
    return {2: [3]}

@pytest.fixture
def movimientos_fuera_tablero(tablero_dimension):
    return tablero_dimension + 1, tablero_dimension + 1

@pytest.fixture
def movimientos_no_ganador():
    return {2: [2, 3]}
@pytest.fixture
def movimientos_ganador():
    # Esto representa una columna: (0,1), (1,1), (2,1)
    return {0: [1], 1: [1], 2: [1]}

def test_no_ganador(movimientos_no_ganador):
    assert not jugada_ganadora(movimientos_no_ganador)

def movimiento_valido(n, x, y, movimientos_otro_jugador):
    if x > n or y > n:
        return False

    if x in movimientos_otro_jugador:
        movimientos_en_columna= movimientos_otro_jugador[x]
        if y in movimientos_en_columna:
            return False
    return True

def test_mostrar_tablero(tablero_dimension, movimientos_ambos_jugadores, capsys):
    mostrar_tablero(tablero_dimension, movimientos_ambos_jugadores)
    captured = capsys.readouterr()
    lineas = captured.out.strip().split("\n")
    lineas= [l for l in lineas if l]
    assert len(lineas) == tablero_dimension
    for linea in lineas:
        assert len(linea.replace(' ', '')) == tablero_dimension

def test_movimiento_columna_fuera_tablero(tablero_dimension, movimientos_vacios):
    movimientos_otro_jugador, _ = movimientos_vacios
    x = 1
    y = tablero_dimension + 1
    assert not movimiento_valido(tablero_dimension, x, y, movimientos_otro_jugador)
def test_movimiento_fila_y_columna_fuera_tablero(tablero_dimension, movimientos_vacios,movimientos_fuera_tablero):
    movimientos_otro_jugador, _ = movimientos_vacios
    x, y = movimientos_fuera_tablero
    assert not movimiento_valido(tablero_dimension, x, y, movimientos_otro_jugador)
def test_movimiento_incorrecto(tablero_dimension, movimientos_ocupados):
    x = 2
    y = 3
    assert not movimiento_valido(tablero_dimension, x, y, movimientos_ocupados)

def test_ganador(movimientos_ganador):
    assert jugada_ganadora(movimientos_ganador)

def jugada_ganadora(movimientos_jugador, n=3):
    # 1. Comprobar FILAS
    for fila in movimientos_jugador:
        if len(movimientos_jugador[fila]) == n:
            return True

    # Creamos una lista de todos los puntos (x, y) para facilitar el chequeo
    puntos = []
    for x, columnas in movimientos_jugador.items():
        for y in columnas:
            puntos.append((x, y))

    # 2. Comprobar COLUMNAS
    for j in range(n):
        columna = [p for p in puntos if p[1] == j]
        if len(columna) == n:
            return True

    # 3. Comprobar DIAGONAL PRINCIPAL (0,0), (1,1), (2,2)...
    diagonal_primaria = [p for p in puntos if p[0] == p[1]]
    if len(diagonal_primaria) == n:
        return True

    # 4. Comprobar DIAGONAL SECUNDARIA (0,2), (1,1), (2,0)...
    diagonal_secundaria = [p for p in puntos if p[0] + p[1] == n - 1]
    if len(diagonal_secundaria) == n:
        return True

    return False

if __name__ == "__main__":
    #Pedimos el tamaño del tablero en que se va a realizar el juego
    n=int(input('Introduce el tamaño del tablero cuadrado:'))
    
    casillas_libres = n*n
    jugador_activo = 0
    
    movimientos_jugador_1 = {}
    movimientos_jugador_2 = {}
    movimientos_jugadores = [movimientos_jugador_1, movimientos_jugador_2]
    
    mostrar_tablero(n,movimientos_jugadores)
    while casillas_libres > 0:
        casilla_jugador = input(f"JUGADOR {jugador_activo+1}: Introduce movimiento (x,y):")
        casilla_jugador= casilla_jugador.strip()
        x= int(casilla_jugador.split(',')[0])-1
        y= int(casilla_jugador.split(',')[1])-1
        print(casilla_jugador,x,y)
        movimientos_jugador_activo= movimientos_jugadores[jugador_activo]
        movimientos_otro_jugador = movimientos_jugadores[(jugador_activo+1)%2]
        if movimiento_valido(x,y, movimientos_otro_jugador):
            mov_col= movimientos_jugador_activo.get(x,[])
            mov_col.append(y)
            movimientos_jugador_activo[x]= mov_col
            clear = lambda: os.system('cls')
            clear()
            mostrar_tablero(n, movimientos_jugadores)
            if jugada_ganadora(movimientos_jugador_activo):
                print(F"ENHORABUENA EL JUGADOR {jugador_activo+1} HA GANADO")
                break
        else:
            frequency = 2000 # Set Frequency To 2500 Hertz
            duration = 1000 # Set Duration To 1000 ms == 1 second
            print('\a')
            winsound.Beep(frequency, duration)
            print("Movimiento invalido. Turno para el siguiente jugador")
            casillas_libres= casillas_libres -1
            jugador_activo = (jugador_activo+1)