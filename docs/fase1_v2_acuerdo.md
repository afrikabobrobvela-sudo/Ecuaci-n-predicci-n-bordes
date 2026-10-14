# Fase 1, versión 2: acuerdo de cierre (Claude y revisión externa)

Fecha: 14 de octubre de 2026. Este documento sustituye las conclusiones de `fase1_estado_del_arte.md` (v1) donde haya conflicto. La v1 se conserva como registro de la búsqueda. **Acuerdo cerrado el 14 de octubre de 2026 (secciones B y C aprobadas). La Fase 2 comienza cuando Rodrigo lo indique.**

---

## A. Fe de erratas de la v1 (correcciones aceptadas)

| # | Afirmación en v1 | Corrección acordada |
|---|---|---|
| E1 | "Potencial absoluto del SHE: −4.44 ± 0.02 eV" | El potencial absoluto del SHE es **U_SHE(abs) = +4.44 ± 0.02 V** a 298.15 K (IUPAC, Trasatti 1986). La energía electrónica asociada es ≈ **−4.44 eV** respecto al vacío. Se usa U para potenciales (V) y ε para energías electrónicas (eV) |
| E2 | Se usa "PZC o punto de potencial zeta cero" como sinónimos | **PZC** (carga superficial neta nula) e **IEP** (punto isoeléctrico electrocinético, movilidad nula) son magnitudes distintas que pueden coincidir. Se registran por separado, con su método de determinación |
| E3 | "E_fb ≈ CBM − ζ en tipo n", sin distinguir energía de potencial | Con Δn = ε_C − ε_F > 0 y Δp = ε_F − ε_V > 0. **Tipo n:** ε_fb = ε_C − Δn, que equivale a U_C = U_fb − Δn/e. **Tipo p:** ε_fb = ε_V + Δp, que equivale a U_V = U_fb + Δp/e. **No** se impone una corrección universal de 0.1 a 0.3 V |
| E4 | "La dispersión experimental es probablemente mayor que el error de la ecuación original" | **Se elimina.** El rango de casi 2 V de Patel mezcla variabilidad física, método, conversiones y valores extremos. Ambas magnitudes aún no se han comparado sobre datos compatibles. La dispersión solo se llamará "límite de exactitud" si está condicionada por fase, superficie, electrolito y procedimiento |
| E5 | Haghshenas "podría estar contaminado" o "sin control de calidad explícito" | Nueva redacción: "la independencia de sus etiquetas respecto a estimaciones por electronegatividad **queda pendiente de auditoría** de las fuentes originales (Tabla S1)". Citar Butler–Ginley no demuestra circularidad |
| E6 | "Xu–Schoonen es la fuente de la mayoría de los valores de χ" | Se retira. Queda: "fuente frecuentemente citada (sin cuantificar)" |
| E7 | Pearson = Mulliken "numéricamente" | Queda: la χ absoluta de Pearson se define igual que la de Mulliken, (I + A)/2. **Cada comparación de escalas debe especificar la tabla, el estado atómico o iónico y la transformación a energía.** La escala de Allen no puede sustituirse en la ecuación energética sin una transformación calibrada |
| E8 | La pH/PZC se presentaba como "toda" la corrección original | Butler–Ginley incluye la adsorción de iones determinantes del potencial. Savadogo (1990) añade el número donador del disolvente. Ali et al. (Catalysts 2021) usan la forma con pH/pzc y −0.5 eV. **Ninguna de estas correcciones es nuestra** |
| E9 | "α·Eg captura la asimetría orbital" | Con Eg fijo, α solo desplaza el centro: U_mid = (χ − E_ref)/e + (½ − α)Eg/e. Se reinterpreta como **corrección del centro dependiente del gap**. La asimetría real solo puede probarse con registros en que la BV y la BC se midieron de forma independiente |
| E10 | Extensión SSE omitida | Se añade Pelatt et al. 2015 (J. Solid State Chem. 231, 138–144; DOI verificado). Según el revisor: 92 compuestos adicionales, 64 elementos y dependencia con el estado de oxidación. Yo solo verifiqué los metadatos; las cifras son del revisor. **Una escala dependiente del estado de oxidación deja de ser una aportación original** |

### Niveles de lectura: corrección de transparencia (importante)
Todas mis lecturas "TC" de la v1 se hicieron con una herramienta que descarga el texto completo y responde preguntas dirigidas sobre él. **No fueron lecturas secuenciales completas.** Para no sobredeclarar, reclasifico así:

- **TC-d** (texto completo, consulta dirigida): Stevanović 2014, Haghshenas 2024 (manuscrito aceptado, **sin la Tabla S1**), InterMat 2024 (preprint), Kavan 2024, Abdullah 2019 y el SI de Castelli 2012.
- **R**: lo que antes estaba en R.
- **M** (metadatos): no respalda ninguna afirmación sustantiva sin indicar la fuente secundaria que la aporta.

---

## B. Decisiones acordadas

1. **Objetivo principal: el medio acuoso.** La fotoemisión forma un conjunto separado. **No se combinan** ambos mediante un único indicador de método.
2. **Tres conjuntos relacionados:**
   - **EQ (electroquímica):** U_fb y otros observables identificados, **al pH experimental**.
   - **AQ (bordes acuosos inferidos):** U_C o U_V **solo** cuando hay soporte suficiente (tipo n/p, Δn o Δp justificados), con la incertidumbre de la inferencia propagada.
   - **FE (fotoemisión):** IP, función de trabajo y VBM, según lo que realmente se midió. Un XPS-VB referido solo al nivel de Fermi **no** es una medición absoluta.
3. **Si AQ no tiene soporte suficiente**, el primer resultado se formula como **evaluación de potenciales de banda plana**, no como BC/BV.
4. **El PZC se registra en tres niveles:** medido en la misma muestra, externo con compatibilidad documentada, o desconocido. El ajuste del término PZC usa el primer nivel y el segundo sirve para análisis de sensibilidad. **No se imputa un valor único por fórmula.**
5. **Familias:** se recopilan sulfuros desde el inicio (sin exigir paridad con los óxidos). Los nitruros quedan como conjunto exploratorio.
6. **Modelos de referencia (todos se evalúan):**
   1. M0: ecuación simplificada habitual (constante y tabla atómica fijadas).
   2. M1: M0 con pH/PZC.
   3. M2: M1 con −0.5 eV de dipolo (forma de Ali et al. 2021 y Stevanović 2014).
   4. M3: SSE (versión y regla de predicción especificadas; se audita el solapamiento con sus datos de calibración).
   5. M4: modelo estadístico simple.
   6. M5: comparador ML del tipo de Haghshenas, reproducible.
   - Las comparaciones se hacen con **las mismas etiquetas, particiones y métricas**. No se compara nuestro MAE con su RMSE publicado.
7. **Originalidad aprobada:**
   > "Evaluación trazable de las estimaciones de bordes de banda por electronegatividad, separando observables y condiciones interfaciales, y determinación de si una corrección interpretable mejora su capacidad predictiva fuera de familia frente a modelos empíricos y de aprendizaje automático existentes."
   - Se admite de antemano un **posible resultado negativo**.
   - La base y la auditoría bibliográfica deben demostrar qué añaden frente a Patel 2022. Patel cubre solo TiO2, ZnO y SnO2 y solo la banda plana.
8. **Reclamaciones descartadas:** primera corrección de Butler–Ginley por pH, primera consideración de la superficie o del disolvente, primer predictor ML entrenado con datos experimentales, primera regresión simbólica de bordes de banda (Chandramohan et al. 2026, pendiente de leer) y primera escala dependiente del estado de oxidación.
9. **Pregunta 1** (fracción que proviene de la ecuación): requiere **una muestra documental propia**, definida con independencia del método de determinación. No puede salir de los excluidos de la búsqueda de mediciones.

---

## C. Formulaciones finales acordadas (cerrado el 14 de octubre de 2026)

**C1. Subconjunto de enlace vacío/agua.** "Se construirá un subconjunto de enlace con materiales caracterizados mediante electroquímica y fotoemisión. Las mediciones emparejadas (misma muestra o muestras equivalentes, con fase, composición y estado superficial caracterizados) permitirán estimar los desplazamientos asociados al cambio de entorno, propagando la incertidumbre de las transformaciones entre observables. Las comparaciones no emparejadas se analizarán como evidencia exploratoria y no se identificarán directamente con un dipolo interfacial."

**C2. Series de pH (corrección aceptada).** U_fb(pH) = A − s·pH, con A = U₀ + s·pH_pzc. Una serie identifica A y s, pero no separa U₀ de pH_pzc: cualquier δ con pH_pzc' = pH_pzc + δ y U₀' = U₀ − s·δ produce la misma curva. Formulación: "Se registrarán series de banda plana frente a pH para estimar pendientes, comprobar el comportamiento nernstiano y detectar cambios de régimen. Estas series no identifican por sí solas el PZC; separarlo de la referencia intrínseca requiere información independiente." **Las mediciones se conservan al pH original.** No se normalizan a pH 0 con una pendiente universal antes del análisis.

**C3. Efecto aleatorio por estudio.** Modelo candidato: y_ij = f(x_ij) + b_j + ε_ij, con b_j ~ N(0, τ²). Formulación: "Se evaluará un efecto aleatorio por estudio para representar la dependencia entre observaciones. La validación agrupará los registros por estudio y, cuando corresponda, por compuesto. Las familias se definirán antes del ajuste. La posible confusión entre método, estudio y familia se examinará mediante análisis estratificados y de sensibilidad." Para predecir un estudio nuevo no se usa un b_j estimado con sus propios resultados: τ² entra en el intervalo predictivo. Si cada familia se mide predominantemente con un método distinto, esa separación **no** está identificada y se declarará así.

**C4. BiOX como prueba externa.** Decisión (Claude): se reserva **toda la familia de oxihaluros de bismuto**: BiOCl, BiOBr, BiOI, BiOF si hay datos, las soluciones sólidas BiOCl_xBr_(1−x) y BiOBr_xI_(1−x) **y las fases ricas en Bi** (Bi4O5Br2, Bi24O31Br10, Bi3O4Cl, Bi5O7I, etc.). En el entrenamiento solo entran compuestos de Bi que **no** sean oxihaluros (BiVO4, Bi2O3, Bi2WO6, Bi2MoO6, Bi2S3, …), con la lista definida antes del ajuste. Lo que se pone a prueba es la **transferencia a la familia oxihaluro con Bi presente en el entrenamiento**, no la extrapolación a un elemento desconocido. Un descriptor asociado al Bi no se interpretará como prueba del mecanismo de par libre sin evidencia adicional.

**C5. Comparador ML.** Si no se dispone del código original: "Reimplementación basada en la arquitectura y el procedimiento publicados por Haghshenas et al., con las diferencias documentadas." No se le atribuyen sus métricas publicadas. Se evalúa sobre nuestras etiquetas curadas y nuestras particiones externas, con el ajuste de hiperparámetros dentro del entrenamiento.

**Estado: acuerdo cerrado.** La única afirmación retirada de mi propuesta es que las series de pH identifiquen el PZC.

## D. Pendientes antes de abrir la Fase 2

1. Auditar la Tabla S1 de Haghshenas (origen de cada uno de los 87 VBM).
2. Leer Pelatt 2015: alcance exacto y regla de predicción de la SSE.
3. Leer Butler y Ginley 1978 y Xu y Schoonen 2000 en su forma original (convenciones y ecuaciones exactas).
4. Leer Chandramohan 2026 y Zhang 2023 en texto completo.
5. (Hecho) Aprobación de las secciones B y C.

---

## E. Referencias nuevas (DOI verificado contra OpenAlex en esta versión)

- Savadogo, O. (1990). Correlation between the flat band potential and electron affinity of semiconductors: (1) equation including the effect of the solvent donor numbers. *Mater. Res. Bull.* 25, 1209–1217. https://doi.org/10.1016/0025-5408(90)90076-E
- Praus, P. (2021). On electronegativity of graphitic carbon nitride. *Carbon* 172, 729–732. https://doi.org/10.1016/j.carbon.2020.10.074
- Ali, H. R. H. et al. (2021). Solid-state synthesis of direct Z-scheme Cu2O/WO3 nanocomposites with enhanced visible-light photocatalytic performance. *Catalysts* 11, 293. https://doi.org/10.3390/catal11020293
- Zhang, X. et al. (2023). Bulk and surface contributions to ionisation potentials of metal oxides. *Angew. Chem.* 135(40). https://doi.org/10.1002/ange.202308411
- Chandramohan, M. et al. (2026). Prediction of aqueous stable lead-free hybrid halide perovskites for efficient solar water splitting using machine learning and molecular dynamics. *J. Mater. Chem. C* 14, 9279–9289. https://doi.org/10.1039/D6TC00296J
- Pelatt, B. D. et al. (2015). Atomic solid state energy scale: universality and periodic trends in oxidation state. *J. Solid State Chem.* 231, 138–144. https://doi.org/10.1016/j.jssc.2015.07.037
- Walsh, A.; Butler, K. T. (2014). Prediction of electron energies in metal oxides. *Acc. Chem. Res.* 47, 364–372. https://doi.org/10.1021/ar400115x
- IUPAC Gold Book: point of zero charge (https://goldbook.iupac.org/terms/view/P04704) y standard hydrogen electrode (https://www.old.goldbook.iupac.org/html/S/S05917.html). Aportados por el revisor; no los consulté.

Nota: verifiqué los metadatos de estas referencias, no su contenido. Lo que se les atribuye (por ejemplo, la ecuación 6 de Ali et al. o el rango de IP de CeO2 en Zhang et al.) procede de la revisión externa y queda marcado como pendiente de lectura propia.
