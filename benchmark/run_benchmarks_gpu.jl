using BenchmarkTools
using MedImages
using CUDA
using KernelAbstractions
using Statistics

# Check if CUDA is available
if !CUDA.functional()
    error("CUDA is not available. This script requires a GPU.")
end

# Setup
const TEST_FILE = "test_data/volume-0.nii.gz"
if !isfile(TEST_FILE)
    error("Test file not found: $TEST_FILE")
end

println("Running GPU benchmarks...")

# Load image (CPU)
med_im_cpu = MedImages.load_image(TEST_FILE, "CT")

# Move to GPU
println("Moving image to GPU...")
med_im_gpu = MedImages.MedImage(
    CuArray(med_im_cpu.voxel_data),
    med_im_cpu.origin,
    med_im_cpu.spacing,
    med_im_cpu.direction,
    med_im_cpu.image_type,
    med_im_cpu.image_subtype,
    med_im_cpu.date_of_saving,
    med_im_cpu.acquistion_time,
    med_im_cpu.patient_id,
    MedImages.CUDA_current_device,
    med_im_cpu.study_uid,
    med_im_cpu.patient_uid,
    med_im_cpu.series_uid,
    med_im_cpu.study_description,
    med_im_cpu.legacy_file_name,
    med_im_cpu.display_data,
    med_im_cpu.clinical_data,
    med_im_cpu.is_contrast_administered,
    med_im_cpu.metadata
)

# Resample Benchmark
println("\n--- Resample Benchmark (GPU, Identity) ---")
# Warmup
MedImages.resample_to_image(med_im_gpu, med_im_gpu, MedImages.Linear_en)

b_resample_gpu = @benchmark MedImages.resample_to_image($med_im_gpu, $med_im_gpu, MedImages.Linear_en) samples=10 seconds=10

println("Julia Resample GPU (Median): ", median(b_resample_gpu).time / 1e6, " ms")
