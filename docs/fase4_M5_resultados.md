# Fase 4, anexo: comparador M5 (Haghshenas et al. 2024) con estructuras del COD

Fecha: 2026-10-14. M5 entra solo como comparador; no se ajustó nada y la reserva BiOX se usa únicamente como prueba, igual que en la fase 4.

Scripts: `scripts/m5/cod_descargar.py` (CIF), `scripts/m5/correr_m5_cod.sh` + `hagh_m5.py` (predicción), `scripts/m5/m5_evaluar.py` (errores). Salidas: `resultados/fase4/m5/` y `data/estructuras_cod/`.

## 1. Qué se hizo

- **Acceso.** Desde este entorno crystallography.net responde (API de búsqueda y descarga de CIF).
- **Código.** Repositorio original `yousof96/physical_band_potentials`, commit 50326f4, sin modificar. Antes de usarlo se comprobó que el envoltorio reproduce los valores de la fase 3 (TiO2 Pmm2 del repo: −7.252 eV y Eg 1.81 eV, idénticos).
- **Estructuras.** Un CIF por fase, elegido en el COD con una regla fijada antes de ver ninguna predicción: grupo espacial de la fase declarada, sin duplicados, presión ambiente, temperatura de celda 200–400 K, menor R y estructura totalmente ordenada con la composición correcta. La fase es la estable a temperatura ambiente, porque los estudios casi nunca la dicen (suposición declarada en `cod_descargar.py`). TiO2 usa anatasa y el rutilo va como sensibilidad.
- **Conversión** (la del repo): U_VB = −E_VBM − 4.44 V; U_CB = −(E_VBM + Eg) − 4.44 V. Igual que M0, se compara con U_fb al pH experimental (tipo n con U_CB, tipo p con U_VB).
  - **M5**: Eg predicho por el CGCNN de band gap del repo (pipeline original).
  - **M5-Egexp**: Eg experimental del registro, la misma información de gap que usa M0 (sensibilidad).

**Cobertura.** Hay CIF para 36 de los 46 compuestos de la base y la reserva (más el rutilo como sensibilidad). Quedan sin predicción 10 compuestos:
- Sin ninguna entrada en el COD: Cu3Ta7O19, Cu3VO4 y Bi12O17Cl2.
- Solo con estructuras desordenadas (ocupación parcial), que el CGCNN no admite: Bi4V2O11, CuFe2O4, MgFe2O4, Li2SnO3, TiVO4 y Bi24O31Br10.
- Ca2Nb3O10 es una nanolámina exfoliada y no tiene un bulk equivalente.

## 2. Resultados

MAE y sesgo en V. Los IC 95 % salen de un bootstrap por estudio. M0a se calcula sobre los mismos registros que M5.

| Conjunto | n (est.) | M0a MAE · sesgo | M5 MAE · sesgo | MAE(M5) − MAE(M0a) |
|---|---|---|---|---|
| Entrenamiento, tipo n | 45 (32) | 0.41 · −0.26 | **0.70** [0.52, 0.87] · −0.43 | **+0.29 [+0.12, +0.47]** |
| ↳ fuera del ajuste de Haghshenas | 15 (13) | 0.39 · −0.21 | 0.57 · −0.44 | +0.18 [−0.03, +0.49] |
| ↳ dentro de su ajuste (no ciego) | 30 (21) | 0.42 · −0.28 | 0.76 · −0.43 | +0.34 [+0.13, +0.55] |
| Entrenamiento, tipo p | 12 (10) | 1.59 · −1.59 | **1.16** [0.89, 1.50] · −1.16 | **−0.43 [−0.66, −0.15]** |
| Reserva BiOX, tipo n | 15 (13) | 0.63 · −0.60 | **2.41** [1.63, 3.37] · −2.41 | **+1.78 [+0.99, +2.74]** |

En la reserva, K1 sobre esos mismos 15 registros da 0.46 V. Con el Eg experimental (M5-Egexp) los números apenas cambian: 0.73 V en tipo n y 2.32 V en BiOX.

Lectura:
1. **Tipo n.** M5 es peor que M0a, incluso en los compuestos con los que se entrenó (TiO2, WO3, ZnO, SnO2…). El IC de la diferencia excluye el 0.
2. **Tipo p.** M5 mejora a M0a en unos 0.4 V, porque predice el VBM de los compuestos de Cu más cerca del vacío. Aun así, deja un sesgo de −1.2 V: tampoco resuelve el problema del borde de valencia en los tipo p con estados d.
3. **BiOX.** M5 falla con fuerza. El VBM predicho baja hasta −11.7 eV en BiOCl y −9.3 eV en BiOBr, y eso pone el borde de conducción 2–4 V por encima de lo medido. Ningún oxihaluro está en su ajuste fino, así que es una extrapolación fuera de dominio.
4. **Sensibilidad a la fase.** El modelo cambia más de 1 eV entre polimorfos del mismo compuesto. En TiO2, la anatasa del COD da −8.63 eV; la estructura Pmm2 que usaron los autores, −7.25 eV; el valor experimental que ajustaron es −7.41 eV. Ocurre lo mismo con WO3 y ZnO. Esto explica por qué el modelo empeora aun con fórmulas que conoce: aprendió el valor experimental asociado a una estructura de Materials Project que no siempre es la fase medida.
5. **No es un artefacto de la celda.** Usar la celda primitiva en lugar de la convencional, o 10 capas en lugar de 30, cambia el VBM en ≤ 0.15 eV (anatasa y BiOCl).
6. **El Eg predicho** se desvía del experimental en 0.36 eV de media absoluta, sin sesgo (−0.04 eV).

## 3. Conclusión para el artículo

Con estructuras de las fases realmente medidas, el modelo ML de Haghshenas no mejora a Butler–Ginley en tipo n y falla de forma grave fuera de su dominio (oxihaluros de Bi). Solo aporta en el borde de valencia de los tipo p, y sin llegar a corregirlo. Esto refuerza la conclusión de la fase 4: la elección del modelo de referencia para las fases 5 y 6 no cambia.

Archivos: `resultados/fase4/m5/m5_registros.csv` (predicción por registro, con fase, id COD y bandera de ajuste), `salida_m5.txt` y `pred_cod.jsonl` (VBM por plano); `data/estructuras_cod/seleccion_cod.csv` y `cif/` (36 CIF).
