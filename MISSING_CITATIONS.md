# Missing Citations Analysis for `main_plos.tex`

This document outlines software libraries, data standards, and algorithms mentioned in the `main_plos.tex` manuscript that currently lack formal citations or references. In scientific computing literature (especially for journals like *Computer Methods and Programs in Biomedicine*), citing the core software stack and data standards is crucial for reproducibility and proper attribution.

## 1. Julia Ecosystem Packages

The manuscript relies heavily on the Julia ecosystem to make its arguments about high performance and SciML. While the language itself is cited (`\cite{BezansonChen2018}`), several critical foundational packages are mentioned as core components of the `MedImages.jl` architecture but are un-cited:

*   **`KernelAbstractions.jl`**: Mentioned frequently as the basis for GPU acceleration and the fused affine kernels. Needs a citation (e.g., pointing to the JuliaGPU organization or specific papers by its authors).
*   **`Enzyme.jl`**: Mentioned as a compiler-level AD framework. Needs a citation (typically the NeurIPS paper by William Moses et al.).
*   **`Zygote.jl`**: Cited once (`\cite{Fischer_2019}`) in the Introduction, but often mentioned alongside `Enzyme.jl` later without citation. Ensure the primary citation is established where it first appears in the Methods.
*   **`DifferentialEquations.jl` / `SciMLSensitivity.jl`**: Mentioned as key components of the SciML ecosystem enabling Universal Differential Equations. These should point to the work by Christopher Rackauckas et al.
*   **`Lux.jl`**: Mentioned as the neural network backend used in the Differentiable Geometric CNN and MultiScaleCNN. While it was cited as `\cite{pal2023lux}` in previous versions, check if this citation is consistently applied where `Lux.jl` is introduced.
*   **`ITKIOWrapper`**: Mentioned in the "Functionalities and I/O Robustness" section. Should cite the ITK community or the specific wrapper repository.

## 2. Python Deep Learning Frameworks

The manuscript contrasts Julia's ecosystem with Python's fragmented "walled gardens." The following frameworks are explicitly named but not cited:

*   **`PyTorch`**: Mentioned as the backend for MONAI and as a general framework. Should cite the original NeurIPS paper (Paszke et al., 2019).
*   **`TensorFlow`**: Mentioned in the Discussion regarding fragmented SciML landscapes. Should cite the original Abadi et al., 2016 paper.
*   **`JAX`**: Mentioned alongside PyTorch and TensorFlow. Should cite Bradbury et al., 2018.

## 3. Data Standards and Formats

Medical imaging heavily relies on established formats. The manuscript mentions these without citing their underlying standards documents or foundational papers:

*   **`BIDS` (Brain Imaging Data Structure)**: The manuscript states MedImages.jl implements a "BIDS-inspired metadata paradigm." BIDS must be cited (e.g., Gorgolewski et al., 2016, *Scientific Data*).
*   **`HDF5`**: Mentioned as the storage backend providing a 7.2x speedup over MONAI caching. Should cite the HDF Group.
*   **`DICOM`**: Mentioned repeatedly. Should cite the NEMA standard.
*   **`NIfTI`**: Mentioned alongside DICOM. Should cite the Neuroimaging Informatics Technology Initiative.

## 4. Algorithms and Clinical Concepts

*   **Euler Integration**: Mentioned in the UDE section ("5-step Euler integration"). While basic, in a medical informatics paper, sometimes citing the numerical method context within SciML is helpful.
*   **MIRD (Medical Internal Radiation Dose)**: Mentioned in the historical context of dosimetry. Should cite the foundational MIRD pamphlets (e.g., Loevinger and Berman).
*   **Targeted Radionuclide Therapy (TRT) / Transarterial Radioembolization (TARE)**: Mentioned as clinical imperatives. Citing recent clinical guidelines or foundational papers on volumetric dosimetry (D95/D70 metrics) would strengthen the clinical justification.

## Action Plan
To resolve these omissions, the corresponding BibTeX entries should be added to `bibl.bib`, and `\cite{...}` commands should be strategically placed in the manuscript at the first mention of each technology or standard.