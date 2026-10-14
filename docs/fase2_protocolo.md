# Fase 2. Protocolo de la base de datos y piloto

Fecha: 14 de octubre de 2026. Este protocolo se basa en el acuerdo de cierre de la Fase 1 v2 (`fase1/fase1_v2_acuerdo.md`, secciones B y C).

**Archivos de esta fase:**
- `piloto_EQ.csv`: 19 registros electroquímicos.
- `piloto_FE.csv`: 7 registros de fotoemisión.
- `piloto_excluidos.csv`: 21 registros excluidos, con su motivo.
- `scripts/piloto_fase2.py` en el repositorio: genera los tres CSV y calcula todas las conversiones. Ningún número convertido se hizo a mano.

---

## 1. Estructura: tres conjuntos y un subconjunto de enlace

| Conjunto | Observable que se guarda | Qué **no** se hace |
|---|---|---|
| **EQ** (electroquímica) | U_fb u otro observable identificado (potencial de transición con luz intermitente, Gärtner–Butler, OCP saturado), **al pH experimental** | No se renombra como BC/BV. No se normaliza a pH 0 antes del análisis. U_SHE(pH 0) existe solo como columna derivada para análisis de sensibilidad |
| **AQ** (bordes acuosos inferidos) | U_C o U_V **solo** con soporte: tipo n/p demostrado y Δn o Δp estimados (densidad de portadores y masa efectiva, o medición independiente), con incertidumbre propagada | No se aplica una resta fija de 0.1 a 0.3 V |
| **FE** (fotoemisión) | Lo realmente medido: función de trabajo (SECO), IP, o VBM − E_F | Un VBM − E_F de XPS **no** se convierte a escala absoluta sin la función de trabajo **de la muestra** (no la del instrumento) |
| **Enlace** | Pares EQ–FE de la misma muestra o de muestras equivalentes caracterizadas | Las comparaciones no emparejadas son exploratorias y no se identifican con un dipolo |

## 2. Criterios de inclusión
1. **Medición propia** del artículo, no citada de otra fuente.
2. **Método identificable**: Mott–Schottky, luz intermitente, Gärtner–Butler, OCP saturado, fotoelectroquímica, metilviológeno (con su modelo), UPS, IPES o XPS-VB.
3. **Escala recuperable**: electrodo de referencia identificado (EQ) o referencia energética explícita (FE). Si no se conoce el relleno de KCl de un Ag/AgCl, el registro se incluye con incertidumbre ampliada (sección 4) y confianza "bajo".
4. **Material monofásico** confirmado o declarado (técnica registrada). Las muestras dopadas o defectuosas se registran como variante, con su bandera.
5. **Valor numérico en el texto o en una tabla.** Los valores leídos de una figura se marcan como tales, y en el piloto no se usaron.
6. Eg: se registra si fue medido, con su método. Si es un valor citado, se marca "no medido".

## 3. Criterios de exclusión (con categoría, para la pregunta 1 y para auditoría)
| Categoría | Ejemplo en el piloto |
|---|---|
| `ecuacion_electronegatividad` | X04: BiOI con χ = 6.10 eV y Ee = 4.50 eV |
| `calculado_DFT` | X01 |
| `conversion_invalida` | X09, X10: VBM − E_F de XPS publicado como "vs NHE" |
| `referencia_no_identificable` | X05–X07 |
| `sin_valor` / `sin_valor_textual` | X03, X11, X15, X17 |
| `sin_medicion` | X02, X13 |
| `no_monofasico` / `fase_no_confirmada` | X08, X12, X14 |
| `fuente_secundaria` | X16 |
| `no_verificado` | X18 |

**Importante (acordado en la Fase 1):** estos excluidos **no** estiman la fracción de la literatura que usa la ecuación. La búsqueda se dirigió a mediciones, así que el denominador está sesgado. La pregunta 1 requiere una muestra documental propia (sección 9).

## 4. Conversiones (verificadas)
| Electrodo | E vs SHE a 25 °C (V) | Fuente | Nota |
|---|---|---|---|
| Ag/AgCl, KCl saturado | +0.197 | Inzelt, Lewenstam y Scholz (eds.), *Handbook of Reference Electrodes*, Springer 2013, https://doi.org/10.1007/978-3-642-36188-3 | El valor de 0.197 V también aparece en Ma et al. 2014, Hankin et al. 2019 y Pawar y Tahir 2018 |
| Ag/AgCl, KCl 3 M | +0.210 | Inzelt et al. 2013 | Bhachu et al. 2016 usan 0.1976 V para 3 M, una discrepancia de 0.012 V que se registra |
| Ag/AgCl, KCl no reportado | +0.216 ± 0.019 | Centro y semiamplitud del intervalo 0.197 (saturado) a 0.235 (1 M) | La incertidumbre se suma en cuadratura |
| SCE saturado | +0.241 | Inzelt et al. 2013 | |
| Hg/Hg2SO4, K2SO4 saturado | +0.640 (declarado por los autores) | Por verificar contra Inzelt | En el registro P14 los autores declaran 0.640 V pero su fórmula usa 0.682 V: incertidumbre de 0.042 V |
| RHE | U_SHE = U_RHE − 0.0592·pH | Nernst a 25 °C | Requiere el pH; sin pH no se convierte |
| Vacío | ε = −e·U_SHE − 4.44 eV | Trasatti 1986 (U_SHE,abs = +4.44 ± 0.02 V) | Solo para comparar con FE; sensibilidad con 4.5 eV |

**Pendiente:** contrastar los valores de 3 M, 1 M y Hg/Hg2SO4 directamente en la tabla de Inzelt. Solo verifiqué los metadatos del libro; los valores numéricos los tomé de fuentes secundarias (tabla NACE en Wikipedia y apuntes del curso de Ardo, UC Irvine).

## 5. Campos (plantilla)
Las columnas están en los encabezados de `piloto_EQ.csv` y `piloto_FE.csv`. Las reglas principales son:

| Campo | Regla |
|---|---|
| `familia_a_priori` | Se asigna **antes** del ajuste: óxido binario, óxido ternario, óxido ternario de Bi, sulfuro, nitruro (exploratorio), oxihaluro de Bi, solución sólida de oxihaluro de Bi, oxihaluro rico en Bi |
| `particion` | `reserva_BiOX` para **todos** los oxihaluros de Bi (incluidas soluciones sólidas y fases ricas en Bi). `entrenamiento` para el resto. Los compuestos de Bi que no son oxihaluros entran en entrenamiento |
| `escala_reportada`, `E_ref_vs_SHE_V`, `fuente_E_ref` | Siempre la escala original y la constante usada, con su fuente |
| `U_SHE_pHexp_V` | Variable principal de EQ |
| `incert_ref_V`, `incert_metodo_V`, `incert_metodo_origen` | Se combinan en cuadratura. Si el estudio no reporta incertidumbre, se usan **0.10 V supuestos**, marcados como "supuesta" (elección provisional, abierta a revisión) |
| `U_SHE_autor_V`, `discrepancia_vs_autor_V` | Se recalcula la conversión del autor. Una discrepancia de más de 0.05 V se marca como error de conversión |
| `pzc`, `pzc_nivel`, `iep` | PZC e IEP por separado. Nivel: misma muestra, externo compatible o desconocido. **No se imputa** |
| `tampon` | Sí o no. Kageshima et al. 2025 muestran que en electrolitos no tamponados casi neutros los bordes pueden dejar de estar fijos bajo iluminación (lo marco como pendiente de leer en detalle) |
| `frecuencia_Hz` | Frecuencia única, barrido o "n.r.". Si existe, se registra la dispersión con la frecuencia |
| `estudio` | Identificador del estudio para el efecto aleatorio y para la validación agrupada |
| `lectura` | TC-d, R o P |

**Campos adicionales para la versión completa** (no hacían falta en el piloto): `serie_pH_n`, `pendiente_mV_pH`, `densidad_portadores`, `Delta_n_o_p`, `enlace_con` (id del registro FE de la misma muestra) y `valor_de_figura`.

## 6. Control de calidad y nivel de confianza
**Banderas** (se registran todas las que apliquen): pH no reportado; relleno de la referencia no reportado; escala ambigua; frecuencia no reportada o única sin verificación de dispersión; error de conversión del autor; tipo n/p atípico sin explicación; contradicciones internas; Eg no medido; variante dopada o defectuosa; fase no confirmada en el texto leído.

**Regla de confianza:**
- **Alto:** referencia y relleno documentados, pH medido o reportado, fase confirmada en el texto leído, sin errores de conversión, y además dos o más métodos concordantes o una dispersión con la frecuencia verificada.
- **Medio:** referencia documentada, pH reportado o deducible del electrolito, fase confirmada o declarada. Admite como máximo una bandera menor (frecuencia única, Eg no medido, discrepancia de conversión menor de 0.05 V, o error de conversión del autor cuando el valor medido y la referencia son recuperables).
- **Bajo:** pH no reportado, relleno no reportado, escala ambigua, tipo o valor atípico sin explicación, contradicciones internas, o variante defectuosa.

## 7. Resultados del piloto
**Composición:**
- **EQ:** 19 registros de 11 estudios. 9 están en la reserva BiOX: BiOCl (×5, uno defectuoso), BiOBr, BiOI, dos soluciones sólidas y Bi24O31Cl10. Los otros 10 son de entrenamiento: α-Fe2O3 (×3, mismo estudio), TiO2 (×3), WO3, ZnO, BiVO4 y LaFeO3.
- **FE:** 7 registros: una función de trabajo y seis VBM − E_F de XPS.
- **Excluidos:** 21 registros.

**Confianza en EQ:**
- Ningún registro alcanza "alto".
- 8 quedan en "medio" (2 de la reserva BiOX y 6 de entrenamiento).
- 11 quedan en "bajo" (7 de la reserva y 4 de entrenamiento).

**Hallazgos que cambian el diseño:**
1. **La reserva BiOX tiene mala calidad de datos.** 7 de sus 9 registros quedan en "bajo": pH no reportado (4 de 9), relleno de la referencia no reportado (4), tipo p atípico para BiOCl (P05) y valores contradictorios. Hay que reservar BiOX, pero la prueba externa solo será informativa si se buscan activamente mediciones de mejor calidad, sobre todo en películas.
2. **El conjunto AQ queda vacío.** Ningún registro del piloto permite inferir Δn o Δp con soporte. Esto confirma la decisión B3: **el primer resultado será una evaluación de potenciales de banda plana**, no de bordes.
3. **El conjunto FE casi no tiene datos absolutos.** En la literatura de fotocatálisis, el XPS-VB se reporta respecto a E_F (6 de 7 registros FE). Sin la función de trabajo de la misma muestra no se puede ubicar en vacío. Hay que buscar FE en la literatura de ciencia de superficies (UPS con SECO, IPES), no en la de fotocatálisis.
4. **Se detectan errores de conversión de los autores:**
   - P07: Bhachu et al. reportan +0.58 V_RHE, pero su medición convertida da unos +0.28 V_RHE (diferencia de 0.285 V).
   - P14: referencia declarada de 0.640 V frente a 0.682 V en la fórmula.
   - X09 y X10: XPS publicado como "vs NHE" sin convertir.
   - Pérez del Pulgar et al. convierten XPS a NHE con la **función de trabajo del instrumento** (4.55 eV), no la de la muestra.
   - Sin el recálculo del script, estos errores habrían entrado en la base.
5. **Un mismo material puede dar valores muy distintos según el método** (Hankin 2019, misma película de α-Fe2O3 a pH 13.65): Mott–Schottky da −0.68 V, mientras que luz intermitente y Gärtner–Butler con H2O2 dan alrededor de −0.39 V. Son 0.29 V de diferencia por el método, y Mott–Schottky con corrección de Helmholtz va de −0.77 a −0.32 V según la capacitancia supuesta. Esto respalda el efecto aleatorio por estudio y una bandera por método.
6. **La respuesta al pH no siempre es nernstiana** (Lee 2023, anatasa): 128, 25 y 137 mV/pH por tramos, y 65 mV/pH en el ajuste global. Esto respalda conservar el pH original.
7. **Faltan sulfuros en el piloto.** No se recuperó ningún registro de sulfuro válido. Para la base completa hay que buscarlos con prioridad.
8. **El acceso es limitado.** RSC, ACS, Elsevier y PMC bloquearon parte de las lecturas automáticas. El piloto se basa sobre todo en Scientific Reports, MDPI y los artículos de RSC que sí se pudieron leer, lo que también sesga la muestra hacia el acceso abierto.

## 8. Decisiones tomadas en esta fase
1. **Incertidumbre por defecto de 0.10 V** cuando el estudio no la reporta. Es una elección provisional y se marca "supuesta".
2. **Ag/AgCl con relleno desconocido:** se usa 0.216 ± 0.019 V en lugar de suponer saturado.
3. **Los valores de figuras no se usan** hasta que se defina un protocolo de digitalización con incertidumbre.
4. **Las muestras amorfas** (P17) se registran, pero se marcan fuera del dominio de los modelos para sólidos cristalinos.
5. **Las variantes defectuosas o dopadas** (P02) se registran y se excluyen del ajuste principal.
6. **Los registros de un mismo estudio** (Hankin, Bhachu, Lee) se agrupan con su identificador para la validación.

## 9. Dudas abiertas
1. ¿Aceptas la incertidumbre por defecto de 0.10 V, o prefieres excluir del ajuste los registros sin incertidumbre reportada?
2. Para la pregunta 1, propongo una muestra aleatoria estratificada de 150 artículos (50 sobre BiOX, 50 sobre TiO2 y 50 sobre g-C3N4, publicados entre 2020 y 2025), seleccionados por palabra clave sin filtrar por método. Se clasificaría el origen de cada posición de banda: ecuación, Mott–Schottky, XPS, DFT, citada o sin fuente. ¿Te parece adecuado el tamaño?
3. ¿Incluimos fotoemisión de monocristales y películas de ciencia de superficies, aunque no sean los materiales de los artículos de fotocatálisis? Recomiendo que sí, porque si no FE queda vacío.
4. Kageshima et al. 2025 sugiere que el tampón importa bajo iluminación. ¿Añadimos el tampón como covariable o solo como bandera? Recomiendo bandera en el piloto y covariable si hay suficientes datos.

## 10. Lo que necesito de ti
1. Tu revisión del protocolo, sobre todo la regla de confianza (sección 6) y las decisiones 1 y 2 de la sección 8.
2. Tus mediciones propias de BiOX (Mott–Schottky con frecuencias, pH y referencia, y XPS-VB con función de trabajo si la tienes). Mejorarían mucho la reserva externa, que hoy es de baja calidad.
3. Si tienes acceso institucional: el SI de Haghshenas (Tabla S1), Pelatt 2015 y Butler y Ginley 1978. Siguen pendientes de la sección D de la Fase 1. El manuscrito aceptado de Haghshenas no incluye la Tabla S1, aunque sí cita a Butler–Ginley como fuente de los VBM de TiO2 (7.32 a 7.5 eV vs vacío). Que esos valores sean medidos o calculados sigue sin verificar.

## Fuentes del piloto (todas con DOI)
Xu, Teng, Teng 2016, https://doi.org/10.1038/srep32457 · Liu et al. 2016, https://doi.org/10.1038/srep28689 · Bhachu et al. 2016, https://doi.org/10.1039/c6sc00389c · Pérez del Pulgar et al. 2024, https://doi.org/10.1039/d4ew00410h · Ma et al. 2014, https://doi.org/10.1039/c4sc00469h · Hankin et al. 2019, https://doi.org/10.1039/c9ta09569a · WO3, RSC Adv. 2019, https://doi.org/10.1039/c8ra08875f · Lee et al. 2023, https://doi.org/10.3390/catal13061000 · Lichterman et al. 2015, https://doi.org/10.1039/c5ee01014d · Pawar y Tahir 2018, https://doi.org/10.1038/s41598-018-21821-z · Kubas et al. 2026, https://doi.org/10.1038/s41598-025-26341-1 · Baddorf 2023, https://doi.org/10.1038/s41598-023-40187-5 · Lv et al. 2016, https://doi.org/10.1038/srep19347 · Zhao et al. 2024, https://doi.org/10.1039/d4ta02605e · Kageshima et al. 2025, https://doi.org/10.1039/d5sc01816a. Los excluidos tienen su DOI en `piloto_excluidos.csv`.

**Nota de lectura:** todos los registros se extrajeron con consultas dirigidas sobre el texto completo (TC-d). Los valores se tomaron del texto, no de las figuras. Antes de usar la base para el ajuste, conviene que un humano revise una muestra de registros contra el PDF.
