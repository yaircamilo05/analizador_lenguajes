// Definición de las producciones y creación de la gramática
var producciones1 = [
    new Produccion("S", ["aB", "bA"]),
    new Produccion("A", ["a", "aS", "bAA", "ε"]),
    new Produccion("B", ["b", "bS", "aBB", "ε"]),
];
var myGramatica = new Gramatica(["a", "b"], ["S", "A", "B"], producciones1, "S");
// Cadena de entrada
var cadena1 = "aab";
// Análisis de la cadena y muestra del árbol de análisis sintáctico
var arbol1 = myGramatica.analizar(cadena1);
if (arbol1) {
    mostrarArbol(arbol1);
}
else {
    console.log("Error de análisis: la cadena no coincide con la gramática");
}
