# Algoritmo CYK (Cocke-Younger-Kasami):
# El algoritmo CYK es un algoritmo de parsing (análisis sintáctico) para determinar si una cadena pertenece a una gramática libre de contexto. 
# Funciona construyendo una tabla de conjuntos de símbolos no terminales que pueden derivar subcadenas de la palabra dada.
# La tabla se llena dinámicamente utilizando las producciones de la gramática, y se verifican todas las combinaciones de subcadenas posibles 
# para cada longitud y posición en la palabra. Si la producción inicial ('S') se encuentra en la última fila y primera columna de la tabla, 
# entonces la palabra es generada por la gramática. Si la palabra es aceptada, el algoritmo también puede reconstruir un árbol de derivación 
# para mostrar cómo se generó la palabra a partir de la gramática.
def cyk(gramatica, palabra):
    n = len(palabra)  # Obtiene la longitud de la palabra
    P = [[set() for j in range(n - i)] for i in range(n)]  # Inicializa una matriz de conjuntos vacíos para almacenar los símbolos no terminales que generan subcadenas de la palabra
    derivaciones = [[{} for j in range(n - i)] for i in range(n)]  # Inicializa una matriz de diccionarios para almacenar las derivaciones de cada símbolo no terminal

    # Paso 1: Se buscan producciones unitarias
    for i, letra in enumerate(palabra):
        for izquierda, derechas in gramatica.items():
            if letra in derechas:
                # Si la letra actual está en las producciones de la gramática, se agrega el símbolo no terminal correspondiente a la posición [0][i] de la matriz P
                P[0][i].add(izquierda)
                # Se registra la derivación correspondiente en el diccionario de derivaciones
                derivaciones[0][i][izquierda] = letra

    # Paso 2: Se buscan producciones binarias
    for longitud in range(2, n + 1):  # Recorre todas las longitudes posibles de subcadenas
        for i in range(n - longitud + 1):  # Recorre todas las posiciones de inicio de las subcadenas de longitud dada
            for k in range(1, longitud):  # Recorre todas las posibles divisiones de la subcadena en dos partes
                for A, Bs in gramatica.items():
                    for B in Bs:
                        if len(B) == 2:
                            B1, B2 = B
                            # Si se encuentra una producción de la forma A -> B1 B2 que pueda generar las subcadenas correspondientes,
                            # se agrega el símbolo no terminal A a la posición [longitud - 1][i] de la matriz P
                            if B1 in P[k - 1][i] and B2 in P[longitud - k - 1][i + k]:
                                P[longitud - 1][i].add(A)
                                # Se registra la derivación correspondiente en el diccionario de derivaciones
                                derivaciones[longitud - 1][i][A] = (B1, B2, k, i)

    # Paso 3: Se verifica si la cadena es generada por el símbolo inicial de la gramática
    if 'S' in P[-1][0]:
        print("La palabra PERTENECE a la gramática.")
        print()
        print("ÁRBOL DE DERIVACIÓN:")
        imprimir_derivaciones(derivaciones, 'S', 0, n - 1)
    else:
        print("La palabra NO PERTENECE a la gramática.")


# IMPRIMIR EL ÁRBOL DE DERIVACIONES DE LA PALABRA EN CASO DE PERTENCER
# A LA GRAMÁTICA 
def imprimir_derivaciones(derivaciones, simbolo, i, j, nivel=0, ultimo=True):
    if simbolo in derivaciones[j - i][i]:
        derivacion = derivaciones[j - i][i][simbolo]
        if isinstance(derivacion, tuple):
            B1, B2, k, idx = derivacion
            if ultimo:
                print(" " * nivel + "└─", simbolo, "->")
            else:
                print(" " * nivel + "├─", simbolo, "->")
            if B1 in derivaciones[j - i][i]:
                imprimir_derivaciones(derivaciones, B1, i, i + k - 1, nivel + 3, ultimo=False)
            else:
                imprimir_derivaciones(derivaciones, B1, i, i + k - 1, nivel + 3, ultimo=True)
            if B2 in derivaciones[j - i][i]:
                imprimir_derivaciones(derivaciones, B2, i + k, j, nivel + 3, ultimo=True)
            else:
                imprimir_derivaciones(derivaciones, B2, i + k, j, nivel + 3, ultimo=False)
        else:
            if ultimo:
                print(" " * nivel + "└─", simbolo, "->", derivacion)
            else:
                print(" " * nivel + "├─", simbolo, "->", derivacion)
    else:
        if ultimo:
            print(" " * nivel + "└─", f"No se encontró una derivación para {simbolo}")
        else:
            print(" " * nivel + "├─", f"No se encontró una derivación para {simbolo}")


# ELIMINAR RESURSIÓN IZQUIERDA 
def eliminar_recursion_izquierda(gramatica):
    nueva_gramatica = {}
    for A, producciones in gramatica.items():
        producciones_directas = [p for p in producciones if not p.startswith(A)]
        producciones_recursivas = [p[1:] for p in producciones if p.startswith(A)]
        if producciones_recursivas:
            A_prima = A + "'"
            nueva_gramatica[A] = [p + A_prima for p in producciones_directas] 
            nueva_gramatica[A_prima] = [p + A_prima for p in producciones_recursivas]+ ['ε']
        else:
            nueva_gramatica[A] = producciones
    return nueva_gramatica

# FORMA NORMAL DE CHOMSKY
# No se usa esta función -_-
def a_forma_normal_chomsky(gramatica):
    nueva_gramatica = {}
    contador_no_terminal = ord('A')  # Comenzamos con 'A'

    def obtener_no_terminal():
        nonlocal contador_no_terminal
        nuevo_no_terminal = chr(contador_no_terminal)
        contador_no_terminal += 1
        return nuevo_no_terminal

    def manejar_produccion_larga(produccion):
        produccion_actual = produccion[0]
        for simbolo in produccion[1:]:
            nuevo_no_terminal = obtener_no_terminal()
            nueva_gramatica[nuevo_no_terminal] = [simbolo]
            produccion_actual += nuevo_no_terminal
        return produccion_actual

    for no_terminal, producciones in gramatica.items():
        nuevas_producciones = []
        for produccion in producciones:
            if len(produccion) == 1:
                nuevas_producciones.append(produccion)
            else:
                nuevas_producciones.append(manejar_produccion_larga(produccion))

        nueva_gramatica[no_terminal] = nuevas_producciones

    return nueva_gramatica



# GRAMÁTICAS 

gramatica = {
    'S': ['AB', 'BC'],
    'A': ['BA', 'a'],
    'B': ['CC', 'b'],
    'C': ['AB', 'a']
}

gramatica2 = {
    'FN': ['FN yx TN', 'TN'],
    'TN': ['tt', 'ff'],
    'IN': ['ee MS - IN', ' '],
    'MS': ['CC'],
    'CC': ['a z CC', ' '],
    'CN': ['CN ox FN', 'FN']
}

gramatica3 = {
    'S': ['PR'],
    'P': ['a'],
    'R': ['c'],
}

gramatica4 = {
    'S': ['XA', 'YB'],
    'A': ['a','ZY','UW'],
    'B': ['b','VX','WU'],
    'X': ['a'],
    'Y': ['b'],
    'Z': ['a'],
    'U': ['b'],
    'V': ['b'],
    'W': ['a'],
}

gramatica5 = {
    'S': ['ASA', 'aB'],
    'A': ['B', 'S'],
    'B': ['B', '']
}

# MAIN 
if __name__ == '__main__':
    print()
    print('ANALIZADOR DE GRAMÁTICA')
    print()

    print('GRAMÁTICA INICIAL\n', gramatica4)
    print()

    print('ELIMINAR RECURSIÓN IZQUIERDA')
    gramaticaSinRecursion = eliminar_recursion_izquierda(gramatica4)
    print('Gramática sin recursión izquierda: \n', gramaticaSinRecursion)
    print()

    print('VERIFICAR PALABRA')
    palabra = 'bab'
    print('Palabra a verificar:', palabra)
    verificarPalabra = cyk(gramaticaSinRecursion, palabra)
