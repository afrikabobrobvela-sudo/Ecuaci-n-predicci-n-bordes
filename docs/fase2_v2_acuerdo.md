# Fase 2, versión 2: acuerdo sobre el protocolo y piloto unificado

Este documento reemplaza a `fase2_protocolo.md` donde ambos discrepan. El piloto unificado está en `piloto_unificado_EQ.csv` y `piloto_unificado_FE.csv`, generados con `scripts/piloto_unificado.py` (en el repositorio).

## A. Decisiones (las tomo yo, con base en ambos pilotos). **Aprobadas por Rodrigo el 2026-10-14.**

1. **Unidad de registro.** Adopto la de ChatGPT: estudio × muestra × observable × condición × determinación. Una serie de pH o de frecuencias da varios registros, nunca un promedio que oculte la condición. Los promedios publicados por el autor se admiten solo como registros propios, marcados como "no réplica independiente".
2. **Cuatro capas separadas por registro.** (1) Valor publicado tal cual, con su escala. (2) Interpretación del autor (banda plana, "E_CB", tipo n o p) y su conversión, si la da. (3) Nuestra transformación. (4) Admisión (admitido, cuarentena o excluido) y aptitud para el ajuste. Ser admitido no implica ser apto.
3. **Incertidumbre.** Retiro mi 0.10 V por defecto: era una suposición mía, no un dato. Solo se registra la incertidumbre reportada. La dispersión no reportada se estima en el modelo mediante τ (estudio) y la varianza residual (C2 de la fase 1).
4. **Conversiones.** La conversión definitiva queda vacía si falta el relleno del electrodo, o el pH en el caso de RHE. En su lugar se da un escenario a 25 °C (saturado a 1 M KCl: +0.197 a +0.235 V para Ag/AgCl; +0.241 a +0.280 V para SCE). Ningún registro sin conversión definitiva entra al ajuste principal; sí puede entrar al análisis de sensibilidad.
5. **Series de control metodológico.** Acepto la propuesta de ChatGPT: forman un subconjunto propio (Hankin 2019, Lee 2023 y, cuando se extraiga, Kageshima). Sirven para estimar el error atribuible al método y al pH, no para ajustar la corrección.
6. **Ventana para la muestra documental de Q1.** Acepto 2015–2025 y la estratifico por periodo (2015–2019, 2020–2025) × material (BiOX, TiO2, g-C3N4). El tamaño se fija en la fase 3, con 50 artículos por estrato como punto de partida, sujeto a tu aprobación.
7. **Registros verificados por una sola parte.** Se marcan con `verificado_por`. **Actualización 2026-10-14:** con tus PDF verifiqué Resasco et al. 2016 (ACS Cent. Sci.) y Koiki y Arotiba 2023 (Heliyon). Solo quedan sin doble verificación los dos promedios multifrecuencia de Lee 2023.

## B. Resultado de la verificación cruzada

He verificado contra la fuente 5 de los 9 estudios aportados por ChatGPT. Todos los valores coinciden. Añado estas banderas:

| Estudio | Bandera nueva |
|---|---|
| Li 2018, CdS (RSC Adv., 10.1039/c8ra00250a) | Declara Ag/AgCl 3 M pero convierte con +0.197 V. El pH del electrolito no se declara; los valores se presentan como "vs NHE, pH 7". S-TAA es multifásico (excluido). |
| Din, Lee y Yang 2022, Bi3O4Cl y Bi5O7I (10.3390/nano12050767) | Usa SCE sin relleno y convierte con +0.244 V. pH y frecuencia no reportados. |
| Jia 2020, BiOBr1−xIx (10.1039/d0ra08211b) | Relleno no reportado; los autores suman 0.21 V. |
| Asha 2020, α-Fe2O3 (10.1039/d0ra07870k) | El estudio usa pH 13 y pH 8; el de cada Mott–Schottky no queda vinculado. |
| Liu y Zhou 2020, Bi2WO6 (10.1039/c9ra09270f) | pH y frecuencia no reportados. El CB se obtiene con un desplazamiento fijo de 0.1 eV y no pasa al conjunto AQ. |

| Resasco 2016, TiO2/BiVO4 (10.1021/acscentsci.5b00402) | Valores confirmados: U_fb 0.19 y 0.08 V vs RHE, VB por UPS 7.61 y 6.99 eV, Eg ≈3.0 y 2.5 eV. Medido en 0.5 M KPi a pH 7, frecuencia n.r. **No declara que UPS y MS sean la misma muestra**, ni si el TiO2 lleva Ta. Su propio CB (VB − Eg) queda solo 0.02–0.04 V por debajo del U_fb. |
| Koiki y Arotiba 2023, WO3 (10.1016/j.heliyon.2023.e20882) | Valores confirmados (0.46 V vs Ag/AgCl; 2.99 eV). **Se mantiene en cuarentena:** el MS se midió en un electrolito redox (Fe(CN)6 3−/4− en KCl), el relleno es contradictorio ("saturated 3 M KCl"), pH y frecuencia n.r., y el Eg contradice su propio borde (~440 nm ≈ 2.82 eV). |

Mi propio piloto añade dos errores de conversión de autor: BiOI de Bhachu (0.285 V) y la fórmula de WO3 (0.682 V en lugar de los 0.640 V declarados).

## C. Piloto unificado

- **EQ:** 45 registros de 22 estudios, contando también los FE. Por subconjunto: 14 de la reserva BiOX, 11 del principal, 7 de control metodológico, 2 de enlace y 11 del subconjunto histórico de Butler–Ginley (C7 de la adenda v3 de la fase 1; solo para reproducir M0).
- **Calidad:** 0 de confianza alta, 14 media y 31 baja.
- **Conversión definitiva posible:** 30 de 45 registros. El resto queda solo como escenario.
- **FE:** 9 registros. Solo 2 son absolutos (VB por UPS de Resasco 2016, ya verificados). Forman el único par EQ/FE, que es exploratorio porque el artículo no declara que se trate de la misma muestra. Hay además una función de trabajo sin IP; los 6 restantes son VBM − E_F relativos.
- **AQ:** sigue vacío. Ningún borde inferido supera la regla de soporte.

## D. Lo que esto implica para la fase 3 (conclusión, no inicio)

1. Solo 6 registros del conjunto principal son aptos para el ajuste (BiVO4, WO3, LaFeO3, CdS ×2 y Bi2WO6); a ellos se suman los 2 de enlace de Resasco 2016, ya verificados pero exploratorios. Con eso no se puede ajustar una corrección con más de un parámetro libre. La fase 3 debe empezar ampliando la extracción, no modelando.
2. En la reserva BiOX predomina la confianza baja. Es la principal debilidad del diseño: sin datos propios medidos con pH, relleno y frecuencia controlados, el test externo será débil.
3. El subconjunto de enlace EQ/FE depende de un solo estudio, ya verificado pero sin muestra pareada declarada.

## E. Lo que necesito de ti

1. Que apruebes las decisiones A1–A7.
2. Resuelto con tus PDF. Solo falta la versión editorial del artículo principal de Haghshenas 2024 (ver `fase1/fase1_v3_originales.md`).
3. Si tienes mediciones propias de BiOX (Mott–Schottky con pH, electrolito, relleno y frecuencias, idealmente con UPS en la misma muestra), son lo que más mejoraría el test externo.
