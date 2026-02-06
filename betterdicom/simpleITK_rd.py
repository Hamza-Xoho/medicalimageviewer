import SimpleITK as sitk
import matplotlib.pyplot as plt

# 1. SETUP
# Make sure this path points to a valid file on your machine
path = "/Users/hamza/Code/Medimaging/pidicom/IN000001"
image = sitk.ReadImage(path)

# 2. EXTRACT DATA
pixel_array = sitk.GetArrayFromImage(image).squeeze()

# 3. GET PHYSICAL DIMENSIONS
spacing = image.GetSpacing()  # Returns tuple: (x_spacing, y_spacing)
size = image.GetSize()        # Returns tuple: (width, height)

def calculate_physical_size():
    # size[0] is width (x), size[1] is height (y)
    calc_width_mm = size[0] * spacing[0]
    calc_height_mm = size[1] * spacing[1]
    return calc_width_mm, calc_height_mm

# FIX: Unpack in the correct order (Width, Height) to match the return statement
phys_width, phys_height = calculate_physical_size()

def inspect_metadata(verbose=True):
    if not verbose:
        return
    
    # FIX: Replaced em-dash '—' with standard hyphen '-'
    print(f"{' Metadata Inspection ':-^40}")
    
    # FIX: Cannot format a tuple directly. Accessed elements [0] and [1].
    print(f"Pixel Spacing (mm) : {spacing[0]:.3f} x {spacing[1]:.3f}")
    
    print(f"Field of View (mm) : {phys_width:.1f} x {phys_height:.1f}")
    print("-" * 40)

def render_radiology_view(data, physical_dims=None, cmap='gray'):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    extent_limit = None
    xlabel, ylabel = "Pixels", "Pixels"
    
    if physical_dims:
        # Expecting tuple (height_mm, width_mm)
        h_mm, w_mm = physical_dims
        
        # Extent format: [left, right, bottom, top]
        # Since origin is 'upper', 'bottom' is the max Y value (height)
        extent_limit = [0, w_mm, h_mm, 0] 
        xlabel, ylabel = "Width (mm)", "Height (mm)"

    im = ax.imshow(data, cmap=cmap, extent=extent_limit, origin='upper')
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Signal Intensity (Raw)')

    # data.shape is (Rows/Height, Cols/Width) in Numpy
    ax.set_title(f"DICOM Viewer | {data.shape[1]}x{data.shape[0]} Matrix", fontsize=12, pad=10)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)

    plt.tight_layout()
    plt.show()

# ==========================================
# 5. EXECUTION FLOW
# ==========================================
inspect_metadata(verbose=True)

# FIX: Use correct variable names (lower case) defined earlier
# We pass (Height, Width) to match the unpacking inside render_radiology_view
dims_tuple = (phys_height, phys_width)

# FIX: Use 'pixel_array' (defined at top), not 'PIXEL_ARRAY'
render_radiology_view(pixel_array, physical_dims=dims_tuple)