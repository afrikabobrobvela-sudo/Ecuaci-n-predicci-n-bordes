"""Construye el piloto de la Fase 2: registros incluidos (EQ y FE) y excluidos.

Las conversiones se calculan aquí, no a mano, para que sean auditables.
Convenciones: U = potencial (V), epsilon = energía electrónica (eV).
U_SHE = U_medido + E_ref_vs_SHE. U_SHE_pH0 se da solo como columna derivada
de sensibilidad (pendiente nernstiana 0.0592 V/pH); el análisis usa el pH original.
"""
import csv, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

# Potenciales de electrodos de referencia vs SHE a 25 °C (V) y fuente.
REF = {
    "Ag/AgCl KCl sat":   (0.197, 0.000, "Inzelt et al. 2013 (Handbook of Reference Electrodes, 10.1007/978-3-642-36188-3); valor tabulado 0.197 V"),
    "Ag/AgCl KCl 3 M":   (0.210, 0.000, "Inzelt et al. 2013; tabla NACE 0.210 V (3.0 mol/kg)"),
    # Concentración de KCl no reportada: centro del intervalo 0.197–0.235 V (sat a 1 M), con incertidumbre de semiamplitud.
    "Ag/AgCl KCl n.r.":  (0.216, 0.019, "Intervalo 0.197 (sat) a 0.235 (1 M); centro ± semiamplitud"),
    "SCE sat":           (0.241, 0.000, "Inzelt et al. 2013; 0.241 V"),
    "Hg/Hg2SO4 K2SO4 sat": (0.640, 0.000, "Valor declarado por los autores (0.640 V vs NHE)"),
    "SHE": (0.0, 0.0, "—"),
}
NERNST = 0.0592  # V/pH a 25 °C

def u_she(valor, escala, ph):
    """Convierte a V vs SHE al pH experimental. Devuelve (U, incert_ref, formula)."""
    if escala == "RHE":
        return valor - NERNST * ph, 0.0, f"U_SHE = U_RHE − 0.0592·pH = {valor} − 0.0592·{ph}"
    e, du, _ = REF[escala]
    return valor + e, du, f"U_SHE = U_{escala} + {e}"

# --- Registros incluidos -------------------------------------------------
# campos: id, conjunto, compuesto, formula, familia, particion, fase, tecnica_fase, muestra,
# metodo, tipo, valor, escala, electrolito, tampon, pH, pH_reportado, frecuencia, Eg, Eg_metodo,
# conversion_autor_SHE, incert_metodo, doi, lectura, estudio, banderas, confianza, notas
R = [
 # Oxihaluros de Bi (reserva externa)
 dict(id="P01", conjunto="EQ", compuesto="BiOCl", formula="BiOCl", familia="oxihaluro_Bi", particion="reserva_BiOX",
      fase="tetragonal (matlockita)", tecnica_fase="no detallada en el extracto", muestra="polvo nanoláminas",
      metodo="Mott-Schottky", tipo="n", valor=-0.37, escala="SCE sat", electrolito="0.1 M Na2SO4", tampon="no",
      pH=7.0, pH_rep="sí", frecuencia="n.r.", Eg=3.25, Eg_metodo="borde de absorción DRS (sin Tauc declarado)",
      conv_autor=None, inc_met=0.10, doi="10.1038/srep32457", lectura="TC-d", estudio="Xu2016",
      banderas="frecuencia n.r.; ΔE=−0.3 V supuesto por autores; inconsistencias internas en el texto", confianza="bajo",
      notas="Muestra sin vacancias (BOC)"),
 dict(id="P02", conjunto="EQ", compuesto="BiOCl (con vacancias de Bi)", formula="BiOCl", familia="oxihaluro_Bi", particion="reserva_BiOX",
      fase="tetragonal", tecnica_fase="no detallada", muestra="polvo nanoláminas defectuoso",
      metodo="Mott-Schottky", tipo="n", valor=-0.84, escala="SCE sat", electrolito="0.1 M Na2SO4", tampon="no",
      pH=7.0, pH_rep="sí", frecuencia="n.r.", Eg=2.91, Eg_metodo="borde de respuesta DRS",
      conv_autor=None, inc_met=0.10, doi="10.1038/srep32457", lectura="TC-d", estudio="Xu2016",
      banderas="variante defectuosa: no representa BiOCl estequiométrico; frecuencia n.r.", confianza="bajo",
      notas="Muestra V-BOC; mismo estudio que P01"),
 dict(id="P03", conjunto="EQ", compuesto="BiOCl", formula="BiOCl", familia="oxihaluro_Bi", particion="reserva_BiOX",
      fase="tetragonal", tecnica_fase="XRD (JCPDS 06-0249), HRTEM, Raman", muestra="polvo",
      metodo="Mott-Schottky", tipo="n (supuesto)", valor=0.46, escala="Ag/AgCl KCl n.r.", electrolito="n.r.", tampon="n.r.",
      pH=None, pH_rep="no", frecuencia="n.r.", Eg=3.19, Eg_metodo="Tauc indirecto (n=4)",
      conv_autor=0.68, inc_met=0.10, doi="10.1038/srep28689", lectura="TC-d", estudio="Liu2016",
      banderas="pH, electrolito y frecuencia n.r.; Vfb positivo atípico para BiOCl tipo n; escala del CB (0.58 eV) ambigua",
      confianza="bajo", notas="Autores convierten con +0.22 V"),
 dict(id="P04", conjunto="EQ", compuesto="Bi24O31Cl10", formula="Bi24O31Cl10", familia="oxihaluro_Bi_rico_en_Bi", particion="reserva_BiOX",
      fase="monoclínica", tecnica_fase="XRD (JCPDS 75-0887), Raman, SAED", muestra="polvo",
      metodo="Mott-Schottky", tipo="n (supuesto)", valor=-0.33, escala="Ag/AgCl KCl n.r.", electrolito="n.r.", tampon="n.r.",
      pH=None, pH_rep="no", frecuencia="n.r.", Eg=2.40, Eg_metodo="Tauc indirecto (n=4)",
      conv_autor=-0.11, inc_met=0.10, doi="10.1038/srep28689", lectura="TC-d", estudio="Liu2016",
      banderas="pH, electrolito y frecuencia n.r.", confianza="bajo", notas="Fase rica en Bi"),
 dict(id="P05", conjunto="EQ", compuesto="BiOCl", formula="BiOCl", familia="oxihaluro_Bi", particion="reserva_BiOX",
      fase="tetragonal", tecnica_fase="PXRD (fase pura)", muestra="película AACVD",
      metodo="Mott-Schottky", tipo="p (según autores)", valor=2.15, escala="Ag/AgCl KCl 3 M", electrolito="0.5 M Na2SO4, Ar", tampon="no",
      pH=6.5, pH_rep="sí", frecuencia="1000", Eg=3.2, Eg_metodo="Tauc indirecto (3.3 en texto, 3.2 en figura)",
      conv_autor=2.73 - NERNST*6.5, inc_met=0.10, doi="10.1039/c6sc00389c", lectura="TC-d", estudio="Bhachu2016",
      banderas="tipo p atípico para BiOCl; autores usan E°=0.1976 V para Ag/AgCl 3 M (tabulado 0.210); Eg inconsistente entre texto y figura",
      confianza="bajo", notas="Frecuencia única"),
 dict(id="P06", conjunto="EQ", compuesto="BiOBr", formula="BiOBr", familia="oxihaluro_Bi", particion="reserva_BiOX",
      fase="tetragonal", tecnica_fase="PXRD (fase pura)", muestra="película AACVD",
      metodo="Mott-Schottky", tipo="n", valor=-0.44, escala="Ag/AgCl KCl 3 M", electrolito="0.5 M Na2SO4, Ar", tampon="no",
      pH=6.5, pH_rep="sí", frecuencia="1000", Eg=2.6, Eg_metodo="Tauc indirecto (2.7 en texto, 2.6 en figura)",
      conv_autor=0.14 - NERNST*6.5, inc_met=0.10, doi="10.1039/c6sc00389c", lectura="TC-d", estudio="Bhachu2016",
      banderas="E° de referencia de los autores 0.1976 V (tabulado 0.210 para 3 M); frecuencia única", confianza="medio", notas=""),
 dict(id="P07", conjunto="EQ", compuesto="BiOI", formula="BiOI", familia="oxihaluro_Bi", particion="reserva_BiOX",
      fase="tetragonal", tecnica_fase="PXRD (fase pura)", muestra="película AACVD",
      metodo="Mott-Schottky", tipo="n", valor=-0.30, escala="Ag/AgCl KCl 3 M", electrolito="0.5 M Na2SO4, Ar", tampon="no",
      pH=6.5, pH_rep="sí", frecuencia="1000", Eg=1.7, Eg_metodo="Tauc indirecto (1.8 en texto, 1.7 en figura)",
      conv_autor=0.58 - NERNST*6.5, inc_met=0.10, doi="10.1039/c6sc00389c", lectura="TC-d", estudio="Bhachu2016",
      banderas="ERROR DE CONVERSIÓN DEL AUTOR: +0.58 V_RHE no corresponde a −0.3 V vs Ag/AgCl (≈+0.28 V_RHE); se usa el valor medido",
      confianza="medio", notas=""),
 dict(id="P08", conjunto="EQ", compuesto="BiOCl0.9I0.1", formula="BiOCl0.9I0.1", familia="oxihaluro_Bi_solucion_solida", particion="reserva_BiOX",
      fase="tetragonal, solución sólida", tecnica_fase="XRD (desplazamiento de picos, sin BiOI)", muestra="polvo",
      metodo="Mott-Schottky", tipo="n", valor=-1.36, escala="Ag/AgCl KCl n.r.", electrolito="0.2 M Na2SO4", tampon="no",
      pH=None, pH_rep="no", frecuencia="500", Eg=2.45, Eg_metodo="Kubelka-Munk, indirecto",
      conv_autor=-1.16, inc_met=0.10, doi="10.1039/d4ew00410h", lectura="TC-d", estudio="PerezDelPulgar2024",
      banderas="pH y concentración de KCl n.r.; Vfb muy negativo", confianza="bajo", notas="Solución sólida Cl/I"),
 dict(id="P09", conjunto="EQ", compuesto="BiOBr0.9I0.1", formula="BiOBr0.9I0.1", familia="oxihaluro_Bi_solucion_solida", particion="reserva_BiOX",
      fase="tetragonal, solución sólida", tecnica_fase="XRD (desplazamiento de picos, sin BiOI)", muestra="polvo",
      metodo="Mott-Schottky", tipo="n", valor=-1.26, escala="Ag/AgCl KCl n.r.", electrolito="0.2 M Na2SO4", tampon="no",
      pH=None, pH_rep="no", frecuencia="500", Eg=2.37, Eg_metodo="Kubelka-Munk, indirecto",
      conv_autor=-1.06, inc_met=0.10, doi="10.1039/d4ew00410h", lectura="TC-d", estudio="PerezDelPulgar2024",
      banderas="pH y concentración de KCl n.r.", confianza="bajo", notas="Solución sólida Br/I"),
 # Otros compuestos (entrenamiento)
 dict(id="P10", conjunto="EQ", compuesto="BiVO4", formula="BiVO4", familia="oxido_ternario_Bi", particion="entrenamiento",
      fase="monoclínica scheelita", tecnica_fase="XRD, SEM", muestra="película",
      metodo="Mott-Schottky (EIS, circuito de Randles)", tipo="n", valor=0.1, escala="RHE", electrolito="0.1 M KPi", tampon="sí",
      pH=6.7, pH_rep="sí", frecuencia="0.01–1e5 (barrido EIS)", Eg=2.45, Eg_metodo="valor de literatura citado (2.4–2.5), no medido",
      conv_autor=None, inc_met=0.10, doi="10.1039/c4sc00469h", lectura="TC-d", estudio="Ma2014",
      banderas="valor aproximado (~0.1 V_RHE); Eg no medido en el estudio", confianza="medio", notas="Referencia Ag/AgCl sat convertida por autores"),
 dict(id="P11", conjunto="EQ", compuesto="α-Fe2O3", formula="Fe2O3", familia="oxido_binario", particion="entrenamiento",
      fase="hematita", tecnica_fase="no explícita en texto (XPS en ESI)", muestra="película 47 nm, pirólisis",
      metodo="Mott-Schottky (sin corrección de Helmholtz)", tipo="n", valor=-0.68, escala="SHE", electrolito="1 M NaOH", tampon="no (alcalino fuerte)",
      pH=13.65, pH_rep="sí (medido)", frecuencia="0.1–1e5 (75 frecuencias)", Eg=2.05, Eg_metodo="óptico (2.05±0.15; 2.2 en otra sección)",
      conv_autor=None, inc_met=0.09, doi="10.1039/c9ta09569a", lectura="TC-d", estudio="Hankin2019",
      banderas="fase no confirmada en texto principal; dependencia del modelo de capacitancia", confianza="medio",
      notas="Media de 3 muestras ±0.09 V"),
 dict(id="P12", conjunto="EQ", compuesto="α-Fe2O3", formula="Fe2O3", familia="oxido_binario", particion="entrenamiento",
      fase="hematita", tecnica_fase="no explícita en texto", muestra="película 47 nm",
      metodo="Iluminación intermitente (potencial de transición)", tipo="n", valor=-0.39, escala="SHE", electrolito="1 M NaOH", tampon="no",
      pH=13.65, pH_rep="sí (medido)", frecuencia="no aplica", Eg=2.05, Eg_metodo="óptico",
      conv_autor=None, inc_met=0.01, doi="10.1039/c9ta09569a", lectura="TC-d", estudio="Hankin2019",
      banderas="fase no confirmada en el texto principal (XPS en ESI, no leído)", confianza="medio", notas="Intervalo −0.40 a −0.38 V; misma muestra que P11 y P13"),
 dict(id="P13", conjunto="EQ", compuesto="α-Fe2O3", formula="Fe2O3", familia="oxido_binario", particion="entrenamiento",
      fase="hematita", tecnica_fase="no explícita en texto", muestra="película 47 nm",
      metodo="Gärtner-Butler con H2O2", tipo="n", valor=-0.395, escala="SHE", electrolito="1 M NaOH + 0.5 M H2O2", tampon="no",
      pH=13.65, pH_rep="sí (supuesto igual)", frecuencia="no aplica", Eg=2.05, Eg_metodo="óptico",
      conv_autor=None, inc_met=0.055, doi="10.1039/c9ta09569a", lectura="TC-d", estudio="Hankin2019",
      banderas="fase no confirmada en el texto principal", confianza="medio", notas="Intervalo −0.45 a −0.34 V"),
 dict(id="P14", conjunto="EQ", compuesto="WO3", formula="WO3", familia="oxido_binario", particion="entrenamiento",
      fase="monoclínica", tecnica_fase="XRD (PCPDF 72-1465), HRTEM", muestra="película",
      metodo="Mott-Schottky", tipo="n", valor=0.5, escala="RHE", electrolito="0.5 M H2SO4", tampon="no",
      pH=0.3, pH_rep="sí", frecuencia="1e2–1e5 (barrido)", Eg=2.7, Eg_metodo="Tauc indirecto",
      conv_autor=None, inc_met=0.10, inc_ref_extra=0.042, doi="10.1039/c8ra08875f", lectura="TC-d", estudio="WO3_RSCAdv2019",
      banderas="inconsistencia del autor: referencia declarada 0.640 V_NHE pero la fórmula usa +0.682 V (incertidumbre 0.042 V)",
      confianza="medio", notas="Muestra prístina R0"),
 dict(id="P15", conjunto="EQ", compuesto="TiO2 anatasa (calcinada 400 °C)", formula="TiO2", familia="oxido_binario", particion="entrenamiento",
      fase="anatasa", tecnica_fase="XRD", muestra="polvo Hombikat UV-100 sobre FTO",
      metodo="Mott-Schottky (serie de pH)", tipo="n", valor=-0.19, escala="Ag/AgCl KCl 3 M", electrolito="Na2SO4 con ajuste de pH", tampon="no",
      pH=1.64, pH_rep="sí", frecuencia="200–2000 recomendado", Eg=3.30, Eg_metodo="Tauc indirecto (Kubelka-Munk)",
      conv_autor=None, inc_met=0.10, doi="10.3390/catal13061000", lectura="TC-d", estudio="Lee2023",
      banderas="escala del valor no explícita en el texto (se asume vs Ag/AgCl 3 M); respuesta al pH no nernstiana",
      confianza="bajo", notas="Serie de pH: pendientes 128, 25 y 137 mV/pH por tramos; 65 mV/pH global"),
 dict(id="P16", conjunto="EQ", compuesto="TiO2 anatasa (calcinada 400 °C)", formula="TiO2", familia="oxido_binario", particion="entrenamiento",
      fase="anatasa", tecnica_fase="XRD", muestra="polvo Hombikat UV-100 sobre FTO",
      metodo="Mott-Schottky (serie de pH)", tipo="n", valor=-0.97, escala="Ag/AgCl KCl 3 M", electrolito="Na2SO4 con ajuste de pH", tampon="no",
      pH=12.11, pH_rep="sí", frecuencia="200–2000 recomendado", Eg=3.30, Eg_metodo="Tauc indirecto (Kubelka-Munk)",
      conv_autor=None, inc_met=0.10, doi="10.3390/catal13061000", lectura="TC-d", estudio="Lee2023",
      banderas="escala no explícita (se asume vs Ag/AgCl 3 M)", confianza="bajo", notas="Mismo electrodo que P15"),
 dict(id="P17", conjunto="EQ", compuesto="TiO2 amorfo (ALD)", formula="TiO2", familia="oxido_binario_amorfo", particion="entrenamiento",
      fase="amorfa", tecnica_fase="declarada por síntesis ALD", muestra="película ~ALD sobre p+-Si",
      metodo="Mott-Schottky (consistente con AP-XPS operando)", tipo="n", valor=-0.9, escala="Ag/AgCl KCl n.r.", electrolito="1.0 M KOH", tampon="no",
      pH=14.0, pH_rep="no (estimado de 1 M KOH)", frecuencia="n.r.", Eg=None, Eg_metodo="n.r.",
      conv_autor=None, inc_met=0.10, doi="10.1039/c5ee01014d", lectura="TC-d", estudio="Lichterman2015",
      banderas="fase amorfa: fuera del alcance de modelos para sólidos cristalinos; Eg n.r.; relleno de Ag/AgCl n.r.", confianza="bajo",
      notas="Autores dan Ag/AgCl a 4.64 eV vs vacío"),
 dict(id="P18", conjunto="EQ", compuesto="LaFeO3", formula="LaFeO3", familia="oxido_ternario", particion="entrenamiento",
      fase="ortorrómbica", tecnica_fase="XRD (JCPDS 00-037-1493), Raman", muestra="película 382 nm sobre FTO",
      metodo="Mott-Schottky", tipo="p", valor=0.328, escala="Ag/AgCl KCl sat", electrolito="0.1 M NaOH", tampon="no",
      pH=13.0, pH_rep="sí", frecuencia="n.r.", Eg=2.4, Eg_metodo="Tauc directo",
      conv_autor=1.29 - NERNST*13.0, inc_met=0.10, doi="10.1038/s41598-018-21821-z", lectura="TC-d", estudio="Pawar2018",
      banderas="frecuencia n.r.", confianza="medio", notas=""),
 dict(id="P19", conjunto="EQ", compuesto="ZnO (nanorods 140 °C)", formula="ZnO", familia="oxido_binario", particion="entrenamiento",
      fase="wurtzita", tecnica_fase="XRD, Raman", muestra="nanorods",
      metodo="Mott-Schottky", tipo="n", valor=-0.95, escala="Ag/AgCl KCl n.r.", electrolito="0.5 M Na2SO4 (conflicto con Na2SO3 en otra sección)", tampon="no",
      pH=None, pH_rep="no", frecuencia="1000", Eg=3.09, Eg_metodo="Tauc (n ambiguo)",
      conv_autor=None, inc_met=0.10, doi="10.1038/s41598-025-26341-1", lectura="TC-d", estudio="Kubas2026",
      banderas="escala no explícita; pH n.r.; electrolito contradictorio", confianza="bajo", notas=""),
]

# --- Registros de fotoemisión (FE) ---------------------------------------
FE = [
 dict(id="F01", compuesto="WO3-x", formula="WO3", familia="oxido_binario", particion="entrenamiento",
      magnitud="función de trabajo (UPS, SECO)", valor=4.6, referencia="vacío (WF)", condicion="película expuesta al aire; sesgo −2 V",
      doi="10.1038/s41598-023-40187-5", lectura="TC-d", estudio="Baddorf2023", confianza="medio",
      banderas="subestequiométrico; tres cortes aparentes, se toma el independiente del sesgo; sin IP", notas="Solo WF: no da IP ni VBM"),
 dict(id="F02", compuesto="BiOCl", formula="BiOCl", familia="oxihaluro_Bi", particion="reserva_BiOX",
      magnitud="VBM − E_F (XPS-VB, extrapolación lineal)", valor=2.9, referencia="nivel de Fermi", condicion="película",
      doi="10.1039/c6sc00389c", lectura="TC-d", estudio="Bhachu2016", confianza="bajo",
      banderas="relativo a E_F: no es absoluto; autores advierten que la extrapolación subestima", notas="Misma muestra que P05 (enlace posible)"),
 dict(id="F03", compuesto="BiOBr", formula="BiOBr", familia="oxihaluro_Bi", particion="reserva_BiOX",
      magnitud="VBM − E_F (XPS-VB)", valor=2.2, referencia="nivel de Fermi", condicion="película",
      doi="10.1039/c6sc00389c", lectura="TC-d", estudio="Bhachu2016", confianza="bajo",
      banderas="relativo a E_F", notas="Misma muestra que P06"),
 dict(id="F04", compuesto="BiOI", formula="BiOI", familia="oxihaluro_Bi", particion="reserva_BiOX",
      magnitud="VBM − E_F (XPS-VB)", valor=1.6, referencia="nivel de Fermi", condicion="película",
      doi="10.1039/c6sc00389c", lectura="TC-d", estudio="Bhachu2016", confianza="bajo",
      banderas="relativo a E_F", notas="Misma muestra que P07"),
 dict(id="F05", compuesto="BiOCl", formula="BiOCl", familia="oxihaluro_Bi", particion="reserva_BiOX",
      magnitud="VBM − E_F (XPS-VB)", valor=2.16, referencia="nivel de Fermi", condicion="polvo",
      doi="10.1038/srep32457", lectura="TC-d", estudio="Xu2016", confianza="bajo",
      banderas="relativo a E_F", notas="Misma muestra que P01"),
 dict(id="F06", compuesto="Bi2WO6", formula="Bi2WO6", familia="oxido_ternario_Bi", particion="entrenamiento",
      magnitud="VBM − E_F (XPS-VB)", valor=1.78, referencia="nivel de Fermi (calibración C1s 284.8 eV)", condicion="polvo",
      doi="10.1038/srep19347", lectura="TC-d", estudio="Lv2016", confianza="bajo",
      banderas="relativo a E_F; Eg sin método declarado (2.8 eV)", notas=""),
 dict(id="F07", compuesto="BiVO4", formula="BiVO4", familia="oxido_ternario_Bi", particion="entrenamiento",
      magnitud="VBM − E_F (XPS-VB)", valor=1.9, referencia="nivel de Fermi", condicion="película AACVD",
      doi="10.1039/d4ta02605e", lectura="TC-d", estudio="Zhao2024", confianza="bajo",
      banderas="relativo a E_F", notas="Eg indirecto 2.55 eV (Tauc)"),
]

# --- Excluidos (registro obligatorio, alimenta la pregunta 1 solo como ilustración) ---
EXC = [
 ("X01","BiOBr/BiOI (bicapas)","10.1038/srep32764","DFT (HSE06+SOC) sin medición","calculado_DFT","TC-d"),
 ("X02","Bi2WO6","10.1038/ncomms9340","Sin medición de bordes","sin_medicion","TC-d"),
 ("X03","BiVO4, Bi4V2O11","10.1038/srep31406","Mott-Schottky sin valor numérico reportado","sin_valor","TC-d"),
 ("X04","BiOI","10.1038/s41598-022-08213-0","Bordes calculados con la ecuación de electronegatividad (χ=6.10 eV, Ee=4.50 eV)","ecuacion_electronegatividad","TC-d"),
 ("X05","BiVO4","10.1038/s41598-022-08213-0","Mott-Schottky sin electrodo de referencia ni electrolito declarados para la medición","referencia_no_identificable","TC-d"),
 ("X06","BiOCl","10.1039/c9ra10256f","Mott-Schottky sin electrodo de referencia, electrolito ni pH","referencia_no_identificable","TC-d"),
 ("X07","BiOBr","10.1039/c9ra10256f","Mott-Schottky sin electrodo de referencia, electrolito ni pH","referencia_no_identificable","TC-d"),
 ("X08","BiOCl0.8Br0.2","10.1039/c9ra10256f","Muestra bifásica (no solución sólida); sin medición propia","fase_no_confirmada","TC-d"),
 ("X09","Bi2WO6","10.1038/s41598-020-75003-x","XPS-VB referido a E_F reportado como 'vs NHE' sin conversión","conversion_invalida","TC-d"),
 ("X10","BiOCl","10.1038/s41598-020-75003-x","XPS-VB referido a E_F reportado como 'vs NHE' sin conversión","conversion_invalida","TC-d"),
 ("X11","Cu2O","10.1039/d1ra08863g","Sin valor numérico para Cu2O monofásico; heteroestructura","sin_valor","TC-d"),
 ("X12","CuBi2O4","10.1038/s41598-023-32804-0","Solo compuesto CuO/CuBi2O4","no_monofasico","TC-d"),
 ("X13","ZnO","10.1038/srep29907","Sin Mott-Schottky ni otra medición de bordes","sin_medicion","TC-d"),
 ("X14","BiVO4","10.3390/molecules30112454","Vfb solo de la muestra modificada (Ag–Fe)","no_monofasico","TC-d"),
 ("X15","Nb:SrTiO3","10.1039/d5sc01816a","Valores solo en figuras; se usa como referencia metodológica (tampón)","sin_valor_textual","TC-d"),
 ("X16","BiOX","10.3389/fchem.2022.900622","Revisión (fuente secundaria)","fuente_secundaria","TC-d"),
 ("X17","Cu2O","10.1038/s41467-019-13987-5","Sin Vfb de Cu2O; VBM ~0.35 eV sin referencia declarada","sin_valor","TC-d"),
 ("X18","Cu2O, CuO","10.1038/srep35158","Mott-Schottky no recuperado en el texto accesible (pendiente)","no_verificado","P"),
 ("X19","TiO2 anatasa","10.5155/eurjchem.10.1.82-94.1809","Bordes calculados con la ecuación de electronegatividad","ecuacion_electronegatividad","TC-d"),
 ("X20","CuFeS2, FeS2, CuS, Cu2S","10.1007/s43630-023-00415-3","Bordes calculados por electronegatividad y función de trabajo atómica","ecuacion_electronegatividad","R"),
 ("X21","~5400 perovskitas","10.1039/c1ee02717d","Butler–Ginley aplicado en cribado computacional","ecuacion_electronegatividad","R (SI TC-d)"),
]

def fmt(x, nd=3):
    return "" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))

cols = ["id","conjunto","compuesto","formula","familia_a_priori","particion","fase","tecnica_fase","muestra","metodo",
        "tipo_semiconductor","valor_reportado","escala_reportada","E_ref_vs_SHE_V","fuente_E_ref","electrolito","tampon",
        "pH","pH_reportado","frecuencia_Hz","U_SHE_pHexp_V","incert_ref_V","incert_metodo_V","incert_metodo_origen","incert_U_V","formula_conversion","U_SHE_autor_V",
        "discrepancia_vs_autor_V","U_SHE_pH0_nernst_V","Eg_eV","Eg_metodo","pzc","pzc_nivel","iep","doi","enlace",
        "lectura","estudio","banderas_QC","confianza","notas"]
with open(os.path.join(OUT, "piloto_EQ.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for r in R:
        u, du_ref, form = u_she(r["valor"], r["escala"], r["pH"] if r["pH"] is not None else 0.0)
        if r["escala"] == "RHE" and r["pH"] is None:
            raise ValueError(r["id"])
        e_ref = "" if r["escala"] == "RHE" else REF[r["escala"]][0]
        fuente = "Nernst 0.0592 V/pH" if r["escala"] == "RHE" else REF[r["escala"]][2]
        du_ref = (du_ref**2 + r.get("inc_ref_extra", 0.0)**2) ** 0.5
        origen = "reportada/intervalo del estudio" if r["estudio"] == "Hankin2019" else "supuesta (0.10 V por defecto)"
        inc = (du_ref**2 + r["inc_met"]**2) ** 0.5
        disc = None if r["conv_autor"] is None else u - r["conv_autor"]
        ph0 = None if r["pH"] is None else u + NERNST * r["pH"]
        w.writerow([r["id"], r["conjunto"], r["compuesto"], r["formula"], r["familia"], r["particion"], r["fase"],
                    r["tecnica_fase"], r["muestra"], r["metodo"], r["tipo"], r["valor"], r["escala"], e_ref, fuente,
                    r["electrolito"], r["tampon"], fmt(r["pH"], 2), r["pH_rep"], r["frecuencia"], fmt(u), fmt(du_ref), fmt(r["inc_met"]), origen, fmt(inc),
                    form, fmt(r["conv_autor"]), fmt(disc), fmt(ph0), fmt(r["Eg"], 2), r["Eg_metodo"], "n.r.", "desconocido",
                    "n.r.", r["doi"], "https://doi.org/" + r["doi"], r["lectura"], r["estudio"], r["banderas"],
                    r["confianza"], r["notas"]])

fcols = ["id","conjunto","compuesto","formula","familia_a_priori","particion","magnitud","valor_eV","referencia_energia",
         "condicion_muestra","doi","enlace","lectura","estudio","banderas_QC","confianza","notas"]
with open(os.path.join(OUT, "piloto_FE.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(fcols)
    for r in FE:
        w.writerow([r["id"],"FE",r["compuesto"],r["formula"],r["familia"],r["particion"],r["magnitud"],r["valor"],
                    r["referencia"],r["condicion"],r["doi"],"https://doi.org/"+r["doi"],r["lectura"],r["estudio"],
                    r["banderas"],r["confianza"],r["notas"]])

with open(os.path.join(OUT, "piloto_excluidos.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id","compuesto","doi","motivo","categoria_exclusion","lectura"])
    for e in EXC: w.writerow(e)

print(f"EQ: {len(R)}  FE: {len(FE)}  excluidos: {len(EXC)}")
