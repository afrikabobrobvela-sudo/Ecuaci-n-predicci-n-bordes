# Fase 5: caso de estudio BiOX (borrador para revisión antes de ejecutar)

Supone la opción A de la fase 4: K1 por tipo de portador, ±0.4 V. Si eliges M0a, cambia solo la ecuación de referencia; el resto del plan es el mismo.

## 1. Preguntas

1. **El sesgo de los oxihaluros.** ¿De dónde sale el sesgo de −0.65 V (−0.38 V tras K1) que tienen los oxihaluros en la reserva? Las hipótesis son: (a) la χ del haluro está mal ponderada por la media geométrica; (b) el dipolo de la capa [Bi2O2]²⁺/X⁻ desplaza los bordes; (c) la muestra experimental tiene un sesgo de método o de superficie.
2. **Composición.** ¿Siguen los bordes medidos la tendencia con la composición que predice la ecuación? Las series son Cl → Br → I y BiOX → Bi24O31X10 → Bi5O7X.
3. **Radicales.** ¿Qué implica la incertidumbre de ±0.4 V para afirmar que un BiOX genera •OH, •O2⁻ o ¹O2? Es la pregunta práctica que más se sobreinterpreta en la literatura.

## 2. Método propuesto

- **Experimental.** Uso solo los 21 registros de la reserva (ya abiertos) y los que fallaron por un único criterio, que van como sensibilidad. Comparo, por compuesto, la media entre estudios con M0a y K1.
- **DFT (cálculo propio).**
  - Calcularía en slab la afinidad electrónica y el potencial de ionización de BiOCl, BiOBr y BiOI (001), y de una fase rica en Bi si es viable, con HSE06 o con PBE más una corrección de gap.
  - Sirve para separar el término de volumen del dipolo de superficie: alineación con el potencial electrostático del vacío (método de Van de Walle).
  - **Necesito saber qué código y qué recursos tienes** (VASP, Quantum ESPRESSO, horas de CPU). En este entorno puedo correr como mucho PBE con QE en celdas pequeñas, y no es suficiente para HSE en slabs.
- **Literatura DFT.** Haría una tabla de EA/IP calculados en slab que ya estén publicados para BiOX, con DOI y nivel de teoría. No se mezcla con los datos experimentales.
- **Radicales.** Para cada BiOX: probabilidad de que E_BV > E(•OH/H2O) y de que E_BC < E(O2/•O2⁻), con la incertidumbre de K1. Los potenciales de referencia se toman de una fuente primaria (Wardman 1989 o Armstrong et al. 2015, IUPAC) y se verificarán antes de usarlos.

## 3. Dudas

1. ¿Tienes datos propios de BiOX (Mott–Schottky, UPS o XPS de valencia) que podamos usar como conjunto independiente? Serían los primeros con condiciones controladas.
2. ¿Qué capacidad de cálculo DFT tienes?
3. ¿Incluimos el análisis de radicales en el artículo 1 o lo dejamos para el artículo 2 (BiOX)?
