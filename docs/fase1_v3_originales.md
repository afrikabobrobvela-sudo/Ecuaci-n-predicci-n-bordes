# Fase 1, adenda v3: contraste con los artículos originales

Esta adenda cierra los pendientes de la sección D de `fase1_v2_acuerdo.md` con los PDF que aportó Rodrigo el 2026-10-14. Las secciones B y C, ya aprobadas, siguen vigentes. Donde algo de abajo las afecta, lo propongo como decisión nueva (sección C de esta adenda) y no modifico lo aprobado.

Lectura: los ocho artículos se leyeron en texto completo (TC). Las tablas que la extracción de texto deformó se comprobaron sobre la imagen del PDF: Tabla I de Butler–Ginley y Tabla 1 de Pelatt.

## A. Erratas nuevas

| # | Afirmación de v1/v2 | Corrección, con cita del original |
|---|---|---|
| E11 | El término 0.059·(pH_PZC − pH) y la constante 4.44 o 4.5 eV "forman parte de Butler–Ginley" | **Falso.** La ecuación original es EA = E0 + V_fb + ΔE_f + ΔpH, con "Eo = 4.75 eV for SCE" (p. 228). Esto equivale a unos 4.51 eV para SHE si se usa +0.241 V. El término con 0.059 y E0 = −4.5 V vs NHE (Bockris y Khan 1993) es de Xu y Schoonen (Ec. 6). El 4.44 eV (Trasatti) es posterior. |
| E12 | Xu y Schoonen validan "unos 50 minerales" | Son unos 50 óxidos **y** unos 50 sulfuros: conté 57 y 56 filas. Su E_CB es siempre calculado. El U_fb⁰ medido solo existe para 21 óxidos y 9 sulfuros, y muchos vienen de Butler–Ginley o Nozik, así que no son independientes. La concordancia declarada es cualitativa: "generally within 0.5 eV" (p. 550). La escala de χ es la de Pearson 1988. |
| E13 | Xu y Schoonen usan pH_PZC medido | Solo a veces. Si falta, lo estiman "using the method developed by Butler and Ginley"; en sulfuros usan 2.0 por defecto. |
| E14 | El centro del gap SSE "se referencia al nivel del H" (Pelatt) | **Impreciso.** Con el conjunto ampliado, las rectas de cationes y aniones se cortan en −4.9 eV (IC 95 %: −4.6 a −5.1). Solo con LOESS se acerca a −4.5. |
| E15 | Haghshenas: auditar la "Tabla S1" (87 VBM) | En el SI la tabla experimental es la **Tabla S5** y tiene 86 filas. No cuadra con la Tabla S1 y los 87 VBM de la v2: hay que contrastarlo con la versión editorial del artículo principal; el manuscrito aceptado que leí en la fase 1 no traía la tabla. |
| E16 | Butler–Ginley "validado en 11 óxidos" | Correcto. Añado lo que faltaba: precisión de medida "about ±0.1V" y error de predicción "∼0.2V" con adsorción específica. El ajuste es "with no adjustable parameters". Los V_fb son secundarios, "measured or corrected to pH = 13.3", sin método declarado. |
| E17 | Cita de Zhang 2023 | Es el mismo trabajo en dos ediciones: Angew. Chem. 135 (10.1002/ange.202308411) y Angew. Chem. Int. Ed. 62 (10.1002/anie.202308411). Citaremos la Int. Ed. |

## B. Hallazgos que cambian el diseño

1. **Haghshenas (base de M5).**
   - Sus 86 VBM "experimentales" van en escala "pH 0 vs vacuum". El método, el electrolito, el pH original y la conversión: no encontrado.
   - CBM = VBM + Eg en las 86 filas, así que el CBM no es un dato independiente.
   - Hay 11 materiales repetidos con discrepancias de hasta 0.9 eV (FeO), y por tanto unas 72 fórmulas únicas.
   - Entre las fuentes hay revisiones, una tesis y artículos explícitamente computacionales ("first-principles", "computational screening").
   - **No hay ningún oxihaluro de Bi.**
   - Su RMSE de 0.27 V en el conjunto "unseen experimental" es con partición aleatoria (70/15/15).
   - **Artículo principal (leído en TC).** Dice "87 samples" y remite a la "Table S1". El SI la rotula como Tabla S5 y en el texto extraído cuento 86 filas; la fila que falta no está resuelta.
   - **Normalización.** Todos los VBM se llevan a pH 0 sumando −0.059 V por unidad de pH. Eso supone una respuesta nernstiana en todos los materiales, sulfuros incluidos, y no consta que hayan distinguido los valores ya dados en RHE.
   - **Respuesta a E5 (verificada en parte).**
     - En la validación de superficies, el artículo dice que en TiO2 anatasa (101) y rutilo (110) "physical VBMs were measured to range from − 7.5 to − 7.32 V vs. vacuum for both [49]", y la ref. 49 es Butler y Ginley 1978.
     - Butler y Ginley no miden ningún VBM ni distinguen facetas. Su Tabla I se titula "Calculated electronegativity and electron affinity and measured flatband potential", con χ(TiO2) = 5.83 eV y EA = 4.33 eV, ambos calculados (comprobado en la imagen, p. 231).
     - χ + ½Eg = 5.83 + 1.5 = 7.33 eV, que coincide con el −7.32 V.
     - **Conclusión:** Haghshenas presenta como medido un valor que es compatible con un cálculo por la propia ecuación de electronegatividad. Esto afecta a su validación de superficies, no a su conjunto de entrenamiento: las tres filas de TiO2 de la Tabla S5 (−7.24, −7.55 y −7.41) citan otras fuentes, no a Butler y Ginley.
     - Que el entrenamiento esté contaminado no está demostrado. Para afirmarlo habría que abrir sus 18 referencias.
2. **Chandramohan 2026.**
   - Promedia la fórmula de electronegatividad con dos modelos de ML; no la corrige.
   - Los datos son solo de perovskitas híbridas, con particiones aleatorias.
   - El solapamiento con nuestra originalidad es bajo, y la declaración aprobada se mantiene.
3. **Zhang 2023.** El IP de un mismo óxido varía varios eV según la faceta (CeO2: 4.2 a 8.2 eV, calculado). Una corrección que dependa solo de la composición tiene un límite físico. Esto respalda separar el conjunto FE y no esperar errores menores que la dispersión entre facetas.
4. **Pelatt 2015 (base de M3).**
   - La SSE da un borde por elemento: Bi³⁺ −4.33, O²⁻ −7.98, Cl⁻ −8.61, Br⁻ −7.12 e I⁻ −6.20 eV.
   - El artículo no da ninguna regla para bordes de ternarios u oxihaluros (no encontrado). M3 necesita una regla nuestra, declarada.
   - Pelatt excluye los cationes s², incluido Bi³⁺, del cálculo de los aniones.

## C. Decisiones nuevas (propuestas para tu aprobación)

- **C6. Constante de M0.** M0 se implementa en dos variantes: 4.44 eV (la de uso común) y la original de Butler–Ginley (4.75 eV vs SCE). La diferencia, unos 0.07 V, se reporta como incertidumbre del propio baseline.
- **C7. Subconjunto histórico.** Los 11 V_fb de la Tabla I de Butler–Ginley entran al piloto como `historico_BG`. Solo sirven para comprobar que nuestro M0 reproduce el original; no entrenan ni validan. Los U_fb⁰ de Xu y Schoonen no se extraen como datos, porque no son independientes.
- **C8. PZC.** Se mantiene la regla de no imputar en el análisis principal. La correlación pzzp–χ de Butler–Ginley (Fig. 2) solo se usa en una variante de sensibilidad de M1, marcada como imputada, porque es lo que hicieron Xu y Schoonen.
- **C9. M3 (SSE).** Para compuestos no binarios, el borde será la media ponderada estequiométrica de las SSE de cationes (CB) y de aniones (VB). Es una regla nuestra, no de Pelatt, y se declara así.
- **C10. M5.** La Tabla S5 de Haghshenas se usa como conjunto de comparación de la literatura, no como etiquetas EQ. Su métrica publicada no se compara con nuestras métricas de partición agrupada (refuerza C5).

## D. Pendiente

Ninguno de lectura. La sección D de la v2 queda cerrada. Lo único opcional es abrir las 18 referencias de la Tabla S5 de Haghshenas, que propongo hacer en la fase 3, como parte de la auditoría del comparador M5.
