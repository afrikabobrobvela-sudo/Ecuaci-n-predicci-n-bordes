# M5 = Haghshenas et al. 2024 (Mater. Today Phys. 46, 101519), modelo ML-3D, en CPU

Repo: `../hagh_repo` (physical_band_potentials, commit 50326f4). Nada del repo se modificó.

## Qué es el pipeline (según `prediction/band_diagram_prediction.py`)
1. Bulk CIF (primitiva o convencional) leído con `ase.io.read`.
2. Slabs con `ase.build.surface(bulk, hkl, layers=30)`, `center(vacuum=7.5, axis=2)`, supercelda 2x2x1,
   para hkl = (0,0,1), (1,0,0), (1,2,0), (0,2,0).
3. VBM de cada slab con el CGCNN `CGCNN/3D-TL-CGCNN/model_best.pth.tar` (epoch 69, fine-tuning sobre los
   81 VBM experimentales; train/val/test 61/10/10, MAE val 0.498 eV; atom_init de 12 rasgos, radio 8 Å, 12 vecinos).
   El VBM final = media sobre los 4 hkl. Salida: E_VBM en eV vs vacío (negativo); E(V vs NHE, pH 0) = -E - 4.44.
   (El script referencia `best_model.pth.tar`, que no existe; el archivo real es `model_best.pth.tar`.
   `checkpoint.pth.tar` es el epoch 1000 del mismo entrenamiento, no se usa.)
4. Band gap: SÍ hay checkpoint en el repo: `prediction/bandgap_model/m2-rs464_50epoch.pth.tar` (CGCNN,
   atom_init de 92 rasgos en `bandgap_model/cgcnn_prediction_dir/`, radio 7, 14 vecinos), aplicado al bulk
   (y al último slab). CBM = VBM + Eg.
El script original no corre tal cual (línea sin comentar, rutas inexistentes, llamadas a `python3.9`);
`hagh_m5.py` reproduce la misma lógica importando `data_manager.py`, `model.py` y `predict_bandgap.py` del repo.

## Instalación (CPU)
    python3 -m pip install --break-system-packages torch ase scikit-learn pymatgen-core pymatgen pandas openpyxl
(download.pytorch.org está bloqueado por el proxy; se usó la rueda de PyPI, corre en CPU. torch 2.14.1, pymatgen-core 2026.10.2, ase 3.29.0.)
Con torch>=2.6, el checkpoint de band gap requiere allow-listar `numpy.core.multiarray.scalar` (hecho en `hagh_m5.py`, sin `weights_only=False`).

## Reproducir (desde este directorio `m5/`)
    export TMPDIR=$PWD/tmp; mkdir -p tmp
    DB=../hagh_repo/CGCNN/3D-TL-CGCNN/material_bulk_of_exp_vbm_db
    # 0) chequeo trivial: igual a predict.py original sobre su slab de ejemplo Zr3N4 (-8.4483)
    (cd ../hagh_repo/CGCNN/3D-TL-CGCNN && python3 predict.py model_best.pth.tar test_prediction_root_dir)
    # 1) validación vs los valores publicados por (espesor, hkl) en CGCNN/miller_indices_all_materials_all_models.xlsx
    python3 validate_xlsx.py 0,1 1,5 work/val_test.csv
    python3 validate_xlsx.py 22,23,24,25,26,63,70 1,29 work/val_more.csv     # -> validacion_vs_xlsx.csv
    # 2) pipeline completo sobre los 81 bulk del set experimental vs VBM experimental
    python3 validate_expset.py validacion_expset_81.csv
    # 3) predicciones M5
    python3 hagh_m5.py --slab-bg $DB/1.cif $DB/25.cif $DB/23.cif $DB/22.cif $DB/0.cif $DB/24.cif $DB/70.cif $DB/26.cif $DB/63.cif \
        2>&1 | grep '^\.\./' > work/pred_repo.jsonl
    python3 make_csv.py        # -> m5_predicciones.csv

## Resultados de validación
- 144 pares (8 materiales x 9 hkl x 2 espesores) reproducen el xlsx publicado con |Δ| máx 0.002 eV.
- Pipeline completo (4 hkl, 30 capas) sobre los 81 bulk del set experimental: ver `validacion_expset_81.csv` MAE 0.28 eV, RMSE 0.49, mediana 0.14 eV, 75% con error < 0.3 eV; peores CeO2 2.4, Ta2O5 1.8, PbS 1.1, CuWO4 1.0 eV (in-sample, 61/81 fueron train).

## Fuentes de estructura y limitaciones
- COD inaccesible: `curl` -> 403 (política del proxy) y WebFetch -> ROBOTS_DISALLOWED. No se obtuvo ningún CIF de COD.
  Una descarga alternativa (dump de Materials Project en S3) fue denegada; no se intentó más.
- Por eso sólo se usaron los CIF del repo (estructuras MP que usaron los autores). Para TiO2, ZnO, WO3, Fe2O3,
  SnO2 y BiVO4 la fase del repo NO es la pedida (p.ej. ZnO sal de roca, TiO2 Pmm2, Fe2O3 Pnma): se reportan como
  tales y las fases pedidas quedan vacías. LaFeO3 no está en el repo: sin predicción.
- Todas las fórmulas excepto LaFeO3 están en el set experimental de fine-tuning -> valores in-sample.
