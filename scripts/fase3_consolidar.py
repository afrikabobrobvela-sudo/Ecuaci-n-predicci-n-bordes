"""Consolida la extracción de la fase 3 con la verificación a ciegas y aplica las reglas A1–A7.

Entrada: data/extraccion_fase3/bruto/<familia>.jsonl (primera extracción) y
         data/extraccion_fase3/bruto/verif_<familia>.jsonl (segunda extracción, a ciegas).
Salida:  data/extraccion_fase3/comparacion_verificacion.csv y data/extraccion_fase3/base_EQ_fase3.csv
"""
import csv, json, glob, os, re, sys

NERNST = 0.0592
# Valores a 25 °C usados en el piloto (fase 2, Inzelt et al. 2013 vía fuentes secundarias).
REF = {"Ag/AgCl sat": 0.197, "Ag/AgCl 3 M": 0.210, "SCE sat": 0.241, "Hg/Hg2SO4 sat": 0.640, "SHE": 0.0}
ESCENARIO = {"Ag/AgCl n.r.": (0.197, 0.235), "SCE n.r.": (0.241, 0.280)}
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "extraccion_fase3")
FAMILIAS = ["oxido_binario", "oxido_ternario", "oxido_ternario_Bi", "sulfuro", "oxihaluro_Bi"]

def num(x):
    if x is None: return None
    if isinstance(x, (int, float)): return float(x)
    m = re.search(r"[-−–+]?\s*\d+(?:\.\d+)?", str(x))
    return float(m.group(0).replace("−", "-").replace("–", "-").replace(" ", "")) if m else None

def escala(ref, relleno):
    """Normaliza la escala publicada a una clave de REF/ESCENARIO, 'RHE', o None si no se reconoce."""
    t = f"{ref or ''} {relleno or ''}".lower()
    if not t.strip(): return None
    if "rhe" in t: return "RHE"
    if "nhe" in t or "she" in t: return "SHE"
    if "hg2so4" in t or "mse" in t: return "Hg/Hg2SO4 sat" if "sat" in t else None
    if "hg/hgo" in t: return "Hg/HgO"            # sin valor verificado en nuestra tabla
    if "sce" in t or "calomel" in t:
        return "SCE sat" if ("sat" in t or t.strip() in ("sce", "sce sce")) else "SCE n.r."
    if "ag/agcl" in t or "agcl" in t:
        if "sat" in t: return "Ag/AgCl sat"
        if re.search(r"\b3(\.0)?\s*m\b", t): return "Ag/AgCl 3 M"
        if re.search(r"\d", t): return "Ag/AgCl otro relleno"  # 3.5 M, 4 M, 1 M, 0.1 M: sin valor verificado
        return "Ag/AgCl n.r."
    return None

def convertir(v, esc, ph):
    if v is None or esc is None: return None, None, None
    if esc == "RHE":
        return (None, None, None) if ph is None else (round(v - NERNST * ph, 3),) * 3
    if esc in REF:
        u = round(v + REF[esc], 3); return u, u, u
    if esc in ESCENARIO:
        lo, hi = ESCENARIO[esc]; return None, round(v + lo, 3), round(v + hi, 3)
    return None, None, None

def cargar(path):
    if not os.path.exists(path): return []
    return [json.loads(l) for l in open(path) if l.strip()]

def comparar(r, v):
    """Devuelve (estado, detalles, pH_consenso, Eg_consenso).
    - El valor debe coincidir (tolerancia de redondeo 0.006 V); si no, 'discrepa_valor'.
    - pH: si las dos extracciones no concuerdan, se toma None (criterio conservador) y se marca.
    - Eg: si solo una extracción lo encontró, se usa ese valor y se marca 'Eg de una sola extracción'."""
    ph1, eg1 = num(r.get("pH")), num(r.get("Eg_eV"))
    if v is None: return "sin_verificar", "", ph1, eg1
    if v.get("no_encontrado"): return "no_encontrado", v.get("nota") or v.get("notas") or "", ph1, eg1
    d = []
    a = num(r.get("valor")); b = num(v.get("U_fb_publicado", v.get("U_fb")))
    if a is None or b is None or abs(a - b) > 0.006:
        return "discrepa_valor", f"valor {a} vs {b}", ph1, eg1
    ph2, eg2 = num(v.get("pH")), num(v.get("Eg_eV"))
    ph = ph1 if (ph1 is not None and ph2 is not None and abs(ph1 - ph2) <= 0.06) else None
    if ph1 != ph2 and ph is None and (ph1 is not None or ph2 is not None): d.append(f"pH {ph1} vs {ph2} (se toma n.r.)")
    if eg1 is not None and eg2 is not None:
        eg = eg1 if abs(eg1 - eg2) <= 0.051 else None
        if eg is None: d.append(f"Eg {eg1} vs {eg2} (se toma n.r.)")
    else:
        eg = eg1 if eg1 is not None else eg2
        if (eg1 is None) != (eg2 is None): d.append("Eg de una sola extracción")
    return ("coincide" if not d else "coincide_valor"), "; ".join(d), ph, eg

ROJAS = ("dopad", "redox", "ferri", "fe(cn)", "iluminac", "luz", "no acuoso", "compuesto", "heterou")

def admision(r, esc, defin, estado):
    motivos = []
    texto = " ".join(map(str, r.get("banderas") or [])).lower() + " " + str(r.get("electrolito") or "").lower()
    if any(k in texto for k in ("fe(cn)", "ferri", "ferro", "redox")): motivos.append("electrolito con par redox")
    if "dopad" in texto or "doped" in texto or "dopad" in str(r.get("muestra", "")).lower(): motivos.append("dopado")
    muestra = str(r.get("muestra", "")).lower()
    if re.search(r"\b(?!0\b)\d+(\.\d+)?\s*kgy", muestra) or "irradi" in muestra:
        motivos.append("variante tratada (irradiada)")
    if "fermi" in texto: motivos.append("observable reportado como nivel de Fermi, no U_fb")
    if str(r.get("unidad", "")).lower().startswith("ev"): motivos.append("publicado en eV")
    if esc is None: motivos.append("escala no identificable")
    if defin is None: motivos.append("sin conversión definitiva")
    if r.get("pH") is None: motivos.append("pH n.r.")
    if r.get("Eg_eV") is None: motivos.append("Eg n.r.")
    if estado not in ("coincide", "coincide_valor"): motivos.append(f"verificación: {estado}")
    adm = "cuarentena" if ("electrolito con par redox" in motivos or esc is None) else "admitido"
    # A4 solo exige el pH para convertir desde RHE (ya cubierto por "sin conversión definitiva").
    # Un pH no reportado no bloquea la aptitud: impide M1/M2/K3 en ese registro y se marca.
    bloqueantes = [m for m in motivos if m != "pH n.r."]
    apto = "sí" if not bloqueantes else "no"
    return adm, apto, "; ".join(motivos)

def main():
    comp_rows, base_rows = [], []
    for fam in FAMILIAS:
        recs = cargar(os.path.join(BASE, "bruto", f"{fam}.jsonl"))
        ver = {v["rid"]: v for v in cargar(os.path.join(BASE, "bruto", f"verif_{fam}.jsonl"))}
        for i, r in enumerate(recs):
            rid = f"{fam}:{i}"
            estado, det, ph, eg = comparar(r, ver.get(rid))
            r = dict(r, pH=ph, Eg_eV=eg)
            esc = escala(r.get("referencia_publicada"), r.get("relleno"))
            v = num(r.get("valor"))
            d, lo, hi = convertir(v, esc, ph)
            adm, apto, mot = admision(r, esc, d, estado)
            comp_rows.append([rid, r.get("estudio"), r.get("doi"), r.get("compuesto"), r.get("valor"),
                              (ver.get(rid) or {}).get("U_fb_publicado", (ver.get(rid) or {}).get("U_fb")), estado, det])
            reserva = fam == "oxihaluro_Bi"
            base_rows.append([rid, r.get("estudio"), r.get("doi"), r.get("muestra"), r.get("compuesto"),
                              r.get("familia"), "reserva_BiOX" if reserva else "principal", r.get("observable"),
                              v, r.get("unidad"), r.get("referencia_publicada"), r.get("relleno"), esc, ph,
                              r.get("electrolito"), r.get("frecuencia_Hz"), r.get("tipo"), num(r.get("Eg_eV")),
                              r.get("Eg_metodo"), d, lo, hi, adm, ("reserva" if reserva and apto == "sí" else apto),
                              mot, estado, "; ".join(map(str, r.get("banderas") or [])), r.get("acceso_url")])
    with open(os.path.join(BASE, "comparacion_verificacion.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["rid", "estudio", "doi", "compuesto", "valor_1a", "valor_2a", "estado", "discrepancias"]); w.writerows(comp_rows)
    with open(os.path.join(BASE, "base_EQ_fase3.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rid", "estudio", "doi", "muestra", "compuesto", "familia", "subconjunto", "observable", "valor_publicado",
                    "unidad", "referencia_publicada", "relleno", "escala_normalizada", "pH", "electrolito", "frecuencia_Hz",
                    "tipo", "Eg_eV", "Eg_metodo", "U_SHE_definitiva_V", "U_SHE_escenario_min_V", "U_SHE_escenario_max_V",
                    "admision", "apto_ajuste", "motivos_no_apto", "verificacion", "banderas_extraccion", "acceso_url"])
        w.writerows(base_rows)
    from collections import Counter
    print("verificación:", Counter(r[6] for r in comp_rows))
    print("apto:", Counter((r[6], r[23]) for r in base_rows))
    print("estudios aptos (principal):", len({r[1] for r in base_rows if r[23] == "sí"}))

if __name__ == "__main__":
    main()
