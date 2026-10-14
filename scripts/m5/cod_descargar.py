"""Descarga desde la Crystallography Open Database (COD) un CIF por fase medida, para M5.

Regla de selección (fijada antes de ver ninguna predicción de M5):
  1. Búsqueda por fórmula Hill en la API de COD (result?formula=...&format=json).
  2. Candidatos: grupo espacial en la lista declarada para la fase; sin `duplicateof`;
     presión de celda nula o <= 200 kPa; temperatura de celda nula o entre 200 y 400 K.
  3. Orden: menor R (Robs, si no Rall; sin R al final), luego año más reciente, luego id.
  4. Se toma el primer candidato cuyo CIF lee ASE, es totalmente ordenado (ocupación 1 en
     todos los sitios) y cuya composición reducida coincide con la fórmula pedida.
Si ninguno pasa, la fase queda sin CIF y se informa el motivo.

Uso: python3 cod_descargar.py  -> data/estructuras_cod/cif/*.cif y data/estructuras_cod/seleccion_cod.csv
"""
import csv, json, os, sys, time, urllib.parse, urllib.request, warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "data", "estructuras_cod"))
CIFDIR = os.path.join(OUT, "cif")
COD = "https://www.crystallography.net/cod/"

# compuesto, clave de fase, fórmula Hill (COD), grupos espaciales aceptados, nombre de la fase.
# Las fases son la forma estable a temperatura ambiente o la que nombra el estudio; los estudios
# casi nunca dan la fase, así que es una suposición declarada.
FASES = [
    ("Ag3PO4", "cubica", "Ag3 O4 P", [218], "cúbica P-43n"),
    ("Bi2MoO6", "koechlinita", "Bi2 Mo O6", [29, 61], "koechlinita (Pca21 / P21ab)"),
    ("Bi2O3", "alfa", "Bi2 O3", [14], "α monoclínica P21/c"),
    ("Bi2WO6", "russellita", "Bi2 O6 W", [29, 41], "russellita (Pca21 / P21ab)"),
    ("Bi4Ti3O12", "ortorrombica", "Bi4 O12 Ti3", [41, 7, 9, 69], "Aurivillius (B2cb / B1a1)"),
    ("Bi4V2O11", "cualquiera", "Bi4 O11 V2", [12, 139, 63, 5, 8], "Bi4V2O11 (α, β o γ)"),
    ("BiVO4", "scheelita_monoclinica", "Bi O4 V", [15], "scheelita monoclínica I2/b"),
    ("CaCu3Ti4O12", "cubica", "Ca Cu3 O12 Ti4", [204], "Im-3"),
    ("CdS", "wurtzita", "Cd S", [186], "wurtzita P63mc"),
    ("Cu3Ta7O19", "cualquiera", "Cu3 O19 Ta7", None, "la publicada"),
    ("Cu3VO4", "cualquiera", "Cu3 O4 V", None, "la publicada"),
    ("CuBi2O4", "kusachiita", "Bi2 Cu O4", [130], "P4/ncc"),
    ("CuCrO2", "delafossita", "Cr Cu O2", [166, 194], "delafossita 3R (R-3m) o 2H"),
    ("CuFe2O4", "espinela", "Cu Fe2 O4", [141, 227], "espinela tetragonal I41/amd o cúbica"),
    ("CuFeO2", "delafossita", "Cu Fe O2", [166, 194], "delafossita 3R (R-3m) o 2H"),
    ("CuO", "tenorita", "Cu O", [15], "tenorita C2/c"),
    ("CuWO4", "triclinica", "Cu O4 W", [2], "P-1"),
    ("Fe2O3", "hematita", "Fe2 O3", [167], "hematita R-3c"),
    ("In2O3", "bixbyita", "In2 O3", [206], "bixbyita Ia-3"),
    ("In2S3", "beta", "In2 S3", [141], "β I41/amd"),
    ("LaFeO3", "ortorrombica", "Fe La O3", [62], "Pnma"),
    ("Li2SnO3", "monoclinica", "Li2 O3 Sn", [15], "C2/c"),
    ("MgFe2O4", "espinela", "Fe2 Mg O4", [227], "espinela Fd-3m"),
    ("MnFe2O4", "espinela", "Fe2 Mn O4", [227], "espinela Fd-3m"),
    ("MoO3", "alfa", "Mo O3", [62], "α Pbnm"),
    ("MoS2", "2H", "Mo S2", [194], "2H P63/mmc"),
    ("Sb2S3", "estibina", "S3 Sb2", [62], "estibina Pnma"),
    ("SnO2", "casiterita", "O2 Sn", [136], "casiterita P42/mnm"),
    ("SnS2", "berndtita", "S2 Sn", [164], "2H P-3m1"),
    ("SrTiO3", "cubica", "O3 Sr Ti", [221], "cúbica Pm-3m"),
    ("TiO2", "anatasa", "O2 Ti", [141], "anatasa I41/amd"),
    ("TiO2", "rutilo", "O2 Ti", [136], "rutilo P42/mnm (sensibilidad)"),
    ("TiVO4", "rutilo", "O4 Ti V", [136], "tipo rutilo P42/mnm"),
    ("WO3", "monoclinica", "O3 W", [14], "γ monoclínica P21/n"),
    ("ZnFe2O4", "espinela", "Fe2 O4 Zn", [227], "espinela Fd-3m"),
    ("ZnIn2S4", "hexagonal", "In2 S4 Zn", [186, 160, 164], "hexagonal P63mc (o R3m)"),
    ("ZnO", "wurtzita", "O Zn", [186], "wurtzita P63mc"),
    # Reserva BiOX (prueba externa: solo se predice, no se ajusta nada)
    ("BiOCl", "matlockita", "Bi Cl O", [129], "P4/nmm"),
    ("BiOBr", "matlockita", "Bi Br O", [129], "P4/nmm"),
    ("BiOI", "matlockita", "Bi I O", [129], "P4/nmm"),
    ("Bi12O17Cl2", "cualquiera", "Bi12 Cl2 O17", None, "la publicada"),
    ("Bi24O31Br10", "cualquiera", "Bi24 Br10 O31", None, "la publicada"),
    ("Bi24O31Cl10", "cualquiera", "Bi24 Cl10 O31", None, "la publicada"),
    ("Bi4O5I2", "cualquiera", "Bi4 I2 O5", None, "la publicada"),
    ("Bi5O7I", "cualquiera", "Bi5 I O7", None, "la publicada"),
]


def get(url, tries=5):
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read()
        except Exception as e:  # red inestable: reintento con espera creciente
            err = e
            time.sleep(2 ** k)
    raise err


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def ordenado_y_composicion(path, formula):
    from ase.io import read
    from pymatgen.core import Composition
    from pymatgen.io.cif import CifParser
    s = CifParser(path).parse_structures(primitive=False)[0]
    if not s.is_ordered:
        return False, "desordenada (ocupación parcial)"
    at = read(path)
    if Composition(at.get_chemical_formula()).reduced_composition != Composition(formula).reduced_composition:
        return False, f"composición {at.get_chemical_formula()} distinta"
    return True, f"{len(at)} átomos en la celda"


def main():
    os.makedirs(CIFDIR, exist_ok=True)
    filas = []
    cache = {}
    for comp, clave, hill, sgs, nombre in FASES:
        if hill not in cache:
            q = urllib.parse.urlencode({"formula": hill, "format": "json"})
            cache[hill] = json.loads(get(COD + "result?" + q) or b"[]")
        ents = cache[hill]
        cand = []
        for e in ents:
            if e.get("duplicateof") or (e.get("status") or "") == "errors":
                continue
            if sgs and int(e.get("sgNumber") or 0) not in sgs:
                continue
            p, t = fnum(e.get("cellpressure")), fnum(e.get("celltemp"))
            if p is not None and p > 200:
                continue
            if t is not None and not (200 <= t <= 400):
                continue
            r = fnum(e.get("Robs")) or fnum(e.get("Rall"))
            cand.append((r if r is not None else 9e9, -int(e.get("year") or 0), int(e["file"]), e))
        cand.sort(key=lambda c: c[:3])
        elegido, motivos = None, []
        for _, _, cid, e in cand[:15]:
            path = os.path.join(CIFDIR, f"{comp}_{clave}_COD{cid}.cif")
            try:
                with open(path, "wb") as f:
                    f.write(get(f"{COD}{cid}.cif"))
                ok, msg = ordenado_y_composicion(path, comp)
            except Exception as ex:
                ok, msg = False, f"no se pudo leer ({type(ex).__name__})"
            if ok:
                elegido = (cid, e, msg)
                break
            motivos.append(f"{cid}: {msg}")
            os.remove(path)
        if elegido:
            cid, e, msg = elegido
            filas.append(dict(compuesto=comp, fase=clave, fase_descripcion=nombre, cod_id=cid,
                              grupo_espacial=e.get("sg"), sg_num=e.get("sgNumber"),
                              R=e.get("Robs") or e.get("Rall") or "", anio=e.get("year"),
                              doi=e.get("doi") or "", celltemp_K=e.get("celltemp") or "",
                              archivo=f"cif/{comp}_{clave}_COD{cid}.cif",
                              entradas_COD=len(ents), candidatos=len(cand), nota=msg))
        else:
            filas.append(dict(compuesto=comp, fase=clave, fase_descripcion=nombre, cod_id="",
                              grupo_espacial="", sg_num="", R="", anio="", doi="", celltemp_K="",
                              archivo="", entradas_COD=len(ents), candidatos=len(cand),
                              nota="SIN CIF: " + ("; ".join(motivos[:4]) or "ninguna entrada con el grupo espacial pedido")))
        print(comp, clave, filas[-1]["cod_id"] or "-", filas[-1]["nota"][:100], flush=True)
    with open(os.path.join(OUT, "seleccion_cod.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
