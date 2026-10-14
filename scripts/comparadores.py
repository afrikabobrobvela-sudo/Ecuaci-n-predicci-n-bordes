"""Comparadores M0–M4 de la fase 3 (M5 se ejecuta aparte con el código de Haghshenas et al.).

Convenciones:
- Potenciales U en V vs SHE; energías en eV vs vacío. SHE absoluto = 4.44 V (Trasatti 1986).
- χ de Mulliken absoluta por elemento: (I1 + A)/2, con I1 y A de la librería `mendeleev`
  (versión registrada en la salida). Elementos sin anión estable (A no tabulada) usan A = 0
  y se marcan; Butler–Ginley 1978 usaron otros valores (ver `chi_bg_implicita`).
- χ del compuesto: media geométrica ponderada por estequiometría (Nethercot / Butler–Ginley).
- Todos los modelos predicen U_CB, que se compara con U_fb al pH experimental (decisión fase 3).
"""
import csv, math, re, sys, os
import mendeleev
from mendeleev import element

E_SHE = 4.44           # eV
E0_BG_SCE = 4.75       # eV, Butler–Ginley 1978, Ec. [1]
SCE_SHE = 0.241        # V
NERNST = 0.0592        # V/pH a 25 °C
DIR = os.path.dirname(os.path.abspath(__file__))

_cache = {}
def chi_elem(s):
    if s not in _cache:
        e = element(s)
        a = e.electron_affinity
        _cache[s] = ((e.ionenergies[1] + (a if a is not None else 0.0)) / 2, a is None)
    return _cache[s]

def parse(formula):
    """'Bi2WO6' -> {'Bi':2,'W':1,'O':6}; admite subíndices decimales (BiOCl0.9I0.1)."""
    out = {}
    for s, n in re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", formula):
        out[s] = out.get(s, 0) + (float(n) if n else 1.0)
    return out

def chi_compuesto(formula):
    comp = parse(formula); n = sum(comp.values())
    logp = sum(k * math.log(chi_elem(s)[0]) for s, k in comp.items())
    sin_A = [s for s in comp if chi_elem(s)[1]]
    return math.exp(logp / n), sin_A

# ---------------- Modelos ----------------
def M0a(formula, Eg):
    """U_CB = (χ − 4.44 − Eg/2)/e  [V vs SHE]."""
    chi, _ = chi_compuesto(formula)
    return chi - E_SHE - Eg / 2

def M0b(formula, Eg):
    """Forma original de Butler–Ginley: EA = χ − Eg/2 = E0(SCE) + U_fb(SCE) ⇒ U_fb(SHE)."""
    chi, _ = chi_compuesto(formula)
    return chi - Eg / 2 - E0_BG_SCE + SCE_SHE

def M1(formula, Eg, pH, pH_pzc):
    """M0a + 0.059·(pH_pzc − pH). Solo con PZC medido (nivel 1); None si falta."""
    if pH is None or pH_pzc is None:
        return None
    return M0a(formula, Eg) + NERNST * (pH_pzc - pH)

def M2(formula, Eg, pH, pH_pzc, dipolo_V=-0.5):
    """M1 + desplazamiento constante por dipolo agua/semiconductor.
    Signo verificado en los originales: Stevanović et al. 2014 (p. 3706: IP y EA se desplazan
    "closer to the vacuum" unos 0.5 eV, dispersión 0.3 eV) y Ali et al. 2021, Catalysts 11, 293,
    Ec. (6): E_CB,pH = E_CB + 0.059(pH_ZPC − pH) − 0.5 eV. Más cerca del vacío = potencial más
    negativo, de ahí −0.5 V. Ali et al. usan 4.5 eV; aquí se mantiene 4.44 eV (M0a) por coherencia."""
    m1 = M1(formula, Eg, pH, pH_pzc)
    return None if m1 is None else m1 + dipolo_V

def _sse_tabla():
    t = {}
    with open(os.path.join(DIR, "..", "data", "escalas", "sse_pelatt2015_tabla1.csv")) as f:
        for r in csv.DictReader(f):
            if r["SSE_eV"]:
                t[(r["elemento"], int(r["estado_oxidacion"]))] = float(r["SSE_eV"])
    return t
SSE = _sse_tabla()
ANION = {"O": -2, "S": -2, "Se": -2, "Te": -2, "F": -1, "Cl": -1, "Br": -1, "I": -1, "N": -3}

def M3(formula, estados=None):
    """SSE (Pelatt 2015) con regla propia C9: E_CB = media estequiométrica de las SSE de cationes.
    `estados` = {elemento: estado de oxidación} para cationes; si hay un solo catión se deduce por
    balance de carga. Devuelve U_CB vs SHE o None si falta algún valor."""
    comp = parse(formula)
    cat = {s: k for s, k in comp.items() if s not in ANION}
    carga_anion = sum(ANION[s] * k for s, k in comp.items() if s in ANION)
    estados = dict(estados or {})
    if len(cat) == 1 and not estados:
        (s, k), = cat.items(); estados[s] = round(-carga_anion / k)
    if set(estados) != set(cat):
        return None
    vals = [(SSE.get((s, estados[s])), k) for s, k in cat.items()]
    if any(v is None for v, _ in vals):
        return None
    e_cb = sum(v * k for v, k in vals) / sum(k for _, k in vals)
    return -e_cb - E_SHE

# ---------------- Comprobación: Butler–Ginley 1978, Tabla I y Fig. 4 ----------------
# Transcrito de la imagen de la Tabla I (p. 231): χ (eV), EA calculada (eV), V_fb (V vs SCE, pH 13.3), pzzp.
BG_TABLA_I = {
    "WO3": (6.53, 5.18, -0.20, 0.43), "Ta2O5": (6.38, 4.08, -1.44, 2.9), "SnO2": (6.24, 4.49, -0.82, 4.3),
    "ZrO2": (5.92, 3.42, -2.04, 6.7), "Fe2O3": (5.88, 4.71, -0.32, 8.6), "TiO2": (5.83, 4.33, -0.90, 5.8),
    "ZnO": (5.75, 4.15, -1.09, 8.8), "FeTiO3": (5.72, 4.30, -0.59, 6.3), "CdO": (5.55, 4.55, -0.22, 11.6),
    "SrTiO3": (5.27, 3.71, -1.19, 8.6), "BaTiO3": (5.19, 3.60, -1.22, 9.9),
}

def reproducir_bg():
    """EA_medida = E0 + V_fb + ΔE_f + 0.059·(pH − pzzp), con E0 = 4.75 eV, ΔE_f = 0.1 eV, pH = 13.3
    (Ec. [1]; el signo del término de pH se fija para que V_fb se refiera al pzzp)."""
    filas = []
    for c, (chi_bg, ea_calc, vfb, pzzp) in BG_TABLA_I.items():
        ea_med = E0_BG_SCE + vfb + 0.1 + NERNST * (13.3 - pzzp)
        eg_impl = 2 * (chi_bg - ea_calc)
        chi_nuevo, sinA = chi_compuesto(c)
        filas.append((c, chi_bg, round(chi_nuevo, 2), ",".join(sinA), round(eg_impl, 2), ea_calc, round(ea_med, 2), round(ea_med - ea_calc, 2)))
    return filas

if __name__ == "__main__":
    print("mendeleev", mendeleev.__version__)
    print("compuesto chi_BG chi_nuestra elementos_sin_A Eg_implicita EA_calc EA_medida residuo")
    fs = reproducir_bg()
    for f in fs:
        print(*f)
    r = [f[-1] for f in fs]
    print("Residuo EA_medida − EA_calc: media %.2f eV, RMS %.2f eV, máx |%.2f| eV (n=%d)" % (
        sum(r) / len(r), math.sqrt(sum(x * x for x in r) / len(r)), max(abs(x) for x in r), len(r)))
    print("Ejemplos M0a:", {f: round(M0a(f, g), 2) for f, g in [("TiO2", 3.0), ("BiVO4", 2.4), ("CdS", 2.4)]})
    print("Ejemplos M3:", {"TiO2": round(M3("TiO2"), 2), "BiVO4": round(M3("BiVO4", {"Bi": 3, "V": 5}), 2), "CdS": round(M3("CdS"), 2)})
