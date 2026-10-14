"""Piloto unificado de la Fase 2 (Claude + ChatGPT).

Unidad de registro: estudio × muestra × observable × condición × determinación.
Cuatro capas separadas: (1) valor publicado, (2) interpretación del autor,
(3) transformación que podemos justificar, (4) admisión y aptitud para ajuste.
No se asignan incertidumbres no reportadas. La conversión definitiva queda vacía
si falta el relleno de la referencia (o el pH para RHE); en ese caso solo se da
un escenario a 25 °C. Toda conversión supone 25 °C salvo que el estudio la reporte.
"""
import csv, sys

NERNST = 0.0592
REF = {"Ag/AgCl sat": 0.197, "Ag/AgCl 3 M": 0.210, "SCE sat": 0.241, "Hg/Hg2SO4 sat": 0.640, "SHE": 0.0}
ESCENARIO_NR = {"Ag/AgCl n.r.": (0.197, 0.235), "Ag/AgCl ?": (0.197, 0.235), "SCE n.r.": (0.241, 0.280)}  # intervalo saturado–1 M

def convertir(valor, ref, ph):
    """Devuelve (definitiva, escenario_min, escenario_max) en V vs SHE al pH experimental."""
    if ref == "RHE":
        return (None, None, None) if ph is None else (round(valor - NERNST * ph, 3),) * 3
    if ref in REF:
        u = round(valor + REF[ref], 3); return u, u, u
    lo, hi = ESCENARIO_NR[ref]
    return None, round(valor + lo, 3), round(valor + hi, 3)

# (id, estudio, doi, muestra, compuesto, familia, subconjunto, observable, valor, unidad, ref, pH, freq,
#  Eg, Eg_metodo, interpretacion_autor, U_autor_SHE, admision, apto, confianza, extraido, verificado, banderas)
F = "fotoemision"
rows = [
 # --- Bhachu 2016 (extraído por ambos) ---
 ("U01","Bhachu2016","10.1039/c6sc00389c","película AACVD","BiOCl","oxihaluro_Bi","reserva_BiOX","U_fb (MS)",2.15,"V","Ag/AgCl 3 M",6.5,"1000",3.2,"Tauc indirecto (3.3 en texto)","banda plana tipo p",2.346,"admitido","reserva","bajo","ambos","ambos","autores usan 0.1976 V para 3 M; tipo p atípico; Eg inconsistente"),
 ("U02","Bhachu2016","10.1039/c6sc00389c","película AACVD","BiOBr","oxihaluro_Bi","reserva_BiOX","U_fb (MS)",-0.44,"V","Ag/AgCl 3 M",6.5,"1000",2.6,"Tauc indirecto (2.7 en texto)","banda plana tipo n",-0.245,"admitido","reserva","medio","ambos","ambos","referencia: 0.1976 vs 0.210 V"),
 ("U03","Bhachu2016","10.1039/c6sc00389c","película AACVD","BiOI","oxihaluro_Bi","reserva_BiOX","U_fb (MS)",-0.30,"V","Ag/AgCl 3 M",6.5,"1000",1.7,"Tauc indirecto (1.8 en texto)","banda plana tipo n",0.195,"cuarentena","no","medio","ambos","ambos","error de conversión del autor (0.285 V)"),
 # --- Lee 2023 (ambos; promedios multifrecuencia solo ChatGPT) ---
 ("U04","Lee2023","10.3390/catal13061000","Ana(400), pH 1.64","TiO2 anatasa","oxido_binario","control_metodologico","U_fb (MS, serie de pH)",-0.19,"V","Ag/AgCl 3 M",1.64,"200–2000",3.30,"Tauc indirecto","banda plana",None,"admitido","control","bajo","ambos","ambos","escala no explícita en texto; respuesta al pH no nernstiana"),
 ("U05","Lee2023","10.3390/catal13061000","Ana(400), pH 12.11","TiO2 anatasa","oxido_binario","control_metodologico","U_fb (MS, serie de pH)",-0.97,"V","Ag/AgCl 3 M",12.11,"200–2000",3.30,"Tauc indirecto","banda plana",None,"admitido","control","bajo","ambos","ambos","mismo electrodo que U04"),
 ("U06","Lee2023","10.3390/catal13061000","anatasa, muestras nuevas","TiO2 anatasa","oxido_binario","control_metodologico","U_fb promedio multifrecuencia",-0.516,"V","Ag/AgCl 3 M",None,"promedio 200–2000",3.30,"Tauc indirecto","banda plana",None,"admitido","control","medio","ChatGPT","ChatGPT","promedio de frecuencias: no es réplica independiente; pH no confirmado"),
 ("U07","Lee2023","10.3390/catal13061000","anatasa, muestra reutilizada","TiO2 anatasa","oxido_binario","control_metodologico","U_fb promedio multifrecuencia",-0.709,"V","Ag/AgCl 3 M",None,"promedio 200–2000",3.30,"Tauc indirecto","banda plana",None,"admitido","control","bajo","ChatGPT","ChatGPT","muestra reutilizada (depósito de tenardita)"),
 # --- Solo Claude ---
 ("U08","Xu2016","10.1038/srep32457","nanoláminas","BiOCl","oxihaluro_Bi","reserva_BiOX","U_fb (MS)",-0.37,"V","SCE sat",7.0,"n.r.",3.25,"borde DRS","banda plana; CB = U_fb − 0.3",None,"admitido","reserva","bajo","Claude","Claude","frecuencia n.r.; contradicciones internas"),
 ("U09","Xu2016","10.1038/srep32457","nanoláminas con vacancias de Bi","BiOCl (defectuoso)","oxihaluro_Bi","reserva_BiOX","U_fb (MS)",-0.84,"V","SCE sat",7.0,"n.r.",2.91,"borde DRS","banda plana",None,"admitido","no (variante)","bajo","Claude","Claude","variante defectuosa"),
 ("U10","Liu2016","10.1038/srep28689","polvo","BiOCl","oxihaluro_Bi","reserva_BiOX","U_fb (MS)",0.46,"V","Ag/AgCl n.r.",None,"n.r.",3.19,"Tauc indirecto","banda plana",0.68,"admitido","reserva","bajo","Claude","Claude","pH, electrolito y frecuencia n.r.; Vfb positivo atípico"),
 ("U11","Liu2016","10.1038/srep28689","polvo","Bi24O31Cl10","oxihaluro_Bi_rico","reserva_BiOX","U_fb (MS)",-0.33,"V","Ag/AgCl n.r.",None,"n.r.",2.40,"Tauc indirecto","banda plana",-0.11,"admitido","reserva","bajo","Claude","Claude","pH, electrolito y frecuencia n.r."),
 ("U12","PerezDelPulgar2024","10.1039/d4ew00410h","polvo","BiOCl0.9I0.1","oxihaluro_Bi_ss","reserva_BiOX","U_fb (MS)",-1.36,"V","Ag/AgCl n.r.",None,"500",2.45,"KM indirecto","banda plana",-1.16,"admitido","reserva","bajo","Claude","Claude","pH n.r.; su XPS a NHE usa la función de trabajo del instrumento (no se admite)"),
 ("U13","PerezDelPulgar2024","10.1039/d4ew00410h","polvo","BiOBr0.9I0.1","oxihaluro_Bi_ss","reserva_BiOX","U_fb (MS)",-1.26,"V","Ag/AgCl n.r.",None,"500",2.37,"KM indirecto","banda plana",-1.06,"admitido","reserva","bajo","Claude","Claude","pH n.r."),
 ("U14","Ma2014","10.1039/c4sc00469h","película","BiVO4","oxido_ternario_Bi","principal","U_fb (EIS/MS)",0.1,"V","RHE",6.7,"barrido 0.01–1e5",None,"Eg citado (2.4–2.5), no medido","banda plana",None,"admitido","sí","medio","Claude","Claude","valor aproximado (~0.1 V_RHE); electrolito tamponado (KPi)"),
 ("U15","Hankin2019","10.1039/c9ta09569a","película 47 nm","α-Fe2O3","oxido_binario","control_metodologico","U_fb (MS sin corrección de Helmholtz)",-0.68,"V","SHE",13.65,"0.1–1e5",2.05,"óptico","banda plana",None,"admitido","control","medio","Claude","Claude","±0.09 V (3 muestras); depende del modelo de capacitancia"),
 ("U16","Hankin2019","10.1039/c9ta09569a","película 47 nm","α-Fe2O3","oxido_binario","control_metodologico","potencial de transición (luz intermitente)",-0.39,"V","SHE",13.65,"no aplica",2.05,"óptico","banda plana",None,"admitido","control","medio","Claude","Claude","intervalo −0.40 a −0.38 V; misma muestra que U15"),
 ("U17","Hankin2019","10.1039/c9ta09569a","película 47 nm","α-Fe2O3","oxido_binario","control_metodologico","Gärtner–Butler con H2O2",-0.395,"V","SHE",13.65,"no aplica",2.05,"óptico","banda plana",None,"admitido","control","medio","Claude","Claude","intervalo −0.45 a −0.34 V"),
 ("U18","WO3_RSCAdv2019","10.1039/c8ra08875f","película R0","WO3","oxido_binario","principal","U_fb (MS)",0.5,"V","RHE",0.3,"barrido 1e2–1e5",2.7,"Tauc indirecto","banda plana",None,"admitido","sí","medio","Claude","Claude","referencia declarada 0.640 V, fórmula con 0.682 V"),
 ("U19","Lichterman2015","10.1039/c5ee01014d","película ALD amorfa","TiO2 amorfo","oxido_binario_amorfo","principal","U_fb (MS, concordante con AP-XPS)",-0.9,"V","Ag/AgCl n.r.",None,"n.r.",None,"n.r.","banda plana",None,"admitido","no (amorfo)","bajo","Claude","Claude","fuera de dominio (amorfo); pH no reportado (1 M KOH)"),
 ("U20","Pawar2018","10.1038/s41598-018-21821-z","película 382 nm","LaFeO3","oxido_ternario","principal","U_fb (MS)",0.328,"V","Ag/AgCl sat",13.0,"n.r.",2.4,"Tauc directo","banda plana tipo p",0.520,"admitido","sí","medio","Claude","Claude","frecuencia n.r."),
 ("U21","Kubas2026","10.1038/s41598-025-26341-1","nanorods 140 °C","ZnO","oxido_binario","principal","U_fb (MS)",-0.95,"V","Ag/AgCl n.r.",None,"1000",3.09,"Tauc (n ambiguo)","banda plana",None,"admitido","no hasta resolver escala","bajo","Claude","Claude","escala no explícita; pH n.r.; electrolito contradictorio"),
 # --- Solo ChatGPT (verificados por Claude salvo indicación) ---
 ("U22","Li2018","10.1039/c8ra00250a","S-TA (tiourea)","CdS hexagonal","sulfuro","principal","intercepto MS publicado como E_CB≈E_fb",-0.59,"V","SHE",7.0,"1500",2.3,"Tauc directo","E_CB (vs NHE, pH 7)",None,"admitido","sí","bajo","ChatGPT","ambos","declara Ag/AgCl 3 M pero convierte con +0.197; pH del electrolito no declarado ('pH 7'); valor ya convertido por el autor"),
 ("U23","Li2018","10.1039/c8ra00250a","S-Cys (L-cisteína)","CdS hexagonal mal cristalizado","sulfuro","principal","intercepto MS publicado como E_CB≈E_fb",-0.40,"V","SHE",7.0,"1500",2.4,"Tauc directo","E_CB (vs NHE, pH 7)",None,"admitido","sí","bajo","ChatGPT","ambos","igual que U22; baja cristalinidad"),
 ("U24","Hwang2015?","10.1021/acscentsci.5b00402","nanohilos","TiO2 rutilo","oxido_binario","enlace","U_fb",0.19,"V","RHE",None,"?",3.0,"≈","banda plana",None,"admitido","pendiente","medio","ChatGPT","ChatGPT","no pude abrir el artículo; pH y autoría por confirmar"),
 ("U25","Hwang2015?","10.1021/acscentsci.5b00402","película","BiVO4","oxido_ternario_Bi","enlace","U_fb",0.08,"V","RHE",None,"?",2.5,"≈","banda plana",None,"admitido","pendiente","medio","ChatGPT","ChatGPT","no pude abrir el artículo"),
 ("U26","DinLeeYang2022","10.3390/nano12050767","polvo","Bi3O4Cl","oxihaluro_Bi_rico","reserva_BiOX","U_fb (MS)",-0.645,"V","SCE n.r.",None,"n.r.",2.67,"Tauc (n=1/2 declarado, indirecto)","banda plana",None,"admitido","reserva","bajo","ChatGPT","ambos","calomelano sin relleno; autores suman 0.244; pH y frecuencia n.r."),
 ("U27","DinLeeYang2022","10.3390/nano12050767","polvo","Bi5O7I","oxihaluro_Bi_rico","reserva_BiOX","U_fb (MS)",-1.101,"V","SCE n.r.",None,"n.r.",3.07,"Tauc","banda plana",None,"admitido","reserva","bajo","ChatGPT","ambos","igual que U26"),
 ("U28","Jia2020","10.1039/d0ra08211b","película","BiOBr0.8I0.2","oxihaluro_Bi_ss","reserva_BiOX","U_fb (MS)",-0.06,"V","Ag/AgCl n.r.",5.8,"1000",2.11,"Tauc indirecto","banda plana",0.15,"admitido","reserva","medio","ChatGPT","ambos","relleno n.r. (los autores suman 0.21); fase de la composición no asignada explícitamente"),
 ("U29","Jia2020","10.1039/d0ra08211b","película","BiOBr0.6I0.4","oxihaluro_Bi_ss","reserva_BiOX","U_fb (MS)",-0.12,"V","Ag/AgCl n.r.",5.8,"1000",2.04,"Tauc indirecto","banda plana",0.09,"admitido","reserva","medio","ChatGPT","ambos","igual que U28"),
 ("U30","Jia2020","10.1039/d0ra08211b","película","BiOBr0.5I0.5","oxihaluro_Bi_ss","reserva_BiOX","U_fb (MS)",-0.03,"V","Ag/AgCl n.r.",5.8,"1000",1.93,"Tauc indirecto","banda plana",0.18,"admitido","reserva","medio","ChatGPT","ambos","fase tetragonal por SAED"),
 ("U31","Heliyon2023","10.1016/j.heliyon.2023.e20882","nanobarras","WO3","oxido_binario","principal","U_fb (MS)",0.46,"V","Ag/AgCl ?",None,"?",2.99,"?","banda plana",None,"cuarentena","no","bajo","ChatGPT","ChatGPT","en cuarentena según ChatGPT; no pude abrir el artículo"),
 ("U32","Asha2020","10.1039/d0ra07870k","S_40s (pirólisis)","α-Fe2O3","oxido_binario","principal","U_fb (MS)",-0.20,"V","SCE n.r.",None,"1000",2.1,"absorción UV-vis (método n.r.)","banda plana",None,"admitido","no hasta vincular el pH","bajo","ChatGPT","ambos","0.1 M NaOH, pero el estudio usa pH 13 y 8; pH de esta medición no vinculado"),
 ("U33","Asha2020","10.1039/d0ra07870k","E_100cy (electrodepósito)","α-Fe2O3","oxido_binario","principal","U_fb (MS)",-0.37,"V","SCE n.r.",None,"1000",2.0,"absorción UV-vis (método n.r.)","banda plana",None,"admitido","no hasta vincular el pH","bajo","ChatGPT","ambos","igual que U32"),
 ("U34","LiuZhou2020","10.1039/c9ra09270f","control individual de heterounión","Bi2WO6","oxido_ternario_Bi","principal","U_fb (MS)",-0.76,"V","Ag/AgCl n.r.",None,"n.r.",2.82,"Tauc indirecto (n=4)","banda plana; CB = U_fb − 0.1",-0.56,"admitido","sí (solo U_fb)","bajo","ChatGPT","ambos","pH y frecuencia n.r.; el CB del autor no pasa a AQ"),
]
fe = [
 ("V01","Hwang2015?","10.1021/acscentsci.5b00402","TiO2 rutilo","oxido_binario","enlace","IP (UPS)",7.61,"eV vs vacío","admitido","pendiente","medio","ChatGPT","ChatGPT","par EQ/FE con U24; no pude abrir el artículo"),
 ("V02","Hwang2015?","10.1021/acscentsci.5b00402","BiVO4","oxido_ternario_Bi","enlace","IP (UPS)",6.99,"eV vs vacío","admitido","pendiente","medio","ChatGPT","ChatGPT","par EQ/FE con U25"),
 ("V03","Baddorf2023","10.1038/s41598-023-40187-5","WO3-x","oxido_binario","principal","función de trabajo (UPS, SECO)",4.6,"eV vs vacío","admitido","no (solo WF)","medio","Claude","Claude","sin IP"),
 ("V04","Bhachu2016","10.1039/c6sc00389c","BiOCl","oxihaluro_Bi","reserva_BiOX","VBM − E_F (XPS)",2.9,"eV vs E_F","admitido","no (relativo)","bajo","Claude","Claude","no absoluto"),
 ("V05","Bhachu2016","10.1039/c6sc00389c","BiOBr","oxihaluro_Bi","reserva_BiOX","VBM − E_F (XPS)",2.2,"eV vs E_F","admitido","no (relativo)","bajo","Claude","Claude","no absoluto"),
 ("V06","Bhachu2016","10.1039/c6sc00389c","BiOI","oxihaluro_Bi","reserva_BiOX","VBM − E_F (XPS)",1.6,"eV vs E_F","admitido","no (relativo)","bajo","Claude","Claude","no absoluto"),
 ("V07","Xu2016","10.1038/srep32457","BiOCl","oxihaluro_Bi","reserva_BiOX","VBM − E_F (XPS)",2.16,"eV vs E_F","admitido","no (relativo)","bajo","Claude","Claude","no absoluto"),
 ("V08","Lv2016","10.1038/srep19347","Bi2WO6","oxido_ternario_Bi","principal","VBM − E_F (XPS)",1.78,"eV vs E_F","admitido","no (relativo)","bajo","Claude","Claude","no absoluto"),
 ("V09","Zhao2024","10.1039/d4ta02605e","BiVO4","oxido_ternario_Bi","principal","VBM − E_F (XPS)",1.9,"eV vs E_F","admitido","no (relativo)","bajo","Claude","Claude","no absoluto"),
]

out = sys.argv[1]
hdr = ["id","estudio","doi","muestra","compuesto","familia_a_priori","subconjunto","observable","valor_publicado","unidad",
       "referencia_publicada","pH","frecuencia_Hz","Eg_eV","Eg_metodo","interpretacion_autor","U_SHE_autor_V",
       "U_SHE_definitiva_V","U_SHE_escenario25C_min_V","U_SHE_escenario25C_max_V","admision","apto_ajuste","confianza",
       "extraido_por","verificado_por","banderas_QC"]
with open(f"{out}/piloto_unificado_EQ.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(hdr)
    for r in rows:
        d, lo, hi = convertir(r[8], r[10], r[11])
        w.writerow(list(r[:16]) + [r[16], d, lo, hi] + list(r[17:]))
with open(f"{out}/piloto_unificado_FE.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["id","estudio","doi","compuesto","familia_a_priori","subconjunto","magnitud","valor","referencia",
                                   "admision","apto_ajuste","confianza","extraido_por","verificado_por","banderas_QC"])
    w.writerows(fe)
import collections
print("EQ", len(rows), "FE", len(fe), "estudios", len({r[1] for r in rows} | {r[1] for r in fe}))
print(collections.Counter(r[6] for r in rows)); print(collections.Counter(r[19] for r in rows)); print(collections.Counter(r[21] for r in rows))
print("definitivas:", sum(convertir(r[8], r[10], r[11])[0] is not None for r in rows))
