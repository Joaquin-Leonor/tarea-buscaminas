import random

tablero = []
visible = []
minas = []
filas_cols = 0
num_minas = 0
primer_movimiento = True


def generar_minas(filas_cols, num_minas):
    global minas
    minas = [True] * num_minas + [False] * (filas_cols ** 2 - num_minas)
    random.shuffle(minas)
    return [minas[i:i+filas_cols] for i in range(0, len(minas), filas_cols)]


def generar_tablero():
    global visible
    visible = []

    for i in range(filas_cols):
        fila = []
        for j in range(filas_cols):
            fila.append(".")
        visible.append(fila)


def imprimir_tablero():

    print("   ", end="")
    for i in range(filas_cols):
        print(f"{i+1:2}", end=" ")
    print()

    for i in range(filas_cols):
        letra = chr(65+i)
        print(f"{letra}  ", end="")

        for j in range(filas_cols):
            print(f"{visible[i][j]:2}", end=" ")
        print()


def iniciar_partida():
    global tablero, primer_movimiento

    tablero = generar_minas(filas_cols, num_minas)
    generar_tablero()
    primer_movimiento = True


def buscar_coordenada(txt):

    if " " in txt:
        return None

    try:
        fila = ord(txt[0].upper()) - 65
        col = int(txt[1:]) - 1

        if fila >= 0 and fila < filas_cols and col >= 0 and col < filas_cols:
            return fila, col
    except:
        return None

    return None

def esta_revelada(f, c):
    return visible[f][c] != "."


def es_mina(f, c):
    return tablero[f][c] == True

def vecinos(f, c):

    lista = []

    for i in range(f-1, f+2):
        for j in range(c-1, c+2):

            if 0 <= i < filas_cols and 0 <= j < filas_cols:
                if not (i == f and j == c):
                    lista.append((i, j))

    return lista

def contar_minas(f, c):

    total = 0

    for i, j in vecinos(f, c):
        if tablero[i][j]:
            total += 1

    return total

def desplazar_mina(f, c):

    global tablero

    if not tablero[f][c]:
        return

    for i in range(filas_cols):
        for j in range(filas_cols):

            if not tablero[i][j]:
                tablero[i][j] = True
                tablero[f][c] = False
                return

def mostrar_contenido(f, c):

    pila = [(f, c)]

    while pila:

        x, y = pila.pop()

        if visible[x][y] != ".":
            continue

        minas_alrededor = contar_minas(x, y)

        if minas_alrededor > 0:
            visible[x][y] = str(minas_alrededor)
        else:
            visible[x][y] = " "

            for i, j in vecinos(x, y):
                if visible[i][j] == ".":
                    pila.append((i, j))


def mostrar_minas():

    for i in range(filas_cols):
        for j in range(filas_cols):

            if tablero[i][j]:
                visible[i][j] = "*"


def revelar_coordenada(f, c):

    global primer_movimiento

    if primer_movimiento:
        desplazar_mina(f, c)
        primer_movimiento = False

    if es_mina(f, c):
        mostrar_minas()
        imprimir_tablero()
        print("\nPerdiste")
        return False

    mostrar_contenido(f, c)
    return True


def pedir_coordenada():

    while True:

        txt = input("Introduce coordenada sin espacios: " .title())
        pos = buscar_coordenada(txt)

        if pos is None:
            print("Coordenada inválida por colocar espacio" .title())
            continue


        f, c = pos

        if esta_revelada(f, c):
            print("Casilla ya revelada")
            continue

        return f, c


def partida():

    iniciar_partida()

    while True:

        imprimir_tablero()

        f, c = pedir_coordenada()

        if not revelar_coordenada(f, c):
            break

        ocultas = 0
        for fila in visible:
            ocultas += fila.count(".")

        if ocultas == num_minas:
            imprimir_tablero()
            print("\nGanaste")
            break


def menu():

    global filas_cols, num_minas

    while True:

        print("\n=== BUSCAMINAS ===")
        print("1. Normal".upper())
        print("2. Avanzado".upper())
        print("3. Salir del juego" .upper())

        op = input("Opcion: ")

        if op == "1":
            filas_cols = 9
            num_minas = 10
            partida()

        elif op == "2":
            filas_cols = 16
            num_minas = 25
            partida()

        elif op == "3":
            break


menu()
