# VERIFICAR PALABRA EN LA GRAMÁTICA 
def cyk(gramatica, palabra):
    n = len(palabra)
    P = [[set() for j in range(n - i)] for i in range(n)]
    derivaciones = [[{} for j in range(n - i)] for i in range(n)]

    for i, letra in enumerate(palabra):
        for izquierda, derechas in gramatica.items():
            if letra in derechas:
                P[0][i].add(izquierda)
                derivaciones[0][i][izquierda] = letra

    for longitud in range(2, n + 1):  
        for i in range(n - longitud + 1):  
            for k in range(1, longitud):  
                for A, Bs in gramatica.items():
                    for B in Bs:
                        if len(B) == 2:
                            B1, B2 = B
                            if B1 in P[k - 1][i] and B2 in P[longitud - k - 1][i + k]:
                                P[longitud - 1][i].add(A)
                                derivaciones[longitud - 1][i][A] = (B1, B2, k, i)

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
