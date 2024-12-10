import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
 
# Initialize Kaggle API
api = KaggleApi()
api.authenticate()
 
# Define dataset and file paths
dataset = "mczielinski/bitcoin-historical-data"
download_path = "bitcoin-historical-data.zip"
extract_to = "bitcoin_data"
 
# Download the dataset
print("Downloading dataset...")
api.dataset_download_files(dataset, path=".", unzip=False)
 
# Unzip the specific file
print("Extracting CSV file...")
with zipfile.ZipFile(download_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)
 
# Cleanup
os.remove(download_path)
 
print(f"Dataset extracted to {extract_to}")
