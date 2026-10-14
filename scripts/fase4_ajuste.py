"""Fase 4: ajuste y validación de las correcciones preregistradas K1–K5 (fase3_definicion.md §3–4).

Análisis principal: registros tipo n (U_fb ≈ U_CB, la identificación de Butler–Ginley). Los tipo p
se analizan aparte (U_fb ≈ U_VB = U_CB + Eg) porque en la fase 3 mostraron un sesgo de ~−1.6 V que una
constante común no puede representar sin degradar el tipo n.
Validación: dejando fuera una familia (LOFO, criterio preregistrado) y, como secundaria, un estudio (LOSO).
Criterio: K mejora a M0a si el IC 95 % (bootstrap por estudio, 5000 réplicas) de la reducción del MAE
excluye 0. Entre las que lo cumplan se elige la de menos parámetros.
La reserva BiOX solo se abre con --abrir-reserva, después de fijar el modelo elegido.
"""
import csv, math, os, random, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comparadores as C
import fase3_evaluar as F3

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SAL = os.path.join(RAIZ, "resultados", "fase4")
B, SEMILLA = 5000, 1

def anion(formula):
    return "S" if "S" in C.parse(formula) and "O" not in C.parse(formula) else "O"

def metodo(f):
    return "MS"  # todos los registros aptos son Mott–Schottky (ver salida); K5 no es identificable

# ---------- ajuste por mínimos cuadrados de cada candidata sobre el residuo r = U − M0a ----------
def ols(X, y):
    """Mínimos cuadrados para 1 o 2 columnas (resuelto en forma cerrada)."""
    k = len(X[0])
    if k == 1:
        return [sum(x[0] * v for x, v in zip(X, y)) / sum(x[0] ** 2 for x in X)]
    a = sum(x[0] * x[0] for x in X); b = sum(x[0] * x[1] for x in X); d = sum(x[1] * x[1] for x in X)
    p = sum(x[0] * v for x, v in zip(X, y)); q = sum(x[1] * v for x, v in zip(X, y))
    det = a * d - b * b
    if abs(det) < 1e-12:
        return None
    return [(d * p - b * q) / det, (a * q - b * p) / det]

def ajustar(nombre, tr):
    r = [f["U"] - f["M0a"] for f in tr]
    if nombre == "K1":
        return {"d": ols([[1] for _ in tr], r)[0]}
    if nombre == "K2":
        eb = sum(f["Eg"] for f in tr) / len(tr)
        c = ols([[1, f["Eg"] - eb] for f in tr], r)
        return None if c is None else {"d": c[0], "b": c[1], "Eb": eb}
    if nombre == "K3":
        sub = [f for f in tr if f["pH"] is not None]
        c = ols([[1, -(f["pH"] - 7)] for f in sub], [f["U"] - f["M0a"] for f in sub])
        return None if c is None else {"d": c[0], "s": c[1]}
    if nombre == "K4":
        g = defaultdict(list)
        for f in tr: g[anion(f["formula"])].append(f["U"] - f["M0a"])
        return {"d_" + k: sum(v) / len(v) for k, v in g.items()} | {"d": sum(r) / len(r)}
    raise ValueError(nombre)

def predecir(nombre, p, f):
    if p is None: return None
    if nombre == "K1": return f["M0a"] + p["d"]
    if nombre == "K2": return f["M0a"] + p["d"] + p["b"] * (f["Eg"] - p["Eb"])
    if nombre == "K3": return None if f["pH"] is None else f["M0a"] + p["d"] - p["s"] * (f["pH"] - 7)
    if nombre == "K4": return f["M0a"] + p.get("d_" + anion(f["formula"]), p["d"])  # anión ausente: δ global
    raise ValueError(nombre)

CANDIDATAS = {"K1": 1, "K2": 2, "K3": 2, "K4": 2}

def validar(filas, grupo):
    """Predicciones fuera de muestra agrupando por 'familia' (LOFO) o 'estudio' (LOSO)."""
    pred = {k: {} for k in CANDIDATAS}
    for g in sorted({f[grupo] for f in filas}):
        tr = [f for f in filas if f[grupo] != g]; te = [f for f in filas if f[grupo] == g]
        for k in CANDIDATAS:
            p = ajustar(k, tr)
            for f in te:
                pred[k][f["id"]] = predecir(k, p, f)
    return pred

def boot_diff(filas, pred_k):
    """Reducción del MAE (M0a − K) en los registros donde K predice; IC por bootstrap de estudios."""
    por = defaultdict(list)
    for f in filas:
        if pred_k.get(f["id"]) is not None:
            por[f["estudio"]].append((abs(f["U"] - f["M0a"]), abs(f["U"] - pred_k[f["id"]])))
    todos = [x for v in por.values() for x in v]
    if not todos: return None
    def st(xs): return (sum(a for a, _ in xs) / len(xs), sum(b for _, b in xs) / len(xs))
    m0, mk = st(todos)
    rnd = random.Random(SEMILLA); est = list(por); bs = []
    for _ in range(B):
        xs = [x for s in (rnd.choice(est) for _ in est) for x in por[s]]
        a, b = st(xs); bs.append(a - b)
    bs.sort()
    return dict(n=len(todos), estudios=len(est), MAE_M0a=m0, MAE_K=mk, reduccion=m0 - mk,
                ic=(bs[int(0.025 * B)], bs[int(0.975 * B) - 1]))

def boot_param(nombre, filas):
    """IC de los parámetros ajustados con toda la base (bootstrap de estudios)."""
    p0 = ajustar(nombre, filas)
    por = defaultdict(list)
    for f in filas: por[f["estudio"]].append(f)
    rnd = random.Random(SEMILLA); est = list(por); bs = defaultdict(list)
    for _ in range(B):
        tr = [f for s in (rnd.choice(est) for _ in est) for f in por[s]]
        p = ajustar(nombre, tr)
        if p:
            for k, v in p.items(): bs[k].append(v)
    ic = {k: (sorted(v)[int(0.025 * len(v))], sorted(v)[int(0.975 * len(v)) - 1]) for k, v in bs.items()}
    return p0, ic

def cargar_reserva():
    filas = []
    for r in csv.DictReader(open(os.path.join(RAIZ, "data", "piloto", "piloto_unificado_EQ.csv"))):
        if r["subconjunto"] == "reserva_BiOX" and r["apto_ajuste"].startswith(("sí", "reserva")) and r["U_SHE_definitiva_V"] and r["Eg_eV"]:
            filas.append(dict(id=r["id"], estudio=r["estudio"], formula=F3.formula(r["compuesto"]), U=float(r["U_SHE_definitiva_V"]),
                              Eg=float(r["Eg_eV"]), pH=float(r["pH"]) if r["pH"] else None,
                              tipo="p" if "tipo p" in r["interpretacion_autor"] else "n"))
    for r in csv.DictReader(open(os.path.join(RAIZ, "data", "extraccion_fase3", "base_EQ_fase3.csv"))):
        if r["apto_ajuste"] == "reserva":
            filas.append(dict(id=r["rid"], estudio=r["estudio"], formula=F3.formula(r["compuesto"]), U=float(r["U_SHE_definitiva_V"]),
                              Eg=float(r["Eg_eV"]), pH=float(r["pH"]) if r["pH"] else None, tipo=r["tipo"] or "n"))
    for f in filas:
        f["M0a"] = C.M0a(f["formula"], f["Eg"]); f["M0b"] = C.M0b(f["formula"], f["Eg"])
    return filas

def main():
    os.makedirs(SAL, exist_ok=True)
    todas = F3.cargar()
    for f in todas:
        f["M0a"] = C.M0a(f["formula"], f["Eg"])  # U_CB predicho
    n = [f for f in todas if f["tipo"] != "p"]
    p = [dict(f, M0a=f["M0a"] + f["Eg"]) for f in todas if f["tipo"] == "p"]  # se compara con U_VB
    print(f"tipo n: {len(n)} registros, {len({f['estudio'] for f in n})} estudios; tipo p: {len(p)}, {len({f['estudio'] for f in p})}")
    print("familias tipo n:", dict(sorted(defaultdict(int, {k: sum(f['familia'] == k for f in n) for k in {f['familia'] for f in n}}).items())))
    print("con pH (tipo n):", sum(f["pH"] is not None for f in n), "| métodos:", {metodo(f) for f in todas}, "→ K5 no identificable")
    filas_out = []
    for nombre_sub, sub in (("n", n), ("p", p)):
        for grupo in ("familia", "estudio"):
            pred = validar(sub, grupo)
            for k in CANDIDATAS:
                r = boot_diff(sub, pred[k])
                if r is None: continue
                excl = r["ic"][0] > 0
                filas_out.append([nombre_sub, "LOFO" if grupo == "familia" else "LOSO", k, CANDIDATAS[k], r["n"], r["estudios"],
                                  f"{r['MAE_M0a']:.3f}", f"{r['MAE_K']:.3f}", f"{r['reduccion']:+.3f}",
                                  f"[{r['ic'][0]:+.3f}, {r['ic'][1]:+.3f}]", "sí" if excl else "no"])
                print(nombre_sub, filas_out[-1][1], k, f"n={r['n']} MAE M0a {r['MAE_M0a']:.3f} → {r['MAE_K']:.3f}; "
                      f"reducción {r['reduccion']:+.3f} [{r['ic'][0]:+.3f}, {r['ic'][1]:+.3f}]", "MEJORA" if excl else "")
        for k in CANDIDATAS:
            p0, ic = boot_param(k, sub)
            print(f"  parámetros {nombre_sub} {k} (toda la base):", {a: f"{v:+.3f} [{ic[a][0]:+.3f}, {ic[a][1]:+.3f}]" for a, v in p0.items() if a in ic})
    with open(os.path.join(SAL, "validacion_K.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["tipo", "validacion", "candidata", "n_param", "n_registros", "n_estudios", "MAE_M0a_V", "MAE_K_V",
                    "reduccion_MAE_V", "IC95_reduccion", "IC_excluye_0"])
        w.writerows(filas_out)
    # Elección según el criterio preregistrado (LOFO, tipo n)
    ok = [r for r in filas_out if r[0] == "n" and r[1] == "LOFO" and r[10] == "sí"]
    elegida = min(ok, key=lambda r: (r[3], -float(r[8])))[2] if ok else "M0a"
    print("modelo elegido (tipo n, LOFO):", elegida)
    if "--abrir-reserva" in sys.argv:
        res = cargar_reserva()
        pk = ajustar(elegida, n) if elegida != "M0a" else None
        print(f"RESERVA BiOX: {len(res)} registros, {len({f['estudio'] for f in res})} estudios")
        with open(os.path.join(SAL, "prueba_reserva_BiOX.csv"), "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["id", "estudio", "formula", "tipo", "pH", "Eg", "U_obs", "M0a", "M0b", elegida])
            for f in res:
                cb = predecir(elegida, pk, f) if pk else f["M0a"]
                sh = f["Eg"] if f["tipo"] == "p" else 0
                w.writerow([f["id"], f["estudio"], f["formula"], f["tipo"], f["pH"], f["Eg"], f["U"],
                            round(f["M0a"] + sh, 3), round(f["M0b"] + sh, 3), None if cb is None else round(cb + sh, 3)])
        print("escrito prueba_reserva_BiOX.csv")

if __name__ == "__main__":
    main()
