import kagglehub

# Download latest version
path = kagglehub.dataset_download("ivivan/real-time-water-quality-data")

print("Path to dataset files:", path)