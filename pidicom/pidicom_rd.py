import pydicom
import matplotlib.pyplot as plt


path = "/Users/hamza/Code/Medimaging/pidicom/IN000001"
ds = pydicom.dcmread(path)

# Extract Global Constants (Immutable Data)
PIXEL_ARRAY = ds.pixel_array
N_ROWS = ds.Rows
N_COLS = ds.Columns

# Spacing: [Row (Y), Column (X)]
ROW_SPACING = ds.PixelSpacing[0] 
COL_SPACING = ds.PixelSpacing[1] 


def calculate_physical_size():
    """
    Calculates the physical field of view in millimeters.
    Returns: (height_mm, width_mm)
    """
    calc_height = N_ROWS * ROW_SPACING
    calc_width  = N_COLS * COL_SPACING
    return calc_height, calc_width

# Capture the physical dimensions globally
PHYSICAL_HEIGHT, PHYSICAL_WIDTH = calculate_physical_size()


def inspect_metadata(verbose=True):
    if not verbose:
        return
        
    print(f"{' Metadata Inspection ':—^40}")
    print(f"Matrix Size (Px)   : {N_ROWS} x {N_COLS}")
    print(f"Pixel Spacing (mm) : {ROW_SPACING:.3f} x {COL_SPACING:.3f}")
    print(f"Field of View (mm) : {PHYSICAL_WIDTH:.1f} x {PHYSICAL_HEIGHT:.1f}")
    print("—" * 40)


def render_radiology_view(data, physical_dims=None, cmap='gray'):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    extent_limit = None
    xlabel, ylabel = "Pixels", "Pixels"
    
    if physical_dims:
        h_mm, w_mm = physical_dims
        extent_limit = [0, w_mm, h_mm, 0] 
        xlabel, ylabel = "Width (mm)", "Height (mm)"

    im = ax.imshow(data, cmap=cmap, extent=extent_limit, origin='upper')
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Signal Intensity (Raw)')

    ax.set_title(f"DICOM Viewer | {data.shape[1]}x{data.shape[0]} Matrix", fontsize=12, pad=10)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)

    plt.tight_layout()
    plt.show()

# ==========================================
# 5. EXECUTION FLOW
# ==========================================
inspect_metadata(verbose=True)

# We pack the dims into a tuple to pass them cleanly
dims_tuple = (PHYSICAL_HEIGHT, PHYSICAL_WIDTH)

# Launch the view
render_radiology_view(PIXEL_ARRAY, physical_dims=dims_tuple)