"""Fase 4, análisis exploratorio (separado de K1–K5): búsqueda tipo SISSO de un descriptor.

Modelo: U = M0a + δ + β·φ, con φ elegido entre descriptores primarios y sus combinaciones
(productos, cocientes, diferencias de pares). Selección por MAE en validación dejando fuera una
familia (LOFO) sobre los registros tipo n. Como se prueban muchos φ, el mejor está optimizado sobre
la propia validación: el resultado sirve para generar hipótesis, no como prueba. La reserva BiOX no se usa.
"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comparadores as C
import fase3_evaluar as F3
import fase4_ajuste as F4
from mendeleev import element

ANIONES = set(C.ANION)
METAL_D = {"Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Nb", "Mo", "Ag", "Cd", "Ta", "W", "Zr", "Y", "La", "Ce"}

def descriptores(f):
    comp = C.parse(f["formula"]); n = sum(comp.values())
    cat = {s: k for s, k in comp.items() if s not in ANIONES}; an = {s: k for s, k in comp.items() if s in ANIONES}
    gm = lambda d: __import__("math").exp(sum(k * __import__("math").log(C.chi_elem(s)[0]) for s, k in d.items()) / sum(d.values()))
    nc = sum(cat.values())
    return {
        "chi": C.chi_compuesto(f["formula"])[0], "Eg": f["Eg"], "chi_cat": gm(cat), "chi_an": gm(an),
        "dchi": gm(an) - gm(cat), "f_cat": nc / n, "f_Bi": comp.get("Bi", 0) / nc,
        "f_d": sum(k for s, k in cat.items() if s in METAL_D) / nc,
        "I1_cat": sum(k * element(s).ionenergies[1] for s, k in cat.items()) / nc,
    }

def main():
    filas = [f for f in F3.cargar() if f["tipo"] != "p"]
    for f in filas:
        f["M0a"] = C.M0a(f["formula"], f["Eg"]); f["D"] = descriptores(f)
    prim = list(filas[0]["D"])
    cand = {k: (lambda d, k=k: d[k]) for k in prim}
    for a, b in itertools.combinations(prim, 2):
        cand[f"{a}*{b}"] = lambda d, a=a, b=b: d[a] * d[b]
        cand[f"{a}-{b}"] = lambda d, a=a, b=b: d[a] - d[b]
        cand[f"{a}/{b}"] = lambda d, a=a, b=b: d[a] / d[b] if d[b] else None
    res = []
    fams = sorted({f["familia"] for f in filas})
    for nombre, fn in cand.items():
        xs = [fn(f["D"]) for f in filas]
        if any(x is None for x in xs) or max(xs) - min(xs) < 1e-9: continue
        for f, x in zip(filas, xs): f["phi"] = x
        pred = {}
        for g in fams:
            tr = [f for f in filas if f["familia"] != g]
            mx = sum(f["phi"] for f in tr) / len(tr)
            c = F4.ols([[1, f["phi"] - mx] for f in tr], [f["U"] - f["M0a"] for f in tr])
            if c is None: break
            for f in filas:
                if f["familia"] == g: pred[f["id"]] = f["M0a"] + c[0] + c[1] * (f["phi"] - mx)
        if len(pred) != len(filas): continue
        r = F4.boot_diff(filas, pred)
        res.append((r["MAE_K"], nombre, r["reduccion"], r["ic"]))
    res.sort()
    print(f"{len(res)} descriptores probados; registros tipo n: {len(filas)}")
    for mae, nombre, red, ic in res[:10]:
        print(f"  {nombre:20s} MAE LOFO {mae:.3f}  reducción vs M0a {red:+.3f} [{ic[0]:+.3f}, {ic[1]:+.3f}]")

if __name__ == "__main__":
    main()
