def cyk(gramatica, palabra):
    n = len(palabra)
    P = [[set() for j in range(n - i)] for i in range(n)]

    for i, letra in enumerate(palabra):
        for izquierda, derechas in gramatica.items():
            if letra in derechas:
                P[0][i].add(izquierda)

    for longitud in range(2, n + 1):  # longitud de la subcadena
        for i in range(n - longitud + 1):  # inicio de la subcadena
            for k in range(1, longitud):  # punto de división de la subcadena
                for A, Bs in gramatica.items():
                    for B in Bs:
                        if len(B) == 2:
                            B1, B2 = B
                            if B1 in P[k - 1][i] and B2 in P[longitud - k - 1][i + k]:
                                P[longitud - 1][i].add(A)
    
    for row in P:
        print(row)
    return 'S' in P[-1][0]

def eliminar_recursion_izquierda(gramatica):
    nueva_gramatica = {}
    for A, producciones in gramatica.items():
        producciones_directas = [p for p in producciones if not p.startswith(A)]
        producciones_recursivas = [p[1:] for p in producciones if p.startswith(A)]
        if producciones_recursivas:
            A_prima = A + "'"
            nueva_gramatica[A] = [p + A_prima for p in producciones_directas] + ['ε']
            nueva_gramatica[A_prima] = [p + A_prima for p in producciones_recursivas]
        else:
            nueva_gramatica[A] = producciones
    return nueva_gramatica
# Path: main.py

def a_forma_normal_chomsky(gramatica):
    nueva_gramatica = {}
    for A, producciones in gramatica.items():
        nuevas_producciones = []
        for produccion in producciones:
            if len(produccion) == 1 and produccion.islower():  # regla de la forma A -> a
                nuevas_producciones.append(produccion)
            elif len(produccion) == 2:  # regla de la forma A -> BC
                nuevas_producciones.append(produccion)
            else:  # regla de la forma A -> aBC... o A -> BCDE...
                # Crear nuevas reglas para cada no terminal en el lado derecho
                # excepto los dos últimos
                for i in range(len(produccion) - 2):
                    nuevo_no_terminal = A + str(i)
                    nuevas_producciones.append((nuevo_no_terminal, produccion[i+1]))
                    nueva_gramatica[nuevo_no_terminal] = [(produccion[i],)]
                # Añadir la última regla con los dos últimos no terminales
                nuevas_producciones.append((A + str(len(produccion) - 3), produccion[-1]))
        nueva_gramatica[A] = nuevas_producciones
    return nueva_gramatica


def main():
    gramatica = {
        'S': {('X', 'A'), ('Y', 'B')},
        'A': {'a', ('Z', 'S'), ('U', 'A')},
        'B': {'b', ('V', 'S'), ('W', 'B')},
        'X': {'a'},
        'Y': {'b'},
        'Z': {'a'},
        'U': {'b'},
        'V': {'b'},
        'W': {'a'},
    }
    palabra = 'abba'
    resultado = cyk(gramatica, palabra)
    print(resultado)

def main1():
    gramatica = {
        'S': {('P', 'R'),},
        'P': {'a'},
        'R': {'c'},
    }
    palabra = 'ac'
    resultado = cyk(gramatica, palabra)
    print(resultado)


def main2():
    gramatica = {
        'S': ['Sa', 'Sb', 'A'],
        'A': ['Ac', 'Ad', 'B'],
        'B': ['Be', 'Bf', 'g']
    }
    print("Gramática original:", gramatica)
    nueva_gramatica = eliminar_recursion_izquierda(gramatica)
    print("Nueva gramática:", nueva_gramatica)

def main3():
    gramatica = {
        'S': ['AB', 'BC'],
        'A': ['BA', 'a'],
        'B': ['CC', 'b'],
        'C': ['AB', 'a']
    }
    print("Gramática original:", gramatica)
    nueva_gramatica = a_forma_normal_chomsky(gramatica)
    print("Nueva gramática:", nueva_gramatica)

if __name__ == '__main__':
    main3()

if __name__ == '__main__':
    main()
    main2()
    main3()
