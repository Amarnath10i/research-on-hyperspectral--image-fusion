# Hyper-Spectral Fusion: Benchmarking HSI-MSI Fusion Methods

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org)
[![Kaggle](https://img.shields.io/badge/Kaggle-Notebooks-20BEFF.svg)](https://kaggle.com)

## Overview

This repository provides a comprehensive benchmarking study of **10 state-of-the-art Hyperspectral Image (HSI) – Multispectral Image (MSI) fusion methods** evaluated on the **CAVE** and **Harvard** datasets. It accompanies an IEEE 2026 literature survey on HSI fusion and super-resolution.

The project includes:
- **20 Kaggle notebooks** (10 methods × 2 datasets) for reproducible evaluation
- **Literature survey tools** that harvest, filter, and compile IEEE 2026 papers on HSI fusion
- **Quantitative metrics**: PSNR, SSIM, SAM, ERGAS

## Benchmarked Methods

| # | Method | Architecture | Paper |
|---|--------|-------------|-------|
| 1 | **AMGSGAN** | Adversarial / GAN | [PDF](papers/) |
| 2 | **DBIN** | Deep Blind Image Network (TensorFlow) | [PDF](papers/) |
| 3 | **DHIF-Net** | Deep Hyperspectral Image Fusion Network | [PDF](papers/) |
| 4 | **Fusformer** | Transformer-based Fusion | [PDF](papers/) |
| 5 | **IFCASformer** | Iterative Fusion Cascade Transformer (CASSI) | [PDF](papers/) |
| 6 | **LRU** | Low-Rank Unfolding | [PDF](papers/) |
| 7 | **MOGDCN** | Model-Guided Deep CNN | [PDF](papers/) |
| 8 | **PSRT** | Progressive Spatial-Spectral Reconstruction Transformer | [PDF](papers/) |
| 9 | **TSFN** | Two-Stream Fusion Network | [PDF](papers/) |
| 10 | **UTAL** | Unfolding Total variation and Low-rank | [PDF](papers/) |

## Results Summary

### CAVE Dataset (12 test scenes, 512×512, 31 bands)

| Method | PSNR ↑ | SSIM ↑ | SAM ↓ | ERGAS ↓ |
|--------|--------|--------|-------|---------|
| Fusformer | 50.20 | 0.9996 | 2.35 | 0.85 |
| DBIN | 47.14 | 0.9939 | 2.97 | 0.33 |
| TSFN | 46.40 | 0.9943 | 2.75 | 0.63 |
| IFCASformer | 35.98 | 0.9602 | 5.15 | 3.55 |
| *More results in notebooks* | | | | |

### Harvard Dataset (20 test scenes, 31 bands)

| Method | PSNR ↑ | SSIM ↑ | SAM ↓ | ERGAS ↓ |
|--------|--------|--------|-------|---------|
| Fusformer | 25.80 | 0.3059 | 58.89 | 302.39 |
| *More results in notebooks* | | | | |

> **Note**: The significant performance drop on Harvard demonstrates the **domain shift problem** — models trained on CAVE's synthetic scenes struggle with Harvard's real-world images. This motivates our research on robust fusion methods.

## Repository Structure

```
hyper-spectral-fusion/
├── README.md                          # This file
├── .gitignore
├── literature_survey/                 # Literature survey pipeline
│   ├── lit_search.py                  # Crossref API harvest
│   ├── check_oa.py                    # Unpaywall open-access check
│   ├── lit_multimodal.py              # Track 2: HSI+LiDAR papers
│   ├── build_lit_excel.py             # Main Excel workbook builder
│   ├── create_excel.py                # Simple Excel creator
│   ├── create_excel_fusion.py         # Fusion-only Excel creator
│   ├── lit_raw.json                   # Raw Crossref results
│   ├── lit_candidates.json            # Filtered candidates with OA status
│   └── lit_multimodal.json            # Multimodal paper candidates
├── notebooks/
│   ├── cave/                          # CAVE dataset notebooks
│   │   ├── amgsgan-test-cave.ipynb
│   │   ├── dbin-test-cave.ipynb
│   │   ├── dhifnet-test-cave.ipynb
│   │   ├── fusformer-test-cave.ipynb
│   │   ├── ifcasformer-test-cave.ipynb
│   │   ├── lru-test-cave.ipynb
│   │   ├── mogdcn-test-cave.ipynb
│   │   ├── psrt-test-cave.ipynb
│   │   ├── tsfn-test-cave.ipynb
│   │   └── utal-test-cave.ipynb
│   └── harvard/                       # Harvard dataset notebooks
│       ├── amgsgan-test-harvard.ipynb
│       ├── dbin-test-harvard.ipynb
│       ├── dhifnet-test-harvard.ipynb
│       ├── fusformer-test-harvard.ipynb
│       ├── ifcasformer-test-harvard.ipynb
│       ├── lru-test-harvard.ipynb
│       ├── mogdcn-test-harvard.ipynb
│       ├── psrt-test-harvard.ipynb
│       ├── tsfn-test-harvard.ipynb
│       └── utal-test-harvard.ipynb
└── papers/                            # Reference papers (not tracked)
```

## Datasets

| Dataset | Spatial Size | Spectral Bands | Train/Test Split |
|---------|-------------|----------------|-----------------|
| **CAVE** | 512 × 512 | 31 (400–700 nm) | 20 / 12 scenes |
| **Harvard** | ~1040 × 1392 | 31 (420–720 nm) | 30 / 20 scenes |

Datasets are hosted on Kaggle:
- [CAVE Dataset](https://kaggle.com/datasets/nikeshreddypatlolla/cave-dataset-2)
- [Harvard Dataset](https://kaggle.com/datasets/nikeshreddypatlolla/harvard-hsi-2)

## Evaluation Metrics

- **PSNR** (Peak Signal-to-Noise Ratio) — higher is better
- **SSIM** (Structural Similarity Index) — higher is better  
- **SAM** (Spectral Angle Mapper, in degrees) — lower is better
- **ERGAS** (Erreur Relative Globale Adimensionnelle de Synthèse) — lower is better

## Running Notebooks

All notebooks are designed to run on **Kaggle** with GPU (T4) acceleration:

1. Upload the notebook to Kaggle
2. Attach the required dataset and model checkpoint (see notebook metadata)
3. Enable GPU accelerator (NVIDIA Tesla T4)
4. Enable Internet access
5. Run all cells

## Literature Survey

The survey pipeline discovers IEEE 2026 papers on HSI fusion:

```bash
# 1. Harvest papers from Crossref
python literature_survey/lit_search.py

# 2. Check open-access status via Unpaywall
python literature_survey/check_oa.py

# 3. Harvest multimodal (HSI+LiDAR) papers
python literature_survey/lit_multimodal.py

# 4. Build the Excel workbook
python literature_survey/build_lit_excel.py
```

### Requirements
```
openpyxl
```

## Related Work

This benchmarking study references the [hif-benchmarking](https://github.com/Nikesh0907/hif-benchmarking) repository for method implementations and pretrained weights.

## Citation

If you use this benchmarking suite, please cite:

```bibtex
@misc{hyper-spectral-fusion-2026,
  title={Hyper-Spectral Fusion: Benchmarking HSI-MSI Fusion Methods on CAVE and Harvard},
  year={2026},
  url={https://github.com/YOUR_USERNAME/hyper-spectral-fusion}
}
```

## License

This project is for academic research purposes. Individual method implementations retain their original licenses.
