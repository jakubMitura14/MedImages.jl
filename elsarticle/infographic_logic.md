# MedImages.jl Infographic Design Logic

This document provides a precise, step-by-step blueprint for visualizing the four core challenges addressed by `MedImages.jl` in the `old_plos.tex` manuscript. Each challenge is broken down into its core conceptual points, followed by exact instructions on how those points should be structured, connected, and represented pictographically.

---

## Challenge 1: The Volume Bottleneck (Scaling to 100 Cases)

### Core Points
1. High-throughput preprocessing of biobank-scale multimodal datasets (e.g., PET and CT) is a major bottleneck.
2. Traditional caching (e.g., MONAI PersistentDataset) relies on heavy Python Pickle/Pt serialization.
3. MedImages.jl uses HDF5 and Fused Affine GPU kernels.
4. Result: 7.2× faster turnaround time (~90 ms vs ~650 ms per subject).

### Pictographic Representation & Layout
*   **Bounding Box (Left - Traditional Pipeline):**
    *   *Iconography:* A slow-moving funnel or a series of stacked, disconnected disk drives representing `Pickle/Pt Caching`.
    *   *Text:* "MONAI PersistentDataset (~650 ms)"
*   **Bounding Box (Right - MedImages Pipeline):**
    *   *Iconography:* A sleek, single solid state drive (HDF5) connected directly to a GPU microchip icon.
    *   *Text:* "MedImages.jl HDF5 + Native GPU (~90 ms)"
*   **Connections (Lines & Arrows):**
    *   Both boxes output to a central target node below them.
    *   The line from the Left box should be dashed, red, and thick (representing friction).
    *   The line from the Right box should be solid, green, and smooth (representing speed).
    *   Both lines converge on a large, central "Results Node" shaped like a biobank vault, with bold text reading "**7.2× Total Turnaround Speedup**".

---

## Challenge 2: The Two-Language Barrier (Execution Speed)

### Core Points
1. The classic "Two-Language Problem": Prototyping in Python requires wrapping opaque, compiled C++ binaries (e.g., SimpleITK).
2. Opaque C++ binaries limit GPU acceleration and deep framework inspection.
3. MedImages.jl is pure Julia, compiled directly via LLVM JIT, unlocking native GPU acceleration (KernelAbstractions.jl).
4. Result: Up to 135× speedup over CPU baselines (e.g., Fused Affine).

### Pictographic Representation & Layout
*   **Vertical Split Layout (Top vs. Bottom):**
*   **Top Region (Python Ecosystem):**
    *   *Iconography:* Two distinctly colored interlocking puzzle pieces. One piece labeled "Python (High-Level)", the other labeled "C++ (SimpleITK)".
    *   *Connection:* A literal "brick wall" graphic or a thick black vertical line between the Python script icon and a GPU icon, symbolizing the barrier to hardware acceleration.
*   **Bottom Region (Julia Ecosystem):**
    *   *Iconography:* A single, unified, glowing crystal or glowing gear labeled "Pure Julia / LLVM JIT".
    *   *Connection:* Smooth, glowing gradient arrows flowing directly from the unified gear into a GPU chip icon.
*   **Annotations:**
    *   Place a speed dial/speedometer icon next to the GPU. The needle is pinned to the maximum redline, accompanied by the text: "**135× Fused Affine Acceleration**" and "**115× Resampling Acceleration**".

---

## Challenge 3: Differentiability (Physics-in-the-Loop UDEs)

### Core Points
1. Pure deep learning ("black boxes") fails to model quantitative dosimetry accurately ($r \approx 0.60$).
2. Traditional analytical clinical models (VSV) assume homogeneous environments, losing 5-10% variance at tissue interfaces.
3. Solution: A 4-State Universal Differential Equation (UDE) combining Mechanistic Knowns with Learned Uncertainties (Neural Residuals).
4. Result: Monte Carlo-level accuracy ($r=0.957$) natively integrated with Zygote.jl/Enzyme.jl.

### Pictographic Representation & Layout
*   **Left Input Node (The Knowns):**
    *   *Shape:* A rigid, solid blue square.
    *   *Iconography:* Mathematical symbols ($S_{homo}$, $\lambda_{phys}$, $CF$, $\rho$).
    *   *Label:* "Mechanistic Physics"
*   **Right Input Node (The Unknowns):**
    *   *Shape:* A flexible, dashed orange cloud or brain icon.
    *   *Iconography:* A neural network perceptron diagram ($\mathcal{N}_\theta$).
    *   *Label:* "Neural Residual Corrector"
*   **Connections (Merging Arrows):**
    *   A solid blue arrow from the Left Node and a dashed orange arrow from the Right Node converge into a central circular hub.
*   **Central Hub (The UDE Integrator):**
    *   *Shape:* A large, spinning gear surrounding a stylized integral symbol ($\int$).
    *   *Label:* "Julia UDE Integrator (SciML)"
*   **Output Node:**
    *   An arrow flows outward from the Central Hub to a final target node shaped like a glowing patient torso (Voxel Dose Map).
    *   *Annotation attached to output:* A green checkmark badge reading "**Pearson r = 0.957 (Monte Carlo Fidelity)**".

---

## Challenge 4: Metadata Management (Theranostic Batched Processing)

### Core Points
1. Medical imaging pipelines easily lose spatial metadata (origin, spacing, direction) when converting formats (e.g., SimpleITK to NumPy).
2. Theranostic workflows require aligning highly heterogeneous, multi-modal data (SPECT AC, SPECT NAC, Dosemap, CT).
3. `BatchedMedImage` explicitly binds metadata to 4D data via Julia's type system.
4. Result: Flawless quantitative alignment (SUV deviated < 1.5% after compound affine transformation).

### Pictographic Representation & Layout
*   **Top Bounding Box (The BIDS-Inspired Tensor):**
    *   *Shape:* A large, transparent 3D cube.
    *   *Internal Structure:* Inside the large cube, stack four distinct 2D slice images vertically.
    *   *Labels for slices:* "CT Anatomy", "177Lu Dosemap", "177Lu NAC", "177Lu AC".
*   **Connecting Lines (Metadata Coupling):**
    *   Draw rigid, solid brackets (like a curly brace `]`) tying the entire stack of slices together.
    *   Attached to the bracket, place a "Data Tag" icon. Inside the tag, list the protected physical properties: "Origin (x,y,z)", "Spacing (x,y,z)", "Direction Matrix".
*   **Bottom Bounding Box (The Compound Transform):**
    *   Draw a thick, downward-pointing arrow from the Top Box, wrapped in a circular rotation vector (symbolizing compound 45° rotation and grid resampling).
    *   At the bottom, redraw the same stack of 4 slices, but rotated 45 degrees.
*   **Annotations:**
    *   Place a "magnifying glass" over the bottom stack showing a graph of Standardized Uptake Values (SUV).
    *   *Text Badge:* "Clinical Metadata Perfectly Synchronized: SUV Consistency < 1.5% Deviation".