"""Errores de los comparadores sobre el conjunto de entrenamiento (fase 3). La reserva BiOX no se toca.

Objetivo: U_fb (V vs SHE, pH experimental). Tipo n: se compara con U_CB predicho; tipo p: con
U_VB = U_CB + Eg (decisión fase 3). Error = observado − predicho.
IC 95 %: bootstrap por estudio (remuestreo de estudios completos, 5000 réplicas, semilla fija).
M4 (nulos) se evalúa con validación dejando fuera un estudio (LOSO), sin usar el estudio evaluado.
"""
import csv, math, os, random, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comparadores as C

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ESTADOS = {  # estados de oxidación de cationes para M3 cuando hay más de un catión (regla C9)
    "CuWO4": {"Cu": 2, "W": 6}, "LaFeO3": {"La": 3, "Fe": 3}, "CuFeO2": {"Cu": 1, "Fe": 3},
    "CaCu3Ti4O12": {"Ca": 2, "Cu": 2, "Ti": 4}, "BiVO4": {"Bi": 3, "V": 5}, "CuBi2O4": {"Cu": 2, "Bi": 3},
    "Bi4Ti3O12": {"Bi": 3, "Ti": 4}, "Bi2WO6": {"Bi": 3, "W": 6}, "ZnIn2S4": {"Zn": 2, "In": 3},
    "CuInS2": {"Cu": 1, "In": 3}, "Bi2Sn2O7": {"Bi": 3, "Sn": 4}, "BiFeO3": {"Bi": 3, "Fe": 3},
    "ZnFe2O4": {"Zn": 2, "Fe": 3}, "CuFe2O4": {"Cu": 2, "Fe": 3}, "SrTiO3": {"Sr": 2, "Ti": 4},
    "Bi2MoO6": {"Bi": 3, "Mo": 6}, "Bi4V2O11": {"Bi": 3, "V": 5}, "MgFe2O4": {"Mg": 2, "Fe": 3},
    "CuCrO2": {"Cu": 1, "Cr": 3}, "Li2SnO3": {"Li": 1, "Sn": 4}, "Cu3Ta7O19": {"Cu": 1, "Ta": 5},
    "Cu3VO4": {"Cu": 1, "V": 5}, "CuNbO3": {"Cu": 1, "Nb": 5}, "Cu5V2O10": {"Cu": 2, "V": 5},
    "MnFe2O4": {"Mn": 2, "Fe": 3}, "Ca2Nb3O10": {"Ca": 2, "Nb": 5},
    # Sin estados asignados (valencia mixta o catión sin SSE en la tabla): Co3O4, TiVO4, Ag3PO4 (P5+).
}

def formula(nombre):
    t = nombre.replace("α-", "").replace("β-", "").replace("γ-", "").strip().split()[0]
    return t

def cargar():
    filas = []
    for r in csv.DictReader(open(os.path.join(RAIZ, "data", "piloto", "piloto_unificado_EQ.csv"))):
        if not r["apto_ajuste"].startswith("sí") or r["subconjunto"] == "reserva_BiOX" or not r["U_SHE_definitiva_V"]:
            continue
        tipo = "p" if "tipo p" in r["interpretacion_autor"] else "n"
        filas.append(dict(id=r["id"], estudio=r["estudio"], formula=formula(r["compuesto"]), familia=r["familia_a_priori"],
                          U=float(r["U_SHE_definitiva_V"]), Eg=float(r["Eg_eV"]) if r["Eg_eV"] else None,
                          pH=float(r["pH"]) if r["pH"] else None, tipo=tipo, origen="piloto"))
    for r in csv.DictReader(open(os.path.join(RAIZ, "data", "extraccion_fase3", "base_EQ_fase3.csv"))):
        if r["apto_ajuste"] != "sí":
            continue
        filas.append(dict(id=r["rid"], estudio=r["estudio"], formula=formula(r["compuesto"]), familia=r["familia"],
                          U=float(r["U_SHE_definitiva_V"]), Eg=float(r["Eg_eV"]), pH=float(r["pH"]) if r["pH"] else None,
                          tipo=(r["tipo"] or "n"), origen="fase3"))
    return [f for f in filas if f["Eg"] is not None]

def pred_borde(cb, f):
    return cb if f["tipo"] != "p" else cb + f["Eg"]

def modelos(f):
    out = {"M0a": pred_borde(C.M0a(f["formula"], f["Eg"]), f), "M0b": pred_borde(C.M0b(f["formula"], f["Eg"]), f)}
    m3 = C.M3(f["formula"], ESTADOS.get(f["formula"]))
    out["M3"] = None if m3 is None else pred_borde(m3, f)
    return out

def metricas(errs_por_estudio, B=5000, semilla=1):
    todos = [e for es in errs_por_estudio.values() for e in es]
    def stats(xs):
        n = len(xs); return (sum(abs(x) for x in xs) / n, math.sqrt(sum(x * x for x in xs) / n), sum(xs) / n)
    base = stats(todos)
    rnd = random.Random(semilla); est = list(errs_por_estudio)
    boot = []
    for _ in range(B):
        xs = [e for s in (rnd.choice(est) for _ in est) for e in errs_por_estudio[s]]
        boot.append(stats(xs))
    ic = [sorted(b[i] for b in boot) for i in range(3)]
    q = lambda v: (v[int(0.025 * B)], v[int(0.975 * B) - 1])
    return len(todos), len(est), base, [q(v) for v in ic]

def main():
    filas = cargar()
    salida = []
    for f in filas:
        m = modelos(f); f.update({k: (None if v is None else round(v, 3)) for k, v in m.items()})
    # M4 nulos con LOSO: (a) media global; (c) media por familia (cae a la global si la familia no tiene otros estudios)
    for f in filas:
        resto = [g for g in filas if g["estudio"] != f["estudio"]]
        f["M4a"] = round(sum(g["U"] for g in resto) / len(resto), 3)
        fam = [g["U"] for g in resto if g["familia"] == f["familia"]]
        f["M4c"] = round(sum(fam) / len(fam), 3) if fam else f["M4a"]
        # (b) regresión lineal U ~ Eg en el resto
        xs = [g["Eg"] for g in resto]; ys = [g["U"] for g in resto]; mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
        b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        f["M4b"] = round(my + b * (f["Eg"] - mx), 3)
    res = {}
    for mod in ["M0a", "M0b", "M3", "M4a", "M4b", "M4c"]:
        d = defaultdict(list)
        for f in filas:
            if f[mod] is not None:
                d[f["estudio"]].append(f["U"] - f[mod])
        res[mod] = metricas(d)
    os.makedirs(os.path.join(RAIZ, "resultados", "fase3"), exist_ok=True)
    with open(os.path.join(RAIZ, "resultados", "fase3", "predicciones_comparadores.csv"), "w", newline="") as fh:
        cols = ["id", "estudio", "formula", "familia", "tipo", "pH", "Eg", "U", "M0a", "M0b", "M3", "M4a", "M4b", "M4c", "origen"]
        w = csv.writer(fh); w.writerow(cols); [w.writerow([f[c] for c in cols]) for f in filas]
    with open(os.path.join(RAIZ, "resultados", "fase3", "errores_comparadores.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["modelo", "n_registros", "n_estudios", "MAE_V", "MAE_IC95", "RMSE_V", "RMSE_IC95", "sesgo_V", "sesgo_IC95"])
        for mod, (n, ne, (mae, rmse, bias), (ci_mae, ci_rmse, ci_b)) in res.items():
            fmt = lambda c: f"[{c[0]:.2f}, {c[1]:.2f}]"
            w.writerow([mod, n, ne, f"{mae:.2f}", fmt(ci_mae), f"{rmse:.2f}", fmt(ci_rmse), f"{bias:+.2f}", fmt(ci_b)])
            print(mod, n, ne, f"MAE {mae:.2f} {fmt(ci_mae)}  RMSE {rmse:.2f} {fmt(ci_rmse)}  sesgo {bias:+.2f} {fmt(ci_b)}")
    # Por tipo de portador (n: borde de conducción; p: borde de valencia)
    for tp in ("n", "p"):
        sub = [f for f in filas if (f["tipo"] == "p") == (tp == "p")]
        for mod in ["M0a", "M0b", "M3", "M4c"]:
            d = defaultdict(list)
            for f in sub:
                if f[mod] is not None: d[f["estudio"]].append(f["U"] - f[mod])
            n, ne, (mae, rmse, bias), (ci_mae, _, ci_b) = metricas(d)
            print(f"tipo {tp} {mod}: n={n} estudios={ne} MAE {mae:.2f} [{ci_mae[0]:.2f}, {ci_mae[1]:.2f}] sesgo {bias:+.2f} [{ci_b[0]:.2f}, {ci_b[1]:.2f}]")
    # Sensibilidad (C2: solo como análisis secundario): normalización nernstiana a pH 0 en registros con pH
    sub = [f for f in filas if f["pH"] is not None and f["tipo"] != "p"]
    e0 = [f["U"] - f["M0a"] for f in sub]
    e = [f["U"] + C.NERNST * f["pH"] - f["M0a"] for f in sub]
    print(f"sensibilidad tipo n con pH conocido (n={len(sub)}): sin normalizar MAE {sum(map(abs, e0))/len(e0):.2f} "
          f"sesgo {sum(e0)/len(e0):+.2f}; llevado a pH 0 (59 mV/pH) MAE {sum(map(abs, e))/len(e):.2f} sesgo {sum(e)/len(e):+.2f}")
    xs = [f["pH"] for f in sub]; mx = sum(xs) / len(xs); my = sum(e0) / len(e0)
    print(f"pendiente del residuo de M0a frente al pH entre estudios: {sum((x-mx)*(y-my) for x, y in zip(xs, e0))/sum((x-mx)**2 for x in xs)*1000:.1f} mV/pH")
    # Por familia, M0a
    print("M0a por familia:")
    fam = defaultdict(list)
    for f in filas: fam[f["familia"]].append(f["U"] - f["M0a"])
    for k, v in sorted(fam.items()):
        print(f"  {k}: n={len(v)} MAE {sum(map(abs, v))/len(v):.2f} sesgo {sum(v)/len(v):+.2f}")
    print("tipo p:", sum(f['tipo'] == 'p' for f in filas), "de", len(filas))

if __name__ == "__main__":
    main()
