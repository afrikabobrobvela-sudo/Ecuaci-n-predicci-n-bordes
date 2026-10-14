# Fase 1. Estado del arte: corrección de la ecuación de electronegatividad para bordes de banda

Fecha de la búsqueda: 14 de octubre de 2026.
Alcance: búsqueda web de fuentes académicas con DOI o enlace verificable. Cada DOI listado se comprobó contra los metadatos de Crossref u OpenAlex.

**Nivel de lectura** (columna "Lectura" en las tablas):
- **TC**: texto completo leído (o el manuscrito aceptado del autor, o el SI completo cuando así se indica).
- **R**: solo resumen o ficha del editor.
- **M**: solo metadatos (título, autores, revista). El contenido no se evaluó y no se cita ninguna afirmación de él más allá del título.

---

## 0. Respuesta corta

**¿Existe ya una ecuación corregida comparable?** No encontré ninguna versión corregida de la ecuación de Butler–Ginley que cumpla las tres condiciones a la vez: ser interpretable y aplicable a mano, estar ajustada con mediciones directas curadas y estar validada por familia de materiales. Hay tres trabajos que se acercan lo suficiente como para obligarnos a replantear la originalidad (sección 7):

1. **Haghshenas et al. 2024 (Materials Today Physics)**. Predice el VBM y el CBM con una red de grafos cristalinos (CGCNN) usando transferencia desde 1382 materiales 2D calculados con HSE y ajuste fino con **87 VBM medidos**. RMSE de prueba de 0.27 eV en el VBM. No es interpretable, no se compara con Butler–Ginley y no aplica un control de calidad explícito a los datos. **Es el competidor directo más cercano.**
2. **Escala SSE de Pelatt et al. 2011 (JACS)**. Es una escala empírica e interpretable de energías atómicas en estado sólido, derivada de la EA y el IP de 69 compuestos binarios. Funciona en la práctica como una "electronegatividad recalibrada" para los bordes de banda, pero está calibrada con fotoemisión en vacío y no con electroquímica en solución.
3. **Stevanović et al. 2014 (PCCP)**. Usa IP y EA calculados con GW más slab, y propone un desplazamiento empírico de aproximadamente 0.5 eV (±0.3 eV) por el dipolo de interfaz con el agua. También documenta que la ecuación de Mulliken falla en Cu2O y NiO por 1.2 a 1.8 eV.

**Advertencia importante para el diseño:** según Patel et al. (2022), los potenciales de banda plana publicados para un mismo material (TiO2, ZnO, SnO2) llegan a abarcar casi 2 V en la escala RHE. Esa dispersión experimental es probablemente mayor que el error de la ecuación original. Si la base no se filtra con rigor, ninguna corrección será distinguible del ruido.

---

## 1. Origen y supuestos de la ecuación

### 1.1 Nethercot (1974)
Propuso que la energía de Fermi y el umbral fotoeléctrico de un sólido pueden estimarse con la media geométrica de las electronegatividades atómicas de Mulliken, por analogía con la igualación de electronegatividades de Sanderson. Es el origen del término χ(compuesto) = (Π χᵢ^nᵢ)^(1/N). [Lectura: M; el contenido se conoce por cómo lo usan los trabajos posteriores.]

### 1.2 Butler y Ginley (1978)
Correlacionaron la afinidad electrónica estimada como EA ≈ χ − ½Eg con el potencial de banda plana medido en **11 óxidos**. Según la lectura de Stevanović et al. (2014, TC), la comparación **solo es válida al pH del punto de carga cero (PZC, o punto de potencial zeta cero)**. Por lo tanto, la formulación original ya incorpora un término de pH respecto del PZC. No pude leer el artículo original porque el sitio del editor bloquea el acceso automático.

### 1.3 Xu y Schoonen (2000)
Compilaron las posiciones de BC y BV de unos 50 minerales semiconductores (óxidos y sulfuros) **combinando datos experimentales de banda plana con estimaciones por electronegatividad** [R]. Su tabla es la fuente de la mayoría de los valores de χ que se usan en fotocatálisis. Hay que tenerlo presente: si un artículo cita "Xu y Schoonen" como fuente de su posición de banda, el valor puede ser medido o calculado según el compuesto.

### 1.4 Supuestos implícitos (análisis propio, no citado)
| Supuesto | Consecuencia | Evidencia en contra |
|---|---|---|
| El centro del gap coincide con −χ en escala de vacío (simetría ½Eg) | Ignora que la BV y la BC tienen distinto carácter orbital (O 2p, X np, Bi 6s y 6p, metal d) | Stevanović 2014: la corrección GW desplaza de forma muy asimétrica el VBM y el CBM (1.5 eV en el VBM de ZnS, 1.3 eV en el CBM de NiO). El "midgap fijo" "obviamente no se cumple" |
| χ depende solo de la composición | Polimorfos y caras distintas reciben el mismo valor | Anatasa y rutilo tienen distinta alineación de bandas (Scanlon 2013 [M]; Kavan 2024 [TC] reporta que la literatura no se pone de acuerdo sobre cuál tiene el CBM más alto). En SrTiO3 las dos terminaciones difieren hasta 2.3 eV (Stevanović 2014) |
| Ee = 4.44 o 4.5 eV | Hay una ambigüedad sistemática de unos 0.06 eV entre autores | Trasatti 1986 (IUPAC) da −4.44 ± 0.02 eV; Kavan 2024 documenta el uso mezclado de 4.44 y 4.5 y de NHE frente a SHE |
| La comparación con la electroquímica es válida a cualquier pH | Sin el término de PZC se introduce un error de 0.059·ΔpH | Butler–Ginley y Stevanović: la comparación solo es válida en el PZC, que no se conoce para muchos materiales |
| El potencial de banda plana es igual al CBM | En un tipo n, E_fb ≈ E_F, no la BC (la diferencia es ζ_nb, típicamente de 0.1 a 0.3 eV) | Kavan 2024 |

---

## 2. Trabajos que evalúan su exactitud

| Trabajo | Qué se compara | Resultado clave (verificado) | Lectura |
|---|---|---|---|
| Stevanović, Lany, Ginley, Tumas, Zunger 2014 | IP/EA (GW + slab) frente a fotoemisión y frente a electroquímica en 17 compuestos; discute las estimaciones de Mulliken | Fotoemisión: unos 0.3 eV en 12 compuestos. Electroquímica a pH 1: 14 de 17 dentro de unos 0.6 eV. Mulliken "falla" en Cu2O y NiO por 1.2 a 1.8 eV, y el PZC no lo explica. InP difiere unos 0.8 eV. El dipolo agua/semiconductor equivale a un desplazamiento de unos 0.5 ± 0.3 eV | TC |
| Patel, Mortelliti, Dempsey 2022 | Metaanálisis de bandas planas de TiO2, ZnO y SnO2 en medio acuoso | Dispersión de casi 2 V vs RHE por material, incluso dentro de categorías estrechas. TiO2 y SnO2 son nernstianos y ZnO no. No hay diferencia significativa entre anatasa y rutilo. El desplazamiento de +400 mV de los nanotubos de anatasa se debe sobre todo a un mal uso de Mott–Schottky. (Kavan 2024 cita 505, 97 y 223 entradas) | R |
| Kavan 2024 (J. Solid State Electrochem.) | Revisión de errores en la electroquímica de TiO2, SnO2 y ZnO | E_fb ≠ CBM. Mott–Schottky depende de la frecuencia y falla en electrodos porosos. Se mezclan las escalas de vacío y SHE. La función de trabajo de la anatasa (001) varía de 3.61 a 6.76 eV según la técnica. "El gap es la magnitud más robusta" | TC (resumen detallado) |
| Hankin et al. 2019 (JMCA) | Métodos de determinación de la banda plana | Errores de la aproximación de Mott–Schottky | R |
| Beranek 2011 | Métodos (foto)electroquímicos para los bordes de TiO2 | Revisión de técnicas, incluidos los polvos | R |
| Abdullah 2019 (Eur. J. Chem.) | Ejemplo con anatasa | Ecuación: −0.24 V vs NHE; experimento: −0.16 V (pH 0). No propone corrección | TC |
| Fuentes et al. 2023 (Photochem. Photobiol. Sci.) | Electronegatividad y función de trabajo aplicadas a CuFeS2, FeS2, CuS y Cu2S | Validación solo cualitativa con TiO2 P25; sin métricas de error | R |
| Das, Rocquefelte, Jobic (arXiv 2018) | Referencia absoluta de vacío por DFT en 11 binarios frente a banda plana | MAE ≈ 0.17 eV frente a la banda plana experimental (no compara con Butler–Ginley) | R |
| Castelli et al. 2012 (EES) | Cribado de unas 5400 perovskitas | **Usa** Butler–Ginley para los bordes y no valida los bordes frente al experimento, solo los gaps. Ejemplo de propagación de la ecuación en cribados de alto rendimiento | SI en TC; artículo R |

**Pregunta 1 (fracción de posiciones de banda que salen de la ecuación):** **no encontré** ningún estudio bibliométrico que la cuantifique. Parece un hueco real, aunque no puedo afirmar que no exista.

---

## 3. Correcciones y alternativas ya propuestas

| Propuesta | Tipo | Qué corrige | Limitación para nuestro objetivo | Lectura |
|---|---|---|---|---|
| Término de pH: 0.059·(pH_PZC − pH) | Ya forma parte de Butler–Ginley y de Xu–Schoonen | El pH | **No es una corrección nueva.** El problema práctico es que el PZC se desconoce en muchos materiales | TC (vía Stevanović) |
| Desplazamiento por dipolo de unos 0.5 eV (Stevanović 2014) | Corrección empírica constante sobre IP/EA calculados | La interfaz con el agua | Es una constante. No depende del material (±0.3 eV) | TC |
| Escala SSE (Pelatt, Ravichandran, Wager, Keszler 2011) | Escala empírica atómica a partir del IP y la EA de 69 binarios | Sustituye a χ de Mulliken; el centro del gap se referencia al nivel donador/aceptor del hidrógeno | Calibrada en vacío (fotoemisión) y solo con binarios. Hay que comprobar si se transfiere a ternarios y oxihaluros | R |
| Nivel de neutralidad de carga (CNL) y estados inducidos por el metal en el gap (Robertson 2000) | Modelo físico para alineamiento en interfaces | La referencia del "centro" | Se aplica a interfaces sólido/sólido y requiere la estructura de bandas | R |
| Esquema de primeros principios para bordes de óxidos de metales de transición (Toroker et al. 2011) | DFT + GW | Bordes de óxidos de MT | No es aplicable a mano | M |
| Solvatación explícita (Park y Kolpak 2019) | DFT con agua explícita | La diferencia entre vacío y agua | Costo alto | R |
| IP/EA de BiOX con DFT híbrido y SOC (Ganose et al. 2016) | DFT de referencia para la Fase 5 | — | Pendiente de lectura | M |

**Escalas de electronegatividad.** La "electronegatividad absoluta" de Pearson (1988) se define como (I + A)/2. **Es numéricamente la definición de Mulliken en eV**, y de hecho las tablas de χ que se usan en fotocatálisis son las de Pearson. Comparar "Mulliken frente a Pearson" casi no aporta información. Las alternativas que sí son distintas son la de Allen (1989, energía media de valencia, espectroscópica), la SSE (2011) y las escalas dependientes del estado de oxidación.

---

## 4. Aprendizaje automático para IP, EA y alineamiento

| Trabajo | Datos | Modelo | Exactitud (verificada) | Interpretable | Lectura |
|---|---|---|---|---|---|
| **Haghshenas, Wong, Sethu, Amal, Kumar, Teoh 2024** | **87 VBM experimentales** (3D, la mayoría óxidos), referenciados a vacío a pH 0 con +0.059 V/pH. Estructuras tomadas de Materials Project por grupo espacial. Transferencia desde 1382 materiales 2D HSE (C2DB) | CGCNN con 12 propiedades elementales, entre ellas la electronegatividad. CBM = VBM + Eg (otro modelo, RMSE 0.29 eV) | VBM: RMSE 0.27 eV (R² 0.89) en un test de unos 13 materiales; CV de 10 particiones 0.28 ± 0.07 eV. Sin modelo base de Butler–Ginley. Mayor error en nitruros | No (lo dicen los propios autores) | TC (manuscrito aceptado) |
| Kiyohara, Hinuma, Oba 2024 (JACS) | **Unas 3000 superficies de óxidos** (alto rendimiento por primeros principios) | Red neuronal con descriptores SOAP aprendibles; transferencia de binarios a ternarios | Numéricamente no verificada (no tuve acceso al texto completo) | No | R |
| Choudhary y Garrity 2024 (InterMat, JARVIS) | 607 superficies, 593 desplazamientos de banda en interfaces explícitas | DFT (OptB88vdW + TBmBJ); ALIGNN | EA frente a experimento: MAE 0.39 eV. Función de trabajo: 0.29 eV. ALIGNN en slabs: MAE de 0.55 eV (VBM) y 0.96 eV (CBM) | No | TC |
| Choudhary et al. 2020 (JARVIS) | Repositorio | — | — | — | M |
| Hinuma, Grüneis, Kresse, Oba 2014 (PRB) | 21 semiconductores | PBE, HSE y GW con corrección de vértice | GWΓ reproduce bien el IP experimental. Error máximo en el IP: unos 0.7 eV | — | R |
| Davies, Butler, Walsh 2019 (Chem. Mater.) | Más de 1 millón de composiciones de óxidos cuaternarios | ML para el gap como filtro | Sin información sobre los bordes en el resumen | No | R |
| Masood et al. 2023 (Cell Rep. Phys. Sci.), mismo grupo que Haghshenas | Gaps experimentales | CGCNN con adaptación de dominio | Gap: MAE 0.23 eV | No | R |

**Observación crítica sobre Haghshenas 2024:** cita a Butler y Ginley como fuente de valores del VBM de TiO2 (7.32 a 7.5 eV vs vacío). Habría que comprobar en su Tabla S1 si esos valores son medidos o si vienen de la propia ecuación. Si vienen de la ecuación, el conjunto de entrenamiento estaría parcialmente contaminado por el modelo que queremos corregir. Esto refuerza el argumento de que hace falta una base curada con criterios explícitos de inclusión y exclusión.

---

## 5. Regresión simbólica en ciencia de materiales

| Trabajo | Aporte | Lectura |
|---|---|---|
| Ouyang, Curtarolo, Ahmetcik, Scheffler, Ghiringhelli 2018 (SISSO) | Sensado comprimido para encontrar descriptores de baja dimensión entre muchísimos candidatos | M |
| Bartel et al. 2019 (Sci. Adv.), factor de tolerancia τ | Uso de SISSO para **reemplazar una regla empírica clásica (Goldschmidt) por una fórmula interpretable mejor**. Es el precedente metodológico más parecido a este proyecto | R |
| Cranmer 2023 (PySR) | Regresión simbólica evolutiva multipoblación; benchmark EmpiricalBench | R |
| Wang, Wagner, Rondinelli 2019 (MRS Commun.) | Revisión de regresión simbólica en materiales | M |

**No encontré** ninguna aplicación de SISSO o PySR a bordes de banda experimentales en solución.

---

## 6. Tabla de antecedentes (resumen)

| # | Referencia | Categoría | Aporte para este proyecto | Lectura |
|---|---|---|---|---|
| 1 | Nethercot 1974 | Origen | χ como media geométrica | M |
| 2 | Butler y Ginley 1978 | Origen | EA = χ − ½Eg, validado en 11 óxidos, válido en el PZC | M (contenido vía #5) |
| 3 | Xu y Schoonen 2000 | Origen y compilación | Unos 50 minerales; mezcla valores medidos y estimados | R |
| 4 | Trasatti 1986 | Conversión | Potencial absoluto del SHE: −4.44 ± 0.02 eV | M (valor vía #8) |
| 5 | Stevanović et al. 2014 | Exactitud | Falla en Cu2O y NiO (1.2 a 1.8 eV); dipolo de unos 0.5 eV; el midgap no es invariante | TC |
| 6 | Patel et al. 2022 | Dispersión experimental | Unos 2 V de dispersión en la banda plana del mismo material | R |
| 7 | Hankin et al. 2019 | Métodos experimentales | Errores de Mott–Schottky | R |
| 8 | Kavan 2024 | Métodos experimentales | E_fb ≠ CBM; dispersión en frecuencia; escalas | TC |
| 9 | Beranek 2011 | Métodos experimentales | Técnicas para polvos y películas | R |
| 10 | Kaufman et al. 2024 (Nat. Catal.) | Marco conceptual | Los bordes absolutos están sobrevalorados como criterio de diseño | R |
| 11 | Scanlon et al. 2013 | Contraejemplo estructural | Alineación de anatasa y rutilo | M |
| 12 | Abdullah 2019 | Exactitud (anécdota) | TiO2: 0.08 V de error | TC |
| 13 | Fuentes et al. 2023 | Aplicación | Sulfuros de Cu y Fe sin validación cuantitativa | R |
| 14 | Castelli et al. 2012 | Uso en cribado | Butler–Ginley aplicado a unas 5400 perovskitas sin validar los bordes | SI en TC |
| 15 | Pelatt et al. 2011 (SSE) | Alternativa empírica | Escala atómica calibrada con IP y EA de 69 binarios | R |
| 16 | Robertson 2000 | Alternativa física | CNL y estados inducidos por el metal | R |
| 17 | Toroker et al. 2011 | Alternativa DFT | Bordes de óxidos de MT | M |
| 18 | Park y Kolpak 2019 | Alternativa DFT | Solvatación explícita | R |
| 19 | Hinuma et al. 2014 | Referencia DFT | IP y EA con GW: error de hasta unos 0.7 eV | R |
| 20 | Das, Rocquefelte, Jobic 2018 | Referencia DFT | MAE de unos 0.17 eV en 11 binarios | R |
| 21 | Ganose et al. 2016 | DFT de BiOX | IP de BiOX con híbrido y SOC (para la Fase 5) | M |
| 22 | **Haghshenas et al. 2024** | **ML experimental (competidor)** | 87 VBM; RMSE 0.27 eV; no interpretable | **TC** |
| 23 | Masood et al. 2023 | ML del gap | MAE 0.23 eV | R |
| 24 | Kiyohara, Hinuma, Oba 2024 | ML de IP y EA | Unas 3000 superficies de óxidos | R |
| 25 | Choudhary y Garrity 2024 (InterMat) | ML y DFT de alineamiento | EA frente a experimento: MAE 0.39 eV | TC |
| 26 | Choudhary et al. 2020 (JARVIS) | Repositorio | — | M |
| 27 | Davies, Butler, Walsh 2019 | ML de cribado | Gap de cuaternarios | R |
| 28 | Pearson 1988; Allen 1989 | Escalas de χ | Pearson = Mulliken en eV; Allen es distinta | M |
| 29 | Ouyang et al. 2018 (SISSO) | Regresión simbólica | Método | M |
| 30 | Bartel et al. 2019 | Regresión simbólica (precedente) | Una regla empírica reemplazada por una fórmula interpretable | R |
| 31 | Cranmer 2023 (PySR) | Regresión simbólica | Método | R |
| 32 | Wang, Wagner, Rondinelli 2019 | Regresión simbólica (revisión) | — | M |

---

## 7. Hueco de investigación y replanteo de la originalidad

### 7.1 Qué ya existe
- La **corrección por pH y PZC ya forma parte de la ecuación original**. Proponerla como término nuevo sería un error que un revisor detectaría. Lo nuevo solo puede ser (a) cómo se trata un PZC desconocido, por ejemplo estimándolo o marginalizándolo, o (b) un término de dipolo dependiente del material, en lugar de la constante de unos 0.5 eV de Stevanović.
- Ya existe un **predictor ML de bandas entrenado con mediciones** (Haghshenas 2024), con RMSE de unos 0.27 eV en el VBM. Afirmar "primer modelo ajustado con datos experimentales" sería falso.
- Ya existe una **escala empírica recalibrada** (SSE), que es interpretable.
- La **falla en Cu2O y NiO** ya está documentada (Stevanović 2014).

### 7.2 Qué no encontré (hueco)
1. Una **versión corregida e interpretable de Butler–Ginley** (aplicable a mano, con pocos parámetros) ajustada con **mediciones electroquímicas o de fotoemisión directas** y validada **dejando fuera una familia completa a la vez**.
2. Una **cuantificación del error de la ecuación original frente a mediciones directas, por familia** y **normalizada por la dispersión experimental** del mismo compuesto.
3. Una **base curada con criterios explícitos de exclusión y niveles de confianza** que separe los valores medidos de los obtenidos con la ecuación. Haghshenas no reporta esos criterios y podría incluir valores de la propia ecuación.
4. Una **estimación de qué fracción** de las posiciones de banda publicadas en fotocatálisis viene de la ecuación (pregunta 1).
5. Una **comparación directa** entre Butler–Ginley, la escala SSE, un modelo ML de caja negra y una ecuación corregida sobre los mismos datos.
6. Una **validación específica en oxihaluros de bismuto** y sus soluciones sólidas, cuyos bordes tienen un fuerte carácter Bi 6s/6p y X np y un fuerte efecto espín-órbita. Es justo el caso en que la simetría de ½Eg es menos creíble.

### 7.3 Replanteo propuesto de la originalidad
El aporte no debe ser "la primera ecuación ajustada a experimento". Propongo plantearlo así:

> **"Base curada y graduada por confianza de bordes de banda medidos directamente, con la que se cuantifica el error real de la ecuación de Butler–Ginley frente al límite impuesto por la dispersión experimental, y una corrección interpretable con pocos parámetros que se compara directamente con la escala SSE y con un modelo ML de caja negra, validada fuera de familia y aplicada a BiOX."**

Con este planteamiento el artículo (a) de la Fase 7 gana peso: la base de datos y la pregunta 1 son originales por sí mismas.

### 7.4 Riesgos que hay que asumir
- **Techo de ruido:** si la dispersión entre mediciones independientes del mismo compuesto es de unos 0.3 a 0.5 eV incluso después de filtrar, y el sesgo de la ecuación es de un orden similar, la mejora puede no ser estadísticamente distinguible. La Fase 2 debe medir esa dispersión **antes** de comprometerse con la Fase 4.
- **Heterogeneidad de la variable objetivo:** Mott–Schottky da E_fb (≈ CBM − ζ en un tipo n, ≈ VBM + ζ en un tipo p), mientras que XPS y UPS dan el VBM con respecto a E_F o al vacío, en vacío y no en electrolito. Mezclarlos sin un término de método introduce un sesgo sistemático que Stevanović estima en unos 0.5 eV (el dipolo con el agua).
- **Marco conceptual:** Kaufman et al. (2024, Nature Catalysis) sostienen que los bordes absolutos están sobrevalorados como criterio de diseño en fotocatálisis. Un revisor puede usarlo en contra. Conviene citarlo y plantear el trabajo como mejora de una herramienta que se usa masivamente, no como un criterio de actividad.

---

## 8. Decisiones tomadas
- Se trata la escala de Pearson como equivalente a la de Mulliken. Las alternativas reales que se compararán son la de Allen y la SSE.
- El término de pH y PZC se considera parte del modelo base (Butler–Ginley completo), no una corrección.
- Haghshenas 2024 se adopta como **modelo de referencia ML** para comparar en la Fase 4, y su Tabla S1 como posible **semilla de datos**, sujeta a nuestra auditoría.
- Para la escala absoluta del SHE se usará −4.44 ± 0.02 eV (Trasatti 1986), con un análisis de sensibilidad usando 4.5 eV.

## 9. Dudas abiertas
1. ¿Qué variable objetivo elegimos: el VBM y el CBM "en electrolito" (electroquímica) o en vacío (fotoemisión)? Propongo usar la electroquímica como objetivo principal, con un término indicador del método para la fotoemisión.
2. ¿Incluimos sulfuros y nitruros, cuyos datos son escasos según Haghshenas, o empezamos con óxidos y Bi-compuestos solamente?
3. Butler–Ginley y Xu–Schoonen dan el valor en el PZC. ¿Imputamos el PZC con una fuente compilada o restringimos el ajuste a los registros con pH y PZC conocidos?

## 10. Qué necesito de ti
1. **Confirmar el replanteo de la originalidad** (7.3) antes de diseñar el protocolo de la Fase 2.
2. **PDFs a los que tengas acceso** (no pude leerlos por bloqueo del editor o del sitio): Butler y Ginley 1978; Xu y Schoonen 2000; Patel et al. 2022 (incluido el SI con la tabla de los unos 825 valores); Kiyohara et al. 2024 (números de MAE); Ganose et al. 2016; Kaufman et al. 2024; el SI de Haghshenas et al. 2024 (Tabla S1).
3. Tu criterio sobre la duda 1, porque cambia el diseño de los campos de la base.
4. Si tienes mediciones propias de BiOX (Mott–Schottky, VB-XPS) que podamos incluir como datos de prueba independientes.

## 11. Páginas que no pude leer
- iopscience (Butler y Ginley), pmc.ncbi.nlm.nih.gov (Kiyohara), osti.gov (Patel y Kaufman) y sciencedirect (Haghshenas): bloqueados por robots o por verificación del navegador. En Haghshenas usé el manuscrito aceptado del repositorio UNSWorks.
- api.crossref.org para Xu y Schoonen y la API de Europe PMC para Kiyohara: respondieron con límite de frecuencia (HTTP 429). Los metadatos de esos dos trabajos se verificaron por OpenAlex.

---

## Referencias (DOI verificado contra Crossref u OpenAlex)

1. Nethercot, A. H. (1974). Prediction of Fermi energies and photoelectric thresholds based on electronegativity concepts. *Phys. Rev. Lett.* 33, 1088–1091. https://doi.org/10.1103/PhysRevLett.33.1088
2. Butler, M. A.; Ginley, D. S. (1978). Prediction of flatband potentials at semiconductor-electrolyte interfaces from atomic electronegativities. *J. Electrochem. Soc.* 125, 228–232. https://doi.org/10.1149/1.2131419
3. Xu, Y.; Schoonen, M. A. A. (2000). The absolute energy positions of conduction and valence bands of selected semiconducting minerals. *Am. Mineral.* 85, 543–556. https://doi.org/10.2138/am-2000-0416
4. Trasatti, S. (1986). The absolute electrode potential: an explanatory note. *Pure Appl. Chem.* 58, 955–966. https://doi.org/10.1351/pac198658070955
5. Stevanović, V.; Lany, S.; Ginley, D. S.; Tumas, W.; Zunger, A. (2014). Assessing capability of semiconductors to split water using ionization potentials and electron affinities only. *Phys. Chem. Chem. Phys.* 16, 3706–3714. https://doi.org/10.1039/c3cp54589j (texto leído: https://www.colorado.edu/faculty/zunger-matter-by-design/sites/default/files/attached-files/649.pdf)
6. Patel, M. Y.; Mortelliti, M. J.; Dempsey, J. L. (2022). A compendium and meta-analysis of flatband potentials for TiO2, ZnO, and SnO2 semiconductors in aqueous media. *Chem. Phys. Rev.* 3, 011303. https://doi.org/10.1063/5.0063170
7. Hankin, A.; Bedoya-Lora, F. E.; Alexander, J. C.; Regoutz, A.; Kelsall, G. H. (2019). Flat band potential determination: avoiding the pitfalls. *J. Mater. Chem. A* 7, 26162–26176. https://doi.org/10.1039/c9ta09569a
8. Kavan, L. (2024). Electrochemistry and band structure of semiconductors (TiO2, SnO2, ZnO): avoiding pitfalls and textbook errors. *J. Solid State Electrochem.* 28, 829–845. https://doi.org/10.1007/s10008-023-05770-w
9. Beranek, R. (2011). (Photo)electrochemical methods for the determination of the band edge positions of TiO2-based nanomaterials. *Adv. Phys. Chem.* 2011, 786759. https://doi.org/10.1155/2011/786759
10. Kaufman, A. J.; Nielander, A. C.; Meyer, G. J.; Maldonado, S.; Ardo, S.; Boettcher, S. W. (2024). Absolute band-edge energies are over-emphasized in the design of photoelectrochemical materials. *Nat. Catal.* 7, 615–623. https://doi.org/10.1038/s41929-024-01161-0
11. Scanlon, D. O. et al. (2013). Band alignment of rutile and anatase TiO2. *Nat. Mater.* 12, 798–801. https://doi.org/10.1038/nmat3697
12. Abdullah, E. A. (2019). Band edge positions as a key parameter to a systematic design of heterogeneous photocatalyst. *Eur. J. Chem.* 10, 82–94. https://doi.org/10.5155/eurjchem.10.1.82-94.1809
13. Fuentes, J. P. et al. (2023). Prediction of band edge potentials and reaction products in photocatalytic copper and iron sulfides. *Photochem. Photobiol. Sci.* 22, 1855–1864. https://doi.org/10.1007/s43630-023-00415-3
14. Castelli, I. E. et al. (2012). Computational screening of perovskite metal oxides for optimal solar light capture. *Energy Environ. Sci.* 5, 5814–5819. https://doi.org/10.1039/c1ee02717d
15. Pelatt, B. D.; Ravichandran, R.; Wager, J. F.; Keszler, D. A. (2011). Atomic solid state energy scale. *J. Am. Chem. Soc.* 133, 16852–16860. https://doi.org/10.1021/ja204670s
16. Robertson, J. (2000). Band offsets of wide-band-gap oxides and implications for future electronic devices. *J. Vac. Sci. Technol. B* 18, 1785–1791. https://doi.org/10.1116/1.591472
17. Toroker, M. C.; Kanan, D. K.; Alidoust, N.; Isseroff, L. Y.; Liao, P.; Carter, E. A. (2011). First principles scheme to evaluate band edge positions in potential transition metal oxide photocatalysts and photoelectrodes. *Phys. Chem. Chem. Phys.* 13, 16644–16654. https://doi.org/10.1039/c1cp22128k
18. Park, K.-W.; Kolpak, A. M. (2019). Optimal methodology for explicit solvation prediction of band edges of transition metal oxide photocatalysts. *Commun. Chem.* 2, 79. https://doi.org/10.1038/s42004-019-0179-3
19. Hinuma, Y.; Grüneis, A.; Kresse, G.; Oba, F. (2014). Band alignment of semiconductors from density-functional theory and many-body perturbation theory. *Phys. Rev. B* 90, 155405. https://doi.org/10.1103/PhysRevB.90.155405
20. Das, T.; Rocquefelte, X.; Jobic, S. (2018). Absolute reference energy to realign the band-edges of inorganic semiconductors using first-principles calculations. arXiv:1812.01293. https://arxiv.org/abs/1812.01293
21. Ganose, A. M.; Cuff, M.; Butler, K. T.; Walsh, A.; Scanlon, D. O. (2016). Interplay of orbital and relativistic effects in bismuth oxyhalides: BiOF, BiOCl, BiOBr, and BiOI. *Chem. Mater.* 28, 1980–1984. https://doi.org/10.1021/acs.chemmater.6b00349
22. Haghshenas, Y.; Wong, W. P.; Sethu, V.; Amal, R.; Kumar, P. V.; Teoh, W. Y. (2024). Full prediction of band potentials in semiconductor materials. *Mater. Today Phys.* 46, 101519. https://doi.org/10.1016/j.mtphys.2024.101519 (manuscrito aceptado: https://unsworks.unsw.edu.au/handle/1959.4/102964)
23. Masood, H. et al. (2023). Enhancing prediction accuracy of physical band gaps in semiconductor materials. *Cell Rep. Phys. Sci.* 4, 101555. https://doi.org/10.1016/j.xcrp.2023.101555
24. Kiyohara, S.; Hinuma, Y.; Oba, F. (2024). Band alignment of oxides by learnable structural-descriptor-aided neural network and transfer learning. *J. Am. Chem. Soc.* 146, 9697–9708. https://doi.org/10.1021/jacs.3c13574
25. Choudhary, K.; Garrity, K. F. (2024). InterMat: accelerating band offset prediction in semiconductor interfaces with DFT and deep learning. *Digital Discovery* 3. https://doi.org/10.1039/d4dd00031e
26. Choudhary, K. et al. (2020). The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design. *npj Comput. Mater.* 6, 173. https://doi.org/10.1038/s41524-020-00440-1
27. Davies, D. W.; Butler, K. T.; Walsh, A. (2019). Data-driven discovery of photoactive quaternary oxides using first-principles machine learning. *Chem. Mater.* 31, 7221–7230. https://doi.org/10.1021/acs.chemmater.9b01519
28. Pearson, R. G. (1988). Absolute electronegativity and hardness: application to inorganic chemistry. *Inorg. Chem.* 27, 734–740. https://doi.org/10.1021/ic00277a030
29. Allen, L. C. (1989). Electronegativity is the average one-electron energy of the valence-shell electrons in ground-state free atoms. *J. Am. Chem. Soc.* 111, 9003–9014. https://doi.org/10.1021/ja00207a003
30. Ouyang, R.; Curtarolo, S.; Ahmetcik, E.; Scheffler, M.; Ghiringhelli, L. M. (2018). SISSO: a compressed-sensing method for identifying the best low-dimensional descriptor in an immensity of offered candidates. *Phys. Rev. Mater.* 2, 083802. https://doi.org/10.1103/PhysRevMaterials.2.083802
31. Bartel, C. J. et al. (2019). New tolerance factor to predict the stability of perovskite oxides and halides. *Sci. Adv.* 5, eaav0693. https://doi.org/10.1126/sciadv.aav0693
32. Cranmer, M. (2023). Interpretable machine learning for science with PySR and SymbolicRegression.jl. arXiv:2305.01582. https://arxiv.org/abs/2305.01582
33. Wang, Y.; Wagner, N.; Rondinelli, J. M. (2019). Symbolic regression in materials science. *MRS Commun.* 9, 793–805. https://doi.org/10.1557/mrc.2019.85

Nota sobre la verificación: los números de página o de artículo de Patel 2022 (011303), Park y Kolpak 2019 (79), Choudhary 2020 (173) y el volumen de InterMat se tomaron de mi conocimiento previo y no del registro consultado. Los DOI sí están verificados.
