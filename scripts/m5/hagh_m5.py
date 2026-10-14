"""CPU wrapper around the published Haghshenas et al. 2024 (Mater. Today Phys. 46, 101519)
ML-3D band-potential pipeline (repo: physical_band_potentials).

It reproduces prediction/band_diagram_prediction.py without the python3.9 subprocess calls:
  * bulk ASE structure -> ase.build.surface(bulk, hkl, layers=N) -> center(vacuum=15/2, axis=2)
    -> 2x2x1 supercell  (my_slab_generator, verbatim logic)
  * VBM: CGCNN/3D-TL-CGCNN/model_best.pth.tar with the repo's data_manager.CIFData
    (radius 8, 12 nbrs, 12-feature atom_init.json), structure written to CIF via pymatgen
    exactly as vb_model.predict_vb does. Output = E_VBM in eV vs vacuum (negative number).
  * Band gap: prediction/predict_bandgap.BG with bandgap_model/m2-rs464_50epoch.pth.tar
    (radius 7, 14 nbrs, 92-feature atom_init.json), applied to bulk (and optionally slab).
Model code is imported from the repo unmodified.
"""
import os, sys, csv, json, shutil, tempfile, argparse, warnings
import numpy as np
import torch

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "hagh_repo"))
VB_DIR = os.path.join(REPO, "CGCNN", "3D-TL-CGCNN")
PRED_DIR = os.path.join(REPO, "prediction")
VB_MODEL = os.path.join(VB_DIR, "model_best.pth.tar")
VB_ATOM_INIT = os.path.join(VB_DIR, "test_prediction_root_dir", "atom_init.json")
BG_MODEL = os.path.join(PRED_DIR, "bandgap_model", "m2-rs464_50epoch.pth.tar")
BG_PRED_DIR = os.path.join(PRED_DIR, "bandgap_model", "cgcnn_prediction_dir")

# import the repo's VB modules (3D-TL-CGCNN/data_manager.py, model.py)
sys.path.insert(0, VB_DIR)
from data_manager import CIFData  # noqa: E402
from model import CrystalGraphConvNet  # noqa: E402
sys.path.pop(0)
for m in ("data_manager", "model"):
    sys.modules.pop(m, None)

_VB = {}


def _load_vb(model_path=VB_MODEL):
    if model_path in _VB:
        return _VB[model_path]
    ck = torch.load(model_path, map_location="cpu", weights_only=False)
    a = ck["args"]
    _VB[model_path] = (ck, a)
    return _VB[model_path]


def predict_vbm(structures, model_path=VB_MODEL):
    """structures: list of pymatgen Structures. Returns list of E_VBM (eV vs vacuum)."""
    ck, a = _load_vb(model_path)
    tmp = tempfile.mkdtemp(prefix="m5vb_")
    try:
        shutil.copy(VB_ATOM_INIT, os.path.join(tmp, "atom_init.json"))
        with open(os.path.join(tmp, "id_prop.csv"), "w") as f:
            w = csv.writer(f)
            for i, s in enumerate(structures):
                s.to(filename=os.path.join(tmp, f"{i}.cif"))
                w.writerow((i, 0))
        ds = CIFData(tmp)
        model = None
        out = {}
        for k in range(len(ds)):
            (af, nf, ni), _, cid = ds[k]
            if model is None:
                model = CrystalGraphConvNet(af.shape[-1], nf.shape[-1],
                                            atom_fea_len=a["atom_fea_len"], n_conv=a["n_conv"],
                                            h_fea_len=a["h_fea_len"], n_h=a["n_h"],
                                            classification=False)
                model.load_state_dict(ck["state_dict"])
                model.eval()
            with torch.no_grad():
                y = model(af, nf, ni, [torch.arange(af.shape[0])])
            out[int(cid)] = float(y.item() * ck["normalizer"]["std"] + ck["normalizer"]["mean"])
        return [out[i] for i in range(len(structures))]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def predict_bg(structure):
    """Band gap (eV) from the repo's bandgap CGCNN (predict_bandgap.BG)."""
    sys.path.insert(0, PRED_DIR)
    import predict_bandgap
    sys.path.pop(0)
    # The BG checkpoint stores best_mae_error as a numpy scalar; allow-list only the numpy
    # types needed so torch>=2.6 can keep weights_only=True (no arbitrary unpickling).
    import numpy._core.multiarray as _ma
    safe = [(_ma.scalar, "numpy.core.multiarray.scalar"), np.dtype] + [type(np.dtype(t)) for t in ("float64", "float32", "int64")]
    with torch.serialization.safe_globals(safe):
        _, pred = predict_bandgap.BG(structure, model=BG_MODEL, predict_dir=BG_PRED_DIR)
    return float(pred[0])


def my_slab_generator(ase_structure, miller_index, num_layers, vacuum=15, slab_dim=(2, 2, 1)):
    """Verbatim logic of prediction/band_diagram_prediction.py::my_slab_generator."""
    from ase.build import surface, make_supercell
    slab = surface(lattice=ase_structure, indices=miller_index, layers=num_layers)
    slab.center(vacuum=vacuum / 2, axis=2)
    P = np.array([[slab_dim[0], 0, 0], [0, slab_dim[1], 0], [0, 0, slab_dim[2]]])
    return make_supercell(slab, P)


DEFAULT_HKL = [(0, 0, 1), (1, 0, 0), (1, 2, 0), (0, 2, 0)]  # list_of_miller_indexes in band_diagram_prediction.py


def band_diagram(cif_path, hkls=DEFAULT_HKL, num_layers=30, vacuum=15, slab_dim=(2, 2, 1),
                 slab_bg=False):
    """Replicates predict_band_diagram(): mean VBM over slabs, bulk BG (and BG of last slab)."""
    from ase import io as ase_io
    from pymatgen.io.ase import AseAtomsAdaptor
    bulk = ase_io.read(cif_path)
    slabs, ok = [], []
    for hkl in hkls:
        try:
            s = my_slab_generator(bulk, hkl, num_layers, vacuum, slab_dim)
            slabs.append(AseAtomsAdaptor.get_structure(s))
            ok.append(hkl)
        except Exception as e:  # same behaviour as original: skip failing index
            print("slab error", hkl, e)
    vbms = predict_vbm(slabs) if slabs else []
    res = {"hkl": [str(h) for h in ok], "vbm_per_hkl": vbms,
           "nat_per_slab": [len(s) for s in slabs],
           "vbm_mean": float(np.mean(vbms)) if vbms else float("nan"),
           "bg_bulk": predict_bg(AseAtomsAdaptor.get_structure(bulk))}
    if slab_bg and slabs:
        res["bg_slab_last"] = predict_bg(slabs[-1])
    return res


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cif", nargs="+")
    p.add_argument("--layers", type=int, default=30)
    p.add_argument("--slab-bg", action="store_true")
    a = p.parse_args()
    for c in a.cif:
        r = band_diagram(c, num_layers=a.layers, slab_bg=a.slab_bg)
        print(c, json.dumps(r))
