import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import csv

def extract_endpoints_nifti(filepath, threshold=0.1):
    img = nib.load(filepath).get_fdata()
    coords = np.array(np.where(img > threshold)).T # (N, 3)
    if len(coords) == 0:
        return [16, 16], [16, 16], [16, 16]
        
    mean = np.mean(coords, axis=0)
    cov = np.cov(coords.T)
    evals, evecs = np.linalg.eigh(cov)
    principal_axis = evecs[:, np.argmax(evals)]
    
    projections = np.dot(coords - mean, principal_axis)
    p1 = coords[np.argmin(projections)]
    p2 = coords[np.argmax(projections)]
    
    return [p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]]

def plot_3d_lines():
    try:
        # Load endpoints from CSV
        epochs = []
        endpoints = []
        with open('endpoints.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                epoch = int(row[0])
                p1x, p1y, p1z, p2x, p2y, p2z = map(float, row[1:])
                epochs.append(epoch)
                endpoints.append( ([p1x, p2x], [p1y, p2y], [p1z, p2z]) )
                
        # Choose epochs: first, last, and 4 in the middle
        n = len(epochs)
        indices = [0, n//5, 2*n//5, 3*n//5, 4*n//5, n-1]
        
        gx, gy, gz = extract_endpoints_nifti("gold_standard.nii.gz")
        ux, uy, uz = extract_endpoints_nifti("uncorrected.nii.gz")

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Gold standard as dashed
        ax.plot(gx, gy, gz, c='#2ecc71', linewidth=6, linestyle='--', label='Gold Standard', alpha=0.6)
        
        # Uncorrected (Rotated Input)
        ax.plot(ux, uy, uz, c='#e74c3c', linewidth=4, label='Uncorrected (Input)', alpha=0.5)

        # Plot the chosen epochs
        # A gradient of blues to show progression
        colors = ['#b3cde0', '#8c96c6', '#8856a7', '#810f7c', '#4d004b', '#000000']
        for i, idx in enumerate(indices):
            ep = epochs[idx]
            px, py, pz = endpoints[idx]
            alpha = 0.4 + 0.6 * (i / (len(indices) - 1)) # fade in
            lw = 2 + 2 * (i / (len(indices) - 1))
            label = f'Epoch {ep} (Reconstructed)'
            ax.plot(px, py, pz, c=colors[i], linewidth=lw, label=label, alpha=alpha)

        ax.set_title("3D Representation of Geometric Transformation Over Time", fontsize=15, fontweight='bold', pad=20)
        ax.set_xlim([0, 32])
        ax.set_ylim([0, 32])
        ax.set_zlim([0, 32])
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        ax.legend(loc='upper left', fontsize=11, bbox_to_anchor=(0.0, 1.0))

        ax.view_init(elev=20, azim=45)

        plt.tight_layout()
        plt.savefig("/home/user/MedImages.jl/docs/src/experiments/viz/differentiability_3d_lines.png", dpi=300)
        print("Successfully saved differentiability_3d_lines.png")
    except Exception as e:
        print(f"Error plotting 3D: {e}")

if __name__ == "__main__":
    plot_3d_lines()
