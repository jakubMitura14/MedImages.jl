
import pypdf
import os

pdf_dir = "soft"
output_file = "soft_example_1.txt"

# Get the first pdf file in the directory
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if not pdf_files:
    print("No PDF files found in directory.")
    exit(1)

pdf_path = os.path.join(pdf_dir, pdf_files[0])
print(f"Reading {pdf_path}...")

reader = pypdf.PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open(output_file, "w") as f:
    f.write(text)

print(f"Extracted text to {output_file}")
