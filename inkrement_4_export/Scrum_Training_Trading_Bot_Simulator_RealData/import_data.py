import os
import zipfile
import subprocess

# Paths
download_path = "./"  # Adjust to your working directory
output_folder = "./data"
dataset = "mczielinski/bitcoin-historical-data"  # Kaggle dataset identifier

# Download the dataset using the Kaggle CLI
print(f"Downloading dataset: {dataset}")
subprocess.run(["kaggle", "datasets", "download", "-d", dataset], check=True)
print("Download complete.")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Find and unzip the downloaded ZIP file
for file in os.listdir(download_path):
    if file.endswith(".zip"):
        zip_path = os.path.join(download_path, file)

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
            print(f"Extracted {file} to {output_folder}")

        # Optional: Delete the zip file after extraction
        os.remove(zip_path)
        print(f"Deleted {file}")
        break
else:
    print("No ZIP files found.")
