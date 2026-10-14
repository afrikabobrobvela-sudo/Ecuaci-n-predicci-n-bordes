# Fase 3: definición (borrador para revisión antes de ejecutar)

La fase 3, según el plan original, es "modelo base y correcciones candidatas". El ajuste y la validación son de la fase 4. Esta fase deja implementados los seis comparadores, mide su error sobre los datos de entrenamiento y preregistra las correcciones que se pondrán a prueba. **No se ajusta ninguna corrección.**

## 1. Por qué la fase empieza ampliando la extracción

El piloto deja 6 registros aptos en el conjunto principal y 2 de enlace exploratorio. Con eso no se puede ajustar ni un modelo de un parámetro con validación agrupada por estudio. Por eso la primera tarea es ampliar la base.

- **Meta mínima para abrir la fase 4:**
  - Al menos 60 registros EQ aptos, de al menos 30 estudios.
  - Al menos 3 familias de entrenamiento con 3 estudios cada una o más: óxidos binarios, óxidos ternarios de Bi que no sean oxihaluros, otros óxidos ternarios y sulfuros.
  - Al menos 20 registros de la reserva BiOX.
- **Prioridad de búsqueda.** Primero, estudios que reportan pH, relleno del electrodo y frecuencia, y series de pH o de frecuencia. Después, estudios con UPS y Mott–Schottky en la misma muestra (subconjunto de enlace), incluido Kageshima.
- **Método.** Búsqueda en OpenAlex con consultas por material y por observable, registradas en un archivo de consultas para que sea reproducible. Doble extracción: ChatGPT extrae en paralelo y yo verifico contra la fuente, como en el piloto. Se aplican las reglas A1–A7.
- **Si no se alcanza la meta,** se reporta el tamaño real y la fase 4 se limita a K1 (un solo parámetro).

## 2. Comparadores (ya aprobados; aquí solo se fija la implementación)

| Modelo | Implementación |
|---|---|
| M0a | U_CB = (χ − 4.44 − ½Eg)/e V vs SHE (χ y Eg en eV; p. ej., TiO2: 5.81 − 4.44 − 1.6 ≈ −0.23 V), comparado con U_fb al pH experimental, que es como se usa en la práctica. |
| M0b | Forma original de Butler–Ginley: E0 = 4.75 eV vs SCE, convertido a SHE (C6). |
| M1 | M0a + 0.059·(pH_PZC − pH), solo con PZC medido (nivel 1). Variante de sensibilidad con PZC imputado (C8). |
| M2 | M1 con el desplazamiento fijo de −0.5 eV por dipolo. |
| M3 | SSE de Pelatt 2015 con la media estequiométrica (C9). |
| M4 | Nulos: (a) media global de U_fb; (b) regresión solo en Eg; (c) media por familia. |
| M5 | **Cambio respecto a C5:** el código de Haghshenas es público (github.com/yousof96/physical_band_potentials, citado en su artículo). Uso su modelo tal cual sobre nuestros registros. Lo reentreno con nuestros datos solo si el tamaño de la base lo justifica, que con unos 60 registros no es el caso. |

**Comprobación previa:** M0b debe reproducir la Fig. 4 de Butler–Ginley con los 11 registros `historico_BG` (C7). Si no la reproduce, se busca el error antes de seguir.

## 3. Correcciones candidatas (preregistradas, a lo sumo 2 parámetros cada una)

| Clave | Forma | Qué pone a prueba |
|---|---|---|
| K1 | M0a + δ | Si basta recalibrar la constante (equivale a ajustar Ee). |
| K2 | M0a + δ + β·(Eg − Ē) | Si el centro de la banda depende del gap (reinterpretación E9; no es asimetría orbital). |
| K3 | M0a + δ − s·(pH − 7) | La pendiente real con el pH. Solo es identificable con series de pH (C2). |
| K4 | M0a + δ_anión (óxido o sulfuro) | Si hace falta un término por química del anión. |
| K5 | K1 + término por método (MS frente a métodos con luz) | Covariable de ruido para estimar sesgo, no para predecir. Se predice para MS. |

No se añaden candidatas después de ver los residuos. La búsqueda simbólica (SISSO/PySR) queda para la fase 4 como análisis exploratorio, separado de K1–K5.

## 4. Lo que se reporta en esta fase

- **Errores de M0–M5** sobre el conjunto de entrenamiento: MAE, RMSE y sesgo, por familia y por método, con IC por bootstrap agrupado por estudio.
- **La reserva BiOX queda sellada.** No se calculan residuos sobre ella hasta la prueba final de la fase 4, para que su forma no influya en el diseño de las correcciones.
- **Criterio de mejora, fijado ahora para la fase 4.** Una corrección mejora a M0a si, en validación con exclusión de familia, la reducción del MAE tiene un IC 95 % (bootstrap por estudio) que excluye el 0. Entre las candidatas que lo cumplan se elige la de menos parámetros.
- **Entregables:** `scripts/comparadores.py`, la base ampliada, la tabla de errores y la comprobación de Butler–Ginley.

## 5. Dudas para revisar antes de ejecutar

1. ¿Te parecen bien las metas de tamaño (60/30/3×3/20) o prefieres otras?
2. ¿Seguimos con ChatGPT extrayendo en paralelo?
3. Que M5 use el código original en vez de una reimplementación es un cambio sobre C5. Lo propongo porque es más justo con su trabajo y más barato.
