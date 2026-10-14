"""M5 (Haghshenas et al. 2024, código original) frente a la base EQ y la reserva BiOX.

Entradas:
  work/pred_cod.jsonl                         salida de hagh_m5.py sobre data/estructuras_cod/cif/*.cif
  data/estructuras_cod/seleccion_cod.csv      qué CIF se eligió para cada fase (cod_descargar.py)
  resultados/fase3/predicciones_comparadores.csv   base de entrenamiento (65 registros) con M0a/M0b
  resultados/fase4/prueba_reserva_BiOX.csv         reserva BiOX (21 registros) con M0a y K1

Conversión (la del propio repo): E_VBM sale en eV vs vacío; U_VB (V vs SHE) = −E_VBM − 4.44;
U_CB = −(E_VBM + Eg) − 4.44. Igual que M0, la predicción no depende del pH y se compara con
U_fb al pH experimental (tipo n con U_CB, tipo p con U_VB).
  M5      : Eg predicho por el CGCNN de band gap del repo (pipeline original).
  M5-Egexp: Eg experimental del registro (misma información de gap que M0; sensibilidad).
TiO2 usa anatasa; rutilo va como sensibilidad. M5 no se ajusta a nada: la reserva BiOX es solo
prueba, como en la fase 4.
"""
import csv, json, math, os, random, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
E_SHE = 4.44
OUTDIR = os.path.join(ROOT, "resultados", "fase4", "m5")


def entrenamiento_haghshenas():
    """Fórmulas reducidas del set experimental de ajuste fino de Haghshenas (89 bulk del repo)."""
    import glob
    from ase.io import read
    from pymatgen.core import Composition
    db = os.path.join(HERE, "..", "hagh_repo", "CGCNN", "3D-TL-CGCNN", "material_bulk_of_exp_vbm_db")
    return {Composition(read(f).get_chemical_formula()).reduced_formula for f in glob.glob(os.path.join(db, "*.cif"))}


def cargar_m5():
    sel = {}
    with open(os.path.join(ROOT, "data", "estructuras_cod", "seleccion_cod.csv")) as f:
        for r in csv.DictReader(f):
            sel[(r["compuesto"], r["fase"])] = r
    pred = {}
    with open(os.path.join(HERE, "work", "pred_cod.jsonl")) as f:
        for line in f:
            path, js = line.split(" ", 1)
            base = os.path.basename(path)[:-4]           # Compuesto_fase_CODid
            comp, rest = base.split("_", 1)
            fase = rest.rsplit("_COD", 1)[0]
            pred[(comp, fase)] = json.loads(js)
    return sel, pred


def metricas(errs_por_estudio, B=5000, semilla=1):
    """MAE, sesgo y bootstrap por estudio (misma función que fase3_evaluar.py)."""
    todos = [e for es in errs_por_estudio.values() for e in es]
    st = lambda xs: (sum(abs(x) for x in xs) / len(xs), sum(xs) / len(xs))
    rnd = random.Random(semilla); est = list(errs_por_estudio); boot = []
    for _ in range(B):
        boot.append(st([e for s in (rnd.choice(est) for _ in est) for e in errs_por_estudio[s]]))
    q = lambda v: (sorted(v)[int(0.025 * B)], sorted(v)[int(0.975 * B) - 1])
    return len(todos), len(est), st(todos), q([b[0] for b in boot]), q([b[1] for b in boot])


def dif_pareada(filas, a, b, B=5000, semilla=1):
    """MAE(a) − MAE(b) sobre los mismos registros, IC por bootstrap de estudios."""
    por = defaultdict(list)
    for f in filas:
        por[f["estudio"]].append(abs(f["U"] - f[a]) - abs(f["U"] - f[b]))
    n = sum(map(len, por.values())); d = sum(sum(v) for v in por.values()) / n
    rnd = random.Random(semilla); est = list(por); boot = []
    for _ in range(B):
        xs = [x for s in (rnd.choice(est) for _ in est) for x in por[s]]
        boot.append(sum(xs) / len(xs))
    boot.sort()
    return d, (boot[int(0.025 * B)], boot[int(0.975 * B) - 1])


def main():
    sel, pred = cargar_m5()
    ent = entrenamiento_haghshenas()
    from pymatgen.core import Composition
    fase_de = {c: f for (c, f) in sel if f != "rutilo" or c != "TiO2"}

    filas = []
    for archivo, conj, ucol in (("resultados/fase3/predicciones_comparadores.csv", "entrenamiento", "U"),
                                ("resultados/fase4/prueba_reserva_BiOX.csv", "reserva_BiOX", "U_obs")):
        with open(os.path.join(ROOT, archivo)) as f:
            for r in csv.DictReader(f):
                c = r["formula"]; fase = fase_de.get(c)
                fila = dict(conjunto=conj, id=r["id"], estudio=r["estudio"], formula=c, tipo=r["tipo"],
                            pH=r["pH"], Eg=float(r["Eg"]), U=float(r[ucol]), M0a=float(r["M0a"]),
                            K1=float(r["K1_por_tipo"]) if "K1_por_tipo" in r else None,
                            fase=fase or "", cod_id=sel.get((c, fase), {}).get("cod_id", "") if fase else "",
                            en_ajuste_Haghshenas="sí" if Composition(c).reduced_formula in ent else "no",
                            VBM_vac=None, Eg_M5=None, M5=None, M5_Egexp=None, M5_rutilo=None, M5_Egexp_rutilo=None)
                p = pred.get((c, fase))
                if p:
                    vbm, eg = p["vbm_mean"], p["bg_bulk"]
                    fila.update(VBM_vac=vbm, Eg_M5=eg)
                    if r["tipo"] == "p":
                        fila["M5"] = fila["M5_Egexp"] = -vbm - E_SHE
                    else:
                        fila["M5"] = -(vbm + eg) - E_SHE
                        fila["M5_Egexp"] = -(vbm + fila["Eg"]) - E_SHE
                    if c == "TiO2" and ("TiO2", "rutilo") in pred:
                        pr = pred[("TiO2", "rutilo")]
                        fila["M5_rutilo"] = -(pr["vbm_mean"] + pr["bg_bulk"]) - E_SHE
                        fila["M5_Egexp_rutilo"] = -(pr["vbm_mean"] + fila["Eg"]) - E_SHE
                filas.append(fila)

    os.makedirs(OUTDIR, exist_ok=True)
    cols = list(filas[0])
    with open(os.path.join(OUTDIR, "m5_registros.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for fl in filas:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else ("" if v is None else v)) for k, v in fl.items()})

    out = []
    pr = lambda *a: out.append(" ".join(str(x) for x in a))
    pr("M5 (Haghshenas 2024, código original, CIF del COD). Error = U_obs − predicho (V vs SHE).")
    pr("Formulas del set de ajuste fino de Haghshenas presentes:", sorted({f["formula"] for f in filas if f["en_ajuste_Haghshenas"] == "sí"}))
    sin = sorted({f["formula"] for f in filas if f["M5"] is None})
    pr("Sin predicción M5 (sin CIF ordenado en COD):", sin)
    for conj in ("entrenamiento", "reserva_BiOX"):
        for tipo in ("n", "p"):
            sub = [f for f in filas if f["conjunto"] == conj and f["tipo"] == tipo]
            con = [f for f in sub if f["M5"] is not None]
            pr(f"\n== {conj}, tipo {tipo}: {len(sub)} registros, {len(con)} con M5 ==")
            if len(con) < 3:
                continue
            for etiqueta, grupo in (("todos", con),
                                    ("fuera del ajuste de Haghshenas", [f for f in con if f["en_ajuste_Haghshenas"] == "no"]),
                                    ("dentro del ajuste (no ciego)", [f for f in con if f["en_ajuste_Haghshenas"] == "sí"])):
                if len(grupo) < 3:
                    pr(f"  [{etiqueta}] n={len(grupo)}: muy pocos"); continue
                pr(f"  [{etiqueta}]")
                for m in ("M0a", "M5", "M5_Egexp") + (("K1",) if conj == "reserva_BiOX" else ()):
                    por = defaultdict(list)
                    for f in grupo:
                        por[f["estudio"]].append(f["U"] - f[m])
                    n, ne, (mae, ses), icm, ics = metricas(por)
                    pr(f"    {m:9s} n={n:2d} est={ne:2d}  MAE {mae:.2f} [{icm[0]:.2f}, {icm[1]:.2f}]  sesgo {ses:+.2f} [{ics[0]:+.2f}, {ics[1]:+.2f}]")
                for m in ("M5", "M5_Egexp"):
                    d, ic = dif_pareada(grupo, m, "M0a")
                    pr(f"    MAE({m}) − MAE(M0a) = {d:+.2f} [{ic[0]:+.2f}, {ic[1]:+.2f}]")
    # Sensibilidad TiO2 rutilo
    ti = [f for f in filas if f["formula"] == "TiO2" and f["M5_rutilo"] is not None]
    if ti:
        pr("\nTiO2 (n=%d): MAE M5 anatasa %.2f, rutilo %.2f; M5_Egexp anatasa %.2f, rutilo %.2f" % (
            len(ti), *[sum(abs(f["U"] - f[k]) for f in ti) / len(ti) for k in ("M5", "M5_rutilo", "M5_Egexp", "M5_Egexp_rutilo")]))
    # Eg predicho frente al experimental (registros con M5)
    eg = [(f["Eg"], f["Eg_M5"]) for f in filas if f["Eg_M5"] is not None]
    pr("\nEg M5 − Eg exp (todos los registros con M5, n=%d): media %+.2f eV, MAE %.2f eV" % (
        len(eg), sum(b - a for a, b in eg) / len(eg), sum(abs(b - a) for a, b in eg) / len(eg)))
    txt = "\n".join(out)
    print(txt)
    with open(os.path.join(OUTDIR, "salida_m5.txt"), "w") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
