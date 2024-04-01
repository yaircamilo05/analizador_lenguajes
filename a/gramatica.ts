interface NodoArbol {
    tipo: string;
    valor?: string;
    hijos?: NodoArbol[];
  }
  
  function crearNodo(tipo: string, valor?: string, hijos?: NodoArbol[]): NodoArbol {
    return { tipo, valor, hijos: hijos || [] }; // Asegura que hijos sea un array vacío si no se proporciona
  }
  
  function mostrarArbol(nodo: NodoArbol, profundidad = 0) {
    const espacio = " ".repeat(profundidad * 2);
    console.log(`${espacio}${nodo.tipo}${nodo.valor ? `: ${nodo.valor}` : ""}`);
    if (nodo.hijos) {
      for (const hijo of nodo.hijos) {
        mostrarArbol(hijo, profundidad + 1);
      }
    }
  }
  
  class Gramatica {
    private readonly producciones: Produccion[];
    private readonly simbolosTerminales: Set<string>; // Utiliza un conjunto para una búsqueda más eficiente
    private readonly simbolosNoTerminales: Set<string>;
    private readonly simboloInicial: string;
  
    constructor(
      simbolosTerminales: string[],
      simbolosNoTerminales: string[],
      producciones: Produccion[],
      simboloInicial: string
    ) {
      this.simbolosTerminales = new Set(simbolosTerminales);
      this.simbolosNoTerminales = new Set(simbolosNoTerminales);
      this.producciones = producciones;
      this.simboloInicial = simboloInicial;
  
      // Validar la gramática
      if (!this.simbolosTerminales.has(simboloInicial)) {
        throw new Error("El símbolo inicial debe ser un símbolo no terminal.");
      }
    }
  
    analizar(cadena: string): NodoArbol | null {
      const pila: string[] = [this.simboloInicial];
      const arbol: NodoArbol = crearNodo(this.simboloInicial);
      let nodoActual = arbol;
  
      while (pila.length > 0) {
        const simbolo = pila.pop()!;
  
        if (this.simbolosTerminales.has(simbolo)) {
          if (cadena.length === 0 || cadena[cadena.length - 1] !== simbolo) {
            return null; // Error: símbolo terminal esperado pero no coincide con la cadena
          }
          nodoActual.hijos?.push(crearNodo(simbolo, cadena[cadena.length - 1]));
          cadena = cadena.substring(0, cadena.length - 1);
        } else {
          const produccion = this.getProduccion(simbolo, cadena);
          if (!produccion) {
            return null; // Error: no se encontró una producción adecuada
          }
          for (const simboloDerecho of produccion.simbolosDerechos.reverse()) {
            if (simboloDerecho !== "ε") { // Ignora las producciones vacías
              pila.push(simboloDerecho);
            }
          }
          nodoActual.hijos?.push(crearNodo(simbolo));
          nodoActual = nodoActual.hijos![nodoActual.hijos!.length - 1];
        }
      }
  
      if (cadena.length > 0) {
        return null; // Error: cadena no completamente consumida
      }
  
      return arbol;
    }
  
    private getProduccion(simbolo: string, cadena: string): Produccion | null {
      for (const produccion of this.producciones) {
        if (produccion.simboloIzquierdo === simbolo) {
          if (cadena.length >= produccion.simbolosDerechos.length) {
            const coincide = produccion.simbolosDerechos.every((simboloDerecho, i) => {
              return simboloDerecho === "ε" || cadena[cadena.length - 1 - i] === simboloDerecho;
            });
            if (coincide) {
              return produccion;
            }
          }
        }
      }
      return null;
    }
  }
  
  class Produccion {
    constructor(
      public readonly simboloIzquierdo: string,
      public readonly simbolosDerechos: string[]
    ) {}
  }