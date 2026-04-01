# MedImages.jl Infographic Design Logic

This document provides a precise, step-by-step blueprint for visualizing the four core challenges addressed by `MedImages.jl` in the `old_plos.tex` manuscript. Each challenge is broken down into its core conceptual points, followed by exact instructions on how those points should be structured, connected, and represented pictographically.

---

## Challenge 1: The Volume Bottleneck (Biobank-Scale Processing)

### Core Points
1. High-throughput preprocessing of biobank-scale multimodal datasets (thousands of studies) is a major bottleneck. Our 100-subject experiment was merely a benchmark to quantify the speedup relative to existing frameworks.
2. Traditional caching (e.g., MONAI PersistentDataset) relies on heavy Python Pickle/Pt serialization, bottlenecking large-scale pipelines.
3. MedImages.jl uses HDF5 and Fused Affine GPU kernels, designed specifically to scale natively to thousands of examinations without cache penalty.
4. Result: A proven 7.2× faster turnaround time (~90 ms vs ~650 ms per subject), enabling true biobank-scale data ingestion in minutes rather than days.

### Pictographic Representation & Layout
*   **Bounding Box (Left - Traditional Pipeline):**
    *   *Iconography:* A slow-moving funnel or a series of stacked, disconnected disk drives representing `Pickle/Pt Caching`.
    *   *Text:* "MONAI PersistentDataset (~650 ms)"
*   **Bounding Box (Right - MedImages Pipeline):**
    *   *Iconography:* A sleek, single solid state drive (HDF5) connected directly to a GPU microchip icon.
    *   *Text:* "MedImages.jl HDF5 + Native GPU (~90 ms)"
*   **Connections (Lines & Arrows):**
    *   Both boxes output to a central target node below them.
    *   The line from the Left box should be dashed, red, and thick (representing I/O friction).
    *   The line from the Right box should be solid, green, and smooth (representing massive I/O throughput).
    *   Both lines converge on a large, central "Results Node" shaped like a massive biobank vault containing thousands of datasets, with bold text reading "**7.2× Speedup, Unlocking Thousands of Studies**".

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
---

## Expanding Challenges 1-4: Adding Framework Comparisons and Experimental Context

To strengthen the narrative and ground the claims in specific experimental results discussed in the manuscript, the infographics for Challenges 1-4 can be visually expanded by introducing explicit comparison markers against existing frameworks (SimpleITK, MONAI, TorchIO).

### Expanding Challenge 1 (Volume)
*   **Context Addition:** Explicitly contrast the data serialization strategies. Add a comparative table or a smaller secondary graphic inside the traditional pipeline box highlighting **TorchIO's** memory buildup issues (Subject Class Attributes) alongside **MONAI's** Python caching (MetaTensor Dict-based).
*   **Visual Logic:** Draw a "memory leak" or "bottleneck" warning sign attached to the MONAI/TorchIO side, directly contrasting it with an HDF5 native disk icon that has a "Zero-Serialization" badge on the Julia side.

### Expanding Challenge 2 (Speed)
*   **Context Addition:** Include specific target hardware (NVIDIA RTX 3090, Intel Core Ultra 9) to qualify the 135× speedup. Add a visual bar chart comparing execution times.
*   **Visual Logic:** Next to the Python/C++ brick wall, place a "SimpleITK (CPU)" box with a slow progress bar (e.g., 6.69 ms for affine transform). On the Julia side, place a "MedImages GPU" box with a nearly instantaneous progress bar (e.g., 0.83 ms).

### Expanding Challenge 3 (Differentiability)
*   **Context Addition:** Show the "Walled Garden" problem of Python frameworks (PyTorch, JAX, TensorFlow).
*   **Visual Logic:** Place icons for PyTorch and JAX inside a locked cage ("Walled Garden") connected by broken arrows. Conversely, show Julia's ecosystem (`DifferentialEquations.jl`, `Lux.jl`, `MedImages.jl`) seamlessly connected by continuous, circular arrows representing "Multiple Dispatch / Expression Problem Solved."

### Expanding Challenge 4 (Metadata Management)
*   **Context Addition:** Highlight the "Metadata Drift" risk in traditional Python arrays.
*   **Visual Logic:** In the top section, show a `sitk.GetArrayFromImage()` operation acting like a pair of scissors, slicing off a "Spacing/Origin" tag and dropping it into a trash bin (NumPy Array conversion). Contrast this with MedImages.jl's `BatchedMedImage` where the tag is locked inside a shield (Julia's Type System).

---

## Dedicated Infographic: Quantitative UDE Dosimetry Experiment

This new, fifth infographic strictly details the experimental methodology and superior performance of the 4-State UDE model for 177Lu-PSMA dosimetry, comparing it explicitly against both analytical and deep learning baselines.

### Core Points
1. **Objective:** Map functional SPECT and anatomical CT data to high-fidelity Monte Carlo (MC) ground truth dosimetry.
2. **Clinical Baseline:** Voxel S-Value (VSV) convolution over Time-Integrated Activity (TIA) using Python (`Evaluate-Proj` / `pytheranostics`), which achieves a Pearson correlation of $r=0.912$.
3. **Deep Learning Baseline:** Pure 3D CNN / U-Net architectures ("Black Boxes" like DblurDoseNet) struggle with physical constraints ($r \approx 0.55 - 0.60$).
4. **The SciML/Julia Solution:** The "No-Approx UDE" model cleanly isolates known physics (primary scatter) from a neural residual, achieving state-of-the-art $r=0.957$.

### Pictographic Representation & Layout
*   **Top Header:** "High-Fidelity 177Lu-PSMA Dosimetry Comparison"
*   **Three Vertical Lanes (The Competitors):**
    *   **Lane 1 (Left - Pure Deep Learning):**
        *   *Icon:* A black box labeled "3D U-Net / DblurDoseNet"
        *   *Flow:* Raw SPECT/CT data points in. Squiggly, uncertain arrow points out.
        *   *Output:* A blurry, unconstrained dose map.
        *   *Metrics Badge:* Red color, "Pearson r = 0.55 - 0.60 (Fails physical constraints)".
    *   **Lane 2 (Center - Clinical Analytical / Python):**
        *   *Icon:* A calculator or standard rigid gears labeled "VSV Convolution (PyTheranostics)".
        *   *Flow:* SPECT TIA maps point in. Straight arrow points out.
        *   *Output:* A crisp but overly smoothed dose map missing boundary details.
        *   *Metrics Badge:* Yellow color, "Pearson r = 0.912 (Ignores tissue heterogeneity)".
    *   **Lane 3 (Right - SciML UDE / Julia):**
        *   *Icon:* A hybrid icon combining a math equation ($S_{homo}$) and a neural network ($\mathcal{N}_\theta$) encased in a golden shield.
        *   *Flow:* SPECT, CT (HU $\to \rho$), and physical constants point in. A glowing, thick green arrow points out.
        *   *Output:* A highly detailed, precise dose map (matching the Monte Carlo Ground Truth).
        *   *Metrics Badge:* Green color, "**State-of-the-Art: Pearson r = 0.957**".

*   **Bottom Anchor (Speed Comparison):**
    *   A horizontal bar or speedometer spanning the bottom connecting Lane 2 (Python VSV) to Lane 3 (Julia UDE).
    *   *Annotation:* "MedImages.jl / SciML architecture maintains a **10× Speed Advantage** over traditional Python analytical frameworks."
