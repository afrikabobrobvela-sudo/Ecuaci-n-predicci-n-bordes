# Ronda 2 de extracción: solo registros de alto rendimiento

Mismas reglas que PROTOCOLO.md (léelo primero), con estos filtros ADICIONALES. Solo extrae un registro si cumple TODO esto en el texto (no en el SI):
1. La escala del valor de U_fb está escrita (vs RHE, vs NHE/SHE, vs Ag/AgCl, vs SCE) y, si es Ag/AgCl o SCE, el relleno está escrito (saturado, 3 M KCl...). "SCE" o "saturated calomel" cuenta como saturado.
2. Si la escala es RHE, el pH del electrolito del Mott–Schottky está escrito.
3. El electrolito del Mott–Schottky es acuoso y SIN par redox (sin ferri/ferrocianuro, sin I3−/I−). Medido en oscuridad.
4. El Eg del mismo material está medido en el estudio (Tauc/DRS/absorción) y escrito como número.
5. Material puro (no dopado intencionalmente, no irradiado, no compuesto). Controles puros dentro de estudios de heterouniones: sí.
Si un estudio no cumple, regístralo en descartados con motivo "ronda2_filtro" y el criterio que falla, y pasa al siguiente sin gastar más tiempo.
Evita todos los DOI de dois_usados.txt.
Estrategia: los artículos de Sci Rep, RSC Adv, Nanoscale Adv, MDPI (Catalysts, Nanomaterials, Materials), Frontiers y ACS Omega (si abre) suelen escribir los valores en texto. Usa WebSearch con frases como "flat band potential" "vs. Ag/AgCl" "saturated KCl" "Mott-Schottky" <material>.
