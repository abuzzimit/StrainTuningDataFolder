import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def load_and_plot_npz(filename='PL_scan.npz'):
    """
    Load data from NPZ file and create plot
    """
    try:
        # Load data
        data = np.load(filename)
        x = data['x']
        y = data['y']
        counts = data['counts']
                
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create the heatmap
        im = ax.imshow(counts, cmap='viridis', aspect='equal', origin='lower',
                       extent=[x.min(), x.max(), y.min(), y.max()])
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Intensity (counts/s)', rotation=270, labelpad=15)
        
        # Set labels and title
        ax.set_xlabel('X Position (µm)')
        ax.set_ylabel('Y Position (µm)')
        ax.set_title('Photoluminescence Scan 2D Map (from NPZ)')
        
        plt.tight_layout()
        plt.show()
        
        return fig, ax
        
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return None, None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def main():
    # Conversion factor from pixels to micrometers
    conversion_factor = 1.51590
    
    # Read the data
    try:        
        # Load and plot from NPZ file
        print("Loading and plotting from NPZ file:")
        fig_npz, ax_npz = load_and_plot_npz('PL_scan.npz')
                
    except FileNotFoundError:
        print("Error: PL_scan.txt file not found!")
    except Exception as e:
        print(f"Error reading data: {e}")

if __name__ == "__main__":
    main()
