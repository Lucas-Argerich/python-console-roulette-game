from random import randint

# FUNCIONES

# Funciones de Programa:


def getValance():  # FUNCIÓN PARA INGRESAR EL VALANCE DEL USUARIO
    valance = input("¿Con cuanto Dinero ingresa a la Ruleta?: ")
    valance = valance.lstrip(
        "$"
    )  # Se puede mejorar el filtro con isdigit, isalnum, etc...
    return int(valance)


def getNumber():  # FUNCIÓN PARA "GIRAR" LA RULETA
    num = randint(0, 36)
    return num


def menuRecursivo(dict, path):  # MENU RECURSIVO PARA SELECCIONAR LAS APUESTAS
    printLinea()

    keys = dict.keys()
    print("Ingrese a que categoría quiere entrar:")

    for key in keys:
        print(key.upper(), end=" ")
    print()

    category = input()
    category = category.lower()
    print()

    if category in keys:
        path.append(category)
        if type(dict[category]) is int:
            n = int(input("Cuanto quieres apostar a {}?: ".format(category.upper())))
        else:
            return menuRecursivo(dict[category], path)
    else:
        res = askUser(
            "Se ingresó una categoría nula o en blanco, ¿desea seguir navegando?: "
        )
        if res:
            return menuRecursivo(dict, path)
        else:
            n = -1
    return [n, path]


def setApuestas(valance):  # FUNCIÓN DE INGRESO DE APUESTAS
    apuestas = {
        "colores": {"rojo": 0, "negro": 0},
        "paridad": {"par": 0, "impar": 0},
        "conjuntos": {"1a12": 0, "13a24": 0, "25a36": 0},
        "mitades": {"1a18": 0, "19a36": 0},
        "filas": {"fila1": 0, "fila2": 0, "fila3": 0},
        "numeros": dict((str(i), 0) for i in range(37)),
    }
    print()
    printCentrado("¡HORA DE APOSTAR!")
    apostando = True
    total = 0
    while apostando:
        value, path = menuRecursivo(apuestas, [])  # (lista de apuestas, lista de path)
        if value != -1:
            if total + value <= valance:
                total += value
                apuestas[path[0]][path[1]] += value
            else:
                print(
                    "No cuentas con el valance suficiente para la ultima apuesta. No será efectuada."
                )
        res = askUser("¿Desea hacer otra apuesta?: ")
        if not res:
            apostando = False
    return apuestas


def processApuesta(apuestas, numero):
    rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    esRojo = numero in rojos
    esNegro = numero not in rojos and numero != 0
    esPar = numero % 2 == 0 and numero != 0
    esImpar = numero % 2 != 0
    es1a12 = numero >= 1 and numero <= 12
    es13a24 = numero >= 13 and numero <= 24
    es25a36 = numero >= 25 and numero <= 36
    es1a18 = numero >= 1 and numero <= 18
    es19a36 = numero >= 19 and numero <= 36
    esFila1 = numero % 3 == 0 and numero != 0
    esFila2 = (numero + 1) % 3 == 0
    esFila3 = (numero + 2) % 3 == 0

    premio = 0
    for i in apuestas:
        for a, b in apuestas[i].items():
            if b > 0:
                if a == "rojos" and esRojo:
                    premio += b * 2
                elif a == "negros" and esNegro:
                    premio += b * 2
                elif a == "par" and esPar:
                    premio += b * 2
                elif a == "impar" and esImpar:
                    premio += b * 2
                elif a == "1a18" and es1a18:
                    premio += b * 2
                elif a == "19a36" and es19a36:
                    premio += b * 2
                elif a == "1a12" and es1a12:
                    premio += b * 3
                elif a == "13a24" and es13a24:
                    premio += b * 3
                elif a == "25a36" and es25a36:
                    premio += b * 3
                elif a == "fila1" and esFila1:
                    premio += b * 3
                elif a == "fila2" and esFila2:
                    premio += b * 3
                elif a == "fila3" and esFila3:
                    premio += b * 3
                elif a == str(numero):
                    premio += b * 36
                else:
                    premio -= b
    return premio


# Funciones Visuales:
# (Funciones innecesarias, pero hacen el código mas legible y entendible)


def printCentrado(str):  # PRINT CENTRADO CON ANCHO PREDEFINIDO
    print(str.center(ANCHO_DE_CONSOLA, " "))


def printLinea():  # PRINT DE UNA LINEA
    print("".center(ANCHO_DE_CONSOLA, "—"))


def askUser(str):  # FUNCIÓN DE INGRESO DE PREGUNTA, DEVUELVE VERDADERO O FALSO
    question = input(str)
    question.lower()
    return question == "si" or question == "s"


def showValance(n):  # MOSTRAR EL VALANCE EN CONSOLA
    text = "USTED CUENTA CON $" + str(n)
    printCentrado("".center(len(text), "#"))
    printCentrado(text)
    printCentrado("".center(len(text), "#"))


def showNumber(n):  # MOSTRAR EL NUMERO DE RULETA
    text = "# " + str(n) + " #"
    printCentrado("".center(len(text), "#"))
    printCentrado(text)
    printCentrado("".center(len(text), "#"))


def showTable(numerosSeleccionados):  # MOSTRAR EL TABLERO
    numeros = [i for i in range(37)]
    for i in range(len(numeros)):
        if numerosSeleccionados[i] > 0:
            numeros[i] = "●"

    tableLength = 39
    row1 = ""
    row2 = ""
    row3 = ""

    for i in range(len(numeros)):
        if i % 3 == 0 and i != 0:
            row1 += "%3s" % numeros[i]
        elif (i + 1) % 3 == 0 or i == 0:
            row2 += "%3s" % numeros[i]
        elif (i + 2) % 3 == 0:
            row3 += "%3s" % numeros[i]

    row1 = row1.rjust(tableLength, " ")
    printCentrado(row1)
    row2 = row2.rjust(tableLength, " ")
    printCentrado(row2)
    row3 = row3.rjust(tableLength, " ")
    printCentrado(row3)


def showApuestas(apuestas):     #MOSTRAR LAS APUESTAS COMPLEJAS
    for i in apuestas:
        printLinea()
        if i != "numeros":
            for key, value in apuestas[i].items():
                print("%6s" % key.upper() + ": " + str(value))


def showResultado(n):   #MOSTRAR LA GANANCIA/PERDIDA
    printCentrado("LOS RULETA GIRÓ Y TÚ RESULTADO FUE...")
    printCentrado(str(n))
    


# PROGRAMA
ANCHO_DE_CONSOLA = 50
valance = getValance()

jugando = True
while jugando:
    showValance(valance)
    showTable([0 for _ in range(37)]) #Como si pasara los valores de numeros en 0.
    apuestas = setApuestas(valance)
    print()
    showTable(list(apuestas["numeros"].values()))
    print()
    showApuestas(apuestas)
    res = askUser("¿Estas conforme con tus apuestas?: ")
    if res:
        number = getNumber()
        showNumber(number)
        showTable(list(apuestas["numeros"].values()))
        resultado = processApuesta(apuestas, number)
        valance += resultado
        print()
        showResultado(resultado)
        printLinea()
            
    res = askUser("¿Quieres seguir jugando?: ")
    print()
    if not res:
        jugando = False
        printCentrado("Se retira con $" + str(valance) + "!")
        print()
    if valance == 0:
        printCentrado("¡Se encuentra sin fondos! Finalizando el Juego :( ")
        print()
