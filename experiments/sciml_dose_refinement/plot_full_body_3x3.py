import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import glob

def load_bin(path, shape):
    if not os.path.exists(path):
        return None
    return np.fromfile(path, dtype=np.float32).reshape(shape, order='F')

def get_mip(data):
    if data is None: return np.zeros((256, 500)) # Placeholder
    mip = np.max(data, axis=1)
    return np.flipud(mip.T)

def run():
    val_dirs = sorted(glob.glob("val_outputs/FDM*"))
    
    for pat_dir in val_dirs:
        pat_name = os.path.basename(pat_dir)
        ct_bin = os.path.join(pat_dir, "full_ct.bin")
        if not os.path.exists(ct_bin): continue
        
        file_size = os.path.getsize(ct_bin)
        z_size = int(file_size / (256 * 256 * 4))
        shape = (256, 256, z_size)
        print(f"Processing {pat_name} with shape {shape}")

        ct = load_bin(ct_bin, shape)
        mc = load_bin(os.path.join(pat_dir, "full_mc.bin"), shape)
        ude = load_bin(os.path.join(pat_dir, "full_ude_imp.bin"), shape)
        baseline = load_bin(os.path.join(pat_dir, "full_baseline.bin"), shape)
        
        # Subtraction models:
        # 1) ude 2) analitical baseline 3) dblurdosenet 4) CNN improved 5) semidose 6) spect0
        models_sub = [
            ("UDE (Ours)", ude),
            ("Analytical Baseline", baseline),
            ("DblurDoseNet", load_bin(os.path.join(pat_dir, "full_dblur.bin"), shape)),
            ("CNN Improved", load_bin(os.path.join(pat_dir, "full_cnn_imp.bin"), shape)),
            ("SemiDose", load_bin(os.path.join(pat_dir, "full_semi.bin"), shape)),
            ("Spect0Net", load_bin(os.path.join(pat_dir, "full_spect0.bin"), shape))
        ]
        
        fig, axes = plt.subplots(3, 3, figsize=(18, 24))
        plt.subplots_adjust(wspace=0.01, hspace=0.1)
        
        # ---------------------------------------------------------------------
        # SHAPE NORMALIZATION (Each to [0, 1])
        # ---------------------------------------------------------------------
        vmax_mc = np.percentile(mc, 99.5) if mc is not None else 1.0
        if vmax_mc == 0: vmax_mc = 1.0
        mc_norm = mc / (vmax_mc + 1e-6) if mc is not None else np.zeros(shape)
        mc_mip_norm = get_mip(mc_norm)
        mask_mip = mc_mip_norm < 0.10

        # Row 1: CT | MC | UDE
        ct_slice = np.flipud(ct[:, 128, :].T) if ct is not None else np.zeros((z_size, 256))
        axes[0, 0].imshow(ct_slice, cmap='gray', vmin=-160, vmax=240)
        axes[0, 0].set_title("Anatomic Reference (CT)", fontsize=18)

        axes[0, 1].imshow(mc_mip_norm, cmap='hot', vmin=0, vmax=1.0)
        axes[0, 1].set_title("Ground Truth (Monte Carlo)", fontsize=18)

        ude_norm = ude / (np.percentile(np.abs(ude), 99.5) + 1e-6) if ude is not None else np.zeros(shape)
        axes[0, 2].imshow(get_mip(ude_norm), cmap='hot', vmin=0, vmax=1.0)
        axes[0, 2].set_title("UDE Prediction (Ours)", fontsize=18)

        # Rows 2-3: Subtractions
        im = None
        for idx, (name, pred) in enumerate(models_sub):
            row = (idx // 3) + 1
            col = idx % 3

            if pred is None:
                axes[row, col].text(0.5, 0.5, "Data Missing", ha='center')
                continue

            # Normalize model prediction to ITS OWN max for shape comparison
            p_peak = np.percentile(np.abs(pred), 99.5)
            p_norm = pred / (p_peak + 1e-6)

            # Subtraction of normalized volumes
            sub_raw = mc_norm - p_norm
            sub_mip = get_mip(sub_raw)
            
            # RESIDUAL NORMALIZATION: center at 0
            s_min = np.percentile(sub_mip[~mask_mip], 0.5)
            s_max = np.percentile(sub_mip[~mask_mip], 99.5)
            sub_centered = (sub_mip - s_min) / (s_max - s_min + 1e-6) - 0.5

            final_sub_mip = np.ma.masked_where(mask_mip, sub_centered)

            im = axes[row, col].imshow(final_sub_mip, cmap='RdBu_r', vmin=-0.5, vmax=0.5)
            im.cmap.set_bad(color='white')

            axes[row, col].set_title(f"Error Pattern: {name}", fontsize=16)

        for ax in axes.flatten(): ax.axis('off')

        if im is not None:
            cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.4])
            cbar = fig.colorbar(im, cax=cbar_ax)
            cbar.ax.tick_params(labelsize=14)
            cbar.set_label('Centered Error (Under-estimate < 0 < Over-estimate)', fontsize=16)

        pat_short = pat_name.split("__")[-1]
        plt.suptitle(f"Multi-Model Comparative Dosimetry ({pat_short})\nPhase 1: Results (Top) | Phase 2: Error Residuals relative to Monte Carlo", fontsize=26, y=0.98)

        out_path = os.path.join(pat_dir, "full_body_comparison_3x3.png")
        plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Grid saved to {out_path}")
        plt.close(fig)

if __name__ == "__main__":
    run()
