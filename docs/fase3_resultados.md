# Fase 3: resultados (base ampliada y comparadores)

Aquí se informa lo que se hizo según `fase3_definicion.md`. No se ajustó ninguna corrección y la reserva BiOX sigue sellada: no se calculó ningún residuo sobre ella.

## 1. Base de datos

| | Meta | Logrado |
|---|---|---|
| Registros EQ aptos (entrenamiento) | ≥ 60 | **52** (6 del piloto y 46 nuevos) |
| Estudios | ≥ 30 | **40** |
| Familias con ≥ 3 estudios | ≥ 3 | **4**: óxidos binarios (12 estudios), óxidos ternarios sin Bi (14), óxidos de Bi no oxihaluros (9) y sulfuros (7) |
| Reserva BiOX utilizable | ≥ 20 | **15** registros de 11 estudios (ninguno de solución sólida) |

- **Extracción.** Hubo dos rondas y se abrieron unos 330 estudios. Se extrajeron 126 registros nuevos y se descartaron 239 entradas de estudios, con el motivo de cada una registrado.
- **Verificación a ciegas.** Una segunda extracción independiente, sin ver los valores de la primera, reprodujo **123 de 126 valores**. Los 3 que no coinciden son de un mismo estudio de Co3O4 y quedan excluidos. Cuando las dos extracciones no coincidían en el pH, se tomó el pH como no reportado.
- **Lo que deja la literatura.** Solo alrededor del 11 % de los estudios abiertos dio al menos un registro apto. Los motivos de rechazo, por orden: falta el relleno del electrodo de referencia o, en RHE, el pH; el Eg no está medido como número en el texto; el electrolito tiene un par redox; o el valor solo aparece en una figura. Esto es un resultado en sí mismo sobre la trazabilidad de las bandas planas publicadas y responde en parte a Q1.
- **PZC.** Ningún registro trae un PZC medido en la misma muestra. Por eso **M1 y M2 no se pueden evaluar** con la regla aprobada de no imputar (C8).

Reglas añadidas durante la consolidación, todas declaradas en `scripts/fase3_consolidar.py`:
- Las muestras irradiadas o dopadas son variantes y no entran al ajuste.
- Un "nivel de Fermi" publicado no se toma como U_fb.
- Un pH no reportado no bloquea la aptitud (es lo que dice A4), pero impide usar ese registro en M1, M2 y K3.

## 2. Errores de los comparadores (entrenamiento, 52 registros, 40 estudios)

Error = U_fb observado − predicho (V vs SHE, al pH experimental). En tipo n se compara con el borde de conducción y en tipo p con el de valencia. Los IC 95 % salen de un bootstrap por estudio. Los nulos M4 se evalúan dejando fuera el estudio.

| Modelo | Tipo n (37 reg., 28 est.) MAE · sesgo | Tipo p (15 reg., 13 est.) MAE · sesgo |
|---|---|---|
| M0a (χ − 4.44 − ½Eg) | 0.38 [0.28, 0.48] · −0.29 | 1.64 [1.36, 1.88] · −1.62 |
| M0b (Butler–Ginley original) | 0.35 [0.26, 0.44] · −0.22 | 1.58 [1.32, 1.81] · −1.56 |
| M3 (SSE, regla C9) | 0.52 [0.43, 0.62] · −0.03 | 1.11 [0.84, 1.52] · −0.71 |
| M4c (media de la familia) | 0.43 [0.36, 0.52] · −0.18 | 0.56 [0.33, 0.83] · +0.45 |
| M1, M2 | no evaluables (sin PZC medido) | ídem |
| M5 (Haghshenas) | pendiente de estructuras (ver §3) | ídem |

Lectura:
1. **Tipo n.** M0 queda a la par del modelo nulo por familia; sus intervalos se solapan. La forma original de Butler–Ginley es algo mejor que la versión con 4.44 eV. Hay un sesgo negativo de unos −0.2 a −0.3 V: el U_fb observado queda más negativo de lo predicho. No lo corrijo aquí; K1 lo pondrá a prueba en la fase 4.
2. **Tipo p.** La ecuación predice la banda de valencia unos 1.6 V demasiado positiva, sobre todo en compuestos de Cu y otros metales de transición (CuO, CuFeO2, CuCrO2, CuBi2O4, Cu3VO4…). Coincide con lo que documenta Stevanović 2014 para Cu2O y NiO. **Este es el hallazgo más fuerte de la fase:** la ecuación no sirve para el borde de valencia de los semiconductores tipo p con estados d del metal en la banda de valencia.
3. **pH.** En los 22 registros tipo n con pH conocido, la pendiente del residuo frente al pH entre estudios es de solo −8 mV/pH. Llevar el pH a 0 con 59 mV/pH no mejora el error: el MAE pasa de 0.35 a 0.37 V. **Corrijo aquí una cifra preliminar mía** (0.72 → 0.26 V): mezclaba registros tipo p en uno de los dos lados de la comparación y no era válida. No llegó a enviarse en el hilo.

Archivos: `resultados/fase3/predicciones_comparadores.csv`, `errores_comparadores.csv` y `salida_evaluacion.txt`.

## 3. M5 (Haghshenas et al. 2024)

- El código público corre en CPU y reproduce sus propios valores por plano a ±0.002 eV en 144 casos.
- **Bloqueo.** Faltan las estructuras cristalinas de las fases que medimos. La Crystallography Open Database está bloqueada en este entorno, y el repositorio solo trae otras fases (por ejemplo, TiO2 Pmm2 en lugar de anatasa o rutilo). Hay predicciones válidas solo para CdS wurtzita y, de forma aproximada, para SrTiO3 y Bi2WO6.
- **Fuga de entrenamiento.** Casi todos nuestros compuestos están en su conjunto de ajuste fino, así que M5 sobre ellos no es una predicción ciega. Cada caso se marca.

## 4. Decisiones que necesito

1. **La base no llega a la meta en registros** (52 de 60) **ni en BiOX** (15 de 20). La regla aprobada dice que, en ese caso, la fase 4 se limita a K1. Propongo una ronda 3 de extracción antes, centrada en BiOX y en tipo n. La ronda 2 muestra que es factible.
2. **Estructuras para M5.** Necesito que habilites el dominio www.crystallography.net en el entorno, o que me pases los CIF de las fases medidas.
