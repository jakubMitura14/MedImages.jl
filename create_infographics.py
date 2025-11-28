from playwright.sync_api import sync_playwright
import os

def generate_infographics():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Infographic 1: Julia's Role in Scientific Computing
        html_content_1 = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f0f0; }
                .container { width: 800px; height: 600px; background: white; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); position: relative; }
                h1 { text-align: center; color: #333; }
                .box { border: 2px solid #333; padding: 10px; border-radius: 8px; width: 200px; text-align: center; position: absolute; background-color: #e0f7fa; font-weight: bold; }
                .arrow { position: absolute; font-size: 24px; color: #555; }

                #high-level { top: 150px; left: 50px; background-color: #fff9c4; }
                #low-level { top: 150px; right: 50px; background-color: #ffccbc; }
                #julia { top: 350px; left: 300px; width: 200px; background-color: #d1c4e9; border: 3px solid #673ab7; }

                .desc { font-size: 14px; color: #666; margin-top: 5px; }

                .arrow-down-left { top: 250px; left: 180px; transform: rotate(45deg); font-size: 40px; }
                .arrow-down-right { top: 250px; right: 180px; transform: rotate(-45deg); font-size: 40px; }

                .label { position: absolute; font-size: 16px; font-weight: bold; color: #333; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Bridging the Two-Language Problem</h1>

                <div id="high-level" class="box">
                    High-Level Languages<br>(Python, R, MATLAB)
                    <div class="desc">Easy to use, but slow</div>
                </div>

                <div id="low-level" class="box">
                    Low-Level Languages<br>(C, C++, Fortran)
                    <div class="desc">Fast, but hard to use</div>
                </div>

                <div class="arrow arrow-down-left">↘</div>
                <div class="arrow arrow-down-right">↙</div>

                <div id="julia" class="box">
                    Julia Language
                    <div class="desc">High Performance + Ease of Use<br>Solves Two-Language Problem</div>
                </div>

                <div style="position: absolute; bottom: 50px; left: 50px; right: 50px; text-align: center; font-style: italic;">
                    Julia acts as a universal adapter, streamlining the scientific workflow from prototype to production.
                </div>
            </div>
        </body>
        </html>
        """
        page.set_content(html_content_1)
        page.screenshot(path="julia_role.png")

        # Infographic 2: Medical Imaging Spatial Metadata Challenges
        html_content_2 = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f0f0; }
                .container { width: 800px; height: 600px; background: white; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); position: relative; }
                h1 { text-align: center; color: #333; }

                .grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-top: 30px;
                }

                .card {
                    border: 1px solid #ddd;
                    padding: 15px;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }

                .card h3 { margin-top: 0; color: #d32f2f; }

                .cube {
                    width: 50px; height: 50px; background-color: #2196f3;
                    margin: 10px auto;
                    display: flex; justify-content: center; align-items: center; color: white;
                }

                .axis {
                    width: 100px; height: 2px; background-color: black; position: relative; margin: 20px auto;
                }
                .axis::after { content: '>'; position: absolute; right: -5px; top: -5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Challenges in Medical Imaging Metadata</h1>

                <div class="grid">
                    <div class="card">
                        <h3>Voxel Spacing</h3>
                        <div style="display: flex; justify-content: center; gap: 10px;">
                            <div class="cube" style="width: 30px;">1mm</div>
                            <div class="cube" style="width: 60px;">2mm</div>
                        </div>
                        <p>Non-isotropic pixels: Voxels can have different physical sizes (e.g., thick slices).</p>
                    </div>

                    <div class="card">
                        <h3>Origin & Direction</h3>
                        <div style="position: relative; height: 80px; width: 100%; border: 1px dashed #ccc;">
                            <div style="position: absolute; top: 10px; left: 10px; width: 10px; height: 10px; background: red; border-radius: 50%;"></div>
                            <div style="position: absolute; top: 10px; left: 20px;">Origin (0,0,0)</div>
                            <div style="position: absolute; top: 40px; left: 50px; transform: rotate(20deg); width: 50px; height: 2px; background: blue;"></div>
                            <div style="position: absolute; top: 30px; left: 110px;">Rotated Frame</div>
                        </div>
                        <p>The patient's position in the scanner varies. Images need a defined physical coordinate system.</p>
                    </div>

                    <div class="card">
                        <h3>DICOM Complexity</h3>
                        <div style="background: #333; color: #0f0; padding: 5px; font-family: monospace; font-size: 10px;">
                            (0028,0030) Pixel Spacing<br>
                            (0020,0032) Image Position<br>
                            (0020,0037) Image Orientation
                        </div>
                        <p>Highly nested and complex standard makes accessing spatial data error-prone.</p>
                    </div>

                    <div class="card">
                        <h3>The Solution</h3>
                        <p>Standardized tools (SimpleITK, MedImages.jl) abstract this complexity into a consistent physical space model.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        page.set_content(html_content_2)
        page.screenshot(path="imaging_challenges.png")

        # Infographic 3: MedImages.jl Architecture
        html_content_3 = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f0f0; }
                .container { width: 800px; height: 600px; background: white; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); position: relative; }
                h1 { text-align: center; color: #333; }

                .core {
                    width: 200px; height: 100px; background-color: #4caf50; color: white;
                    display: flex; justify-content: center; align-items: center;
                    border-radius: 10px; margin: 0 auto; font-weight: bold; font-size: 18px;
                    z-index: 10; position: relative;
                }

                .module {
                    width: 150px; padding: 10px; background-color: #2196f3; color: white;
                    text-align: center; border-radius: 5px; position: absolute;
                    font-size: 14px;
                }

                #load { top: 150px; left: 100px; }
                #resample { top: 150px; right: 100px; }
                #transform { bottom: 150px; left: 100px; }
                #spatial { bottom: 150px; right: 100px; }

                .line { position: absolute; background-color: #999; z-index: 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>MedImages.jl Architecture</h1>

                <div style="position: relative; height: 400px; margin-top: 50px;">
                    <div class="line" style="top: 50px; left: 175px; width: 450px; height: 2px;"></div>
                    <div class="line" style="top: 50px; left: 175px; width: 2px; height: 300px;"></div>
                    <div class="line" style="top: 50px; right: 175px; width: 2px; height: 300px;"></div>
                    <div class="line" style="bottom: 50px; left: 175px; width: 450px; height: 2px;"></div>

                    <div style="position: absolute; top: 150px; left: 400px; transform: translateX(-50%); width: 2px; height: 100px; background: #999;"></div>

                    <div class="core">MedImage Struct<br>(Voxel Data + Metadata)</div>

                    <div id="load" class="module">Load_and_save<br>(NIfTI, DICOM)</div>
                    <div id="resample" class="module">Resample_to_target<br>(Spacing, Size)</div>
                    <div id="transform" class="module">Basic_transformations<br>(Rotate, Crop, Pad)</div>
                    <div id="spatial" class="module">Spatial_metadata<br>(Orientation, Origin)</div>
                </div>

                <p style="text-align: center; margin-top: 20px; color: #666;">
                    The <code>MedImage</code> struct acts as the central data carrier, ensuring metadata (origin, spacing, direction)
                    is preserved and manipulated correctly across all modules.
                </p>
            </div>
        </body>
        </html>
        """
        page.set_content(html_content_3)
        page.screenshot(path="medimages_arch.png")

        browser.close()

if __name__ == "__main__":
    generate_infographics()
