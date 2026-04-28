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

def bresenham_3d(x1, y1, z1, x2, y2, z2):
    points = []
    x1, y1, z1 = int(round(x1)), int(round(y1)), int(round(z1))
    x2, y2, z2 = int(round(x2)), int(round(y2)), int(round(z2))
    
    # Grid size is 128
    x1, y1, z1 = max(0, min(127, x1)), max(0, min(127, y1)), max(0, min(127, z1))
    x2, y2, z2 = max(0, min(127, x2)), max(0, min(127, y2)), max(0, min(127, z2))

    points.append((x1, y1, z1))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    xs = 1 if x2 > x1 else -1
    ys = 1 if y2 > y1 else -1
    zs = 1 if z2 > z1 else -1

    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != x2:
            x1 += xs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            points.append((x1, y1, z1))
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != y2:
            y1 += ys
            if p1 >= 0:
                x1 += xs
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            points.append((x1, y1, z1))
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != z2:
            z1 += zs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            points.append((x1, y1, z1))
    return points

def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)] + [alpha]

def scale_coords(arr):
    # Scale from [0, 31] to [0, 127]
    return [v * (127.0 / 31.0) for v in arr]

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

        # Determine the central region first to trim lines
        all_x = gx + ux + [p[0][0] for p in endpoints] + [p[0][1] for p in endpoints]
        all_y = gy + uy + [p[1][0] for p in endpoints] + [p[1][1] for p in endpoints]
        all_z = gz + uz + [p[2][0] for p in endpoints] + [p[2][1] for p in endpoints]
        
        center_x = (min(all_x) + max(all_x)) / 2.0 * (127.0/31.0)
        center_y = (min(all_y) + max(all_y)) / 2.0 * (127.0/31.0)
        center_z = (min(all_z) + max(all_z)) / 2.0 * (127.0/31.0)
        
        # Zoom window size in 128 space
        ws = 40 
        x_lims = (max(0, center_x - ws/2), min(128, center_x + ws/2))
        y_lims = (max(0, center_y - ws/2), min(128, center_y + ws/2))
        z_lims = (max(0, center_z - ws/2), min(128, center_z + ws/2))

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        filled = np.zeros((128, 128, 128), dtype=bool)
        colors_grid = np.zeros((128, 128, 128, 4), dtype=np.float32)

        def add_line(x_arr, y_arr, z_arr, color, alpha=1.0, thickness=0):
            sx = scale_coords(x_arr)
            sy = scale_coords(y_arr)
            sz = scale_coords(z_arr)
            pts = bresenham_3d(sx[0], sy[0], sz[0], sx[1], sy[1], sz[1])
            rgba = hex_to_rgba(color, alpha)
            for p in pts:
                for dx in range(-thickness, thickness + 1):
                    for dy in range(-thickness, thickness + 1):
                        for dz in range(-thickness, thickness + 1):
                            nx, ny, nz = p[0] + dx, p[1] + dy, p[2] + dz
                            # Trim lines to the zoom window
                            if x_lims[0] <= nx < x_lims[1] and \
                               y_lims[0] <= ny < y_lims[1] and \
                               z_lims[0] <= nz < z_lims[1]:
                                filled[nx, ny, nz] = True
                                colors_grid[nx, ny, nz] = rgba

        # All lines same thickness (0 = 1 voxel thick)
        add_line(gx, gy, gz, '#2ecc71', alpha=0.9, thickness=0)
        add_line(ux, uy, uz, '#e74c3c', alpha=0.6, thickness=0)

        colors = ['#b3cde0', '#8c96c6', '#8856a7', '#810f7c', '#4d004b', '#000000']
        for i, idx in enumerate(indices):
            ep = epochs[idx]
            px, py, pz = endpoints[idx]
            alpha = 0.4 + 0.6 * (i / (len(indices) - 1))
            add_line(px, py, pz, colors[i], alpha=alpha, thickness=0)

        ax.voxels(filled, facecolors=colors_grid, edgecolors='k', linewidth=0.1)

        import matplotlib.patches as mpatches
        legend_elements = [
            mpatches.Patch(color='#2ecc71', alpha=0.9, label='Gold Standard'),
            mpatches.Patch(color='#e74c3c', alpha=0.6, label='Uncorrected (Input)')
        ]
        for i, idx in enumerate(indices):
            ep = epochs[idx]
            alpha = 0.4 + 0.6 * (i / (len(indices) - 1))
            legend_elements.append(mpatches.Patch(color=colors[i], alpha=alpha, label=f'Epoch {ep}'))

        ax.set_title("3D Differentiable Proof: Rotation Learning", fontsize=18, fontweight='bold', pad=30)
        
        ax.set_xlim(x_lims)
        ax.set_ylim(y_lims)
        ax.set_zlim(z_lims)
        
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        
        ax.set_xticks(np.linspace(x_lims[0], x_lims[1], 4, dtype=int))
        ax.set_yticks(np.linspace(y_lims[0], y_lims[1], 4, dtype=int))
        ax.set_zticks(np.linspace(z_lims[0], z_lims[1], 4, dtype=int))
        
        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.set_zlabel("Z", fontsize=12)
        
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.85, 0.9), fontsize=10, frameon=True)

        ax.view_init(elev=20, azim=45)

        plt.tight_layout()
        plt.savefig("/home/user/MedImages.jl/docs/src/experiments/viz/differentiability_3d_lines.png", dpi=300, bbox_inches='tight')
        print("Successfully saved differentiability_3d_lines.png")
    except Exception as e:
        print(f"Error plotting 3D: {e}")

if __name__ == "__main__":
    plot_3d_lines()
