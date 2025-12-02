using BenchmarkTools
using MedImages
using PyCall
using Printf
using HDF5

# Setup
sitk = pyimport("SimpleITK")
const TEST_FILE = "test_data/volume-0.nii.gz"
const OUTPUT_DIR = "test_data/benchmark_output"
mkpath(OUTPUT_DIR)

println("Running benchmarks...")

if !isfile(TEST_FILE)
    error("Test file not found: $TEST_FILE")
end

# Load
println("\n--- Load Benchmark ---")
b_load_julia = @benchmark MedImages.load_image($TEST_FILE, "CT") samples=10 seconds=5
b_load_sitk = @benchmark $sitk.ReadImage($TEST_FILE) samples=10 seconds=5

println("Julia Load (Median): ", median(b_load_julia).time / 1e6, " ms")
println("SimpleITK Load (Median): ", median(b_load_sitk).time / 1e6, " ms")

# Prepare images for processing
med_im = MedImages.load_image(TEST_FILE, "CT")
sitk_im = sitk.ReadImage(TEST_FILE)

# Rotation
println("\n--- Rotation Benchmark (30 deg, axis 1) ---")
b_rot_julia = @benchmark MedImages.rotate_mi($med_im, 1, 30.0, MedImages.Linear_en) samples=5 seconds=10

# Helper for SITK rotation to be fair comparison (include transform creation?)
function run_sitk_rotation(image)
    euler_transform = sitk.Euler3DTransform()
    # Approx center calculation
    sz = image.GetSize()
    # SimpleITK uses 0-based indexing for GetSize but physical point calc might need careful index
    center_idx = [(s-1)/2.0 for s in sz]
    center = image.TransformContinuousIndexToPhysicalPoint(center_idx)
    euler_transform.SetCenter(center)
    euler_transform.SetRotation(deg2rad(30.0), 0.0, 0.0)
    return sitk.Resample(image, image, euler_transform, sitk.sitkLinear, 0.0)
end

b_rot_sitk = @benchmark run_sitk_rotation($sitk_im) samples=5 seconds=10

println("Julia Rotation (Median): ", median(b_rot_julia).time / 1e6, " ms")
println("SimpleITK Rotation (Median): ", median(b_rot_sitk).time / 1e6, " ms")

# Save (HDF5 vs NIfTI)
println("\n--- Save Benchmark ---")
out_sitk = joinpath(OUTPUT_DIR, "bench_sitk.nii.gz")
h5_path = joinpath(OUTPUT_DIR, "bench_julia.h5")

# HDF5 Save
b_save_julia = @benchmark begin
    if isfile($h5_path)
        rm($h5_path)
    end
    f = HDF5.h5open($h5_path, "w")
    MedImages.save_med_image(f, "bench_group", $med_im)
    close(f)
end samples=5 seconds=5

# SITK Save
b_save_sitk = @benchmark $sitk.WriteImage($sitk_im, $out_sitk) samples=5 seconds=5

println("Julia Save (HDF5) (Median): ", median(b_save_julia).time / 1e6, " ms")
println("SimpleITK Save (NIfTI) (Median): ", median(b_save_sitk).time / 1e6, " ms")
