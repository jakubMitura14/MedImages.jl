# MedImages.jl Infographic Design Logic

This document provides a precise, step-by-step blueprint for visualizing the four core challenges addressed by `MedImages.jl` in the `old_plos.tex` manuscript, as well as a dedicated section for the Quantitative UDE Dosimetry Experiment. Each section strictly follows a four-part narrative flow.

---

## 1. Challenge 1: The Volume Bottleneck (Biobank-Scale Processing)

### Core Narrative Flow
1. **Challenge (Issue):** High-throughput preprocessing of biobank-scale multimodal datasets (thousands of 3D/4D studies) is a major hardware and I/O bottleneck in modern clinical research.
2. **Knowledge Gap (Other Solutions):** Traditional caching solutions in Python, such as MONAI's `PersistentDataset` or TorchIO, rely on heavy Pickle/Pt dict-based serialization. This creates immense memory buildup and I/O friction, severely bottlenecking large-scale pipelines and preventing true biobank-scale deployment.
3. **How Addressed:** `MedImages.jl` solves this by implementing zero-serialization HDF5 persistence combined with Fused Affine GPU kernels.
4. **How Experiments Prove the Point:** Our 100-subject benchmark experiment proved a **7.2× faster turnaround time** (~90 ms vs ~650 ms per subject), enabling true biobank-scale data ingestion in minutes rather than days without cache penalties.

### Pictographic Representation & Layout
*   **Bounding Box (Left - Traditional Pipeline):**
    *   *Iconography:* A slow-moving funnel or a series of stacked, disconnected disk drives representing `Pickle/Pt Caching`.
    *   *Context Addition:* Draw a "memory leak" or "bottleneck" warning sign attached to highlight TorchIO's memory buildup issues and MONAI's Python caching limits.
    *   *Text:* "MONAI PersistentDataset (~650 ms)"
*   **Bounding Box (Right - MedImages Pipeline):**
    *   *Iconography:* A sleek, single solid state drive (HDF5) connected directly to a GPU microchip icon.
    *   *Context Addition:* Attach a "Zero-Serialization" badge.
    *   *Text:* "MedImages.jl HDF5 + Native GPU (~90 ms)"
*   **Connections (Lines & Arrows):**
    *   Both boxes output to a central target node below them.
    *   The line from the Left box should be dashed, red, and thick (representing I/O friction).
    *   The line from the Right box should be solid, green, and direct (representing massive I/O throughput).
    *   Both lines converge on a large, central "Results Node" shaped like a massive biobank vault containing thousands of datasets, with bold text reading "**7.2× Speedup, Unlocking Thousands of Studies**".
*   **Clinical Integration (Real Scanner Data):**
    *   Replace the central "Results Node" vault icon with an actual Maximum Intensity Projection (MIP) rendering of a whole-body [177Lu]Lu-PSMA SPECT/CT study sourced directly from the clinical biobank, visually anchoring the scale of the dataset to real patient anatomy.

---

## 2. Challenge 2: The Two-Language Barrier (Execution Speed)

### Core Narrative Flow
1. **Challenge (Issue):** The classic "Two-Language Problem" forces medical researchers to prototype in high-level languages while relying on opaque, pre-compiled low-level binaries for performance.
2. **Knowledge Gap (Other Solutions):** Python ecosystems rely heavily on wrapping C++ libraries (e.g., SimpleITK). These opaque binaries act as a "brick wall," fundamentally limiting native GPU acceleration, creating CPU bottlenecks for spatial operations, and preventing deep framework inspection or custom hardware compilation.
3. **How Addressed:** `MedImages.jl` is written in pure Julia, compiled directly via LLVM JIT. This unified approach inherently unlocks native hardware acceleration via `KernelAbstractions.jl`.
4. **How Experiments Prove the Point:** Our experiments on target hardware (NVIDIA RTX 3090, Intel Core Ultra 9) demonstrate massive performance gains: an **135× speedup** for Fused Affine transformations (0.83 ms vs 6.69 ms on CPU) and a **115× speedup** for spatial resampling compared to standard Python/C++ baselines.

### Pictographic Representation & Layout
*   **Vertical Split Layout (Top vs. Bottom):**
*   **Top Region (Python Ecosystem):**
    *   *Iconography:* Two distinctly colored interlocking puzzle pieces. One piece labeled "Python (High-Level)", the other labeled "C++ (SimpleITK)".
    *   *Connection:* A literal "brick wall" graphic or a thick black vertical line between the Python script icon and a GPU icon, symbolizing the barrier to hardware acceleration. Next to the brick wall, place a "SimpleITK (CPU)" box with a slow progress bar (e.g., 6.69 ms for affine transform).
*   **Bottom Region (Julia Ecosystem):**
    *   *Iconography:* A single, unified, glowing crystal or glowing gear labeled "Pure Julia / LLVM JIT".
    *   *Connection:* Direct, continuous gradient arrows flowing from the unified gear into a GPU chip icon. Place a "MedImages GPU" box with a nearly instantaneous progress bar (e.g., 0.83 ms).
*   **Annotations:**
    *   Place a speed dial/speedometer icon next to the GPU. The needle is pinned to the maximum redline, accompanied by the text: "**135× Fused Affine Acceleration**" and "**115× Resampling Acceleration**".
*   **Clinical Integration (Real Scanner Data):**
    *   Instead of standard progress bars, use a sequence of real CT cross-sections undergoing rapid spatial resampling (e.g., scaling from $512\times512$ to $128\times128$). The CPU side shows a single frame rendering slowly, while the MedImages GPU side displays a rapid cascade of successfully transformed clinical overlays.

---

## 3. Challenge 3: Differentiability (Physics-in-the-Loop UDEs)

### Core Narrative Flow
1. **Challenge (Issue):** Accurately modeling physical phenomena (like quantitative voxel-level dosimetry) requires integrating known scientific equations directly into the training loop of machine learning architectures.
2. **Knowledge Gap (Other Solutions):** Pure deep learning ("black box" CNNs/U-Nets) fails to respect physical constraints. Conversely, traditional analytical clinical models (like VSV) assume homogeneous environments and ignore critical tissue heterogeneity. Furthermore, Python's fragmented "Walled Gardens" (PyTorch/JAX) struggle to differentiate through arbitrary mechanistic simulators.
3. **How Addressed:** We implement a 4-State Universal Differential Equation (UDE) in Julia, natively integrating Mechanistic Knowns with Learned Uncertainties (Neural Residuals) using `Zygote.jl`.
4. **How Experiments Prove the Point:** Our experiments proved this architecture connects Julia's ecosystem (`DifferentialEquations.jl`, `Lux.jl`, `MedImages.jl`) to achieve Monte Carlo-level accuracy (**Pearson $r=0.957$**) while avoiding the "Walled Garden" problem.

### Pictographic Representation & Layout
*   **Left Input Node (The Knowns):**
    *   *Shape:* A rigid, solid blue square.
    *   *Iconography:* Mathematical symbols ($S_{homo}$, $\lambda_{phys}$, $CF$, $\rho$).
    *   *Label:* "Mechanistic Physics"
*   **Right Input Node (The Unknowns):**
    *   *Shape:* A flexible, dashed orange cloud or brain icon.
    *   *Iconography:* A neural network perceptron diagram ($\mathcal{N}_\theta$).
    *   *Context Addition:* Place icons for PyTorch and JAX inside a locked cage ("Walled Garden") connected by broken arrows to illustrate standard framework limitations.
    *   *Label:* "Neural Residual Corrector"
*   **Connections (Merging Arrows):**
    *   A solid blue arrow from the Left Node and a dashed orange arrow from the Right Node converge into a central circular hub.
*   **Central Hub (The UDE Integrator):**
    *   *Shape:* A large, spinning gear surrounding a stylized integral symbol ($\int$). Show continuous circular arrows representing "Multiple Dispatch / Expression Problem Solved."
    *   *Label:* "Julia UDE Integrator (SciML)"
*   **Output Node:**
    *   An arrow flows outward from the Central Hub to a final target node shaped like a glowing patient torso (Voxel Dose Map).
    *   *Annotation attached to output:* A green checkmark badge reading "**Pearson r = 0.957 (Monte Carlo Fidelity)**".
*   **Clinical Integration (Real Scanner Data):**
    *   The "Voxel Dose Map" output should be an authentic, pseudo-colored dose map overlay on an axial CT slice, generated directly from the scanner's DICOM data via the UDE pipeline, explicitly demonstrating real-world tissue heterogeneity.

---

## 4. Challenge 4: Metadata Management (Theranostic Batched Processing)

### Core Narrative Flow
1. **Challenge (Issue):** Complex theranostic workflows require perfectly aligning highly heterogeneous, multi-modal spatial data (e.g., mapping SPECT AC, SPECT NAC, and Dosemaps to a single CT anatomical grid).
2. **Knowledge Gap (Other Solutions):** In standard Python pipelines, spatial metadata (origin, spacing, direction) is easily decoupled and lost the moment a medical image (e.g., SimpleITK) is converted into a raw NumPy tensor for deep learning. This "Metadata Drift" leads to catastrophic spatial misalignment and quantitative errors downstream.
3. **How Addressed:** `MedImages.jl` solves this via the `BatchedMedImage` structure, which explicitly binds physical metadata to the 4D voxel tensor using Julia's rigorous type system.
4. **How Experiments Prove the Point:** Our compound affine transformation experiments demonstrated flawless quantitative alignment, ensuring Standardized Uptake Value (SUV) consistency with **< 1.5% deviation** across massive multimodal batches.

### Pictographic Representation & Layout
*   **Top Bounding Box (The BIDS-Inspired Tensor):**
    *   *Shape:* A large, transparent 3D cube.
    *   *Internal Structure:* Inside the large cube, stack four distinct 2D slice images vertically.
    *   *Labels for slices:* "CT Anatomy", "177Lu Dosemap", "177Lu NAC", "177Lu AC".
*   **Connecting Lines (Metadata Coupling):**
    *   Draw rigid, solid brackets (like a curly brace `]`) tying the entire stack of slices together.
    *   Attached to the bracket, place a "Data Tag" icon locked inside a shield (Julia's Type System). Inside the tag, list the protected physical properties: "Origin (x,y,z)", "Spacing (x,y,z)", "Direction Matrix".
    *   *Context Addition:* Show a `sitk.GetArrayFromImage()` operation acting like a pair of scissors, slicing off a "Spacing/Origin" tag and dropping it into a trash bin (NumPy Array conversion) to contrast standard methods.
*   **Bottom Bounding Box (The Compound Transform):**
    *   Draw a thick, downward-pointing arrow from the Top Box, wrapped in a circular rotation vector (symbolizing compound 45° rotation and grid resampling).
    *   At the bottom, redraw the same stack of 4 slices, but rotated 45 degrees.
*   **Annotations:**
    *   Place a "magnifying glass" over the bottom stack showing a graph of Standardized Uptake Values (SUV).
    *   *Text Badge:* "Clinical Metadata Perfectly Synchronized: SUV Consistency < 1.5% Deviation".
*   **Clinical Integration (Real Scanner Data):**
    *   The 2D slice stack must use genuine, coregistered clinical data. Specifically, show real clinical NIfTI slices corresponding to the patient's CT Anatomy, 177Lu-PSMA Dosemap, and SPECT (AC/NAC) arrays, visualizing the exact coordinate matrices being protected.

---

## 5. Quantitative UDE Dosimetry Experiment

This section strictly details the experimental methodology and superior performance of the 4-State UDE model for 177Lu-PSMA dosimetry.

### Core Narrative Flow
1. **Challenge (Issue):** The clinical objective is to accurately map functional SPECT and anatomical CT data to high-fidelity Monte Carlo (MC) ground truth dosimetry.
2. **Knowledge Gap (Other Solutions):**
    * *Clinical Baseline:* Voxel S-Value (VSV) convolution over Time-Integrated Activity (TIA) using Python (`Evaluate-Proj` / `pytheranostics`) ignores tissue heterogeneity.
    * *Deep Learning Baseline:* Pure 3D CNN / U-Net architectures ("Black Boxes" like DblurDoseNet) struggle with physical constraints.
3. **How Addressed:** The SciML/Julia "No-Approx UDE" model cleanly isolates known physics (primary scatter) from a neural residual.
4. **How Experiments Prove the Point:** Experiments show the clinical VSV baseline achieves a Pearson correlation of $r=0.912$, and pure deep learning achieves $r \approx 0.557$. In stark contrast, the SciML UDE achieves state-of-the-art **$r=0.957$** while maintaining a **10× speed advantage** over traditional Python analytical frameworks.

### Pictographic Representation & Layout
*   **Top Header:** "High-Fidelity 177Lu-PSMA Dosimetry Comparison"
*   **Three Vertical Lanes (The Competitors):**
    *   **Lane 1 (Left - Pure Deep Learning):**
        *   *Icon:* A black box labeled "3D U-Net / DblurDoseNet"
        *   *Flow:* Raw SPECT/CT data points in. A non-linear, poorly constrained arrow points out.
        *   *Output:* A low-fidelity dose map exhibiting widespread unconstrained spatial artifacts.
        *   *Metrics Badge:* Red color, "Pearson r = 0.557 (Fails physical constraints)".
    *   **Lane 2 (Center - Clinical Analytical / Python):**
        *   *Icon:* A calculator or standard rigid gears labeled "VSV Convolution (PyTheranostics)".
        *   *Flow:* SPECT TIA maps point in. Straight arrow points out.
        *   *Output:* A homogeneous dose map lacking high-frequency anatomical definition at tissue boundaries.
        *   *Metrics Badge:* Yellow color, "Pearson r = 0.912 (Ignores tissue heterogeneity)".
    *   **Lane 3 (Right - SciML UDE / Julia):**
        *   *Icon:* A hybrid icon combining a math equation ($S_{homo}$) and a neural network ($\mathcal{N}_\theta$) encased in a golden shield.
        *   *Flow:* SPECT, CT (HU $\to \rho$), and physical constants point in. A glowing, thick green arrow points out.
        *   *Output:* A highly detailed, precise dose map (matching the Monte Carlo Ground Truth).
        *   *Metrics Badge:* Green color, "**State-of-the-Art: Pearson r = 0.957**".
*   **Clinical Integration (Real Scanner Data):**
    *   For the three outputs in the respective lanes, embed real 2D axial dose profiles (isodose contours overlaid on anatomical CT) derived directly from the $177$Lu-PSMA patient cohort. This contrasts the unconstrained neural artifacts of Lane 1, the homogeneous lack of boundary detail in Lane 2, and the high-fidelity anatomical constraints achieved in Lane 3 against Monte Carlo ground truth.
*   **Bottom Anchor (Speed Comparison):**
    *   A horizontal bar or speedometer spanning the bottom connecting Lane 2 (Python VSV) to Lane 3 (Julia UDE).
    *   *Annotation:* "MedImages.jl / SciML architecture maintains a **10× Speed Advantage** over traditional Python analytical frameworks."

---

## 6. Appendix: Clinical Asset Generation Guide

To seamlessly integrate your clinical NIfTI/DICOM assets into the rendered PNG infographics via the HTML placeholders, please create the following PNG files and place them inside `elsarticle/figures_new/clinical_assets/`:

**1. mip_wholebody.png** (For Challenge 1)
*   **Dimensions:** ~ 100x120 pixels (Portrait)
*   **Content:** A high-contrast, black-and-white Maximum Intensity Projection (MIP) rendering of a whole-body [177Lu]Lu-PSMA SPECT/CT study.

**2. resampling_ct.png** (For Challenge 2)
*   **Dimensions:** ~ 100x100 pixels (Square)
*   **Content:** A real axial CT cross-section showing rapid spatial resampling (perhaps slightly pixelated or undergoing an explicit interpolation transform).

**3. dose_overlay_ct.png** (For Challenge 3)
*   **Dimensions:** ~ 80x100 pixels (Portrait)
*   **Content:** An authentic, pseudo-colored (or high-contrast grayscale) 177Lu-PSMA dose map overlay on an axial CT slice, explicitly demonstrating tissue heterogeneity and boundary adherence.

**4. Challenge 4 Slice Assets** (For the 3D Metadata Stack)
*   **Dimensions for each:** ~ 120x50 pixels (Wide Landscape)
*   **Content:** Genuine, coregistered clinical NIfTI slices corresponding to the same patient anatomy.
    *   `spect_ac_slice.png` (SPECT AC)
    *   `spect_nac_slice.png` (SPECT NAC)
    *   `dosemap_slice.png` (Dosemap)
    *   `ct_slice.png` (CT Anatomy)
    *   *Optional but recommended: Create rotated versions (`spect_ac_slice_rot.png`, etc.) for the bottom "Aligned" stack if you want the 45-degree rotation to be explicitly visible in the data itself.*

**5. Quantitative UDE Dosimetry Experiment Assets** (For the 3 Comparison Lanes)
*   **Dimensions for each:** ~ 80x100 pixels (Portrait)
*   **Content:** Real 2D axial dose profiles (isodose contours overlaid on anatomical CT) derived directly from the cohort.
    *   `dl_artifacts.png` (Showing unconstrained/failed spatial approximation)
    *   `vsv_homo.png` (Showing homogeneous lack of boundary detail)
    *   `ude_highfi.png` (Showing the precise high-fidelity output)
