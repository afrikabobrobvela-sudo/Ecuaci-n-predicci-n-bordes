# Fase 4: ajuste y validación (K1–K5) y prueba final en BiOX

Fecha: 2026-10-14. Scripts: `scripts/fase4_ajuste.py`, `scripts/fase4_exploratorio.py`. Salidas en `resultados/fase4/`.

## 0. Ronda 3 y metas de la base

| | Meta | Antes (fase 3) | Ahora |
|---|---|---|---|
| Registros EQ aptos | ≥ 60 | 52 | **65** (49 tipo n, 16 tipo p) |
| Estudios | ≥ 30 | 40 | **48** |
| Familias con ≥ 3 estudios | ≥ 3 | 4 | **4** |
| Reserva BiOX | ≥ 20 | 15 | **21** registros de 15 estudios |

- **Ronda 3.** Se extrajeron 23 registros (óxidos 10, sulfuros 6, BiOX 7) y se abrieron unos 190 estudios más. La verificación a ciegas reprodujo los 23 valores. Uno de BiOX quedó fuera porque las dos extracciones dan Eg distintos (3.34 frente a 3.41 eV). SnS y CeO2 quedaron fuera porque el artículo no dice si el material es tipo n o p.
- **Fases ricas en Bi.** La reserva incluye ahora Bi24O31Br10 (4 registros), Bi24O31Cl10, Bi4O5I2, Bi12O17Cl2 y Bi5O7I. No hay ninguna solución sólida BiOX1−xYx: todas las que se encontraron fallaban algún filtro.
- **Reglas nuevas de consolidación** (no cambian ningún registro apto anterior; comprobado con un diff):
  - Un registro sin tipo n/p declarado no es apto.
  - Un electrolito con S2− se excluye por adsorción específica. El sulfito solo queda como bandera.
  - Si el autor declara el potencial del electrodo de referencia (p. ej., "E = 0.208 V vs SHE"), se usa ese valor.
  - Un valor "vs NHE" al que el autor sumó 0.059·pH se trata como RHE.
  - Cuando el texto nombra varias escalas, manda la que aparece primero.
  - **Corrección:** con estas reglas, Kovačić2018 (SnS2) se había convertido mal, como si estuviera vs SHE. No era apto (Eg n.r.), así que no afectó a ningún resultado.

Errores de los comparadores con la base nueva (tipo n, 49 registros, 35 estudios):

| Modelo | MAE (V) | Sesgo (V) |
|---|---|---|
| M0a | 0.41 [0.32, 0.50] | −0.27 |
| M0b | 0.38 [0.29, 0.46] | −0.20 |
| M3 | 0.52 | −0.10 |
| M4c | 0.43 | −0.22 |

En tipo p (16 registros, 14 estudios), el MAE de M0a es 1.55 V, con un sesgo de −1.54 V. Las conclusiones de la fase 3 se mantienen.

## 1. Criterio preregistrado (análisis principal: tipo n)

La regla era: una corrección mejora a M0a si, dejando fuera una familia (LOFO), el IC 95 % de la reducción del MAE excluye el 0 (bootstrap por estudio).

| Candidata | Parámetros | MAE M0a → K (LOFO) | Reducción [IC 95 %] | ¿Pasa? |
|---|---|---|---|---|
| K1: + δ | 1 | 0.406 → 0.364 | +0.041 [−0.032, +0.119] | no |
| K2: + δ + β(Eg − Ē) | 2 | 0.406 → 0.386 | +0.020 [−0.064, +0.110] | no |
| K3: + δ − s(pH − 7) | 2 | 0.392 → 0.361 (29 reg.) | +0.032 [−0.083, +0.143] | no |
| K4: + δ por anión | 2 | 0.406 → 0.364 | +0.042 [−0.044, +0.130] | no |
| K5: término por método | — | no identificable: los 65 registros son Mott–Schottky | — | — |

**Resultado: ninguna corrección pasa el criterio, así que según la regla preregistrada se queda M0a.** LOSO da lo mismo.

Parámetros ajustados con toda la base de tipo n (IC por bootstrap de estudios):

| Parámetro | Valor | Lectura |
|---|---|---|
| δ (K1) | **−0.27 V [−0.39, −0.15]** | El sesgo es real: el IC no toca el 0. Pero quitarlo apenas baja el MAE, porque la dispersión domina. |
| β (K2) | +0.18 [−0.09, +0.43] | Sin evidencia de dependencia con el gap. |
| s (K3) | +0.007 V/pH [−0.041, +0.046] | **La pendiente con el pH entre estudios es nula, no de 59 mV/pH.** Es una pendiente entre estudios, no una serie de pH (C2), así que no refuta el comportamiento nernstiano dentro de un estudio. Indica que, mezclando estudios, el pH no explica el error. |
| δ_O, δ_S (K4) | −0.33 y −0.09 V | Sus IC se solapan. |

## 2. Por qué ninguna corrección pasa: el límite está en los datos

Comparé el mismo compuesto medido en estudios distintos. La desviación estándar combinada de U_fb es **0.43 V** en el entrenamiento (tipo n: WO3, CdS, TiO2, BiVO4, Fe2O3, ZnO, Bi2O3, ZnFe2O4, ZnIn2S4) y **0.39 V** en la reserva BiOX. Algunos rangos:

| Compuesto | Rango de U_fb entre estudios |
|---|---|
| BiOBr | −0.73 a +0.36 V |
| BiVO4 | −0.33 a +0.53 V |
| WO3 | −0.55 a +0.64 V |

Ese ruido entre estudios (muestra, método de preparación, condiciones) es del mismo tamaño que el MAE de M0a (0.41 V). **Ninguna ecuación que solo use la composición y el Eg puede bajar mucho de ~0.4 V frente a la literatura publicada.** Creo que este es el mensaje central del primer artículo: el error de Butler–Ginley frente a datos reales está dominado por la reproducibilidad experimental, no por la forma de la ecuación.

## 3. Prueba final en la reserva BiOX (abierta una sola vez, con el modelo ya fijado)

| Modelo (parámetros fijados con el entrenamiento) | Tipo n: 20 registros, 15 estudios. MAE · sesgo |
|---|---|
| M0a | 0.67 [0.52, 0.80] · −0.65 |
| M0b | 0.61 [0.48, 0.74] · −0.58 |
| K1 (δ = −0.27 V) | **0.47 [0.38, 0.57] · −0.38** |

- **Reducción de K1 frente a M0a en la reserva:** +0.20 V [+0.10, +0.26]. Aquí el IC sí excluye el 0.
- En los oxihaluros, la ecuación predice el borde de conducción unos 0.65 V más positivo que lo medido, más del doble del sesgo del entrenamiento. K1 corrige parte, pero queda un sesgo de −0.38 V propio de la familia. Es relevante para la fase 5.
- Solo hay 1 registro tipo p en la reserva (BiOCl). No se puede sacar ninguna conclusión de él.

## 4. Tipo p (análisis secundario; la separación n/p se decidió en la fase 3, después de ver los residuos)

- **El valor de δ.** K1 da δ_p = **−1.54 V [−1.82, −1.19]**, con LOFO 1.55 → 0.43 V (reducción [+0.53, +1.48]).
- **Lectura física.** El borde de valencia de los tipo p con metal d (Cu, Fe, Co, Ni) está mucho más arriba de lo que da χ + ½Eg. Encaja con la hibridación d–O 2p (Stevanović 2014). Una sola constante lo arregla en promedio.
- **Advertencia.** Esta separación no estaba preregistrada en la fase 3 §3. La presento como hallazgo exploratorio con validación interna; para confirmarla haría falta una muestra tipo p independiente.

## 5. Búsqueda simbólica exploratoria (tipo SISSO, sin PySR)

- **Qué se probó.** Se probaron 93 descriptores φ en U = M0a + δ + β·φ, con selección por MAE LOFO. Los descriptores salen de 9 primarios (χ, Eg, χ del catión, χ del anión, Δχ, fracción de catión, fracción de Bi, fracción de metal d, I₁ medio del catión) y de sus sumas, diferencias, productos y cocientes por pares.
- **Resultado.** El mejor es el propio χ: MAE 0.330 V, reducción +0.075 [−0.018, +0.152], así que **tampoco pasa**, aun después de elegir el mejor de 93. Con β = −0.35, la ecuación efectiva sería U_CB ≈ 0.65·χ + … : la pendiente real frente a χ es menor que 1. Es una hipótesis para comprobar con más datos, no un resultado.
- **Por qué no PySR.** No usé PySR: con 49 registros y este ruido, una búsqueda más amplia solo sobreajusta.

## 6. Decisión que necesito

¿Qué ecuación llevamos a la fase 5 (BiOX) y a la herramienta de la fase 6?
- **A (recomendada).** K1 por tipo de portador, que es una ecuación aplicable a mano:
  - Tipo n: E_BC = χ − 4.44 − ½Eg − 0.27 (V vs SHE).
  - Tipo p: E_BV = χ − 4.44 + ½Eg − 1.54.
  - Banda de incertidumbre de ±0.4 V (el piso de reproducibilidad).
  - Se declara que en tipo n no pasó el criterio LOFO preregistrado, pero sí la prueba externa en BiOX, y que el término p es exploratorio.
- **B.** M0a sin cambios (estrictamente lo que dice el criterio), con la banda de ±0.4 V y la advertencia de que en tipo p no sirve.

## 7. M5 (Haghshenas et al. 2024), completado en otro hilo

Detalle en `fase4/fase4_M5_resultados.md` (código y 36 CIF del COD en la rama `claude/project-thread-ho6xsd`). En los mismos registros:

| Conjunto | M0a MAE | M5 MAE | MAE(M5) − MAE(M0a) |
|---|---|---|---|
| Tipo n (45 reg., 32 est.) | 0.41 | 0.70 | +0.29 [+0.12, +0.47] |
| Tipo p (12 reg., 10 est.) | 1.59 | 1.16 | −0.43 [−0.66, −0.15] |
| Reserva BiOX tipo n (15 reg., 13 est.) | 0.63 | 2.41 | +1.78 [+0.99, +2.74] |

- **Tipo n.** El modelo ML es peor que la ecuación simple, incluso en compuestos de su propio ajuste.
- **BiOX.** Fuera de su dominio colapsa: predice VBM de −11.7 eV en BiOCl.
- **Tipo p.** Mejora algo, pero deja un sesgo de −1.2 V.
- **Causa dominante.** La fase cristalina: el modelo cambia más de 1 eV entre polimorfos (TiO2 anatasa −8.63 eV, la Pmm2 de los autores −7.25 eV).

Esto refuerza la conclusión de §2: una ecuación simple, con su incertidumbre declarada, no es peor que el modelo ML frente a datos experimentales reales. No cambia la decisión pendiente.

## 8. Pendientes

- Faltan soluciones sólidas BiOX1−xYx con Mott–Schottky trazable. La fase 5 puede tratarlas con DFT en lugar de con datos experimentales.
